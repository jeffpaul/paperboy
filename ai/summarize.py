import requests
import json
from typing import Dict, Any, List
import logging
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import clean_text

logger = logging.getLogger(__name__)

class StorySummarizer:
    def __init__(self, model: str = "mixtral"):
        self.model = model
        self.ollama_url = "http://localhost:11434/api/generate"
        
    def _generate_prompt(self, story: Dict[str, Any]) -> str:
        """Generate a prompt for the LLM."""
        return f"""Please provide a concise, engaging summary of this news story in 2-3 sentences. 
        Write in a casual, journalistic tone. Focus on the key facts and why they matter.

        Title: {story['title']}
        Source: {story['source']}
        Content: {story.get('text', story.get('summary', ''))}

        Summary:"""

    def summarize_story(self, story: Dict[str, Any]) -> Dict[str, Any]:
        """Summarize a single story using Ollama."""
        try:
            prompt = self._generate_prompt(story)
            
            response = requests.post(
                self.ollama_url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                summary = clean_text(result.get('response', ''))
                
                # Update the story with the new summary
                story['summary'] = summary
                return story
            else:
                logger.error(f"Error from Ollama API: {response.status_code}")
                return story
                
        except Exception as e:
            logger.error(f"Error summarizing story: {str(e)}")
            return story

    def summarize_stories(self, stories: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Summarize a list of stories."""
        summarized_stories = []
        
        for story in stories:
            try:
                summarized = self.summarize_story(story)
                summarized_stories.append(summarized)
            except Exception as e:
                logger.error(f"Error processing story {story.get('title', '')}: {str(e)}")
                summarized_stories.append(story)
                
        return summarized_stories

def main():
    """Test function for the summarizer."""
    # Test story
    test_story = {
        'title': 'Test Article',
        'source': 'Test Source',
        'text': 'This is a test article with some content that needs to be summarized.',
        'url': 'https://example.com'
    }
    
    summarizer = StorySummarizer()
    result = summarizer.summarize_story(test_story)
    
    print(f"Original: {test_story['text']}")
    print(f"Summarized: {result['summary']}")

if __name__ == "__main__":
    main()
