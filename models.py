from app import db
from datetime import datetime
from sqlalchemy import Text, Float, DateTime, Integer, String

class Analysis(db.Model):
    """Model to store fake news analysis results"""
    id = db.Column(Integer, primary_key=True)
    content = db.Column(Text, nullable=False)
    url = db.Column(String(500))
    credibility_score = db.Column(Float, nullable=False)
    is_fake = db.Column(db.Boolean, nullable=False)
    keyword_score = db.Column(Float)
    sentiment_score = db.Column(Float)
    source_score = db.Column(Float)
    analysis_details = db.Column(Text)
    created_at = db.Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Analysis {self.id}>'
    
    def to_dict(self):
        """Convert analysis to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'content': self.content[:200] + '...' if len(self.content) > 200 else self.content,
            'url': self.url,
            'credibility_score': self.credibility_score,
            'is_fake': self.is_fake,
            'keyword_score': self.keyword_score,
            'sentiment_score': self.sentiment_score,
            'source_score': self.source_score,
            'analysis_details': self.analysis_details,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class TrustedSource(db.Model):
    """Model to store trusted news sources"""
    id = db.Column(Integer, primary_key=True)
    domain = db.Column(String(200), unique=True, nullable=False)
    trust_score = db.Column(Float, nullable=False, default=0.5)
    created_at = db.Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<TrustedSource {self.domain}>'
