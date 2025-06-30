from datetime import datetime, timedelta
import pandas as pd
import numpy as np

class MoodTracker:
    """
    Tracks and manages mood entries with functionality for analysis and statistics.
    """
    
    def __init__(self):
        self.entries = []
    
    def add_entry(self, text, emotion, confidence, sentiment_score):
        """
        Add a new mood entry.
        
        Args:
            text (str): Original text input
            emotion (str): Detected emotion
            confidence (float): Confidence score (0-1)
            sentiment_score (float): Sentiment score (-1 to 1)
        """
        entry = {
            'timestamp': datetime.now(),
            'text': text,
            'emotion': emotion,
            'confidence': confidence,
            'sentiment_score': sentiment_score
        }
        
        self.entries.append(entry)
    
    def get_entries_by_date_range(self, days_back=7):
        """Get entries within a specific date range."""
        cutoff_date = datetime.now() - timedelta(days=days_back)
        return [entry for entry in self.entries if entry['timestamp'] >= cutoff_date]
    
    def get_statistics(self, days_back=7):
        """
        Get comprehensive statistics for the mood entries.
        
        Args:
            days_back (int): Number of days to look back
            
        Returns:
            dict: Statistics including counts, averages, and trends
        """
        entries = self.get_entries_by_date_range(days_back)
        
        if not entries:
            return {
                'total_entries': 0,
                'most_common_emotion': 'none',
                'avg_confidence': 0,
                'avg_sentiment': 0,
                'emotion_distribution': {},
                'daily_counts': {},
                'trend': 'no data'
            }
        
        # Basic statistics
        emotions = [entry['emotion'] for entry in entries]
        confidences = [entry['confidence'] for entry in entries]
        sentiments = [entry['sentiment_score'] for entry in entries]
        
        # Most common emotion
        emotion_counts = {}
        for emotion in emotions:
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        most_common_emotion = max(emotion_counts.items(), key=lambda x: x[1])[0]
        
        # Daily entry counts
        daily_counts = {}
        for entry in entries:
            date_key = entry['timestamp'].strftime('%Y-%m-%d')
            daily_counts[date_key] = daily_counts.get(date_key, 0) + 1
        
        # Sentiment trend (comparing first half vs second half of period)
        if len(entries) >= 4:
            mid_point = len(entries) // 2
            first_half_sentiment = np.mean([entry['sentiment_score'] for entry in entries[:mid_point]])
            second_half_sentiment = np.mean([entry['sentiment_score'] for entry in entries[mid_point:]])
            
            if second_half_sentiment > first_half_sentiment + 0.1:
                trend = 'improving'
            elif second_half_sentiment < first_half_sentiment - 0.1:
                trend = 'declining'
            else:
                trend = 'stable'
        else:
            trend = 'insufficient data'
        
        return {
            'total_entries': len(entries),
            'most_common_emotion': most_common_emotion,
            'avg_confidence': np.mean(confidences),
            'avg_sentiment': np.mean(sentiments),
            'emotion_distribution': emotion_counts,
            'daily_counts': daily_counts,
            'trend': trend
        }
    
    def get_emotion_patterns(self, days_back=30):
        """Analyze patterns in emotions over time."""
        entries = self.get_entries_by_date_range(days_back)
        
        if not entries:
            return {}
        
        # Group by day of week
        day_patterns = {}
        for entry in entries:
            day_name = entry['timestamp'].strftime('%A')
            if day_name not in day_patterns:
                day_patterns[day_name] = []
            day_patterns[day_name].append(entry['emotion'])
        
        # Find most common emotion for each day
        day_emotions = {}
        for day, emotions in day_patterns.items():
            emotion_counts = {}
            for emotion in emotions:
                emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
            day_emotions[day] = max(emotion_counts.items(), key=lambda x: x[1])[0]
        
        # Group by time of day
        time_patterns = {'morning': [], 'afternoon': [], 'evening': [], 'night': []}
        for entry in entries:
            hour = entry['timestamp'].hour
            if 5 <= hour < 12:
                time_patterns['morning'].append(entry['emotion'])
            elif 12 <= hour < 17:
                time_patterns['afternoon'].append(entry['emotion'])
            elif 17 <= hour < 22:
                time_patterns['evening'].append(entry['emotion'])
            else:
                time_patterns['night'].append(entry['emotion'])
        
        # Find most common emotion for each time period
        time_emotions = {}
        for time_period, emotions in time_patterns.items():
            if emotions:
                emotion_counts = {}
                for emotion in emotions:
                    emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
                time_emotions[time_period] = max(emotion_counts.items(), key=lambda x: x[1])[0]
        
        return {
            'day_patterns': day_emotions,
            'time_patterns': time_emotions
        }
    
    def get_recent_streaks(self):
        """Identify streaks of similar emotions."""
        if len(self.entries) < 2:
            return []
        
        streaks = []
        current_streak = {'emotion': self.entries[-1]['emotion'], 'count': 1, 'start_date': self.entries[-1]['timestamp']}
        
        for i in range(len(self.entries) - 2, -1, -1):
            if self.entries[i]['emotion'] == current_streak['emotion']:
                current_streak['count'] += 1
                current_streak['start_date'] = self.entries[i]['timestamp']
            else:
                if current_streak['count'] >= 2:
                    streaks.append(current_streak.copy())
                current_streak = {'emotion': self.entries[i]['emotion'], 'count': 1, 'start_date': self.entries[i]['timestamp']}
        
        # Add the final streak if it's significant
        if current_streak['count'] >= 2:
            streaks.append(current_streak)
        
        return streaks
    
    def export_data(self, format='csv', include_text=True):
        """
        Export mood data in specified format.
        
        Args:
            format (str): Export format ('csv' or 'json')
            include_text (bool): Whether to include original text
            
        Returns:
            str: Exported data as string
        """
        if not self.entries:
            return ""
        
        df = pd.DataFrame(self.entries)
        
        if not include_text:
            df = df.drop('text', axis=1)
        
        if format.lower() == 'csv':
            return df.to_csv(index=False)
        elif format.lower() == 'json':
            return df.to_json(orient='records', date_format='iso')
        else:
            raise ValueError("Format must be 'csv' or 'json'")
    
    def get_insights(self, days_back=14):
        """Generate insights about mood patterns."""
        stats = self.get_statistics(days_back)
        patterns = self.get_emotion_patterns(days_back)
        streaks = self.get_recent_streaks()
        
        insights = []
        
        # Frequency insights
        if stats['total_entries'] > 0:
            insights.append(f"You've logged {stats['total_entries']} mood entries in the past {days_back} days.")
            insights.append(f"Your most common emotion has been {stats['most_common_emotion']}.")
        
        # Sentiment trend insights
        if stats['trend'] == 'improving':
            insights.append("Your overall mood has been trending upward recently. Keep up the positive momentum!")
        elif stats['trend'] == 'declining':
            insights.append("Your mood has been trending downward recently. Consider reaching out for support if needed.")
        elif stats['trend'] == 'stable':
            insights.append("Your mood has been relatively stable recently.")
        
        # Pattern insights
        if patterns.get('day_patterns'):
            busiest_days = [day for day, emotion in patterns['day_patterns'].items()]
            if len(busiest_days) > 0:
                insights.append(f"You tend to log entries most often on {', '.join(busiest_days)}.")
        
        # Streak insights
        if streaks:
            recent_streak = streaks[0]
            if recent_streak['count'] >= 3:
                insights.append(f"You've had {recent_streak['count']} consecutive entries of {recent_streak['emotion']}.")
        
        return insights
