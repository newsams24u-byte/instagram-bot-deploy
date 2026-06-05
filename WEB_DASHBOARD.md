# 🌐 WEB DASHBOARD - Complete Documentation

## Overview

The **Instagram Post Manager Web Dashboard** is a **free, simple web interface** where you can:

✅ **See Generated Posts** - All bot-created content with images  
✅ **Edit Captions** - Modify text before posting  
✅ **Approve/Reject** - One-click approval workflow  
✅ **Drag to Reorder** - Arrange posting order  
✅ **Auto-Approve** - Auto-approves after 30 mins  
✅ **Auto-Post** - Auto-posts approved content to Instagram  
✅ **Posted History** - Archive of all published posts

---

## 🏗️ Architecture

```
┌──────────────────────────────────────┐
│  Bot Agent (bot_agent_with_web.py)  │
│  - Fetches content (news, weather)   │
│  - Generates captions with Claude AI │
│  - Creates images                    │
│  - SAVES to Database                 │
└──────────────┬───────────────────────┘
               │
               ▼
┌──────────────────────────────────────┐
│  SQLite Database (instagram_posts.db)│
│  - Pending Posts                     │
│  - Approved Posts                    │
│  - Posted History                    │
└──────────────┬───────────────────────┘
               │
               ▼
┌──────────────────────────────────────┐
│  Web Dashboard (Flask + JavaScript)  │
│  http://localhost:5000               │
│  - View pending posts                │
│  - Edit captions                     │
│  - Approve/Reject                    │
│  - Drag to reorder                   │
└──────────────┬───────────────────────┘
               │
               ▼
┌──────────────────────────────────────┐
│  Instagram (via Instagrapi)          │
│  - Posts approved content            │
│  - Archives to history               │
└──────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Option 1: Run Bot + Web Dashboard Together

```bash
cd instagram_agent
chmod +x run_complete_system.sh
./run_complete_system.sh
```

Then open: **http://localhost:5000** in browser

### Option 2: Run Separately

**Terminal 1 - Web Dashboard:**

```bash
cd instagram_agent
source venv/bin/activate
python3 web_app.py
```

**Terminal 2 - Bot Agent:**

```bash
cd instagram_agent
source venv/bin/activate
python3 bot_agent_with_web.py
```

---

## 🎨 Dashboard Features

### 📋 Pending Posts Tab

Shows all posts waiting for review:

- **Image Preview** - See what will be posted
- **Content Type Badge** - News, Weather, Traffic, etc.
- **Status Badge** - Pending, Approved, Posted, Rejected
- **Auto-Approve Timer** - Countdown to auto-approval
- **Caption Preview** - Read the caption text
- **Created Date** - When post was generated

### 💫 Post Actions

#### Edit ✏️

- Click "Edit" button
- Modify caption text
- See character count (max 2200)
- Save changes

#### Approve ✅

- Instant approval
- Post moves to approved queue
- Manual posting option available

#### Reject ❌

- Remove post from queue
- Post archived as rejected

#### Post Now 📤

- For approved posts
- Manually post to Instagram immediately
- Moves to posted history

### 🔄 Drag to Reorder

- Click and drag posts to reorder
- Affects posting order
- Changes saved automatically

### ✅ Posted History Tab

Archive of all posted content:

- Shows posted date/time
- Images and captions
- Complete history

### 📊 Statistics Bar

Top-right shows real-time stats:

- Pending posts count
- Approved posts count
- Posted posts count
- Rejected posts count

---

## ⚙️ How It Works

### Timeline Example

**10:00 AM** - Bot generates post

- Content created
- Caption generated
- Image created
- Saved to dashboard
- Auto-approve timer: 30 mins

**10:05 AM** - You review post

- Open dashboard
- See new post
- Edit caption if needed
- Click "Approve"
- Status changes to "Approved"

**10:06 AM** - Auto-post starts

- Post Manager checks approved posts
- Posts to Instagram automatically
- Moves to history

**Alternative: No Manual Review**

- If you don't review by **10:30 AM**
- Post auto-approves
- Auto-posts within 5 minutes
- You never have to click anything!

---

## 🗄️ Database Structure

### Posts Table

| Column            | Type     | Purpose                              |
| ----------------- | -------- | ------------------------------------ |
| id                | Integer  | Post ID                              |
| image_path        | String   | Path to generated image              |
| caption           | Text     | Current caption                      |
| original_caption  | Text     | Original caption                     |
| content_type      | String   | news/weather/traffic/metro/meme/poll |
| status            | String   | pending/approved/rejected/posted     |
| order             | Integer  | Drag-drop order                      |
| created_at        | DateTime | When generated                       |
| approved_at       | DateTime | When approved                        |
| posted_at         | DateTime | When posted                          |
| auto_approve_time | DateTime | Auto-approve countdown               |
| metadata          | Text     | Additional data                      |

---

## 🔧 Configuration

Edit `.env`:

```env
POST_INTERVAL_MINUTES=30      # Generate new post every 30 mins
REPLY_TO_COMMENTS=true         # Bot replies to comments
MAX_REPLIES_PER_POST=5         # Max replies per post
```

---

## 📱 Frontend Features

### Beautiful Design

- Modern gradient UI
- Responsive (mobile-friendly)
- Dark/light compatible
- Smooth animations

### Real-Time Updates

- Auto-refresh every 30 seconds
- Live statistics
- Auto-approve countdown

### Drag-and-Drop

- Reorder posts by dragging
- Uses SortableJS library
- Changes saved automatically

### Modal Editor

- Large text area for caption editing
- Live character counter
- Image preview
- Save/Cancel buttons

---

## 🔄 Automated Workflows

### Auto-Approve (Every minute)

```
Check all pending posts
IF auto_approve_time <= now THEN
    Mark as "approved"
    Set approved_at timestamp
