#!/usr/bin/env python3
"""
Updated Bot Agent that saves posts to database for web review
"""
import os
import sys
import time
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from content_fetcher import ContentFetcher
from advanced_content_generator import AdvancedContentGenerator
from advanced_image_creator import AdvancedImageCreator
from models import db
from post_manager import PostManager
from web_app import app

# Load environment variables
load_dotenv()

class BotAgentWithWebDashboard:
    def __init__(self):
        self.content_fetcher = ContentFetcher()
        self.content_generator = AdvancedContentGenerator()
        self.image_creator = AdvancedImageCreator()
        self.post_manager = PostManager()
        self.scheduler = BackgroundScheduler()
    
    def create_and_queue_post(self):
        """Fetch content, generate caption, create image, and SAVE to database for review"""
        print("\n" + "="*70)
        print("🤖 INSTAGRAM BOT - Content Creation Cycle")
        print("="*70)
        
        try:
            # Step 1: Fetch random content
            print("📥 Fetching random Bangalore content...")
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
            
            # Step 4: SAVE to database (not post yet)
            print("💾 Saving to dashboard for review...")
            with app.app_context():
                post = self.post_manager.create_post(
                    image_path=image_path,
                    caption=caption,
                    content_type=content_type,
                    auto_approve_minutes=30,  # Auto-approve after 30 mins
                    metadata=str(content)
                )
            
            print(f"✅ Post created! ID: {post.id}")
            print("⏳ Waiting for your approval in the dashboard...")
            print("   (Auto-posting in 30 minutes if not reviewed)")
        
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
    
    def start_agent(self, post_interval: int = 30):
        """Start the bot scheduler"""
        print("\n" + "="*70)
        print("🚀 BANGALORE INSTAGRAM BOT - WITH WEB DASHBOARD")
        print("="*70)
        print(f"⏱️ Creating posts every {post_interval} minutes")
        print("📋 Posts will appear in web dashboard for review")
        print("⏳ Auto-approve after 30 minutes if not reviewed")
        print("📤 Auto-post to Instagram after approval")
        print("\n🌐 Open http://localhost:5000 in your browser")
        print("Press Ctrl+C to stop\n")
        
        # Run first post immediately
        self.create_and_queue_post()
        
        # Schedule posting
        self.scheduler.add_job(
            self.create_and_queue_post,
            'interval',
            minutes=post_interval,
            id='post_creator'
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
    
    agent = BotAgentWithWebDashboard()
    agent.start_agent(post_interval=interval)

if __name__ == "__main__":
    main()
