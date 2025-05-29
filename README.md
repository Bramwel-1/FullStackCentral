# Fake News Detector

A comprehensive AI-powered fake news detection system built with Flask and machine learning. This system analyzes news articles and provides credibility scores to help identify potentially fake or misleading content.

## Features

- **AI-Powered Detection**: Uses multiple machine learning algorithms including Logistic Regression and Random Forest
- **Text & URL Analysis**: Analyze news content by pasting text directly or providing article URLs
- **Source Credibility Assessment**: Evaluates the trustworthiness of news sources
- **Sentiment Analysis**: Analyzes emotional tone and bias in articles
- **Keyword Detection**: Identifies patterns commonly found in fake news
- **Analysis History**: Saves all analyses with detailed results and statistics
- **Interactive Dashboard**: Beautiful dark-themed interface with charts and visualizations
- **Export Functionality**: Download analysis results in JSON format
- **Batch Processing**: Analyze multiple articles at once via API

## How It Works

### 1. Content Analysis
The system analyzes news content using several methods:
- **Machine Learning Models**: Trained algorithms detect patterns in fake vs real news
- **Keyword Analysis**: Scans for suspicious phrases and credibility indicators
- **Sentiment Evaluation**: Measures emotional bias and tone
- **Source Verification**: Checks against database of trusted news sources
- **Readability Assessment**: Evaluates writing quality and structure

### 2. Scoring System
Each article receives scores from 0-100%:
- **0-30%**: Likely fake or highly questionable
- **30-50%**: Questionable, requires verification
- **50-70%**: Moderately credible
- **70-100%**: Likely credible and trustworthy

### 3. Analysis Components
- **Overall Credibility Score**: Combined assessment from all algorithms
- **Keyword Score**: Based on presence of fake news indicators vs credible terms
- **Sentiment Score**: Emotional neutrality and objectivity assessment
- **Source Score**: Domain and publisher trustworthiness rating

## Prerequisites

### System Requirements
- Python 3.11 or higher
- PostgreSQL database
- 2GB RAM minimum
- Internet connection for URL analysis

### Required Python Packages
All dependencies are automatically installed. The system uses:
- Flask (web framework)
- SQLAlchemy (database management)
- scikit-learn (machine learning)
- NLTK (natural language processing)
- Trafilatura (web content extraction)
- BeautifulSoup4 (HTML parsing)
- Pandas & NumPy (data processing)

## Installation

### Quick Start
1. **Clone or download the project files**
2. **Start the application**:
   ```bash
   python main.py
   ```
3. **Open your web browser** and go to `http://localhost:5000`

The system will automatically:
- Install required dependencies
- Set up the database
- Train machine learning models
- Download language processing resources

### Manual Setup (if needed)
If you encounter any issues, you can manually install dependencies:
```bash
pip install flask flask-sqlalchemy scikit-learn nltk trafilatura beautifulsoup4 pandas numpy requests joblib psycopg2-binary email-validator werkzeug gunicorn
```

## User Guide

### Getting Started

1. **Open the Application**
   - Navigate to `http://localhost:5000` in your web browser
   - You'll see the main analysis page with two input options

2. **Choose Analysis Method**
   - **Text Input**: Paste news article text directly (minimum 50 characters)
   - **URL Input**: Provide a link to a news article for automatic content extraction

### Analyzing News Content

#### Method 1: Text Analysis
1. Click the "Text Input" tab
2. Paste your news article text in the text area
3. Click "Analyze for Fake News"
4. Wait for processing (usually 5-15 seconds)
5. Review the detailed results

#### Method 2: URL Analysis
1. Click the "URL Input" tab
2. Enter the complete URL of the news article
3. Click "Analyze for Fake News"
4. The system will extract content and analyze it automatically

### Understanding Results

#### Credibility Score
- **Green (70-100%)**: Likely credible content
- **Yellow (50-69%)**: Moderately credible, verify with other sources
- **Orange (30-49%)**: Questionable content, high skepticism recommended
- **Red (0-29%)**: Likely fake or highly unreliable

