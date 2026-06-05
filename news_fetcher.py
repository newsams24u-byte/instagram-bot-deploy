import requests
import os
from typing import List, Dict

class NewsFetcher:
    def __init__(self):
        self.newsapi_key = os.getenv("NEWSAPI_KEY")
        self.base_url = "https://newsapi.org/v2"
    
    def fetch_bangalore_news(self) -> List[Dict]:
        """Fetch latest Bangalore news"""
        try:
            url = f"{self.base_url}/everything"
            params = {
                "q": "Bangalore OR Bengaluru",
                "sortBy": "publishedAt",
                "language": "en",
                "apiKey": self.newsapi_key,
                "pageSize": 5
            }
            response = requests.get(url, params=params)
            if response.status_code == 200:
                articles = response.json().get("articles", [])
                return [self._format_article(a) for a in articles]
        except Exception as e:
            print(f"Error fetching Bangalore news: {e}")
        return []
    
    def fetch_india_news(self) -> List[Dict]:
        """Fetch latest India news"""
        try:
            url = f"{self.base_url}/everything"
            params = {
                "q": "India",
                "sortBy": "publishedAt",
                "language": "en",
                "apiKey": self.newsapi_key,
                "pageSize": 5
            }
            response = requests.get(url, params=params)
            if response.status_code == 200:
                articles = response.json().get("articles", [])
                return [self._format_article(a) for a in articles]
        except Exception as e:
            print(f"Error fetching India news: {e}")
        return []
    
    def _format_article(self, article: Dict) -> Dict:
        """Format article for processing"""
        return {
            "title": article.get("title", ""),
            "description": article.get("description", ""),
            "content": article.get("content", ""),
            "url": article.get("url", ""),
            "image": article.get("urlToImage", ""),
            "source": article.get("source", {}).get("name", ""),
            "publishedAt": article.get("publishedAt", "")
        }
    
    def get_top_news(self) -> Dict:
        """Get the most important news (Bangalore first, then India)"""
        bangalore_news = self.fetch_bangalore_news()
        
        if bangalore_news:
            return {
                "type": "bangalore",
                "article": bangalore_news[0]
            }
        
        # Fallback to India news if no Bangalore news
        india_news = self.fetch_india_news()
        if india_news:
            return {
                "type": "india",
                "article": india_news[0]
            }
        
        return None
