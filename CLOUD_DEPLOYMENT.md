# 🚀 CLOUD DEPLOYMENT GUIDE

## Current Architecture

```
Local Machine
├── Bot Agent (bot_agent_with_web.py)
│   └── Creates posts every 30 mins
├── SQLite Database (instagram_posts.db)
│   └── Stores posts locally
└── Web Dashboard (http://localhost:5000)
    └── Review & approve posts
```

**Problem:** Everything is local. Can't access from anywhere.

**Solution:** Deploy to cloud!

---

## ☁️ What Gets Deployed

✅ **Web App** (Flask backend)  
✅ **Database** (SQLite or PostgreSQL)  
✅ **Static Files** (HTML, CSS, JS)  
✅ **API Endpoints** (/api/posts, /api/stats, etc.)

**NOT deployed:** Bot Agent (runs on your machine)

---

## 📋 Backend Structure (What's Deployed)

```
instagram_agent/
├── web_app.py              ← Flask web server (DEPLOYED)
├── models.py               ← Database models (DEPLOYED)
├── post_manager.py         ← Post management logic (DEPLOYED)
├── wsgi.py                 ← Production entry point (NEW)
├── Procfile                ← Deployment config (NEW)
├── requirements_deploy.txt ← Dependencies (NEW)
├── templates/              ← HTML (DEPLOYED)
│   └── dashboard.html
├── static/                 ← CSS/JS (DEPLOYED)
│   ├── style.css
│   └── app.js
└── instagram_posts.db      ← Database (DEPLOYED)
```

---

## 🎯 Best Free Options

### 1️⃣ **RENDER.COM** (RECOMMENDED)

**Pros:**

- ✅ Free tier: 750 hours/month
- ✅ Auto-deploy from GitHub
- ✅ PostgreSQL available
- ✅ Simple UI
- ✅ SSL included
- ✅ 0.5GB RAM free

**Cons:**

- Spins down after 15 mins (paid tier to keep alive)

**Cost:** FREE  
**URL:** https://instagram-bot.onrender.com

---

### 2️⃣ **PYTHONANYWHERE**

**Pros:**

- ✅ Free tier always available
- ✅ Python-focused
- ✅ Easy console access
- ✅ File upload support

**Cons:**

- Limited compute power
- Limited storage
- Slower

**Cost:** FREE  
**URL:** https://<username>.pythonanywhere.com

---

### 3️⃣ **REPLIT** (EASIEST!)

**Pros:**

- ✅ Super easy setup
- ✅ Works immediately
- ✅ GitHub sync
- ✅ Browser-based editor

**Cons:**

- Goes to sleep after inactivity
- Limited compute

**Cost:** FREE  
**URL:** https://<project>.replit.dev

---

### 4️⃣ **GOOGLE CLOUD RUN**

**Pros:**

- ✅ Scalable
- ✅ Free: 2M requests/month
- ✅ Fast

**Cons:**

- More complex setup
- Requires Docker knowledge

**Cost:** FREE (within limits)

---

## 🚀 Deployment Steps (Render.com)

### Step 1: Prepare Code

```bash
cd instagram_agent

# Initialize git
git init
git add .
git commit -m "Initial commit"
```

### Step 2: Push to GitHub

```bash
# Create repo on github.com named "instagram-bot-deploy"
# Then:
git remote add origin https://github.com/YOUR-USERNAME/instagram-bot-deploy.git
git branch -M main
git push -u origin main
```

### Step 3: Create Render Account

1. Go to https://render.com
2. Sign up
3. Connect GitHub

### Step 4: Deploy

1. Click "New +" → "Web Service"
2. Connect "instagram-bot-deploy" repository
3. Configure:
   - Name: instagram-bot
   - Runtime: Python 3
   - Build: `pip install -r requirements_deploy.txt`
   - Start: `gunicorn wsgi:app`
   - Plan: Free

### Step 5: Add Environment Variables

In Render dashboard:

1. Go to Environment tab
2. Add variables:
   ```
   INSTAGRAM_USERNAME=bengaluru_nagara
   INSTAGRAM_PASSWORD=Welcome1@!
   NEWSAPI_KEY=your_key
   OPENWEATHER_API_KEY=your_key
   FLASK_ENV=production
   ```

