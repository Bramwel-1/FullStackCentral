import re
import nltk
from collections import Counter
from urllib.parse import urlparse
import logging

# Download required NLTK data
try:
    nltk.download('vader_lexicon', quiet=True)
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize, sent_tokenize
except Exception as e:
    logging.warning(f"NLTK download error: {str(e)}")

class TextAnalyzer:
    """Analyze text for various features related to fake news detection"""
    
    def __init__(self):
        try:
            self.sentiment_analyzer = SentimentIntensityAnalyzer()
            self.stop_words = set(stopwords.words('english'))
        except:
            self.sentiment_analyzer = None
            self.stop_words = set()
        
        # Common fake news keywords and patterns
        self.fake_keywords = [
            'breaking', 'urgent', 'shocking', 'bombshell', 'exposed', 'leaked',
            'secret', 'hidden', 'conspiracy', 'cover-up', 'mainstream media',
            'deep state', 'fake news', 'hoax', 'scam', 'lies', 'deception',
            'you won\'t believe', 'doctors hate', 'one simple trick',
            'this will blow your mind', 'they don\'t want you to know'
        ]
        
        # Credible source indicators
        self.credible_keywords = [
            'study', 'research', 'according to', 'data shows', 'evidence',
            'peer-reviewed', 'university', 'institution', 'official',
            'government', 'reuters', 'associated press', 'published',
            'journal', 'investigation', 'verified', 'confirmed'
        ]
        
        # Trusted news domains
        self.trusted_domains = [
            'reuters.com', 'ap.org', 'bbc.com', 'cnn.com', 'nytimes.com',
            'washingtonpost.com', 'theguardian.com', 'wsj.com', 'npr.org',
            'abc.com', 'cbsnews.com', 'nbcnews.com', 'usatoday.com'
        ]
    
    def analyze_keywords(self, text):
        """Analyze text for fake news keywords"""
        try:
            text_lower = text.lower()
            
            # Count fake news indicators
            fake_count = sum(1 for keyword in self.fake_keywords if keyword in text_lower)
            
            # Count credible indicators
            credible_count = sum(1 for keyword in self.credible_keywords if keyword in text_lower)
            
            # Calculate score (higher = more credible)
            total_indicators = fake_count + credible_count
            if total_indicators == 0:
                score = 0.5  # Neutral
            else:
                score = credible_count / total_indicators
            
            # Find specific indicators present
            fake_indicators = [kw for kw in self.fake_keywords if kw in text_lower]
            credible_indicators = [kw for kw in self.credible_keywords if kw in text_lower]
            
            return {
                'score': score,
                'fake_indicators': fake_indicators,
                'credible_indicators': credible_indicators,
                'indicators': fake_indicators + credible_indicators
            }
        
        except Exception as e:
            logging.error(f"Keyword analysis error: {str(e)}")
            return {'score': 0.5, 'fake_indicators': [], 'credible_indicators': [], 'indicators': []}
    
    def analyze_sentiment(self, text):
        """Analyze sentiment of the text"""
        try:
            if not self.sentiment_analyzer:
                return {'sentiment': 'neutral', 'score': 0.5, 'confidence': 0}
            
            scores = self.sentiment_analyzer.polarity_scores(text)
            
            # Determine sentiment
            if scores['compound'] >= 0.05:
                sentiment = 'positive'
            elif scores['compound'] <= -0.05:
                sentiment = 'negative'
            else:
                sentiment = 'neutral'
            
            # Convert compound score to 0-1 range (0.5 = neutral)
            sentiment_score = (scores['compound'] + 1) / 2
            
            return {
                'sentiment': sentiment,
                'score': sentiment_score,
                'confidence': abs(scores['compound']),
                'details': scores
            }
        
        except Exception as e:
            logging.error(f"Sentiment analysis error: {str(e)}")
            return {'sentiment': 'neutral', 'score': 0.5, 'confidence': 0}
    
    def analyze_readability(self, text):
        """Analyze readability and writing quality"""
        try:
            # Basic readability metrics
            sentences = sent_tokenize(text) if 'sent_tokenize' in globals() else text.split('.')
            words = word_tokenize(text) if 'word_tokenize' in globals() else text.split()
            
            # Remove empty sentences
            sentences = [s.strip() for s in sentences if s.strip()]
            
            if not sentences or not words:
                return {'score': 0.5, 'details': 'Insufficient text'}
            
            # Calculate metrics
            avg_sentence_length = len(words) / len(sentences)
            avg_word_length = sum(len(word) for word in words) / len(words)
            
            # Count complex patterns
            exclamation_count = text.count('!')
            question_count = text.count('?')
            caps_words = sum(1 for word in words if word.isupper() and len(word) > 2)
            
            # Calculate readability score (0-1, higher = better)
            score = 0.5
            
            # Adjust based on sentence length (moderate length is good)
            if 10 <= avg_sentence_length <= 25:
                score += 0.1
            elif avg_sentence_length > 35:
                score -= 0.1
            
            # Adjust based on excessive punctuation
            punct_ratio = (exclamation_count + question_count) / len(text)
            if punct_ratio > 0.02:  # More than 2% punctuation
                score -= 0.15
            
            # Adjust based on excessive caps
            caps_ratio = caps_words / len(words) if words else 0
            if caps_ratio > 0.1:  # More than 10% caps
                score -= 0.1
            
            return {
                'score': max(0, min(1, score)),
                'avg_sentence_length': avg_sentence_length,
                'avg_word_length': avg_word_length,
                'exclamation_ratio': exclamation_count / len(text),
                'caps_ratio': caps_ratio
            }
        
        except Exception as e:
            logging.error(f"Readability analysis error: {str(e)}")
            return {'score': 0.5, 'details': 'Analysis failed'}
    
    def analyze_source_credibility(self, url):
        """Analyze source credibility based on URL"""
        try:
            if not url:
                return 0.5
            
            parsed_url = urlparse(url.lower())
            domain = parsed_url.netloc.replace('www.', '')
            
            # Check against trusted domains
            if domain in self.trusted_domains:
                return 0.9
            
            # Check for common unreliable patterns
            unreliable_patterns = [
                'blogspot', 'wordpress', 'tumblr', 'medium',
                'fake', 'hoax', 'conspiracy', 'truth',
                'patriot', 'freedom', 'liberty'
            ]
            
            if any(pattern in domain for pattern in unreliable_patterns):
                return 0.2
            
            # Check TLD credibility
            if domain.endswith(('.gov', '.edu', '.org')):
                return 0.8
            elif domain.endswith('.com'):
                return 0.5
            else:
                return 0.4
        
        except Exception as e:
            logging.error(f"Source credibility analysis error: {str(e)}")
            return 0.5
    
    def extract_entities(self, text):
        """Extract named entities from text"""
        try:
            # Simple entity extraction using regex patterns
            entities = {
                'organizations': [],
                'locations': [],
                'persons': [],
                'dates': []
            }
            
            # Extract potential organizations (capitalized words/phrases)
            org_pattern = r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*(?:\s+(?:Inc|Corp|LLC|Ltd|Organization|Institute|University|College))\b'
            entities['organizations'] = re.findall(org_pattern, text)
            
            # Extract potential locations (capitalized words)
            location_pattern = r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*(?:\s+(?:City|State|Country|County|Province))\b'
            entities['locations'] = re.findall(location_pattern, text)
            
            # Extract dates
            date_pattern = r'\b(?:\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4}[/-]\d{1,2}[/-]\d{1,2}|\w+\s+\d{1,2},?\s+\d{4})\b'
            entities['dates'] = re.findall(date_pattern, text)
            
            return entities
        
        except Exception as e:
            logging.error(f"Entity extraction error: {str(e)}")
            return {'organizations': [], 'locations': [], 'persons': [], 'dates': []}
