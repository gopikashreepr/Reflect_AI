import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class MoodVisualizer:
    """
    Creates interactive visualizations for mood tracking data using Plotly.
    """
    
    def __init__(self):
        # Color palette for emotions
        self.emotion_colors = {
            'joy': '#FFD700',      # Gold
            'sadness': '#4169E1',   # Royal Blue
            'anger': '#FF4500',     # Orange Red
            'fear': '#9370DB',      # Medium Purple
            'surprise': '#FF69B4',  # Hot Pink
            'disgust': '#8FBC8F',   # Dark Sea Green
            'anticipation': '#FFA500', # Orange
            'trust': '#20B2AA',     # Light Sea Green
            'love': '#FF1493',      # Deep Pink
            'anxiety': '#DC143C',   # Crimson
            'neutral': '#808080'    # Gray
        }
    
    def get_emotion_color(self, emotion):
        """Get color for a specific emotion."""
        return self.emotion_colors.get(emotion, '#808080')
    
    def create_emotion_timeline(self, entries, days_back=7):
        """
        Create a timeline visualization of emotions over time.
        
        Args:
            entries (list): List of mood entries
            days_back (int): Number of days to include
            
        Returns:
            plotly.graph_objects.Figure: Timeline chart
        """
        # Filter entries by date range
        cutoff_date = datetime.now() - timedelta(days=days_back)
        filtered_entries = [entry for entry in entries if entry['timestamp'] >= cutoff_date]
        
        if not filtered_entries:
            # Return empty chart with message
            fig = go.Figure()
            fig.add_annotation(
                text="No data available for the selected time range",
                xref="paper", yref="paper",
                x=0.5, y=0.5, xanchor='center', yanchor='middle',
                showarrow=False, font_size=16
            )
            fig.update_layout(
                title="Emotion Timeline",
                xaxis_title="Time",
                yaxis_title="Emotions"
            )
            return fig
        
        # Create DataFrame
        df = pd.DataFrame(filtered_entries)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Create color mapping
        colors = [self.get_emotion_color(emotion) for emotion in df['emotion']]
        
        # Create timeline scatter plot
        fig = go.Figure()
        
        # Add scatter points for each emotion
        for emotion in df['emotion'].unique():
            emotion_data = df[df['emotion'] == emotion]
            fig.add_trace(go.Scatter(
                x=emotion_data['timestamp'],
                y=emotion_data['emotion'],
                mode='markers',
                marker=dict(
                    size=12,
                    color=self.get_emotion_color(emotion),
                    opacity=0.8,
                    line=dict(width=2, color='white')
                ),
                name=emotion.title(),
                text=emotion_data['text'].apply(lambda x: x[:50] + "..." if len(x) > 50 else x),
                hovertemplate='<b>%{y}</b><br>%{x}<br>%{text}<extra></extra>'
            ))
        
        # Update layout
        fig.update_layout(
            title=f"Emotion Timeline - Last {days_back} Days",
            xaxis_title="Time",
            yaxis_title="Emotions",
            hovermode='closest',
            height=500,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        return fig
    
    def create_emotion_distribution(self, entries, days_back=7):
        """
        Create a pie chart showing emotion distribution.
        
        Args:
            entries (list): List of mood entries
            days_back (int): Number of days to include
            
        Returns:
            plotly.graph_objects.Figure: Pie chart
        """
        # Filter entries by date range
        cutoff_date = datetime.now() - timedelta(days=days_back)
        filtered_entries = [entry for entry in entries if entry['timestamp'] >= cutoff_date]
        
        if not filtered_entries:
            fig = go.Figure()
            fig.add_annotation(
                text="No data available for the selected time range",
                xref="paper", yref="paper",
                x=0.5, y=0.5, xanchor='center', yanchor='middle',
                showarrow=False, font_size=16
            )
            fig.update_layout(title="Emotion Distribution")
            return fig
        
        # Count emotions
        emotion_counts = {}
        for entry in filtered_entries:
            emotion = entry['emotion']
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        # Create pie chart
        emotions = list(emotion_counts.keys())
        counts = list(emotion_counts.values())
        colors = [self.get_emotion_color(emotion) for emotion in emotions]
        
        fig = go.Figure(data=[go.Pie(
            labels=[emotion.title() for emotion in emotions],
            values=counts,
            marker_colors=colors,
            textinfo='label+percent',
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
        )])
        
        fig.update_layout(
            title=f"Emotion Distribution - Last {days_back} Days",
            height=500
        )
        
        return fig
    
    def create_mood_heatmap(self, entries, days_back=30):
        """
        Create a heatmap showing mood patterns by day and time.
        
        Args:
            entries (list): List of mood entries
            days_back (int): Number of days to include
            
        Returns:
            plotly.graph_objects.Figure: Heatmap
        """
        # Filter entries by date range
        cutoff_date = datetime.now() - timedelta(days=days_back)
        filtered_entries = [entry for entry in entries if entry['timestamp'] >= cutoff_date]
        
        if not filtered_entries:
            fig = go.Figure()
            fig.add_annotation(
                text="No data available for the selected time range",
                xref="paper", yref="paper",
                x=0.5, y=0.5, xanchor='center', yanchor='middle',
                showarrow=False, font_size=16
            )
            fig.update_layout(title="Mood Heatmap")
            return fig
        
        # Create DataFrame
        df = pd.DataFrame(filtered_entries)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['date'] = df['timestamp'].dt.date
        df['hour'] = df['timestamp'].dt.hour
        
        # Map emotions to sentiment scores for heatmap
        emotion_to_score = {
            'joy': 2, 'love': 2, 'trust': 1, 'anticipation': 1,
            'neutral': 0, 'surprise': 0,
            'fear': -1, 'anxiety': -1, 'disgust': -1,
            'sadness': -2, 'anger': -2
        }
        
        df['mood_score'] = df['emotion'].map(emotion_to_score)
        
        # Create pivot table for heatmap
        pivot_table = df.pivot_table(
            values='mood_score',
            index='date',
            columns='hour',
            aggfunc='mean'
        )
        
        # Create heatmap
        fig = go.Figure(data=go.Heatmap(
            z=pivot_table.values,
            x=[f"{hour:02d}:00" for hour in pivot_table.columns],
            y=[str(date) for date in pivot_table.index],
            colorscale='RdYlBu',
            zmid=0,
            hovertemplate='Date: %{y}<br>Time: %{x}<br>Mood Score: %{z:.1f}<extra></extra>',
            colorbar=dict(
                title="Mood Score",
                tickvals=[-2, -1, 0, 1, 2],
                ticktext=['Very Negative', 'Negative', 'Neutral', 'Positive', 'Very Positive']
            )
        ))
        
        fig.update_layout(
            title=f"Daily Mood Heatmap - Last {days_back} Days",
            xaxis_title="Hour of Day",
            yaxis_title="Date",
            height=max(400, len(pivot_table.index) * 25)
        )
        
        return fig
    
    def create_sentiment_trend(self, entries, days_back=14):
        """
        Create a line chart showing sentiment trend over time.
        
        Args:
            entries (list): List of mood entries
            days_back (int): Number of days to include
            
        Returns:
            plotly.graph_objects.Figure: Line chart
        """
        # Filter entries by date range
        cutoff_date = datetime.now() - timedelta(days=days_back)
        filtered_entries = [entry for entry in entries if entry['timestamp'] >= cutoff_date]
        
        if not filtered_entries:
            fig = go.Figure()
            fig.add_annotation(
                text="No data available for the selected time range",
                xref="paper", yref="paper",
                x=0.5, y=0.5, xanchor='center', yanchor='middle',
                showarrow=False, font_size=16
            )
            fig.update_layout(title="Sentiment Trend")
            return fig
        
        # Create DataFrame
        df = pd.DataFrame(filtered_entries)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp')
        
        # Calculate rolling average
        if len(df) > 3:
            df['rolling_sentiment'] = df['sentiment_score'].rolling(window=3, center=True).mean()
        else:
            df['rolling_sentiment'] = df['sentiment_score']
        
        # Create line chart
        fig = go.Figure()
        
        # Add scatter points for individual entries
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['sentiment_score'],
            mode='markers',
            name='Individual Entries',
            marker=dict(size=8, opacity=0.6),
            hovertemplate='<b>%{x}</b><br>Sentiment: %{y:.2f}<extra></extra>'
        ))
        
        # Add trend line
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['rolling_sentiment'],
            mode='lines',
            name='Trend (3-entry average)',
            line=dict(width=3),
            hovertemplate='<b>%{x}</b><br>Average Sentiment: %{y:.2f}<extra></extra>'
        ))
        
        # Add horizontal reference lines
        fig.add_hline(y=0, line_dash="dash", line_color="gray", annotation_text="Neutral")
        fig.add_hline(y=0.5, line_dash="dot", line_color="green", annotation_text="Positive")
        fig.add_hline(y=-0.5, line_dash="dot", line_color="red", annotation_text="Negative")
        
        fig.update_layout(
            title=f"Sentiment Trend - Last {days_back} Days",
            xaxis_title="Time",
            yaxis_title="Sentiment Score",
            yaxis=dict(range=[-1.1, 1.1]),
            height=500,
            hovermode='x unified'
        )
        
        return fig
    
    def create_confidence_analysis(self, entries, days_back=14):
        """
        Create a visualization showing confidence scores of emotion detection.
        
        Args:
            entries (list): List of mood entries
            days_back (int): Number of days to include
            
        Returns:
            plotly.graph_objects.Figure: Box plot
        """
        # Filter entries by date range
        cutoff_date = datetime.now() - timedelta(days=days_back)
        filtered_entries = [entry for entry in entries if entry['timestamp'] >= cutoff_date]
        
        if not filtered_entries:
            fig = go.Figure()
            fig.add_annotation(
                text="No data available for the selected time range",
                xref="paper", yref="paper",
                x=0.5, y=0.5, xanchor='center', yanchor='middle',
                showarrow=False, font_size=16
            )
            fig.update_layout(title="Confidence Analysis")
            return fig
        
        # Create DataFrame
        df = pd.DataFrame(filtered_entries)
        
        # Create box plot for confidence by emotion
        fig = go.Figure()
        
        emotions = df['emotion'].unique()
        for emotion in emotions:
            emotion_data = df[df['emotion'] == emotion]
            fig.add_trace(go.Box(
                y=emotion_data['confidence'],
                name=emotion.title(),
                marker_color=self.get_emotion_color(emotion),
                boxpoints='all',
                jitter=0.3,
                pointpos=-1.8
            ))
        
        fig.update_layout(
            title=f"Emotion Detection Confidence - Last {days_back} Days",
            xaxis_title="Emotion",
            yaxis_title="Confidence Score",
            yaxis=dict(range=[0, 1]),
            height=500
        )
        
        return fig
