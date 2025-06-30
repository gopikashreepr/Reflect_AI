import random

class EmotionSuggestor:
    """
    Provides personalized self-care suggestions and tips based on detected emotions.
    """
    
    def __init__(self):
        self.suggestions = {
            'joy': [
                "That's wonderful! Consider sharing your happiness with someone special.",
                "Great to hear you're feeling good! Maybe try a new activity while you're in this positive mood.",
                "Your joy is contagious! Consider doing something creative to express these positive feelings.",
                "Fantastic! Take a moment to appreciate what's bringing you joy today.",
                "Love the positive energy! Maybe write down what's making you happy to remember later.",
                "Wonderful news! Consider spreading some of that joy by helping someone else today."
            ],
            'sadness': [
                "It's okay to feel sad sometimes. Try reaching out to a friend or family member for support.",
                "Consider gentle activities like listening to soothing music or taking a warm bath.",
                "Remember that sadness is temporary. Try journaling about your feelings to process them.",
                "Be kind to yourself today. Maybe watch a comforting movie or read an uplifting book.",
                "Consider going for a gentle walk in nature - fresh air can help lift your spirits.",
                "It's important to acknowledge your feelings. Consider talking to someone you trust about how you're feeling."
            ],
            'anger': [
                "Take deep breaths and count to ten before reacting to anything.",
                "Try some physical exercise to channel that energy constructively - maybe a walk or workout.",
                "Consider writing down what's bothering you to help process these feelings.",
                "Step away from the situation if possible and return when you feel calmer.",
                "Try progressive muscle relaxation or meditation to help release tension.",
                "Remember that it's okay to feel angry, but focus on healthy ways to express it."
            ],
            'fear': [
                "Fear is natural. Try some deep breathing exercises to help calm your nervous system.",
                "Consider breaking down what you're afraid of into smaller, manageable parts.",
                "Remember past times when you overcame challenges - you're stronger than you think.",
                "Try grounding techniques: name 5 things you can see, 4 you can touch, 3 you can hear.",
                "Consider talking to someone you trust about your fears - sharing can help reduce their power.",
                "Focus on what you can control in the situation, rather than what you can't."
            ],
            'anxiety': [
                "Try the 4-7-8 breathing technique: breathe in for 4, hold for 7, exhale for 8.",
                "Ground yourself by focusing on your physical senses - what can you see, hear, feel right now?",
                "Consider gentle movement like stretching or yoga to help release physical tension.",
                "Remember that anxiety often involves worrying about future events - try to focus on the present moment.",
                "Consider limiting caffeine today and make sure you're staying hydrated.",
                "Progressive muscle relaxation can help - tense and release each muscle group slowly."
            ],
            'surprise': [
                "Embrace the unexpected! Sometimes surprises lead to wonderful new experiences.",
                "Take a moment to process what just happened before making any big decisions.",
                "Surprise can be energizing - consider channeling that energy into something positive.",
                "It's okay to feel unsettled by unexpected events. Give yourself time to adjust.",
                "Consider sharing your surprise with someone - sometimes talking it through helps.",
                "Use this moment of surprise as an opportunity to practice adaptability."
            ],
            'disgust': [
                "It's okay to feel disgusted by things that don't align with your values.",
                "Consider removing yourself from the situation if possible, at least temporarily.",
                "Try to understand what specifically is bothering you about this situation.",
                "Focus on things that align with your values and bring you peace.",
                "Consider whether this feeling is pointing to something important about your boundaries.",
                "Sometimes disgust helps us identify what we don't want - use it as guidance."
            ],
            'anticipation': [
                "Channel that excited energy into preparation for what's coming!",
                "Try to stay present while also looking forward to what's ahead.",
                "Consider making a plan for the thing you're anticipating to feel more prepared.",
                "Use this positive energy to tackle other tasks while you're feeling motivated.",
                "Share your excitement with someone who will celebrate with you!",
                "Remember to enjoy the anticipation itself - it's part of the joy of the experience."
            ],
            'trust': [
                "It's wonderful that you're feeling secure and confident. Embrace that feeling!",
                "Consider using this sense of trust to try something new or take a positive risk.",
                "Your trust in yourself and others is a strength - acknowledge that about yourself.",
                "Maybe use this confident feeling to reach out to someone or strengthen a relationship.",
                "Trust is built over time - appreciate the relationships and experiences that have led to this feeling.",
                "Consider how you can extend this trust and confidence to other areas of your life."
            ],
            'love': [
                "Love is a beautiful emotion! Consider expressing your love to those who matter to you.",
                "Take time to appreciate the relationships and experiences that bring love into your life.",
                "Consider doing something kind for the person or thing you love.",
                "Self-love is important too - make sure you're being kind and compassionate to yourself.",
                "Love multiplies when shared - consider how you can spread more love today.",
                "Cherish this feeling and maybe write down what you love and why."
            ],
            'neutral': [
                "A calm, neutral state can be very peaceful. Enjoy this moment of balance.",
                "Consider using this stable emotional state to plan or organize something important.",
                "Neutral feelings are completely valid - not every moment needs to be intense.",
                "Maybe this is a good time for reflection or meditation.",
                "Consider doing something small that usually brings you joy.",
                "Use this calm moment to check in with yourself - how are you really doing overall?"
            ]
        }
        
        # Self-care activities by emotion category
        self.activities = {
            'positive': ['gratitude journaling', 'creative expression', 'connecting with loved ones', 'trying something new'],
            'negative': ['gentle exercise', 'meditation', 'talking to a friend', 'engaging in a comforting routine'],
            'energy': ['physical activity', 'organizing or cleaning', 'starting a project', 'social activities'],
            'calm': ['reading', 'listening to music', 'spending time in nature', 'practicing mindfulness']
        }
        
        # Emergency resources for intense negative emotions
        self.emergency_resources = {
            'crisis': [
                "If you're having thoughts of self-harm, please reach out to a crisis helpline immediately.",
                "Crisis Text Line: Text HOME to 741741",
                "National Suicide Prevention Lifeline: 988",
                "Remember: You matter, and help is available."
            ]
        }
    
    def get_suggestion(self, emotion):
        """
        Get a personalized suggestion based on the detected emotion.
        
        Args:
            emotion (str): The detected emotion
            
        Returns:
            str: A personalized suggestion or tip
        """
        if emotion in self.suggestions:
            return random.choice(self.suggestions[emotion])
        else:
            # Fallback for unknown emotions
            return "Take a moment to acknowledge your feelings. Sometimes just recognizing how we feel is the first step to understanding ourselves better."
    
    def get_multiple_suggestions(self, emotion, count=3):
        """Get multiple suggestions for an emotion."""
        if emotion in self.suggestions:
            suggestions = self.suggestions[emotion].copy()
            random.shuffle(suggestions)
            return suggestions[:count]
        else:
            return [self.get_suggestion(emotion)]
    
    def get_activity_suggestions(self, emotion):
        """Get activity suggestions based on emotion category."""
        positive_emotions = ['joy', 'love', 'trust', 'anticipation']
        negative_emotions = ['sadness', 'anger', 'fear', 'anxiety', 'disgust']
        energetic_emotions = ['anger', 'anticipation', 'surprise']
        calm_emotions = ['trust', 'neutral']
        
        if emotion in positive_emotions:
            activities = self.activities['positive']
        elif emotion in negative_emotions:
            activities = self.activities['negative']
        elif emotion in energetic_emotions:
            activities = self.activities['energy']
        elif emotion in calm_emotions:
            activities = self.activities['calm']
        else:
            activities = ['mindful breathing', 'gentle stretching', 'listening to calming music']
        
        return random.sample(activities, min(2, len(activities)))
    
    def get_emergency_support(self):
        """Get emergency support resources."""
        return self.emergency_resources['crisis']
    
    def get_comprehensive_support(self, emotion, confidence):
        """
        Get comprehensive support including suggestion, activities, and additional resources.
        
        Args:
            emotion (str): The detected emotion
            confidence (float): Confidence score of the emotion detection
            
        Returns:
            dict: Comprehensive support information
        """
        suggestion = self.get_suggestion(emotion)
        activities = self.get_activity_suggestions(emotion)
        
        support = {
            'primary_suggestion': suggestion,
            'activities': activities,
            'confidence_note': f"I'm {confidence:.0%} confident about this emotion detection."
        }
        
        # Add specific notes for certain emotions
        if emotion in ['sadness', 'fear', 'anxiety'] and confidence > 0.7:
            support['additional_note'] = "If these feelings persist or become overwhelming, consider speaking with a mental health professional."
        elif emotion == 'anger' and confidence > 0.8:
            support['additional_note'] = "Remember that anger is often a secondary emotion. Consider what might be underneath - hurt, fear, or frustration."
        elif emotion == 'joy' and confidence > 0.8:
            support['additional_note'] = "Savor this positive moment! Research shows that actively appreciating good feelings can help them last longer."
        
        return support
    
    def get_daily_affirmation(self, emotion):
        """Get a daily affirmation based on the current emotion."""
        affirmations = {
            'joy': "I deserve happiness and allow myself to fully experience joy.",
            'sadness': "My feelings are valid, and it's okay to experience sadness as part of being human.",
            'anger': "I can feel anger without being controlled by it, and I choose healthy ways to express it.",
            'fear': "I am brave enough to face my fears, and I have overcome challenges before.",
            'anxiety': "I am safe in this moment, and I have the tools to manage my anxiety.",
            'surprise': "I am adaptable and can handle unexpected situations with grace.",
            'disgust': "I trust my instincts and honor my values and boundaries.",
            'anticipation': "I embrace the future with hope and excitement for what's to come.",
            'trust': "I am worthy of trust and capable of making good decisions.",
            'love': "I am deserving of love and capable of giving love freely.",
            'neutral': "I appreciate this moment of calm and use it to center myself."
        }
        
        return affirmations.get(emotion, "I am worthy of compassion, especially from myself.")
