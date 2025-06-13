# Paperboy

A free, automated, daily email newsletter that delivers 7 timely stories from curated news sources in a casual, fact-based tone. Named in homage to the classic NES game where you delivered newspapers to subscribers, this project brings that same spirit of daily news delivery into the digital age.

## Features

- Automated daily newsletter generation
- RSS and HTML scraping from multiple sources
- AI-powered story summarization using Ollama
- Responsive email template using MJML
- Free tier optimized (GitHub Actions + Resend)

## Setup

### Local Development

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/paperboy.git
   cd paperboy
   ```

2. Create and activate a virtual environment:
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install MJML:
   ```bash
   npm install -g mjml
   ```

5. Create a `.env` file with your configuration:
   ```
   RESEND_API_KEY=your_resend_api_key_here
   EMAIL_FROM=newsletter@yourdomain.com
   EMAIL_TO=your-email@example.com
   ```

6. Run the newsletter generation:
   ```bash
   python send_email.py
   ```

### GitHub Actions Setup

1. Fork this repository

2. Add the following secrets to your repository:
   - `RESEND_API_KEY`: Your Resend API key
   - `EMAIL_FROM`: The sender email address
   - `EMAIL_TO`: The recipient email address

3. The workflow will run daily at 8 AM UTC and send the newsletter to your email.

## Configuration

Edit `config.yaml` to customize:
- News sources
- Maximum number of articles
- Email settings
- Summary length

## Project Structure

```
/paperboy
├── .github/workflows/daily.yml  # Scheduled GitHub Action
├── config.yaml                  # List of news sources
├── crawler/                     # News scraping
├── ai/                         # LLM summarization
├── templates/                  # MJML email template
├── output/                     # Generated HTML
├── send_email.py              # Email sending
├── utils.py                   # Shared helpers
└── requirements.txt           # Python dependencies
```

## Contributing

Feel free to submit issues and enhancement requests! 

## License

This project is licensed under the MIT License - see the LICENSE file for details. 