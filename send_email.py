import os
import sys
import logging
import argparse
from datetime import datetime
from dotenv import load_dotenv
import resend
# from utils import ensure_dir
# from crawler.scrape import get_stories
# from ai.summarize import summarize_stories
# from templates.newsletter import generate_newsletter

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description='Generate and send daily newsletter')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose logging')
    args = parser.parse_args()
    
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    # Load environment variables
    load_dotenv()
    
    # Debug: Print environment variables (without values)
    logger.debug("Environment variables:")
    for var in ['RESEND_API_KEY', 'EMAIL_FROM', 'EMAIL_TO']:
        if os.getenv(var):
            logger.debug(f"{var} is set")
        else:
            logger.debug(f"{var} is not set")
    
    # Get API key from environment
    api_key = os.getenv('RESEND_API_KEY')
    if not api_key:
        logger.error("RESEND_API_KEY not found in environment variables")
        sys.exit(1)
    
    # Get email configuration
    email_from = os.getenv('EMAIL_FROM')
    email_to = os.getenv('EMAIL_TO')
    
    if not email_from or not email_to:
        logger.error("EMAIL_FROM and EMAIL_TO must be set in environment variables")
        sys.exit(1)
    
    logger.info(f"Sending email from {email_from} to {email_to}")
    
    # Initialize Resend client
    try:
        resend_client = resend.Client(api_key)
        logger.debug("Resend client initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Resend client: {str(e)}")
        sys.exit(1)
    
    # Simple test email content
    html_content = """
    <html>
        <body>
            <h1>Paperboy Test Email</h1>
            <p>This is a test email from your Paperboy newsletter service.</p>
            <p>Sent at: {}</p>
        </body>
    </html>
    """.format(datetime.now().strftime("%B %d, %Y %H:%M:%S"))
    
    text_content = "Paperboy Test Email\n\nThis is a test email from your Paperboy newsletter service.\nSent at: {}".format(
        datetime.now().strftime("%B %d, %Y %H:%M:%S")
    )
    
    try:
        # Send email
        logger.debug("Attempting to send email...")
        response = resend_client.emails.send({
            "from": email_from,
            "to": email_to,
            "subject": "Paperboy Test Email",
            "html": html_content,
            "text": text_content
        })
        logger.info("Email sent successfully!")
        logger.debug(f"Email response: {response}")
    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")
        sys.exit(1)

    # TODO: Uncomment when ready to implement full newsletter functionality
    """
    logger.info("Starting newsletter generation...")
    
    # Get stories
    logger.debug("Fetching stories...")
    stories = get_stories()
    logger.info(f"Found {len(stories)} stories")
    
    # Summarize stories
    logger.debug("Summarizing stories...")
    summarized_stories = summarize_stories(stories)
    logger.info("Stories summarized successfully")
    
    # Generate newsletter
    logger.debug("Generating newsletter...")
    html_content, text_content = generate_newsletter(summarized_stories)
    logger.info("Newsletter generated successfully")
    
    # Save to files
    ensure_dir('output')
    with open('output/newsletter.html', 'w') as f:
        f.write(html_content)
    with open('output/newsletter.txt', 'w') as f:
        f.write(text_content)
    logger.info("Newsletter saved to output directory")
    """

if __name__ == "__main__":
    main()
