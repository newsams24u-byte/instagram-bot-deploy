# 🏗️ BACKEND ARCHITECTURE EXPLAINED

## What's Currently Running

Your Instagram bot has **2 parts**:

### Part 1: Bot Agent (Local - Your Machine)

```python
bot_agent_with_web.py
├── Fetches Bangalore news, weather, traffic, etc.
├── Generates captions with Claude AI
├── Creates Instagram images
├── SAVES to database every 30 minutes
└── Runs 24/7 on your computer
```

### Part 2: Web Dashboard (Local - Your Machine)

```python
web_app.py (Flask Backend)
├── Stores posts in SQLite database
├── Provides REST API (/api/posts, /api/stats, etc.)
├── Serves HTML/CSS/JavaScript dashboard
├── Runs on http://localhost:5000
└── Only accessible from YOUR computer
```

---

## The Problem

```
Current Setup:
┌─────────────────────────────┐
│   Your Computer             │
│ ┌───────────────────────┐   │
│ │ Bot Agent             │   │
│ │ (generates posts)     │   │
│ └───────────────────────┘   │
│            ↓                 │
│ ┌───────────────────────┐   │
│ │ SQLite Database       │   │
│ │ (stores posts)        │   │
│ └───────────────────────┘   │
│            ↓                 │
│ ┌───────────────────────┐   │
│ │ Flask Web App         │   │
│ │ (dashboard)           │   │
│ └───────────────────────┘   │
│            ↓                 │
│    http://localhost:5000    │
│ (only YOU can access)       │
└─────────────────────────────┘

❌ Problem:
- Can only access from home WiFi
- If computer shuts down, app stops
- Can't share link with others
- Not scalable
```

---

## The Solution: Cloud Deployment

```
After Deployment:
┌─────────────────────────────┐
│   Your Computer             │
│ ┌───────────────────────┐   │
│ │ Bot Agent             │   │
│ │ (generates posts)     │   │
│ └───────────────────────┘   │
│            ↓                 │
│     (Sends POST requests)    │
│            ↓                 │
└─────────────────────────────┘
            ↓
┌──────────────────────────────────────────────┐
│         CLOUD (Render.com)                   │
│ ┌──────────────────────────────────────────┐ │
│ │ PostgreSQL Database                      │ │
│ │ (Persistent, always available)           │ │
│ └──────────────────────────────────────────┘ │
│            ↑                                  │
│ ┌──────────────────────────────────────────┐ │
│ │ Flask Web App (Deployed)                 │ │
│ │ /api/posts                               │ │
│ │ /api/stats                               │ │
│ │ /api/posts/<id>/approve                  │ │
│ └──────────────────────────────────────────┘ │
│            ↓                                  │
│ https://instagram-bot.onrender.com          │
│ (Anyone can access from anywhere!)          │
└──────────────────────────────────────────────┘

✅ Benefits:
- Access from anywhere
- Always running (no downtime)
- Share link with others
- Bot runs independently
- Database persists
- Professional setup
```

---

## Backend Files Explained

### Core Backend (What Gets Deployed)

**`web_app.py`** - Flask web server

```python
@app.route('/api/posts')           # Get pending posts
@app.route('/api/posts/<id>/approve')  # Approve post
@app.route('/api/stats')           # Get statistics
# ... more endpoints
```

- Runs on cloud
- Responds to API requests
- Handles database operations

**`models.py`** - Database models

```python
class Post(db.Model):
    id = Column(Integer)
    image_path = Column(String)
    caption = Column(Text)
    status = Column(String)  # pending/approved/posted
    # ... more fields
```

- Defines database structure
- Auto-creates tables on deployment

**`post_manager.py`** - Business logic

```python
def create_post()      # Save new post to database
def approve_post()     # Mark post as approved
def post_to_instagram() # Post to Instagram
def auto_approve_posts() # Auto-approve after 30 mins
```

- Manages post lifecycle
- Handles database operations

**`templates/dashboard.html`** - Frontend HTML

```html
<div id="posts-list">
  <!-- Posts display here -->
</div>
```

- Beautiful dashboard UI
- Runs in browser

**`static/app.js`** - Frontend logic

```javascript
function loadPosts() { ... }        // Fetch posts from API
function approvePost(id) { ... }    // Approve via API
function updateCaption(id) { ... }  // Edit caption
```

- Interactive dashboard
- Calls backend API

### Deployment Files (New!)

**`wsgi.py`** - Production entry point

```python
from web_app import app
if __name__ == "__main__": app.run()
```

- Tells cloud provider how to start app
- Used by Render, Heroku, etc.

**`Procfile`** - Deployment configuration

```
web: gunicorn wsgi:app
```

- Tells Render: "Start Flask app with gunicorn"

**`requirements_deploy.txt`** - Dependencies

