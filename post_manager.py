import os
from datetime import datetime, timedelta
from models import db, Post, PostHistory
from instagram_poster import InstagramPoster
from pathlib import Path

class PostManager:
    """Manage post lifecycle: create, approve, post, archive"""
    
    def __init__(self):
        self.instagram_poster = InstagramPoster()
    
    def create_post(self, image_path: str, caption: str, content_type: str, 
                   auto_approve_minutes: int = 30, metadata: str = None) -> Post:
        """Create a new pending post"""
        
        post = Post(
            image_path=image_path,
            caption=caption,
            original_caption=caption,
            content_type=content_type,
            status='pending',
            auto_approve_time=datetime.utcnow() + timedelta(minutes=auto_approve_minutes),
            metadata=metadata,
            order=self._get_next_order()
        )
        
        db.session.add(post)
        db.session.commit()
        
        print(f"✅ Post created (ID: {post.id}, Auto-approve in {auto_approve_minutes} mins)")
        return post
    
    def get_pending_posts(self) -> list:
        """Get all pending posts sorted by order"""
        posts = Post.query.filter_by(status='pending').order_by(Post.order).all()
        return [p.to_dict() for p in posts]
    
    def get_all_posts(self, limit: int = 100):
        """Get all posts with various statuses"""
        posts = Post.query.order_by(Post.created_at.desc()).limit(limit).all()
        return [p.to_dict() for p in posts]
    
    def approve_post(self, post_id: int, modified_caption: str = None) -> bool:
        """Approve a post for publishing"""
        try:
            post = Post.query.get(post_id)
            if not post:
                print(f"❌ Post {post_id} not found")
                return False
            
            # Update caption if modified
            if modified_caption:
                post.caption = modified_caption
            
            post.status = 'approved'
            post.approved_at = datetime.utcnow()
            db.session.commit()
            
            print(f"✅ Post {post_id} approved")
            return True
        
        except Exception as e:
            print(f"❌ Error approving post: {e}")
            return False
    
    def reject_post(self, post_id: int) -> bool:
        """Reject a post"""
        try:
            post = Post.query.get(post_id)
            if not post:
                return False
            
            post.status = 'rejected'
            db.session.commit()
            
            print(f"✅ Post {post_id} rejected")
            return True
        
        except Exception as e:
            print(f"❌ Error rejecting post: {e}")
            return False
    
    def reorder_posts(self, post_ids: list) -> bool:
        """Reorder pending posts via drag-drop"""
        try:
            for order, post_id in enumerate(post_ids):
                post = Post.query.get(post_id)
                if post:
                    post.order = order
            
            db.session.commit()
            print(f"✅ Posts reordered")
            return True
        
        except Exception as e:
            print(f"❌ Error reordering posts: {e}")
            return False
    
    def update_caption(self, post_id: int, new_caption: str) -> bool:
        """Update caption of a pending post"""
        try:
            post = Post.query.get(post_id)
            if not post or post.status != 'pending':
                return False
            
            post.caption = new_caption
            db.session.commit()
            
            print(f"✅ Caption updated for post {post_id}")
            return True
        
        except Exception as e:
            print(f"❌ Error updating caption: {e}")
            return False
    
    def auto_approve_posts(self) -> int:
        """Auto-approve posts that exceeded auto-approve time"""
        try:
            now = datetime.utcnow()
            expired_posts = Post.query.filter(
                Post.status == 'pending',
                Post.auto_approve_time <= now
            ).all()
            
            approved_count = 0
            for post in expired_posts:
                post.status = 'approved'
                post.approved_at = now
                approved_count += 1
            
            if approved_count > 0:
                db.session.commit()
                print(f"⏰ Auto-approved {approved_count} posts")
            
            return approved_count
        
        except Exception as e:
            print(f"❌ Error in auto-approve: {e}")
            return 0
    
    def post_to_instagram(self, post_id: int) -> bool:
        """Post an approved post to Instagram"""
        try:
            post = Post.query.get(post_id)
            if not post or post.status != 'approved':
                print(f"❌ Post {post_id} not approved or not found")
                return False
            
            # Check if image exists
            if not os.path.exists(post.image_path):
                print(f"❌ Image not found: {post.image_path}")
                post.status = 'rejected'
                db.session.commit()
                return False
            
            # Post to Instagram
            success = self.instagram_poster.post_to_instagram(post.image_path, post.caption)
            
            if success:
                post.status = 'posted'
                post.posted_at = datetime.utcnow()
                
                # Archive to history
                history = PostHistory(
                    post_id=post.id,
                    image_path=post.image_path,
                    caption=post.caption,
                    content_type=post.content_type,
                    posted_at=datetime.utcnow()
                )
                db.session.add(history)
                db.session.commit()
                
                print(f"✅ Post {post_id} published to Instagram")
                return True
            else:
                print(f"❌ Failed to post {post_id} to Instagram")
                return False
        
        except Exception as e:
            print(f"❌ Error posting to Instagram: {e}")
            return False
    
    def post_all_approved(self) -> int:
        """Post all approved posts to Instagram"""
        try:
            approved_posts = Post.query.filter_by(status='approved').order_by(Post.order).all()
            
            posted_count = 0
            for post in approved_posts:
                if self.post_to_instagram(post.id):
                    posted_count += 1
            
            return posted_count
        
        except Exception as e:
            print(f"❌ Error posting approved posts: {e}")
            return 0
    
    def _get_next_order(self) -> int:
        """Get next order number for new post"""
        last_post = Post.query.order_by(Post.order.desc()).first()
        return (last_post.order + 1) if last_post else 0
