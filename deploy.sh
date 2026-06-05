#!/bin/bash
# Deployment Quick Start Script

cd "$(dirname "$0")"

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║     🚀 INSTAGRAM BOT - CLOUD DEPLOYMENT WIZARD               ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git not found. Please install git first:"
    echo "   https://git-scm.com/download"
    exit 1
fi

echo "📋 STEP 1: Check Prerequisites"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ -f .gitignore ]; then
    echo "✅ .gitignore exists"
else
    echo "⚠️  .gitignore missing"
fi

if [ -f wsgi.py ]; then
    echo "✅ wsgi.py exists"
else
    echo "⚠️  wsgi.py missing"
fi

if [ -f Procfile ]; then
    echo "✅ Procfile exists"
else
    echo "⚠️  Procfile missing"
fi

if [ -f requirements_deploy.txt ]; then
    echo "✅ requirements_deploy.txt exists"
else
    echo "⚠️  requirements_deploy.txt missing"
fi

echo ""
echo "📋 STEP 2: Initialize Git Repository"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ -d .git ]; then
    echo "✅ Git repository already exists"
    git status
else
    echo "🔄 Initializing git repository..."
    git init
    git config user.email "you@example.com"
    git config user.name "Instagram Bot"
    echo "✅ Git initialized"
fi

echo ""
echo "📋 STEP 3: Show What Will Be Committed"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo ""
echo "Files to be committed:"
git add --dry-run . | head -20

echo ""
echo "📋 STEP 4: Ready to Deploy?"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Next steps:"
echo ""
echo "1️⃣  Create GitHub repository:"
echo "    $ Go to https://github.com/new"
echo "    $ Name it: instagram-bot-deploy"
echo "    $ DO NOT initialize with README"
echo "    $ Click 'Create repository'"
echo ""
echo "2️⃣  Add remote and push:"
echo "    $ git remote add origin https://github.com/YOUR-USERNAME/instagram-bot-deploy.git"
echo "    $ git add ."
echo "    $ git commit -m 'Initial Instagram bot deployment'"
echo "    $ git branch -M main"
echo "    $ git push -u origin main"
echo ""
echo "3️⃣  Go to Render.com:"
echo "    $ https://render.com"
echo "    $ Sign up with GitHub"
echo "    $ Click 'New +' → 'Web Service'"
echo "    $ Connect instagram-bot-deploy repo"
echo ""
echo "4️⃣  Configure on Render:"
echo "    $ Name: instagram-bot"
echo "    $ Runtime: Python 3"
echo "    $ Build: pip install -r requirements_deploy.txt"
echo "    $ Start: gunicorn wsgi:app"
echo "    $ Plan: Free"
echo ""
echo "5️⃣  Add Environment Variables:"
echo "    $ INSTAGRAM_USERNAME=bengaluru_nagara"
echo "    $ INSTAGRAM_PASSWORD=Welcome1@!"
echo "    $ NEWSAPI_KEY=your_key"
echo "    $ OPENWEATHER_API_KEY=your_key"
echo ""
echo "6️⃣  Deploy!"
echo "    $ Click 'Create Web Service'"
echo "    $ Wait 5-10 minutes"
echo "    $ Your app is LIVE! 🎉"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Open deployment agent
echo "Opening Deployment Agent..."
echo ""

python3 deployment_agent.py
