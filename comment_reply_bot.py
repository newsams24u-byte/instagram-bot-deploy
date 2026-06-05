import os
from instagrapi import Client
from typing import List, Dict

class CommentReplyBot:
    def __init__(self):
        self.username = os.getenv("INSTAGRAM_USERNAME")
        self.password = os.getenv("INSTAGRAM_PASSWORD")
        self.cl = None
        self.max_replies = int(os.getenv("MAX_REPLIES_PER_POST", 5))
    
    def connect(self) -> bool:
        """Login to Instagram"""
        try:
            self.cl = Client()
            self.cl.login(self.username, self.password)
            print("✅ Connected to Instagram")
            return True
        except Exception as e:
            print(f"❌ Failed to connect: {e}")
            return False
    
    def get_post_comments(self, media_id: int) -> List[Dict]:
        """Get recent comments on a post"""
        try:
            media = self.cl.media_info(media_id)
            comments = self.cl.media_comments(media_id, amount=self.max_replies)
            
            comment_data = []
            for comment in comments[:self.max_replies]:
                comment_data.append({
                    "id": comment.pk,
                    "text": comment.text,
                    "user": comment.user.username,
                    "media_id": media_id
                })
            
            return comment_data
        except Exception as e:
            print(f"❌ Error getting comments: {e}")
            return []
    
    def reply_to_comment(self, media_id: int, comment_id: int, reply_text: str) -> bool:
        """Reply to a comment"""
        try:
            self.cl.comment_reply(reply_text, comment_id)
            print(f"✅ Replied to comment: {reply_text[:50]}...")
            return True
        except Exception as e:
            print(f"❌ Failed to reply: {e}")
            return False
    
    def engage_on_post(self, media_id: int, reply_generator, post_type: str) -> int:
        """Reply to comments on a post"""
        try:
            comments = self.get_post_comments(media_id)
            replied_count = 0
            
            for comment in comments[:self.max_replies]:
                reply_text = reply_generator(comment["text"], post_type)
                if self.reply_to_comment(media_id, comment["id"], reply_text):
                    replied_count += 1
            
            print(f"💬 Replied to {replied_count} comments")
            return replied_count
        
        except Exception as e:
            print(f"❌ Error engaging: {e}")
            return 0