END
```

### Auto-Post (Every 5 minutes)

```
Check all approved posts
FOR EACH approved post DO
    Post to Instagram
    IF successful THEN
        Mark as "posted"
        Add to history
    END
END
```

---

## 📂 Files Structure

```
instagram_agent/
├── web_app.py                 # Flask web server
├── models.py                  # Database models
├── post_manager.py            # Post lifecycle management
├── bot_agent_with_web.py      # Updated bot agent
├── web_requirements.txt       # Web dependencies
├── run_complete_system.sh     # Combined launcher
│
├── templates/
│   └── dashboard.html         # Main UI
│
├── static/
│   ├── style.css             # Styling
│   └── app.js                # Frontend logic
│
├── posts/                     # Generated images
└── instagram_posts.db         # SQLite database
```

---

## 🚦 API Endpoints

### GET /api/posts

Get all pending posts

```json
{
  "success": true,
  "posts": [...],
  "count": 5
}
```

### POST /api/posts/<id>/approve

Approve a post

```json
{
  "success": true,
  "message": "Post approved"
}
```

### POST /api/posts/<id>/reject

Reject a post

### PUT /api/posts/<id>/caption

Update caption

```json
{
  "caption": "New caption text"
}
```

### POST /api/posts/reorder

Reorder posts

```json
{
  "post_ids": [1, 3, 2, 4]
}
```

### GET /api/stats

Get statistics

```json
{
  "stats": {
    "pending": 5,
    "approved": 2,
    "posted": 10,
    "rejected": 0
  }
}
```

---

## 💰 Cost Analysis

| Component           | Cost            |
| ------------------- | --------------- |
| Flask (Web Server)  | FREE            |
| SQLite (Database)   | FREE            |
| HTML/CSS/JavaScript | FREE            |
| Bot + APIs          | Already covered |
| **TOTAL**           | **FREE** ✅     |

---

## 🎯 Use Cases

### Use Case 1: Manual Review Mode

- Check dashboard every morning
- Review 10 posts
- Approve/edit as needed
- Post manually or let auto-post handle it

### Use Case 2: Hands-Free Mode

- Generate posts automatically
- Don't check dashboard
- Let auto-approve trigger after 30 mins
- Let auto-post post to Instagram
- Check history later

### Use Case 3: Hybrid Mode

- Review important posts manually
- Let regular posts auto-approve
- Drag to prioritize important content
- Post priority content immediately

---

## 🚨 Troubleshooting

### "Port 5000 already in use"

```bash
# Use different port
python3 web_app.py --port 5001
```

### "Database locked"

- Close other instances
- Delete `.db` file to reset
- Restart application

### "Posts not showing"

- Refresh browser (Ctrl+R)
- Check bot agent is running
- Check console for errors

### "Can't post to Instagram"

- Verify Instagram credentials in `.env`
- Check internet connection
- Review bot_agent_with_web.py logs

---

## 📈 Performance Tips

1. **Limit dashboard refresh** - Already set to 30 seconds
2. **Archive old posts** - Posts older than 30 days
3. **Database cleanup** - Periodic maintenance

---

## 🔒 Security Notes

- `.env` stores credentials locally (never shared)
- Database is local (instagram_posts.db)
- Web dashboard accessible only on localhost by default
- No authentication (for local use)

---

## 🎉 Summary

✅ **No Coding Required** - Just click buttons  
✅ **100% Free** - All open-source components  
✅ **Simple** - Minimal design, maximum functionality  
✅ **Auto-Capable** - Works hands-free  
✅ **Fully Featured** - Edit, reorder, approve, reject, post  
✅ **Mobile Responsive** - Works on phone too

---

**Ready? Start the system and open http://localhost:5000! 🚀**
