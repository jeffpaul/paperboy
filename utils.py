import yaml
import os
from datetime import datetime
import pytz
from typing import Dict, List, Any
import logging
import nltk
import re
from bs4 import BeautifulSoup
import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def ensure_dir(directory: str) -> None:
    """Ensure a directory exists, create if it doesn't."""
    if not os.path.exists(directory):
        os.makedirs(directory)
        logger.info(f"Created directory: {directory}")

def load_config() -> Dict[str, Any]:
    """Load configuration from YAML file."""
    try:
        with open('config.yaml', 'r') as f:
            config = yaml.safe_load(f)
        logger.info("Configuration loaded successfully")
        return config
    except Exception as e:
        logger.error(f"Error loading configuration: {str(e)}")
        raise

def get_current_date() -> str:
    """Get current date in EST timezone."""
    est = pytz.timezone('America/New_York')
    return datetime.now(est).strftime('%B %d, %Y')

def get_current_year() -> str:
    """Get current year as string."""
    return datetime.now().strftime('%Y')

def setup_nltk() -> None:
    """Download required NLTK data."""
    try:
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        logger.info("NLTK data downloaded successfully")
    except Exception as e:
        logger.error(f"Error downloading NLTK data: {str(e)}")
        raise

# Initialize NLTK data when module is imported
setup_nltk()

def ensure_directory(directory: str) -> None:
    """Ensure a directory exists, create if it doesn't."""
    if not os.path.exists(directory):
        os.makedirs(directory)
        logger.info(f"Created directory: {directory}")

def clean_text(text: str) -> str:
    """Clean and normalize text content."""
    if not text:
        return ""
    
    # Remove HTML tags
    text = BeautifulSoup(text, 'html.parser').get_text()
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s.,!?-]', '', text)
    
    return text.strip()

def extract_image_url(html_content: str) -> str:
    """Extract the first image URL from HTML content."""
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        img = soup.find('img')
        return img['src'] if img and 'src' in img.attrs else ''
    except Exception as e:
        logger.error(f"Error extracting image URL: {str(e)}")
        return ''

def format_story(story: Dict[str, Any]) -> Dict[str, Any]:
    """Format and clean a story object."""
    try:
        # Clean text fields
        story['title'] = clean_text(story.get('title', ''))
        story['summary'] = clean_text(story.get('summary', ''))
        
        # Ensure URL is absolute
        if story.get('url') and not story['url'].startswith(('http://', 'https://')):
            story['url'] = f"https://{story['url']}"
        
        # Clean and validate image URL
        if story.get('image'):
            if not story['image'].startswith(('http://', 'https://')):
                story['image'] = f"https://{story['image']}"
        else:
            story['image'] = ''
        
        # Add timestamp if not present
        if not story.get('published'):
            story['published'] = datetime.now().isoformat()
        
        return story
    except Exception as e:
        logger.error(f"Error formatting story: {str(e)}")
        return story
