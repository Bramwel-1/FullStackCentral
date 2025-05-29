from flask import render_template, request, jsonify, flash, redirect, url_for
from app import app, db
from models import Analysis, TrustedSource
from ml_models import FakeNewsDetector
from text_analyzer import TextAnalyzer
from url_extractor import URLExtractor
import logging
import json
from datetime import datetime

# Initialize components
detector = FakeNewsDetector()
text_analyzer = TextAnalyzer()
url_extractor = URLExtractor()

@app.route('/')
def index():
    """Home page with input forms"""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze text or URL for fake news"""
    try:
        content = request.form.get('content', '').strip()
        url = request.form.get('url', '').strip()
        
        if not content and not url:
            flash('Please provide either text content or a URL to analyze.', 'error')
            return redirect(url_for('index'))
        
        # Extract content from URL if provided
        if url and not content:
            try:
                content = url_extractor.extract_text(url)
                if not content:
                    flash('Unable to extract content from the provided URL.', 'error')
                    return redirect(url_for('index'))
            except Exception as e:
                logging.error(f"URL extraction error: {str(e)}")
                flash('Error extracting content from URL. Please check the URL and try again.', 'error')
                return redirect(url_for('index'))
        
        if len(content.strip()) < 50:
            flash('Content is too short for reliable analysis. Please provide at least 50 characters.', 'error')
            return redirect(url_for('index'))
        
        # Perform analysis
        try:
            # Get credibility score and detailed analysis
            credibility_score = detector.predict_credibility(content)
            is_fake = credibility_score < 0.5
            
            # Get detailed analysis
            keyword_analysis = text_analyzer.analyze_keywords(content)
            sentiment_analysis = text_analyzer.analyze_sentiment(content)
            source_analysis = text_analyzer.analyze_source_credibility(url) if url else 0.5
            
            # Create analysis details
            analysis_details = {
                'keyword_indicators': keyword_analysis.get('indicators', []),
                'sentiment': sentiment_analysis.get('sentiment', 'neutral'),
                'sentiment_confidence': sentiment_analysis.get('confidence', 0),
                'readability': text_analyzer.analyze_readability(content),
                'length': len(content),
                'word_count': len(content.split()),
                'timestamp': datetime.utcnow().isoformat()
            }
            
            # Save to database
            analysis = Analysis(
                content=content,
                url=url if url else None,
                credibility_score=credibility_score,
                is_fake=is_fake,
                keyword_score=keyword_analysis.get('score', 0),
                sentiment_score=sentiment_analysis.get('score', 0),
                source_score=source_analysis,
                analysis_details=json.dumps(analysis_details)
            )
            
            db.session.add(analysis)
            db.session.commit()
            
            return render_template('results.html', 
                                 analysis=analysis,
                                 analysis_details=analysis_details)
        
        except Exception as e:
            logging.error(f"Analysis error: {str(e)}")
            flash('An error occurred during analysis. Please try again.', 'error')
            return redirect(url_for('index'))
    
    except Exception as e:
        logging.error(f"Route error: {str(e)}")
        flash('An unexpected error occurred. Please try again.', 'error')
        return redirect(url_for('index'))

@app.route('/history')
def history():
    """View analysis history"""
    try:
        page = request.args.get('page', 1, type=int)
        analyses = Analysis.query.order_by(Analysis.created_at.desc()).paginate(
            page=page, per_page=10, error_out=False
        )
        return render_template('history.html', analyses=analyses)
    except Exception as e:
        logging.error(f"History route error: {str(e)}")
        flash('Error loading analysis history.', 'error')
        return redirect(url_for('index'))

@app.route('/analysis/<int:analysis_id>')
def view_analysis(analysis_id):
    """View specific analysis details"""
    try:
        analysis = Analysis.query.get_or_404(analysis_id)
        analysis_details = json.loads(analysis.analysis_details) if analysis.analysis_details else {}
        return render_template('results.html', 
                             analysis=analysis,
                             analysis_details=analysis_details)
    except Exception as e:
        logging.error(f"View analysis error: {str(e)}")
        flash('Error loading analysis details.', 'error')
        return redirect(url_for('history'))

@app.route('/export/<int:analysis_id>')
def export_analysis(analysis_id):
    """Export analysis results as JSON"""
    try:
        analysis = Analysis.query.get_or_404(analysis_id)
        return jsonify(analysis.to_dict())
    except Exception as e:
        logging.error(f"Export error: {str(e)}")
        return jsonify({'error': 'Failed to export analysis'}), 500

@app.route('/batch_analyze', methods=['POST'])
def batch_analyze():
    """Analyze multiple articles at once"""
    try:
        data = request.get_json()
        articles = data.get('articles', [])
        
        if not articles:
            return jsonify({'error': 'No articles provided'}), 400
        
        results = []
        for article in articles[:10]:  # Limit to 10 articles
            content = article.get('content', '').strip()
            url = article.get('url', '').strip()
            
            if not content and not url:
                continue
            
            try:
                # Extract content from URL if needed
                if url and not content:
                    content = url_extractor.extract_text(url)
                
                if content and len(content.strip()) >= 50:
                    credibility_score = detector.predict_credibility(content)
                    is_fake = credibility_score < 0.5
                    
                    results.append({
                        'content': content[:200] + '...' if len(content) > 200 else content,
                        'url': url,
                        'credibility_score': credibility_score,
                        'is_fake': is_fake
                    })
            except Exception as e:
                logging.error(f"Batch analysis item error: {str(e)}")
                continue
        
        return jsonify({'results': results})
    
    except Exception as e:
        logging.error(f"Batch analysis error: {str(e)}")
        return jsonify({'error': 'Batch analysis failed'}), 500

@app.errorhandler(404)
def not_found(error):
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('index.html'), 500