```
Flask==2.3.0
gunicorn==21.2.0      # NEW - for production
psycopg2-binary==2.9.0  # NEW - PostgreSQL support
# ... rest of packages
```

- Lists all Python packages needed

**`.gitignore`** - Don't commit secrets

```
.env                  # Don't push credentials
*.db                  # Don't push database
posts/               # Don't push images
```

**`render.yaml`** - Render-specific config

```yaml
runtime: python-3.11
install: pip install -r requirements_deploy.txt
start: gunicorn wsgi:app
```

---

## Data Flow Architecture

### Creating a Post

```
Bot Agent (Local)
  ↓
1. fetch_content()       Get news, weather, etc.
2. generate_caption()    Claude AI creates text
3. create_image()        Generate Instagram image
4. POST /api/posts       Send to cloud API
  ↓
Cloud Backend
  ↓
5. post_manager.create_post()
6. db.session.add(new_post)
7. db.session.commit()    Save to cloud database
  ↓
Cloud Database (PostgreSQL)
  ↓
8. posts table updated with new record
```

### Approving a Post

```
You (Browser)
  ↓
1. Open https://instagram-bot.onrender.com
2. See pending posts
3. Click "Approve" button
4. JavaScript: POST /api/posts/<id>/approve
  ↓
Cloud Backend
  ↓
5. post_manager.approve_post(post_id)
6. post.status = "approved"
7. post.approved_at = now
8. db.session.commit()
  ↓
Auto-Post (every 5 mins)
  ↓
9. Check approved posts
10. instagram_poster.post_to_instagram()
11. Instagram API uploads image
12. Post goes LIVE!
13. post.status = "posted"
14. Archive to history
```

---

## Technology Stack

```
Frontend (Browser)
├── HTML (dashboard.html)
├── CSS (style.css)
└── JavaScript (app.js)
    └── Calls REST API endpoints

Backend (Cloud Server - Render.com)
├── Python 3.11
├── Flask (web framework)
├── Gunicorn (production server)
├── SQLAlchemy (ORM)
├── SQLite/PostgreSQL (database)
└── APScheduler (task scheduling)

Local Bot (Your Machine)
├── Python 3.x
├── requests (fetch APIs)
├── Pillow (image creation)
├── anthropic (Claude AI)
├── instagrapi (Instagram)
└── APScheduler (30-min posts)
```

---

## API Endpoints (Backend)

```
GET  /api/posts                          Get pending posts
GET  /api/posts/all?limit=50            Get all posts
POST /api/posts/<id>/approve            Approve post
POST /api/posts/<id>/reject             Reject post
PUT  /api/posts/<id>/caption            Edit caption
POST /api/posts/reorder                 Reorder posts
POST /api/posts/<id>                    Post to Instagram
GET  /api/stats                         Get statistics
GET  /                                  Serve dashboard HTML
```

Each endpoint:

- Receives HTTP requests from browser
- Processes request (database operation)
- Returns JSON response
- Updates UI automatically

---

## Environment Variables (Backend)

```env
# Instagram Credentials
INSTAGRAM_USERNAME=bengaluru_nagara
INSTAGRAM_PASSWORD=Welcome1@!

# API Keys (for generating posts)
NEWSAPI_KEY=your_key
OPENWEATHER_API_KEY=your_key

# Database Connection (cloud)
DATABASE_URL=postgresql://user:pass@host/db

# App Config
FLASK_ENV=production
SECRET_KEY=random_secret
```

---

## Deployment Process

```
1. Code pushed to GitHub
   $ git push origin main
   ↓
2. Render webhook triggered
   $ Detects new push
   ↓
3. Build phase
   $ git clone your repo
   $ pip install -r requirements_deploy.txt
   ↓
4. Run phase
   $ gunicorn wsgi:app
   $ App starts on https://instagram-bot.onrender.com
   ↓
5. Your app is LIVE!
   Anyone can visit: https://instagram-bot.onrender.com
```

---

## Summary

```
BACKEND = Everything that runs on the cloud server

Files That Deploy:
✅ web_app.py (Flask app)
✅ models.py (database models)
✅ post_manager.py (business logic)
✅ templates/dashboard.html (UI HTML)
✅ static/app.js (interactive code)
✅ static/style.css (styling)
✅ instagram_posts.db (initial database)
✅ wsgi.py (entry point)
✅ requirements_deploy.txt (packages)

Files That Don't Deploy:
❌ bot_agent_with_web.py (runs on YOUR machine)
❌ .env (secrets, kept locally)
❌ posts/ (images saved locally during creation)

Result:
🌐 Web app accessible from anywhere
📱 Approve posts from phone
🤖 Bot runs independently on your machine
💾 Database persists in cloud
✅ Professional setup
```

---

**Next: Run the deployment agent to move your backend to the cloud!** 🚀
