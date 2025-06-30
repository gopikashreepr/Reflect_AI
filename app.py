import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from utils.emotion_analyzer import EmotionAnalyzer
from utils.suggestor import EmotionSuggestor
from utils.mood_tracker import MoodTracker
from utils.visualizer import MoodVisualizer

# Initialize session state
if 'mood_tracker' not in st.session_state:
    st.session_state.mood_tracker = MoodTracker()
if 'emotion_analyzer' not in st.session_state:
    st.session_state.emotion_analyzer = EmotionAnalyzer()
if 'suggestor' not in st.session_state:
    st.session_state.suggestor = EmotionSuggestor()
if 'visualizer' not in st.session_state:
    st.session_state.visualizer = MoodVisualizer()
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Page configuration
st.set_page_config(
    page_title="Mood Tracker & Emotion Detection",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main title
st.title("🎭 Emotion Detection & Mood Tracking")
st.markdown("Share your thoughts and feelings, and I'll help you understand your emotional patterns.")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Choose a page:", ["Chat & Analysis", "Mood Dashboard", "Export Data"])

if page == "Chat & Analysis":
    # Main chat interface
    st.header("💬 Chat with Your Mood Tracker")
    
    # Input area
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_input = st.text_area(
            "How are you feeling today? Share your thoughts:",
            placeholder="I'm feeling anxious about my upcoming presentation...",
            height=100,
            key="user_input"
        )
    
    with col2:
        st.write("")  # Spacing
        st.write("")  # Spacing
        analyze_button = st.button("Analyze Emotion", type="primary", use_container_width=True)
    
    # Process input when button is clicked or Enter is pressed
    if analyze_button and user_input.strip():
        # Analyze emotion
        emotion_result = st.session_state.emotion_analyzer.analyze_emotion(user_input)
        
        # Get suggestion
        suggestion = st.session_state.suggestor.get_suggestion(
            emotion_result['primary_emotion']
        )
        
        # Store in mood tracker
        st.session_state.mood_tracker.add_entry(
            text=user_input,
            emotion=emotion_result['primary_emotion'],
            confidence=emotion_result['confidence'],
            sentiment_score=emotion_result['sentiment_score']
        )
        
        # Add to chat history
        st.session_state.chat_history.append({
            'timestamp': datetime.now(),
            'text': user_input,
            'emotion': emotion_result['primary_emotion'],
            'confidence': emotion_result['confidence'],
            'suggestion': suggestion
        })
        
        # Clear input
        st.rerun()
    
    # Display analysis results
    if st.session_state.chat_history:
        st.header("🔍 Recent Analysis")
        
        # Show latest analysis
        latest = st.session_state.chat_history[-1]
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.subheader("Detected Emotion")
            emotion_color = st.session_state.visualizer.get_emotion_color(latest['emotion'])
            st.markdown(f"<h3 style='color: {emotion_color};'>{latest['emotion'].title()}</h3>", 
                       unsafe_allow_html=True)
            
            # Confidence score
            st.metric("Confidence", f"{latest['confidence']:.1%}")
        
        with col2:
            st.subheader("Suggestion")
            st.info(latest['suggestion'])
        
        with col3:
            st.subheader("Quick Stats")
            total_entries = len(st.session_state.mood_tracker.entries)
            st.metric("Total Entries", total_entries)
            
            if total_entries > 1:
                recent_emotions = [entry['emotion'] for entry in st.session_state.mood_tracker.entries[-7:]]
                most_common = max(set(recent_emotions), key=recent_emotions.count)
                st.metric("Recent Trend", most_common.title())
    
    # Chat history
    if st.session_state.chat_history:
        st.header("💭 Chat History")
        
        # Reverse order to show newest first
        for i, chat in enumerate(reversed(st.session_state.chat_history)):
            with st.expander(f"{chat['timestamp'].strftime('%Y-%m-%d %H:%M')} - {chat['emotion'].title()}"):
                st.write(f"**Your message:** {chat['text']}")
                st.write(f"**Emotion:** {chat['emotion'].title()} (Confidence: {chat['confidence']:.1%})")
                st.write(f"**Suggestion:** {chat['suggestion']}")

elif page == "Mood Dashboard":
    st.header("📊 Mood Dashboard")
    
    if not st.session_state.mood_tracker.entries:
        st.info("No mood data available yet. Start by sharing your thoughts in the Chat & Analysis section!")
    else:
        # Time range selector
        col1, col2 = st.columns(2)
        with col1:
            days_back = st.selectbox("View data for:", [7, 14, 30, 90], index=0)
        with col2:
            chart_type = st.selectbox("Chart type:", ["Timeline", "Distribution", "Heatmap"])
        
        # Generate visualizations
        if chart_type == "Timeline":
            fig = st.session_state.visualizer.create_emotion_timeline(
                st.session_state.mood_tracker.entries, days_back
            )
            st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == "Distribution":
            fig = st.session_state.visualizer.create_emotion_distribution(
                st.session_state.mood_tracker.entries, days_back
            )
            st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == "Heatmap":
            fig = st.session_state.visualizer.create_mood_heatmap(
                st.session_state.mood_tracker.entries, days_back
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Summary statistics
        st.subheader("📈 Summary Statistics")
        stats = st.session_state.mood_tracker.get_statistics(days_back)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Entries", stats['total_entries'])
        
        with col2:
            st.metric("Most Common Emotion", stats['most_common_emotion'].title())
        
        with col3:
            st.metric("Average Confidence", f"{stats['avg_confidence']:.1%}")
        
        with col4:
            st.metric("Average Sentiment", f"{stats['avg_sentiment']:.2f}")
        
        # Detailed breakdown
        st.subheader("🔍 Detailed Breakdown")
        
        df = pd.DataFrame(st.session_state.mood_tracker.entries)
        df = df[df['timestamp'] >= datetime.now() - timedelta(days=days_back)]
        
        if not df.empty:
            # Emotion frequency table
            emotion_counts = df['emotion'].value_counts()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Emotion Frequency:**")
                for emotion, count in emotion_counts.items():
                    percentage = (count / len(df)) * 100
                    st.write(f"• {emotion.title()}: {count} times ({percentage:.1f}%)")
            
            with col2:
                st.write("**Recent Entries:**")
                recent_df = df.tail(5)[['timestamp', 'emotion', 'confidence']].copy()
                recent_df['timestamp'] = recent_df['timestamp'].dt.strftime('%Y-%m-%d %H:%M')
                recent_df['confidence'] = recent_df['confidence'].apply(lambda x: f"{x:.1%}")
                recent_df.columns = ['Time', 'Emotion', 'Confidence']
                st.dataframe(recent_df, use_container_width=True)

elif page == "Export Data":
    st.header("📤 Export Your Data")
    
    if not st.session_state.mood_tracker.entries:
        st.info("No data available for export. Start tracking your mood first!")
    else:
        st.write("Export your mood tracking data for personal records or further analysis.")
        
        # Export options
        col1, col2 = st.columns(2)
        
        with col1:
            export_format = st.selectbox("Export format:", ["CSV", "JSON"])
        
        with col2:
            include_text = st.checkbox("Include original text", value=True)
        
        # Preview data
        df = pd.DataFrame(st.session_state.mood_tracker.entries)
        
        if not include_text:
            df = df.drop('text', axis=1)
        
        st.subheader("📊 Data Preview")
        st.dataframe(df.head(10), use_container_width=True)
        
        # Export buttons
        col1, col2 = st.columns(2)
        
        with col1:
            if export_format == "CSV":
                csv_data = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv_data,
                    file_name=f"mood_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        
        with col2:
            if export_format == "JSON":
                json_data = df.to_json(orient='records', date_format='iso')
                st.download_button(
                    label="Download JSON",
                    data=json_data,
                    file_name=f"mood_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
        
        # Data summary
        st.subheader("📊 Export Summary")
        st.write(f"• Total entries: {len(df)}")
        st.write(f"• Date range: {df['timestamp'].min().strftime('%Y-%m-%d')} to {df['timestamp'].max().strftime('%Y-%m-%d')}")
        st.write(f"• Unique emotions: {df['emotion'].nunique()}")

# Footer
st.markdown("---")
st.markdown("*This app uses sentiment analysis to detect emotions and provide personalized suggestions. Your data is stored locally in your session.*")
