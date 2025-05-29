import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
import joblib
import logging
import os
import re
from collections import Counter

class FakeNewsDetector:
    """Main fake news detection model using multiple algorithms"""
    
    def __init__(self):
        self.models = {}
        self.vectorizer = TfidfVectorizer(
            max_features=10000,
            stop_words='english',
            ngram_range=(1, 2),
            min_df=2,
            max_df=0.95
        )
        self.is_trained = False
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize ML models with default training data"""
        try:
            # Create synthetic training data based on common fake news patterns
            self._create_training_data()
            self._train_models()
            self.is_trained = True
            logging.info("Fake news detector initialized successfully")
        except Exception as e:
            logging.error(f"Error initializing models: {str(e)}")
            self.is_trained = False
    
    def _create_training_data(self):
        """Create training data based on fake news patterns"""
        # Fake news indicators
        fake_patterns = [
            "BREAKING: Shocking truth revealed",
            "Doctors hate this one simple trick",
            "You won't believe what happened next",
            "This will blow your mind",
            "URGENT: Share before it's deleted",
            "Secret information they don't want you to know",
            "Mainstream media won't tell you this",
            "LEAKED: Confidential documents expose",
            "EXPOSED: The hidden agenda behind",
            "BOMBSHELL: Investigation reveals shocking",
        ]
        
        # Real news patterns
        real_patterns = [
            "According to a study published in",
            "Reuters reports that officials confirmed",
            "The Associated Press has learned that",
            "Government data shows a trend of",
            "Research conducted by university scientists",
            "Official statements from the department",
            "Investigation by journalists revealed",
            "Data from the national statistics office",
            "Peer-reviewed research indicates that",
            "Official government press release states",
        ]
        
        # Generate training samples
        fake_samples = []
        real_samples = []
        
        for pattern in fake_patterns:
            for i in range(20):
                fake_samples.append(f"{pattern} and many people are concerned about the implications of these findings for the future.")
        
        for pattern in real_patterns:
            for i in range(20):
                real_samples.append(f"{pattern} and the findings have been verified through multiple independent sources.")
        
        # Create training dataset
        X = fake_samples + real_samples
        y = [0] * len(fake_samples) + [1] * len(real_samples)  # 0 = fake, 1 = real
        
        self.X_train = X
        self.y_train = y
    
    def _train_models(self):
        """Train multiple ML models"""
        try:
            # Vectorize the training data
            X_vectorized = self.vectorizer.fit_transform(self.X_train)
            
            # Train Logistic Regression
            self.models['logistic'] = LogisticRegression(random_state=42, max_iter=1000)
            self.models['logistic'].fit(X_vectorized, self.y_train)
            
            # Train Random Forest
            self.models['random_forest'] = RandomForestClassifier(
                n_estimators=100, 
                random_state=42,
                max_depth=10
            )
            self.models['random_forest'].fit(X_vectorized, self.y_train)
            
            logging.info("Models trained successfully")
        except Exception as e:
            logging.error(f"Error training models: {str(e)}")
            raise
    
    def predict_credibility(self, text):
        """
        Predict credibility score for given text
        Returns: float between 0 and 1 (0 = likely fake, 1 = likely real)
        """
        if not self.is_trained:
            logging.warning("Models not trained, using rule-based fallback")
            return self._rule_based_prediction(text)
        
        try:
            # Preprocess text
            processed_text = self._preprocess_text(text)
            
            # Vectorize input
            X_vectorized = self.vectorizer.transform([processed_text])
            
            # Get predictions from all models
            predictions = []
            
            for model_name, model in self.models.items():
                try:
                    if hasattr(model, 'predict_proba'):
                        prob = model.predict_proba(X_vectorized)[0][1]  # Probability of being real
                        predictions.append(prob)
                    else:
                        pred = model.predict(X_vectorized)[0]
                        predictions.append(float(pred))
                except Exception as e:
                    logging.error(f"Error with model {model_name}: {str(e)}")
                    continue
            
            if not predictions:
                return self._rule_based_prediction(text)
            
            # Average predictions
            credibility_score = np.mean(predictions)
            
            # Apply rule-based adjustments
            rule_score = self._rule_based_prediction(text)
            
            # Weighted combination (70% ML, 30% rules)
            final_score = 0.7 * credibility_score + 0.3 * rule_score
            
            return float(np.clip(final_score, 0, 1))
        
        except Exception as e:
            logging.error(f"Prediction error: {str(e)}")
            return self._rule_based_prediction(text)
    
    def _preprocess_text(self, text):
        """Preprocess text for analysis"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Remove URLs
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        
        return text
    
    def _rule_based_prediction(self, text):
        """Rule-based prediction as fallback"""
        score = 0.5  # Neutral starting score
        text_lower = text.lower()
        
        # Fake news indicators (decrease score)
        fake_indicators = [
            'breaking:', 'urgent:', 'shocking', 'bombshell', 'exposed', 'leaked',
            'secret', 'hidden truth', 'they don\'t want you to know', 'mainstream media',
            'wake up', 'sheeple', 'conspiracy', 'cover-up', 'you won\'t believe',
            'doctors hate', 'one simple trick', 'this will blow your mind'
        ]
        
        # Real news indicators (increase score)
        real_indicators = [
            'according to', 'study shows', 'research indicates', 'data suggests',
            'reuters', 'associated press', 'government officials', 'peer-reviewed',
            'university', 'published in', 'sources confirm', 'investigation'
        ]
        
        # Check for fake indicators
        fake_count = sum(1 for indicator in fake_indicators if indicator in text_lower)
        score -= fake_count * 0.1
        
        # Check for real indicators
        real_count = sum(1 for indicator in real_indicators if indicator in text_lower)
        score += real_count * 0.1
        
        # Excessive punctuation (fake news often uses !!!)
        exclamation_count = text.count('!')
        if exclamation_count > 3:
            score -= 0.15
        
        # All caps words (often used in fake news)
        words = text.split()
        caps_count = sum(1 for word in words if word.isupper() and len(word) > 2)
        if caps_count > len(words) * 0.1:  # More than 10% caps
            score -= 0.1
        
        # Ensure score is within bounds
        return float(np.clip(score, 0, 1))
