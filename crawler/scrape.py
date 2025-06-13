import feedparser
import requests
from newspaper import Article
from bs4 import BeautifulSoup
from typing import Dict, List, Any
import logging
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import load_config, clean_text, extract_image_url, format_story

logger = logging.getLogger(__name__)

class NewsScraper:
    def __init__(self):
        self.config = load_config()
        self.max_articles = self.config['project']['max_articles']
        self.sources = self.config['sources']
        
    def fetch_rss_feed(self, url: str) -> List[Dict[str, Any]]:
        """Fetch and parse RSS feed."""
        try:
            feed = feedparser.parse(url)
            articles = []
            
            for entry in feed.entries[:self.max_articles]:
                article = {
                    'title': entry.get('title', ''),
                    'url': entry.get('link', ''),
                    'summary': entry.get('summary', ''),
                    'published': entry.get('published', ''),
                    'source': feed.feed.get('title', '')
                }
                articles.append(article)
                
            return articles
        except Exception as e:
            logger.error(f"Error fetching RSS feed {url}: {str(e)}")
            return []

    def fetch_html_content(self, url: str) -> List[Dict[str, Any]]:
        """Fetch and parse HTML content."""
        try:
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            articles = []
            
            # Basic article extraction - can be customized per source
            for article in soup.find_all(['article', 'div'], class_=['article', 'story', 'post'])[:self.max_articles]:
                title_elem = article.find(['h1', 'h2', 'h3'])
                link_elem = article.find('a')
                
                if title_elem and link_elem:
                    article_data = {
                        'title': title_elem.get_text(),
                        'url': link_elem.get('href', ''),
                        'summary': '',
                        'source': url
                    }
                    
                    # Try to get summary
                    summary_elem = article.find(['p', 'div'], class_=['summary', 'excerpt'])
                    if summary_elem:
                        article_data['summary'] = summary_elem.get_text()
                    
                    articles.append(article_data)
            
            return articles
        except Exception as e:
            logger.error(f"Error fetching HTML content {url}: {str(e)}")
            return []

    def fetch_article_content(self, url: str) -> Dict[str, Any]:
        """Fetch full article content using newspaper3k."""
        try:
            article = Article(url)
            article.download()
            article.parse()
            
            return {
                'title': article.title,
                'text': article.text,
                'image': article.top_image,
                'summary': article.summary
            }
        except Exception as e:
            logger.error(f"Error fetching article content {url}: {str(e)}")
            return {}

    def scrape_all_sources(self) -> List[Dict[str, Any]]:
        """Scrape all configured sources and return formatted stories."""
        all_stories = []
        
        for source in self.sources:
            try:
                if source['type'] == 'rss':
                    stories = self.fetch_rss_feed(source['url'])
                else:  # HTML
                    stories = self.fetch_html_content(source['url'])
                
                # Enrich stories with additional data
                for story in stories:
                    # Add source info
                    story['source'] = source['name']
                    story['tags'] = source.get('tags', [])
                    
                    # Fetch full content if needed
                    if not story.get('summary'):
                        content = self.fetch_article_content(story['url'])
                        story['summary'] = content.get('summary', '')
                        if source.get('include_images', True):
                            story['image'] = content.get('image', '')
                    
                    # Format and clean the story
                    formatted_story = format_story(story)
                    all_stories.append(formatted_story)
                    
            except Exception as e:
                logger.error(f"Error processing source {source['name']}: {str(e)}")
                continue
        
        # Sort by date if available, otherwise keep original order
        all_stories.sort(key=lambda x: x.get('published', ''), reverse=True)
        
        # Return top N stories
        return all_stories[:self.max_articles]

def main():
    """Main function for testing the scraper."""
    scraper = NewsScraper()
    stories = scraper.scrape_all_sources()
    
    for story in stories:
        print(f"\nTitle: {story['title']}")
        print(f"Source: {story['source']}")
        print(f"URL: {story['url']}")
        print(f"Summary: {story['summary'][:200]}...")
        print("-" * 80)

if __name__ == "__main__":
    main()
