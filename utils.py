import yaml
import os
from datetime import datetime
import pytz
from typing import Dict, List, Any
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_config() -> Dict[str, Any]:
    """Load and validate the configuration from config.yaml."""
    try:
        with open('config.yaml', 'r') as f:
            config = yaml.safe_load(f)
        
        # Validate required sections
        required_sections = ['project', 'sources', 'email']
        for section in required_sections:
            if section not in config:
                raise ValueError(f"Missing required section '{section}' in config.yaml")
        
        return config
    except Exception as e:
        logger.error(f"Error loading config: {str(e)}")
        raise

def get_current_date() -> str:
    """Get current date in EST timezone."""
    est = pytz.timezone('America/New_York')
    return datetime.now(est).strftime('%B %d, %Y')

def get_current_year() -> str:
    """Get current year as string."""
    return datetime.now().strftime('%Y')

def ensure_directory(directory: str) -> None:
    """Ensure a directory exists, create if it doesn't."""
    if not os.path.exists(directory):
        os.makedirs(directory)
        logger.info(f"Created directory: {directory}")

def clean_text(text: str) -> str:
    """Clean and normalize text content."""
    if not text:
        return ""
    # Remove extra whitespace
    text = ' '.join(text.split())
    # Remove special characters that might cause issues
    text = text.replace('\n', ' ').replace('\r', ' ')
    return text.strip()

def extract_image_url(html_content: str) -> str:
    """Extract the first image URL from HTML content."""
    from bs4 import BeautifulSoup
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Try to find og:image first
    og_image = soup.find('meta', property='og:image')
    if og_image and og_image.get('content'):
        return og_image['content']
    
    # Fallback to first image in content
    img = soup.find('img')
    if img and img.get('src'):
        return img['src']
    
    return ""

def format_story(story: Dict[str, Any]) -> Dict[str, Any]:
    """Format a story dictionary with required fields."""
    return {
        'title': clean_text(story.get('title', '')),
        'url': story.get('url', ''),
        'summary': clean_text(story.get('summary', '')),
        'image': story.get('image', ''),
        'source': story.get('source', ''),
        'tags': story.get('tags', [])
    }
