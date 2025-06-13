import os
import logging
from dotenv import load_dotenv
from resend import Resend
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    # Load environment variables
    load_dotenv()
    
    # Get API key from environment
    api_key = os.getenv('RESEND_API_KEY')
    if not api_key:
        logger.error("RESEND_API_KEY not found in environment variables")
        return
    
    # Get email configuration
    email_from = os.getenv('EMAIL_FROM')
    email_to = os.getenv('EMAIL_TO')
    
    if not email_from or not email_to:
        logger.error("EMAIL_FROM and EMAIL_TO must be set in environment variables")
        return
    
    # Initialize Resend client
    resend = Resend(api_key)
    
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
        response = resend.emails.send({
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

if __name__ == "__main__":
    main()
