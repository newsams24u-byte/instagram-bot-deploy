#!/usr/bin/env python3
import os
import sys
import time
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from content_fetcher import ContentFetcher
from advanced_content_generator import AdvancedContentGenerator
from advanced_image_creator import AdvancedImageCreator
from instagram_poster import InstagramPoster
from comment_reply_bot import CommentReplyBot

# Load environment variables
load_dotenv()

class AdvancedInstagramBotAgent:
    def __init__(self):
        self.content_fetcher = ContentFetcher()
        self.content_generator = AdvancedContentGenerator()
        self.image_creator = AdvancedImageCreator()
        self.instagram_poster = InstagramPoster()
        self.comment_bot = CommentReplyBot()
        self.scheduler = BackgroundScheduler()
        self.last_media_id = None
    
    def create_and_post(self):
        """Main function to fetch content, generate caption, create image, and post"""
        print("\n" + "="*70)
        print("🤖 ADVANCED INSTAGRAM BOT - Content Creation Cycle")
        print("="*70)
        
        try:
            # Step 1: Fetch random content
            print("\n📥 Fetching random Bangalore content...")
            content = self.content_fetcher.get_random_content()
            
            if not content:
                print("❌ No content found. Skipping this cycle.")
                return
            
            content_type = content.get("type", "unknown")
            print(f"✅ Got: {content_type.upper()} content")
            
            # Step 2: Generate caption
            print(f"✍️ Generating {content_type} caption...")
            caption, title = self.content_generator.generate_caption(content)
            print(f"✅ Caption created (length: {len(caption)} chars)")
            
            # Step 3: Create image
            print("🖼️ Creating visual content...")
            image_path = self.image_creator.create_image(content)
            
            # Step 4: Post to Instagram
            print("📤 Posting to Instagram...")
            success = self.instagram_poster.post_to_instagram(image_path, caption)
            
            if success:
                print("🎉 POST PUBLISHED SUCCESSFULLY!")
                self.last_media_id = self._extract_media_id(image_path)
            else:
                print("⚠️ Post saved locally (Instagram posting unavailable)")
                self.last_media_id = None
        
        except Exception as e:
            print(f"❌ Error in content creation: {e}")
            import traceback
            traceback.print_exc()
    
    def engage_with_followers(self):
        """Reply to comments on posts"""
        print("\n" + "="*70)
        print("💬 COMMENT ENGAGEMENT CYCLE")
        print("="*70)
        
        if not self.last_media_id:
            print("⏭️ No recent post to engage with")
            return
        
        try:
            if not self.comment_bot.cl:
                if not self.comment_bot.connect():
                    print("❌ Cannot engage: Not connected to Instagram")
                    return
            
            print(f"📱 Engaging with recent post...")
            self.comment_bot.engage_on_post(
                self.last_media_id,
                self.content_generator.generate_comment_reply,
                "general"
            )
        
        except Exception as e:
            print(f"❌ Engagement error: {e}")
    
    def _extract_media_id(self, image_path: str):
        """Extract or generate media ID from image path"""
        import hashlib
        return int(hashlib.md5(image_path.encode()).hexdigest(), 16) % 10**10
    
    def start_agent(self, post_interval: int = 30, engage_after: int = 5):
        """Start the bot scheduler"""
        print("\n" + "="*70)
        print("🚀 BANGALORE INSTAGRAM BOT AGENT STARTED")
        print("="*70)
        print(f"⏱️ Posting every {post_interval} minutes")
        print(f"💬 Engaging with followers every {engage_after} posts")
        print("📍 Content: Bangalore News, Weather, Traffic, Metro, Memes, Polls")
        print("\nPress Ctrl+C to stop\n")
        
        # Verify Instagram credentials
        if not self.instagram_poster.is_configured():
            print("⚠️ Instagram credentials not configured!")
            print("   Add INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD to .env")
        
        # Verify API keys
        if not os.getenv("NEWSAPI_KEY"):
            print("❌ ERROR: NEWSAPI_KEY missing")
            sys.exit(1)
        if not os.getenv("OPENWEATHER_API_KEY"):
            print("❌ ERROR: OPENWEATHER_API_KEY missing")
            sys.exit(1)
        
        # Run first post immediately
        self.create_and_post()
        
        # Schedule posting
        self.scheduler.add_job(
            self.create_and_post,
            'interval',
            minutes=post_interval,
            id='post_creator'
        )
        
        # Schedule engagement
        self.scheduler.add_job(
            self.engage_with_followers,
            'interval',
            minutes=post_interval * engage_after,
            id='engagement_bot'
        )
        
        self.scheduler.start()
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n⏹️ Stopping bot agent...")
            self.scheduler.shutdown()
            print("✅ Bot agent stopped.")

def main():
    interval = int(os.getenv("POST_INTERVAL_MINUTES", 30))
    
    agent = AdvancedInstagramBotAgent()
    agent.start_agent(post_interval=interval)

if __name__ == "__main__":
    main()
