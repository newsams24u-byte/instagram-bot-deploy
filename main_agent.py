#!/usr/bin/env python3
import os
import sys
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from news_fetcher import NewsFetcher
from content_generator import ContentGenerator
from image_creator import ImageCreator
from instagram_poster import InstagramPoster
import time

# Load environment variables
load_dotenv()

class InstagramNewsAgent:
    def __init__(self):
        self.news_fetcher = NewsFetcher()
        self.content_generator = ContentGenerator()
        self.image_creator = ImageCreator()
        self.instagram_poster = InstagramPoster()
        self.scheduler = BackgroundScheduler()
    
    def create_and_post(self):
        """Main function to fetch news, generate content, create image, and post"""
        print("\n" + "="*60)
        print("🤖 Instagram News Agent - Creating Post")
        print("="*60)
        
        try:
            # Step 1: Fetch news
            print("📰 Fetching news...")
            news_data = self.news_fetcher.get_top_news()
            
            if not news_data:
                print("❌ No news found. Skipping this cycle.")
                return
            
            article = news_data['article']
            print(f"✅ Found {news_data['type'].upper()} news: {article['title'][:50]}...")
            
            # Step 2: Generate caption with hashtags
            print("✍️ Generating caption and hashtags...")
            caption, title = self.content_generator.generate_caption(article)
            print(f"✅ Caption generated:\n{caption[:100]}...")
            
            # Step 3: Create image
            print("🖼️ Creating image...")
            subtitle = article.get('description', '')[:80]
            image_path = self.image_creator.create_post_image(title, subtitle)
            
            # Step 4: Post to Instagram
            print("📤 Posting to Instagram...")
            if self.instagram_poster.is_configured():
                success = self.instagram_poster.post_to_instagram(image_path, caption)
                if success:
                    print("🎉 Post published successfully!")
                else:
                    print("⚠️ Failed to post. Image saved locally at:", image_path)
            else:
                print("⚠️ Instagram credentials not configured. Image saved at:", image_path)
                print("   Configure credentials in .env file to enable auto-posting")
        
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
    
    def start_scheduler(self, interval_minutes: int = 30):
        """Start the scheduler to post every N minutes"""
        print(f"\n🚀 Starting Instagram News Agent")
        print(f"⏱️ Will post every {interval_minutes} minutes")
        print("Press Ctrl+C to stop\n")
        
        # Run first post immediately
        self.create_and_post()
        
        # Schedule recurring posts
        self.scheduler.add_job(
            self.create_and_post,
            'interval',
            minutes=interval_minutes,
            id='instagram_poster'
        )
        
        self.scheduler.start()
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n⏹️ Stopping agent...")
            self.scheduler.shutdown()
            print("✅ Agent stopped.")

def main():
    # Get interval from environment or use default
    interval = int(os.getenv("POST_INTERVAL_MINUTES", 30))
    
    # Check for required API keys
    if not os.getenv("NEWSAPI_KEY"):
        print("❌ ERROR: NEWSAPI_KEY not found in .env file")
        print("Get it from: https://newsapi.org/")
        sys.exit(1)
    
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ ERROR: ANTHROPIC_API_KEY not found in .env file")
        print("Get it from: https://console.anthropic.com/")
        sys.exit(1)
    
    # Initialize and start agent
    agent = InstagramNewsAgent()
    agent.start_scheduler(interval)

if __name__ == "__main__":
    main()
