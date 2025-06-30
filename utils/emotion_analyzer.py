import numpy as np
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re

class EmotionAnalyzer:
    """
    Lightweight emotion analyzer using TextBlob and VADER sentiment analysis
    to classify emotions from text input.
    """
    
    def __init__(self):
        self.vader_analyzer = SentimentIntensityAnalyzer()
        
        # Emotion keywords mapping
        self.emotion_keywords = {
            'joy': ['happy', 'joyful', 'excited', 'cheerful', 'delighted', 'elated', 'thrilled', 'content', 'pleased', 'glad'],
            'sadness': ['sad', 'depressed', 'melancholy', 'gloomy', 'dejected', 'downhearted', 'sorrowful', 'unhappy', 'blue', 'down'],
            'anger': ['angry', 'furious', 'mad', 'irritated', 'annoyed', 'rage', 'outraged', 'livid', 'frustrated', 'pissed'],
            'fear': ['afraid', 'scared', 'frightened', 'terrified', 'anxious', 'worried', 'nervous', 'panicked', 'fearful', 'apprehensive'],
            'surprise': ['surprised', 'shocked', 'amazed', 'astonished', 'stunned', 'bewildered', 'startled', 'astounded'],
            'disgust': ['disgusted', 'revolted', 'repulsed', 'nauseated', 'sickened', 'appalled', 'repelled'],
            'anticipation': ['excited', 'eager', 'hopeful', 'expectant', 'anticipating', 'looking forward', 'optimistic'],
            'trust': ['confident', 'secure', 'trusting', 'faithful', 'assured', 'certain', 'believing'],
            'love': ['love', 'adore', 'cherish', 'affectionate', 'devoted', 'caring', 'tender', 'romantic'],
            'anxiety': ['anxious', 'stressed', 'overwhelmed', 'tense', 'uneasy', 'restless', 'agitated', 'troubled']
        }
        
        # Emotion intensity modifiers
        self.intensity_modifiers = {
            'very': 1.5,
            'extremely': 2.0,
            'really': 1.3,
            'quite': 1.2,
            'somewhat': 0.8,
            'slightly': 0.6,
            'a bit': 0.7,
            'incredibly': 1.8,
            'totally': 1.6,
            'completely': 1.7
        }
    
    def preprocess_text(self, text):
        """Clean and preprocess the input text."""
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def analyze_sentiment(self, text):
        """Analyze sentiment using both TextBlob and VADER."""
        # TextBlob sentiment
        blob = TextBlob(text)
        textblob_polarity = blob.sentiment.polarity
        textblob_subjectivity = blob.sentiment.subjectivity
        
        # VADER sentiment
        vader_scores = self.vader_analyzer.polarity_scores(text)
        
        # Combine both approaches for more robust analysis
        combined_sentiment = (textblob_polarity + vader_scores['compound']) / 2
        
        return {
            'textblob_polarity': textblob_polarity,
            'textblob_subjectivity': textblob_subjectivity,
            'vader_scores': vader_scores,
            'combined_sentiment': combined_sentiment
        }
    
    def detect_emotion_keywords(self, text):
        """Detect emotions based on keyword matching."""
        text = self.preprocess_text(text)
        emotion_scores = {}
        
        for emotion, keywords in self.emotion_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword in text:
                    # Base score for keyword match
                    base_score = 1
                    
                    # Check for intensity modifiers
                    for modifier, multiplier in self.intensity_modifiers.items():
                        if f"{modifier} {keyword}" in text:
                            base_score *= multiplier
                            break
                    
                    score += base_score
            
            emotion_scores[emotion] = score
        
        return emotion_scores
    
    def classify_emotion_from_sentiment(self, sentiment_data):
        """Map sentiment scores to emotions."""
        sentiment_score = sentiment_data['combined_sentiment']
        vader_scores = sentiment_data['vader_scores']
        
        # Primary emotion based on sentiment polarity
        if sentiment_score > 0.5:
            return 'joy'
        elif sentiment_score < -0.5:
            return 'sadness'
        elif sentiment_score > 0.1:
            return 'anticipation'
        elif sentiment_score < -0.1:
            if vader_scores['neg'] > 0.3:
                return 'anger' if vader_scores['compound'] < -0.3 else 'fear'
            else:
                return 'sadness'
        else:
            # Neutral sentiment, check for other indicators
            if vader_scores['neu'] > 0.7:
                return 'trust'
            else:
                return 'anticipation'
    
    def calculate_confidence(self, emotion_scores, primary_emotion, sentiment_data):
        """Calculate confidence score for the emotion prediction."""
        keyword_score = emotion_scores.get(primary_emotion, 0)
        sentiment_confidence = abs(sentiment_data['combined_sentiment'])
        subjectivity = sentiment_data['textblob_subjectivity']
        
        # Combine different confidence indicators
        base_confidence = 0.4  # Base confidence
        keyword_confidence = min(keyword_score * 0.2, 0.3)  # Keyword contribution
        sentiment_confidence_contrib = sentiment_confidence * 0.2  # Sentiment contribution
        subjectivity_contrib = subjectivity * 0.1  # Subjectivity contribution
        
        total_confidence = base_confidence + keyword_confidence + sentiment_confidence_contrib + subjectivity_contrib
        
        # Ensure confidence is between 0 and 1
        return min(max(total_confidence, 0.3), 0.95)
    
    def analyze_emotion(self, text):
        """
        Main method to analyze emotion from text input.
        
        Args:
            text (str): Input text to analyze
            
        Returns:
            dict: Contains primary emotion, confidence score, and additional data
        """
        if not text or not text.strip():
            return {
                'primary_emotion': 'neutral',
                'confidence': 0.5,
                'sentiment_score': 0.0,
                'emotion_scores': {},
                'sentiment_data': {}
            }
        
        # Analyze sentiment
        sentiment_data = self.analyze_sentiment(text)
        
        # Detect emotions from keywords
        emotion_scores = self.detect_emotion_keywords(text)
        
        # Determine primary emotion
        if emotion_scores and max(emotion_scores.values()) > 0:
            # Use keyword-based emotion if strong matches found
            primary_emotion = max(emotion_scores.items(), key=lambda x: x[1])[0]
        else:
            # Fall back to sentiment-based classification
            primary_emotion = self.classify_emotion_from_sentiment(sentiment_data)
        
        # Calculate confidence
        confidence = self.calculate_confidence(emotion_scores, primary_emotion, sentiment_data)
        
        return {
            'primary_emotion': primary_emotion,
            'confidence': confidence,
            'sentiment_score': sentiment_data['combined_sentiment'],
            'emotion_scores': emotion_scores,
            'sentiment_data': sentiment_data
        }
    
    def get_emotion_explanation(self, analysis_result):
        """Generate explanation for the emotion detection."""
        emotion = analysis_result['primary_emotion']
        confidence = analysis_result['confidence']
        sentiment_score = analysis_result['sentiment_score']
        
        explanation = f"I detected {emotion} with {confidence:.1%} confidence. "
        
        if sentiment_score > 0.3:
            explanation += "The text has a positive sentiment. "
        elif sentiment_score < -0.3:
            explanation += "The text has a negative sentiment. "
        else:
            explanation += "The text has a neutral sentiment. "
        
        keyword_matches = [k for k, v in analysis_result['emotion_scores'].items() if v > 0]
        if keyword_matches:
            explanation += f"Keywords associated with {', '.join(keyword_matches)} were found."
        
        return explanation
