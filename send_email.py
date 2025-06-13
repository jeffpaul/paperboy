import os
import sys
import logging
from typing import Dict, Any
import subprocess
from jinja2 import Environment, FileSystemLoader
from resend import Resend
from dotenv import load_dotenv

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from crawler.scrape import NewsScraper
from ai.summarize import StorySummarizer
from utils import load_config, get_current_date, get_current_year, ensure_directory

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class NewsletterGenerator:
    def __init__(self):
        self.config = load_config()
        load_dotenv()  # Load environment variables
        
        # Initialize components
        self.scraper = NewsScraper()
        self.summarizer = StorySummarizer()
        self.resend = Resend(api_key=os.getenv('RESEND_API_KEY'))
        
        # Ensure output directory exists
        ensure_directory('output')
        
    def generate_html(self, stories: list) -> str:
        """Generate HTML from MJML template."""
        try:
            # Load and render MJML template
            env = Environment(loader=FileSystemLoader('templates'))
            template = env.get_template('newsletter.mjml')
            
            # Render template with data
            mjml_content = template.render(
                stories=stories,
                date=get_current_date(),
                year=get_current_year()
            )
            
            # Write MJML to temporary file
            with open('output/temp.mjml', 'w') as f:
                f.write(mjml_content)
            
            # Convert MJML to HTML
            result = subprocess.run(
                ['mjml', 'output/temp.mjml', '-o', 'output/newsletter.html'],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                raise Exception(f"MJML conversion failed: {result.stderr}")
            
            # Read generated HTML
            with open('output/newsletter.html', 'r') as f:
                html_content = f.read()
            
            # Clean up temporary file
            os.remove('output/temp.mjml')
            
            return html_content
            
        except Exception as e:
            logger.error(f"Error generating HTML: {str(e)}")
            raise

    def send_newsletter(self, html_content: str) -> bool:
        """Send the newsletter via Resend."""
        try:
            email_config = self.config['email']
            
            response = self.resend.emails.send({
                "from": email_config['from'],
                "to": email_config['to'],
                "subject": email_config['subject'].replace('{{ date }}', get_current_date()),
                "html": html_content
            })
            
            logger.info(f"Newsletter sent successfully: {response}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending newsletter: {str(e)}")
            return False

    def generate_and_send(self) -> bool:
        """Main function to generate and send the newsletter."""
        try:
            # Scrape stories
            logger.info("Scraping stories...")
            stories = self.scraper.scrape_all_sources()
            
            if not stories:
                logger.error("No stories found!")
                return False
            
            # Summarize stories
            logger.info("Summarizing stories...")
            stories = self.summarizer.summarize_stories(stories)
            
            # Generate HTML
            logger.info("Generating HTML...")
            html_content = self.generate_html(stories)
            
            # Send newsletter
            logger.info("Sending newsletter...")
            success = self.send_newsletter(html_content)
            
            return success
            
        except Exception as e:
            logger.error(f"Error in newsletter generation: {str(e)}")
            return False

def main():
    """Main entry point."""
    generator = NewsletterGenerator()
    success = generator.generate_and_send()
    
    if success:
        logger.info("Newsletter process completed successfully!")
    else:
        logger.error("Newsletter process failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
