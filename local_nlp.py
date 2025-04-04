#!/usr/bin/env python3

import re
import json
import os
import random
from collections import Counter
import math

class LocalNLP:
    def __init__(self):
        self.sentiment_lexicon = self.load_sentiment_lexicon()
        self.patterns = self.load_patterns()
        self.response_templates = self.load_response_templates()
    
    def load_sentiment_lexicon(self):
        """Load a simple sentiment lexicon of words and their polarity."""
        # This is a small subset; in production you'd use a much larger lexicon
        return {
            # Positive words
            "good": 1,
            "great": 2,
            "excellent": 2,
            "wonderful": 2,
            "happy": 1,
            "glad": 1,
            "positive": 1,
            "awesome": 2,
            "fantastic": 2,
            "terrific": 2,
            "enjoy": 1,
            "enjoyable": 1,
            "pleased": 1,
            "grateful": 1,
            "thankful": 1,
            "appreciate": 1,
            "love": 2,
            "lovely": 1,
            "amazing": 2,
            "better": 1,
            "best": 2,
            "excited": 1,
            "joy": 1,
            "peaceful": 1,
            "calm": 1,
            "relaxed": 1,
            "satisfied": 1,
            "proud": 1,
            "confident": 1,
            "hopeful": 1,
            
            # Negative words
            "bad": -1,
            "terrible": -2,
            "awful": -2,
            "horrible": -2,
            "sad": -1,
            "unhappy": -1,
            "negative": -1,
            "depressed": -2,
            "depressing": -2,
            "anxious": -1,
            "anxiety": -1,
            "worry": -1,
            "worried": -1,
            "upset": -1,
            "angry": -2,
            "mad": -1,
            "frustrated": -1,
            "disappointing": -1,
            "disappointed": -1,
            "hate": -2,
            "dislike": -1,
            "tired": -1,
            "exhausted": -2,
            "stressed": -1,
            "stress": -1,
            "afraid": -1,
            "scared": -1,
            "fear": -1,
            "lonely": -2,
            "alone": -1,
            "miserable": -2,
            "pain": -1,
            "painful": -1,
            "hurt": -1,
            "suffering": -2,
            "suffer": -1,
            "struggle": -1,
            "difficult": -1,
            "hard": -1,
            "trouble": -1,
            
            # Negations (these flip sentiment)
            "not": -1,
            "no": -1,
            "never": -1,
            "don't": -1,
            "doesn't": -1,
            "didn't": -1,
            "won't": -1,
            "wouldn't": -1,
            "can't": -1,
            "cannot": -1,
            "couldn't": -1,
            "shouldn't": -1
        }
    
    def load_patterns(self):
        """Load regex patterns for identifying common expressions."""
        return {
            "greeting": r"\b(hi|hello|hey|greetings|good morning|good afternoon|good evening)\b",
            "gratitude": r"\b(thanks|thank you|appreciate|grateful|thankful)\b",
            "farewell": r"\b(goodbye|bye|see you|talk to you later|until next time)\b",
            "affirmation": r"\b(yes|yeah|sure|absolutely|definitely|of course)\b",
            "negation": r"\b(no|nope|not really|i don't think so)\b",
            "question": r"\b(what|who|when|where|why|how|can you|could you|would you)\b.*\?",
            "stress": r"\b(stress|pressure|overwhelm|tension|anxiety|anxious|nervous|worry|worried|panic)\b",
            "sleep": r"\b(sleep|tired|exhausted|insomnia|rest|awake|dream|nightmar)\b",
            "mood": r"\b(feeling|mood|emotion|happy|sad|angry|upset|content|joy|delight|miserable)\b",
            "self_critical": r"\b(failure|fail|mistake|blame|fault|should have|regret|disappoint|mess up)\b"
        }
    
    def load_response_templates(self):
        """Load response templates for different detected patterns."""
        return {
            "greeting": [
                "Hello! How are you feeling today?",
                "Hi there! How's your day going?",
                "Hey! It's good to see you. How are you doing?"
            ],
            "gratitude": [
                "You're welcome. I'm here to support you.",
                "I'm glad I could help in some way.",
                "It's my pleasure to be here for you."
            ],
            "farewell": [
                "Take care of yourself. I'll be here when you return.",
                "Goodbye for now. Remember to be kind to yourself.",
                "Until next time. Remember that each day is a new opportunity."
            ],
            "affirmation": [
                "I'm glad to hear that.",
                "That's good to know.",
                "I understand."
            ],
            "negation": [
                "I understand. Can you tell me more about that?",
                "That's okay. Would you like to share why you feel that way?",
                "I hear you. What would feel better for you right now?"
            ],
            "question": [
                "That's a good question to reflect on. What are your thoughts?",
                "I'd encourage you to explore that question. What feels right to you?",
                "That's something worth considering carefully. What do you think?"
            ],
            "stress": [
                "It sounds like you're feeling stressed. Would a breathing exercise help right now?",
                "Stress can be challenging. What has helped you manage stress in the past?",
                "When you're feeling this way, it can help to focus on what's in your control."
            ],
            "sleep": [
                "Sleep is so important for wellbeing. Have you been having trouble sleeping?",
                "Rest is essential. What's your sleep routine like currently?",
                "Sleep challenges can affect our mood significantly. Would you like some tips for better sleep?"
            ],
            "mood": [
                "It's important to acknowledge your feelings. How long have you been feeling this way?",
                "Thank you for sharing how you're feeling. Is there anything specific triggering this emotion?",
                "I appreciate you opening up about your mood. What might help you feel a bit better right now?"
            ],
            "self_critical": [
                "I notice you're being quite hard on yourself. How would you talk to a friend in this situation?",
                "We all make mistakes. Can you try to show yourself the same compassion you'd offer others?",
                "It's natural to have regrets, but dwelling on them isn't always helpful. What could you learn from this experience?"
            ]
        }
    
    def analyze_sentiment(self, text):
        """Analyze the sentiment of a text, returning a score and label."""
        if not text:
            return {"score": 0, "label": "neutral", "confidence": 0}
        
        # Lowercase and split into words
        words = re.findall(r'\b[\w\']+\b', text.lower())
        
        if not words:
            return {"score": 0, "label": "neutral", "confidence": 0}
        
        # Calculate sentiment score
        score = 0
        total_matches = 0
        
        # Track negations for simple negation handling
        negation = False
        
        for i, word in enumerate(words):
            if word in self.sentiment_lexicon:
                word_score = self.sentiment_lexicon[word]
                
                # Check if this is a negation word
                if word_score == -1 and word in ["not", "no", "never", "don't", "doesn't", 
                                                "didn't", "won't", "wouldn't", "can't", 
                                                "cannot", "couldn't", "shouldn't"]:
                    negation = True
                    continue
                
                # Apply negation (flip the sentiment)
                if negation and i > 0:
                    word_score = -word_score
                    negation = False
                
                score += word_score
                total_matches += 1
        
        # Normalize score
        normalized_score = score / max(total_matches, 1)
        
        # Determine sentiment label
        if normalized_score > 0.3:
            label = "positive"
        elif normalized_score < -0.3:
            label = "negative"
        else:
            label = "neutral"
        
        # Calculate confidence (how many words matched our lexicon)
        confidence = min(total_matches / max(len(words), 1), 1.0)
        
        return {
            "score": normalized_score,
            "label": label,
            "confidence": confidence
        }
    
    def detect_patterns(self, text):
        """Detect patterns in text and return matched categories."""
        if not text:
            return []
        
        matches = []
        for category, pattern in self.patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                matches.append(category)
        
        return matches
    
    def get_response(self, text):
        """Generate a response based on detected patterns and sentiment."""
        patterns = self.detect_patterns(text)
        sentiment = self.analyze_sentiment(text)
        
        # If we detect patterns, respond to the most relevant one
        if patterns:
            # Prioritize certain patterns
            priority_order = ["greeting", "farewell", "stress", "self_critical", 
                              "mood", "sleep", "question", "gratitude", 
                              "affirmation", "negation"]
            
            for pattern in priority_order:
                if pattern in patterns:
                    return random.choice(self.response_templates[pattern])
        
        # If no patterns or just falling back to sentiment-based response
        if sentiment["label"] == "positive":
            return random.choice([
                "I'm glad to hear you're feeling positive.",
                "That sounds really good. What's been helping you feel this way?",
                "It's great that you're in a good place right now."
            ])
        elif sentiment["label"] == "negative":
            return random.choice([
                "I'm sorry to hear you're feeling this way. Would you like to talk more about it?",
                "That sounds difficult. What might help you feel a bit better right now?",
                "I hear that you're struggling. Remember that feelings are temporary, even when they seem overwhelming."
            ])
        else:
            return random.choice([
                "I'm here to listen if you'd like to share more.",
                "How can I best support you today?",
                "Would you like to explore that further?"
            ])
    
    def extract_topics(self, text, num_topics=3):
        """Extract main topics/keywords from text."""
        if not text:
            return []
        
        # Simple stopwords list
        stopwords = {"the", "a", "an", "and", "or", "but", "is", "are", "was", 
                     "were", "be", "been", "being", "in", "on", "at", "to", "for", 
                     "with", "by", "about", "like", "through", "over", "before", 
                     "between", "after", "since", "without", "under", "within", 
                     "along", "following", "across", "behind", "beyond", "plus", 
                     "except", "but", "up", "down", "out", "off", "above", "below",
                     "use", "using", "used", "do", "does", "did", "doing", "done",
                     "i", "me", "my", "mine", "myself", "you", "your", "yours", 
                     "yourself", "he", "him", "his", "himself", "she", "her", "hers", 
                     "herself", "it", "its", "itself", "we", "us", "our", "ours", 
                     "ourselves", "they", "them", "their", "theirs", "themselves",
                     "this", "that", "these", "those", "here", "there", "when", 
                     "where", "why", "how", "all", "any", "both", "each", "few", 
                     "more", "most", "other", "some", "such", "no", "nor", "not", 
                     "only", "own", "same", "so", "than", "too", "very", "as", "just",
                     "can", "will", "should", "now", "I'm", "I'll", "I've", "I'd",
                     "you're", "you'll", "you've", "you'd", "he's", "he'll", "he'd",
                     "she's", "she'll", "she'd", "it's", "it'll", "it'd", "we're",
                     "we'll", "we've", "we'd", "they're", "they'll", "they've", "they'd",
                     "don't", "doesn't", "didn't", "can't", "couldn't", "won't", 
                     "wouldn't", "shouldn't", "haven't", "hasn't", "hadn't", "isn't",
                     "aren't", "wasn't", "weren't"}
        
        # Tokenize and filter
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        filtered_words = [w for w in words if w not in stopwords]
        
        # Count frequencies
        word_counts = Counter(filtered_words)
        
        # Return top N topics
        return [word for word, count in word_counts.most_common(num_topics)]
    
    def suggest_journal_prompt(self, text):
        """Suggest a journal prompt based on detected patterns and topics."""
        patterns = self.detect_patterns(text)
        sentiment = self.analyze_sentiment(text)
        topics = self.extract_topics(text)
        
        prompts = []
        
        # Pattern-based prompts
        if "stress" in patterns:
            prompts.append("What specific situations are causing you stress right now, and what resources could help you handle them?")
            prompts.append("When you feel stressed, what activities or practices help you find calm?")
        
        if "sleep" in patterns:
            prompts.append("Describe your ideal evening routine for better sleep. What steps could you take to make it reality?")
            prompts.append("How does your quality of sleep affect your mood and energy the next day?")
        
        if "mood" in patterns:
            prompts.append("What patterns have you noticed in your mood changes? Are there specific triggers?")
            prompts.append("Describe a recent situation where your mood shifted. What contributed to that change?")
        
        if "self_critical" in patterns:
            prompts.append("Write a compassionate letter to yourself about the situation you're facing, as if writing to a dear friend.")
            prompts.append("What would you say to a friend who was being as hard on themselves as you are being on yourself?")
        
        # Sentiment-based prompts
        if sentiment["label"] == "positive":
            prompts.append("Describe three things that contributed to your positive feelings today.")
            prompts.append("How can you bring more of what's working well into other areas of your life?")
        
        elif sentiment["label"] == "negative":
            prompts.append("What would help you feel even slightly better right now?")
            prompts.append("Is there a small action you could take today to address what's bothering you?")
        
        # Topic-based prompts
        if topics:
            main_topic = topics[0] if topics else ""
            prompts.append(f"What thoughts or feelings come up for you around the topic of {main_topic}?")
            
            if len(topics) >= 2:
                prompts.append(f"How do {topics[0]} and {topics[1]} connect in your life right now?")
        
        # Default prompts if nothing specific was detected
        if not prompts:
            prompts = [
                "What's on your mind today that you'd like to explore further?",
                "Describe a moment from today that stood out to you, and why it matters.",
                "What's one small thing you could do tomorrow to support your wellbeing?",
                "What are you learning about yourself right now?",
                "What would you like to remind yourself of when things get difficult?"
            ]
        
        return random.choice(prompts)

# Example usage if run directly
if __name__ == "__main__":
    nlp = LocalNLP()
    
    print("Simple NLP Therapist (type 'exit' to quit)")
    print("-------------------------------------------")
    
    while True:
        user_input = input("\nYou: ")
        
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("\nTake care. Remember I'm here anytime you want to talk.")
            break
        
        # Analyze the input
        sentiment = nlp.analyze_sentiment(user_input)
        patterns = nlp.detect_patterns(user_input)
        topics = nlp.extract_topics(user_input)
        
        # Generate a response
        response = nlp.get_response(user_input)
        
        print(f"\nTherapist: {response}")
        
        # Occasionally suggest a journal prompt
        if random.random() < 0.3:  # 30% chance
            prompt = nlp.suggest_journal_prompt(user_input)
            print(f"\nJournal Prompt: {prompt}") 