#!/usr/bin/env python3
"""
Cloud Deployment Agent
Automated setup and deployment to free cloud hosting
"""
import os
import sys
import json
import subprocess
import webbrowser
from pathlib import Path

class CloudDeploymentAgent:
    """Manages deployment to free cloud platforms"""
    
    def __init__(self, project_path):
        self.project_path = project_path
        self.options = {
            "1": "Render.com (RECOMMENDED)",
            "2": "PythonAnywhere",
            "3": "Google Cloud Run",
            "4": "Replit"
        }
    
    def print_header(self):
        """Print welcome header"""
        print("\n" + "="*70)
        print("🚀 INSTAGRAM BOT - CLOUD DEPLOYMENT AGENT")
        print("="*70)
        print("\n📍 Current Project: " + self.project_path)
        print("\n")
    
    def show_options(self):
        """Show deployment options"""
        print("Choose your deployment platform:\n")
        for key, value in self.options.items():
            print(f"  {key}. {value}")
        print()
    
    def get_choice(self):
        """Get user choice"""
        while True:
            choice = input("Enter choice (1-4): ").strip()
            if choice in self.options:
                return choice
            print("❌ Invalid choice. Please try again.")
    
    def deploy_to_render(self):
        """Deploy to Render.com (EASIEST)"""
        print("\n" + "="*70)
        print("🎯 DEPLOYING TO RENDER.COM")
        print("="*70)
        
        instructions = """
STEP 1: Prepare Your Code
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Create a Git repository:
   $ cd instagram_agent
   $ git init
   $ git add .
   $ git commit -m "Initial commit"

2. Push to GitHub:
   a) Create new repository on GitHub (github.com)
   b) Name it: "instagram-bot-deploy"
   c) Copy the git URL
   d) Run in terminal:
      $ git remote add origin <your-github-url>
      $ git push -u origin main

STEP 2: Create Render Account
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Go to: https://render.com
2. Click "Sign Up"
3. Connect your GitHub account
4. Click "Authorize"

STEP 3: Create Web Service on Render
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. In Render dashboard, click "New +" → "Web Service"
2. Connect GitHub repository "instagram-bot-deploy"
3. Fill in settings:
   - Name: instagram-bot
   - Environment: Python 3
   - Build Command: pip install -r requirements_deploy.txt
   - Start Command: gunicorn wsgi:app
   - Plan: Free (sufficient for learning)
4. Click "Create Web Service"

STEP 4: Add Environment Variables
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

In Render dashboard:
1. Go to your service
2. Click "Environment" tab
3. Add these variables:
   INSTAGRAM_USERNAME = bengaluru_nagara
   INSTAGRAM_PASSWORD = Welcome1@!
   NEWSAPI_KEY = your_newsapi_key
   OPENWEATHER_API_KEY = your_weather_key
   FLASK_ENV = production

STEP 5: Wait for Deployment
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⏳ Render will automatically:
   - Clone your repository
   - Install dependencies
   - Create database
   - Deploy your app
   
📌 Look for: "Your service is live at: https://instagram-bot.onrender.com"

✅ YOUR APP IS NOW LIVE!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Access your dashboard at:
🌐 https://instagram-bot.onrender.com

IMPORTANT NOTES:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Free tier limitations:
   - Service spins down after 15 mins of inactivity
   - Database resets if using SQLite
   - For persistence, consider:
     a) Render PostgreSQL (free tier)
     b) MongoDB Atlas (free tier)

2. Run bot agent locally:
   $ python3 bot_agent_with_web.py
   (This creates posts in the cloud database)

3. Access web dashboard:
   Just visit: https://instagram-bot.onrender.com

4. Auto-updating:
   Any push to GitHub automatically redeploys!
   $ git push origin main  (auto-deploys)
        """
        
        print(instructions)
        
        # Open browser
        print("\n🌐 Opening Render.com in browser...")
        webbrowser.open("https://render.com")
    
    def deploy_to_pythonanywhere(self):
        """Deploy to PythonAnywhere"""
        print("\n" + "="*70)
        print("🎯 DEPLOYING TO PYTHONANYWHERE")
        print("="*70)
        
        instructions = """
STEP 1: Create Account
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Go to: https://www.pythonanywhere.com
2. Click "Pricing" → Choose "Free Account"
3. Sign up with email
4. Verify email

STEP 2: Upload Your Code
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. In PythonAnywhere dashboard:
   - Click "Files" tab
   - Upload instagram_agent folder
   - Or clone from GitHub via terminal

STEP 3: Create Web App
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Click "Web" tab
2. Click "Add a new web app"
3. Choose "Python 3.10"
4. Choose "Flask"
5. Configure WSGI file to point to wsgi.py

STEP 4: Set Environment Variables
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

In PythonAnywhere terminal:
$ python
>>> import os
>>> os.environ['INSTAGRAM_USERNAME'] = 'bengaluru_nagara'
>>> os.environ['INSTAGRAM_PASSWORD'] = '...'

STEP 5: Access Your App
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Your app will be at:
🌐 https://<yourusername>.pythonanywhere.com
        """
        
        print(instructions)
        print("\n🌐 Opening PythonAnywhere in browser...")
        webbrowser.open("https://www.pythonanywhere.com")
    
    def deploy_to_gcp(self):
        """Deploy to Google Cloud Run"""
        print("\n" + "="*70)
        print("🎯 DEPLOYING TO GOOGLE CLOUD RUN")
        print("="*70)
        
        print("""
Google Cloud Run is FREE for:
- 2 million requests per month
- 360,000 GB-seconds per month
- Perfect for your bot!

However, setup is more complex. Using Render instead.

Would you like to proceed with Render.com instead? (Y/n)
        """)
    
    def deploy_to_replit(self):
        """Deploy to Replit (EASIEST!)"""
        print("\n" + "="*70)
        print("🎯 DEPLOYING TO REPLIT (SIMPLEST!)")
        print("="*70)
        
        instructions = """
STEP 1: Create Account
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Go to: https://replit.com
2. Sign up with GitHub/Google
3. Verify email

STEP 2: Create New Replit
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Click "Create Repl"
2. Choose "Import from GitHub"
3. Paste your GitHub repo URL
4. Click "Import"

STEP 3: Install Dependencies
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

In Replit terminal:
$ pip install -r requirements_deploy.txt

STEP 4: Add .env File
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. In Replit file explorer, click "Add file"
2. Create ".env"
3. Paste your environment variables

STEP 5: Run
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

In terminal:
$ python3 web_app.py

Your app will be at:
🌐 https://<project-name>.replit.dev

✅ LIVE IMMEDIATELY!
        """
        
        print(instructions)
        print("\n🌐 Opening Replit in browser...")
        webbrowser.open("https://replit.com")
    
    def start(self):
        """Start deployment agent"""
        self.print_header()
        
        print("Free Cloud Hosting Options:\n")
        print("1. ✨ RENDER.COM - Best for Flask")
        print("   - Free tier: 750 hours/month")
        print("   - PostgreSQL support")
        print("   - Auto-deploy from GitHub\n")
        
        print("2. 🐍 PYTHONANYWHERE - Python focus")
        print("   - Free tier: Always available")
        print("   - Easy setup")
        print("   - Limited resources\n")
        
        print("3. ☁️  GOOGLE CLOUD RUN - Scalable")
        print("   - Free tier: 2M requests/month")
        print("   - Containerized (Docker required)")
        print("   - More complex\n")
        
        print("4. 🟪 REPLIT - Easiest!")
        print("   - Super simple")
        print("   - Works out of the box")
        print("   - Limited compute\n")
        
        choice = input("Choose platform (1-4) [recommend 1]: ").strip() or "1"
        
        if choice == "1":
            self.deploy_to_render()
        elif choice == "2":
            self.deploy_to_pythonanywhere()
        elif choice == "3":
            self.deploy_to_gcp()
        elif choice == "4":
            self.deploy_to_replit()
        else:
            print("Invalid choice")
            return
        
        print("\n" + "="*70)
        print("📚 NEXT STEPS")
        print("="*70)
        print("""
1. ✅ Set up your chosen platform (click link above)
2. 🔧 Add environment variables
3. 🚀 Deploy your app
4. 🤖 Run bot agent on your LOCAL machine
   $ python3 bot_agent_with_web.py
   (Creates posts → saves to CLOUD database)
5. 📱 Access web dashboard
   $ Open your deployed app URL
6. 👀 Review posts in cloud dashboard
7. ✅ Approve/post to Instagram

🎉 Your Instagram bot is now LIVE in the cloud!
        """)

if __name__ == "__main__":
    agent = CloudDeploymentAgent("/Users/yn00000/agent1/silver-agent/instagram_agent")
    agent.start()
