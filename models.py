import os
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Post(db.Model):
    """Database model for Instagram posts"""
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    image_path = db.Column(db.String(500), nullable=False)
    caption = db.Column(db.Text, nullable=False)
    original_caption = db.Column(db.Text, nullable=False)
    content_type = db.Column(db.String(50), nullable=False)  # news, weather, traffic, etc.
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected, posted
    order = db.Column(db.Integer, default=0)  # for drag-drop ordering
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    approved_at = db.Column(db.DateTime)
    posted_at = db.Column(db.DateTime)
    instagram_media_id = db.Column(db.String(100))
    auto_approve_time = db.Column(db.DateTime)  # When to auto-approve
    metadata = db.Column(db.Text)  # JSON string for additional data
    
    def to_dict(self):
        """Convert to dictionary for JSON response"""
        return {
            'id': self.id,
            'image_path': self.image_path,
            'caption': self.caption,
            'original_caption': self.original_caption,
            'content_type': self.content_type,
            'status': self.status,
            'order': self.order,
            'created_at': self.created_at.isoformat(),
            'approved_at': self.approved_at.isoformat() if self.approved_at else None,
            'posted_at': self.posted_at.isoformat() if self.posted_at else None,
            'auto_approve_time': self.auto_approve_time.isoformat() if self.auto_approve_time else None,
            'time_until_auto_approve': self._get_time_until_auto_approve()
        }
    
    def _get_time_until_auto_approve(self):
        """Get remaining time until auto-approve"""
        if self.auto_approve_time and self.status == 'pending':
            remaining = self.auto_approve_time - datetime.utcnow()
            if remaining.total_seconds() > 0:
                return int(remaining.total_seconds())
        return 0


class PostHistory(db.Model):
    """Archive of posted content"""
    __tablename__ = 'post_history'
    
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    image_path = db.Column(db.String(500))
    caption = db.Column(db.Text)
    content_type = db.Column(db.String(50))
    instagram_media_id = db.Column(db.String(100))
    posted_at = db.Column(db.DateTime, default=datetime.utcnow)
    engagement_comments = db.Column(db.Integer, default=0)
    engagement_likes = db.Column(db.Integer, default=0)
