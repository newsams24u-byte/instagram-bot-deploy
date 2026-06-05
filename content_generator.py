import os
from typing import Dict, Tuple
import anthropic

class ContentGenerator:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.viral_hashtags = [
            "#BangaloreNews", "#BangaloreUpdates", "#BangaloreToday",
            "#IndiaNews", "#IndiaUpdates", "#BreakingNews",
            "#InstaNews", "#NewsAlert", "#TrendingNews",
            "#MustRead", "#StayUpdated", "#NewsOfTheDay",
            "#ShareThis", "#Bangalore", "#India"
        ]
        self.engagement_captions = [
            "What do you think about this?",
            "Drop your thoughts below 👇",
            "Tell us your take!",
            "Do you agree?",
            "Your opinion matters! Comment below",
            "Let's discuss this in the comments",
            "What's your view on this?",
            "Tag someone who needs to see this",
            "Swipe up to learn more",
            "Save this for later!"
        ]
    
    def generate_caption(self, article: Dict) -> Tuple[str, str]:
        """Generate Instagram caption with hashtags using Claude"""
        try:
            prompt = f"""Create a viral, engaging Instagram caption for this news article.

Title: {article.get('title', '')}
Description: {article.get('description', '')}

Requirements:
1. Keep it under 150 characters for main caption
2. Use emojis strategically (2-3)
3. Include an engagement hook
4. Add relevant hashtags (5-7)
5. Make it shareable and relatable

Return format:
CAPTION: [main caption]
HASHTAGS: [hashtags]"""

            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=200,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            response = message.content[0].text
            
            # Parse response
            caption = ""
            hashtags = ""
            
            for line in response.split("\n"):
                if line.startswith("CAPTION:"):
                    caption = line.replace("CAPTION:", "").strip()
                elif line.startswith("HASHTAGS:"):
                    hashtags = line.replace("HASHTAGS:", "").strip()
            
            # Add engagement caption
            engagement = self._get_random_engagement()
            full_caption = f"{caption}\n\n{engagement}\n\n{hashtags}"
            
            # Extract title for image
            title = article.get('title', '')[:50]
            
            return full_caption, title
            
        except Exception as e:
            print(f"Error generating caption: {e}")
            return self._get_fallback_caption(article)
    
    def _get_fallback_caption(self, article: Dict) -> Tuple[str, str]:
        """Fallback caption if AI generation fails"""
        title = article.get('title', '')[:50]
        source = article.get('source', 'News')
        
        caption = f"Breaking: {title}...\n\n"
        caption += self._get_random_engagement() + "\n\n"
        caption += " ".join(self.viral_hashtags[:5])
        
        return caption, title
    
    def _get_random_engagement(self) -> str:
        """Get random engagement caption"""
        import random
        return random.choice(self.engagement_captions)
