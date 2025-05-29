import requests
import trafilatura
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import logging
import time

class URLExtractor:
    """Extract and analyze content from URLs"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.timeout = 10
    
    def extract_text(self, url):
        """
        Extract main text content from URL using trafilatura
        Returns: str - extracted text content
        """
        try:
            # Validate URL format
            if not self._is_valid_url(url):
                raise ValueError("Invalid URL format")
            
            # Use trafilatura for better content extraction
            downloaded = trafilatura.fetch_url(url)
            if not downloaded:
                raise ValueError("Failed to download content from URL")
            
            text = trafilatura.extract(downloaded)
            if not text:
                # Fallback to BeautifulSoup if trafilatura fails
                text = self._extract_with_beautifulsoup(url)
            
            if not text or len(text.strip()) < 50:
                raise ValueError("Insufficient content extracted from URL")
            
            return text.strip()
        
        except Exception as e:
            logging.error(f"URL extraction error for {url}: {str(e)}")
            raise
    
    def _extract_with_beautifulsoup(self, url):
        """Fallback extraction method using BeautifulSoup"""
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "header", "footer", "aside"]):
                script.decompose()
            
            # Try to find main content areas
            content_selectors = [
                'article', 'main', '.content', '.article-content',
                '.post-content', '.entry-content', '.article-body'
            ]
            
            text_content = ""
            for selector in content_selectors:
                elements = soup.select(selector)
                if elements:
                    text_content = ' '.join([elem.get_text() for elem in elements])
                    break
            
            # If no specific content area found, get all text
            if not text_content:
                text_content = soup.get_text()
            
            # Clean up text
            lines = (line.strip() for line in text_content.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text_content = ' '.join(chunk for chunk in chunks if chunk)
            
            return text_content
        
        except Exception as e:
            logging.error(f"BeautifulSoup extraction error: {str(e)}")
            return ""
    
    def extract_metadata(self, url):
        """Extract metadata from URL (title, description, etc.)"""
        try:
            # Use trafilatura for metadata extraction
            downloaded = trafilatura.fetch_url(url)
            if not downloaded:
                return {}
            
            metadata = trafilatura.extract_metadata(downloaded)
            
            result = {}
            if metadata:
                result['title'] = getattr(metadata, 'title', '')
                result['description'] = getattr(metadata, 'description', '')
                result['author'] = getattr(metadata, 'author', '')
                result['date'] = getattr(metadata, 'date', '')
                result['site_name'] = getattr(metadata, 'sitename', '')
                result['url'] = getattr(metadata, 'url', url)
            
            # Fallback to manual extraction if needed
            if not result.get('title'):
                result.update(self._extract_metadata_manual(url))
            
            return result
        
        except Exception as e:
            logging.error(f"Metadata extraction error: {str(e)}")
            return {}
    
    def _extract_metadata_manual(self, url):
        """Manual metadata extraction using BeautifulSoup"""
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            metadata = {}
            
            # Extract title
            title_tag = soup.find('title')
            if title_tag:
                metadata['title'] = title_tag.get_text().strip()
            
            # Extract meta description
            desc_tag = soup.find('meta', attrs={'name': 'description'})
            if desc_tag:
                metadata['description'] = desc_tag.get('content', '').strip()
            
            # Extract Open Graph data
            og_title = soup.find('meta', property='og:title')
            if og_title:
                metadata['og_title'] = og_title.get('content', '').strip()
            
            og_desc = soup.find('meta', property='og:description')
            if og_desc:
                metadata['og_description'] = og_desc.get('content', '').strip()
            
            # Extract author
            author_tag = soup.find('meta', attrs={'name': 'author'})
            if author_tag:
                metadata['author'] = author_tag.get('content', '').strip()
            
            return metadata
        
        except Exception as e:
            logging.error(f"Manual metadata extraction error: {str(e)}")
            return {}
    
    def get_domain_info(self, url):
        """Get domain information from URL"""
        try:
            parsed = urlparse(url)
            return {
                'domain': parsed.netloc.replace('www.', ''),
                'subdomain': parsed.netloc.split('.')[0] if '.' in parsed.netloc else '',
                'tld': parsed.netloc.split('.')[-1] if '.' in parsed.netloc else '',
                'path': parsed.path,
                'scheme': parsed.scheme
            }
        except Exception as e:
            logging.error(f"Domain info extraction error: {str(e)}")
            return {}
    
    def _is_valid_url(self, url):
        """Validate URL format"""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False
    
    def check_url_accessibility(self, url):
        """Check if URL is accessible"""
        try:
            response = self.session.head(url, timeout=self.timeout)
            return {
                'accessible': response.status_code == 200,
                'status_code': response.status_code,
                'content_type': response.headers.get('content-type', ''),
                'content_length': response.headers.get('content-length', '')
            }
        except Exception as e:
            logging.error(f"URL accessibility check error: {str(e)}")
            return {
                'accessible': False,
                'status_code': None,
                'error': str(e)
            }