#### Detailed Metrics
- **Keyword Analysis**: Shows suspicious vs credible language patterns
- **Sentiment Analysis**: Measures emotional bias and objectivity
- **Source Credibility**: Evaluates publisher trustworthiness
- **Content Statistics**: Word count, readability, and writing quality

#### Key Indicators
The system highlights specific words or phrases that influenced the analysis:
- **Red badges**: Suspicious or fake news indicators
- **Green badges**: Credible journalism markers
- **Blue badges**: Neutral sentiment indicators

### Managing Analysis History

1. **View History**: Click "History" in the navigation menu
2. **Review Past Analyses**: See all previous checks with scores and dates
3. **Detailed View**: Click "View Details" on any analysis for complete results
4. **Export Data**: Use the "Export" button to download analysis data
5. **Statistics**: View summary statistics of all your analyses

### Best Practices

#### For Accurate Results
- **Use Complete Articles**: Provide full article text, not just headlines
- **Check Multiple Sources**: Use the tool alongside other fact-checking methods
- **Consider Context**: The system provides guidance, not absolute truth
- **Regular Updates**: The system learns from new patterns over time

#### Content Guidelines
- **Minimum Length**: At least 50 characters for reliable analysis
- **Language**: Currently optimized for English content
- **Format**: Plain text works best; complex formatting may affect accuracy

## API Usage

### Batch Analysis Endpoint
For analyzing multiple articles programmatically:

```bash
POST /batch_analyze
Content-Type: application/json

{
  "articles": [
    {
      "content": "Article text here...",
      "url": "https://example.com/article1"
    },
    {
      "content": "Another article...",
      "url": "https://example.com/article2"
    }
  ]
}
```

### Export Analysis
```bash
GET /export/{analysis_id}
```
Returns JSON with complete analysis details.

## Database Storage

The system automatically stores:
- **All analysis results** with detailed scores and metadata
- **Source credibility ratings** for continuous improvement
- **User analysis history** for tracking and statistics
- **Performance metrics** for system optimization

## Troubleshooting

### Common Issues

**"Content too short" error**
- Ensure text has at least 50 characters
- Use complete sentences, not just headlines

**URL extraction fails**
- Check that the URL is accessible and contains text content
- Some sites may block automated content extraction
- Try copying the article text manually instead

**Analysis takes too long**
- Very long articles (>10,000 words) may take longer to process
- Check your internet connection for URL analysis
- Refresh the page if it seems stuck

**Missing analysis features**
- Some advanced text statistics require additional language resources
- The core fake news detection still works without these features

### Getting Help

If you encounter persistent issues:
1. Check that Python 3.11+ is installed
2. Ensure you have internet connectivity
3. Verify the database is running properly
4. Try restarting the application

## Technical Details

### Machine Learning Models
- **Training Data**: Uses patterns from known fake and real news examples
- **Algorithms**: Combines Logistic Regression and Random Forest classifiers
- **Features**: TF-IDF vectorization with n-gram analysis
- **Accuracy**: Continuously improving through pattern recognition

### Security & Privacy
- **No Data Sharing**: All analysis is performed locally
- **Secure Storage**: Database uses encrypted connections
- **Privacy First**: No tracking or external data transmission
- **Open Source**: All algorithms are transparent and verifiable

## System Requirements

### Minimum Specifications
- **CPU**: Dual-core processor
- **RAM**: 2GB available memory
- **Storage**: 1GB free space
- **Network**: Internet connection for URL analysis

### Recommended Specifications
- **CPU**: Quad-core processor or better
- **RAM**: 4GB+ available memory
- **Storage**: 2GB+ free space
- **Network**: Broadband internet connection

## Support & Updates

The system is designed to work out of the box with automatic setup and configuration. All machine learning models are trained automatically on first startup, and the database schema is created automatically.

For optimal performance, ensure your system meets the minimum requirements and has a stable internet connection when analyzing URLs.