### Step 6: Deploy

Click "Deploy"  
⏳ Wait 5-10 minutes  
✅ Your app is live!

**Your URL:** https://instagram-bot.onrender.com

---

## 🤖 How It Works After Deployment

### Architecture (After Deployment)

```
Your Local Machine
├── Bot Agent (bot_agent_with_web.py) ← RUN THIS
│   ├── Fetches news
│   ├── Generates captions
│   ├── Creates images
│   └── SAVES TO → CLOUD DATABASE
│
└── Shows logs: "Post saved to cloud database"

CLOUD (Render.com)
├── Flask Web App (deployed)
├── PostgreSQL Database (cloud)
├── Web Dashboard (https://...)
└── API Endpoints

You (Browser)
└── Open: https://instagram-bot.onrender.com
    ├── See posts from cloud database
    ├── Approve posts
    └── Posts go to Instagram
```

### Workflow

1. **On Your Machine:** Run bot agent

   ```bash
   python3 bot_agent_with_web.py
   ```

2. **Bot Creates Posts**
   - Fetches content
   - Generates caption
   - Creates image
   - **Sends to cloud database**

3. **On Your Phone/Browser**
   - Open: https://instagram-bot.onrender.com
   - See posts in real-time
   - Approve posts
   - Posts go to Instagram

4. **Auto-Actions**
   - Auto-approve after 30 mins
   - Auto-post after approval
   - Auto-archive to history

---

## 📊 Database Options

### Option 1: SQLite (Current)

- **Pros:** Simple, no setup
- **Cons:** Gets deleted on Render free tier
- **Recommendation:** For learning only

### Option 2: PostgreSQL (FREE on Render)

- **Pros:** Persistent, industry standard
- **Cons:** Need to modify code slightly
- **Recommendation:** For production

### Option 3: MongoDB Atlas (FREE)

- **Pros:** NoSQL, generous free tier
- **Cons:** Need to rewrite models
- **Recommendation:** For advanced users

For now, we'll use **SQLite on Render** (works fine for learning).

---

## 🎯 Run Deployment Agent

```bash
cd instagram_agent
python3 deployment_agent.py
```

This will:

1. Show deployment options
2. Provide step-by-step instructions
3. Open browser to hosting platform
4. Guide you through setup

---

## ✅ Verification

After deployment, check:

```bash
# Check if running
curl https://instagram-bot.onrender.com

# Response should be HTML dashboard
# Or try in browser: https://instagram-bot.onrender.com
```

---

## 🔄 Auto-Deployment from GitHub

After first deploy, any changes auto-deploy:

```bash
# Make changes
nano web_app.py

# Push to GitHub
git add .
git commit -m "Updated UI"
git push origin main

# Render automatically redeploys! ✅
```

---

## 📋 Files for Deployment

New files created:

```
wsgi.py                  ← Production entry point
Procfile                 ← Deployment config
requirements_deploy.txt  ← Dependencies
.gitignore              ← Don't commit secrets
render.yaml             ← Render-specific config
deployment_agent.py     ← Deployment helper
```

---

## 🚨 Troubleshooting

### "App keeps crashing"

- Check logs in Render dashboard
- Verify environment variables set
- Make sure requirements installed

### "Database disappears"

- Render free tier has ephemeral storage
- Use PostgreSQL for persistence
- Or use MongoDB Atlas

### "Images not showing"

- Make sure /posts directory exists
- Check image paths in database
- Upload images to cloud storage (Cloudinary - free tier)

---

## 💰 Cost Estimate

| Service             | Cost                 |
| ------------------- | -------------------- |
| Render.com          | FREE (750 hrs/month) |
| Cloudinary (images) | FREE (25GB)          |
| PostgreSQL          | FREE (1GB)           |
| **TOTAL**           | **FREE** ✅          |

---

## 🎉 Next Steps

1. Run `python3 deployment_agent.py`
2. Choose deployment platform
3. Follow step-by-step instructions
4. Deploy your app
5. Run bot agent locally
6. Access dashboard from anywhere
7. Approve & post from cloud!

---

**Your Instagram bot is now ready for the cloud!** 🚀
