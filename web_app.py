import os
import json
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from models import db, Post
from post_manager import PostManager

# Load environment
load_dotenv()

# Initialize Flask app
app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instagram_posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)
post_manager = PostManager()
scheduler = BackgroundScheduler()

# ======================== DATABASE SETUP ========================

def init_db():
    """Initialize database"""
    with app.app_context():
        db.create_all()
        print("✅ Database initialized")

# ======================== BACKGROUND TASKS ========================

def auto_approve_task():
    """Auto-approve posts every minute"""
    with app.app_context():
        post_manager.auto_approve_posts()

def auto_post_task():
    """Auto-post approved posts every 5 minutes"""
    with app.app_context():
        posted = post_manager.post_all_approved()
        if posted > 0:
            print(f"📤 Auto-posted {posted} posts to Instagram")

# ======================== API ROUTES ========================

@app.route('/')
def dashboard():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/posts', methods=['GET'])
def get_posts():
    """Get all pending posts"""
    try:
        posts = post_manager.get_pending_posts()
        return jsonify({
            'success': True,
            'posts': posts,
            'count': len(posts)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/posts/all', methods=['GET'])
def get_all_posts():
    """Get all posts with history"""
    try:
        limit = request.args.get('limit', 50, type=int)
        posts = post_manager.get_all_posts(limit=limit)
        return jsonify({
            'success': True,
            'posts': posts,
            'count': len(posts)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/posts/<int:post_id>/approve', methods=['POST'])
def approve_post(post_id):
    """Approve a post"""
    try:
        data = request.json
        modified_caption = data.get('caption')
        
        success = post_manager.approve_post(post_id, modified_caption)
        
        return jsonify({
            'success': success,
            'message': 'Post approved' if success else 'Failed to approve'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/posts/<int:post_id>/reject', methods=['POST'])
def reject_post(post_id):
    """Reject a post"""
    try:
        success = post_manager.reject_post(post_id)
        
        return jsonify({
            'success': success,
            'message': 'Post rejected' if success else 'Failed to reject'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/posts/reorder', methods=['POST'])
def reorder_posts():
    """Reorder posts via drag-drop"""
    try:
        data = request.json
        post_ids = data.get('post_ids', [])
        
        success = post_manager.reorder_posts(post_ids)
        
        return jsonify({
            'success': success,
            'message': 'Posts reordered' if success else 'Failed to reorder'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/posts/<int:post_id>/caption', methods=['PUT'])
def update_caption(post_id):
    """Update post caption"""
    try:
        data = request.json
        new_caption = data.get('caption', '')
        
        success = post_manager.update_caption(post_id, new_caption)
        
        return jsonify({
            'success': success,
            'message': 'Caption updated' if success else 'Failed to update'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/posts/<int:post_id>', methods=['POST'])
def post_single(post_id):
    """Manually post a single post to Instagram"""
    try:
        post = Post.query.get(post_id)
        if not post or post.status != 'approved':
            return jsonify({
                'success': False,
                'message': 'Post not approved'
            }), 400
        
        success = post_manager.post_to_instagram(post_id)
        
        return jsonify({
            'success': success,
            'message': 'Posted to Instagram' if success else 'Failed to post'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get dashboard statistics"""
    try:
        with app.app_context():
            pending = Post.query.filter_by(status='pending').count()
            approved = Post.query.filter_by(status='approved').count()
            posted = Post.query.filter_by(status='posted').count()
            rejected = Post.query.filter_by(status='rejected').count()
            
            return jsonify({
                'success': True,
                'stats': {
                    'pending': pending,
                    'approved': approved,
                    'posted': posted,
                    'rejected': rejected,
                    'total': pending + approved + posted + rejected
                }
            })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ======================== ERROR HANDLERS ========================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# ======================== STARTUP ========================

def start_app():
    """Start the web app and scheduler"""
    init_db()
    
    # Start scheduler
    scheduler.add_job(auto_approve_task, 'interval', minutes=1, id='auto_approve')
    scheduler.add_job(auto_post_task, 'interval', minutes=5, id='auto_post')
    scheduler.start()
    
    print("\n" + "="*60)
    print("🌐 INSTAGRAM POST MANAGER - WEB DASHBOARD")
    print("="*60)
    print("✅ Database initialized")
    print("✅ Auto-approve scheduler active (every minute)")
    print("✅ Auto-post scheduler active (every 5 minutes)")
    print("🚀 Starting web server...")
    print("\n📱 Open: http://localhost:5000")
    print("\n")

if __name__ == '__main__':
    start_app()
    app.run(debug=False, host='0.0.0.0', port=5000)
