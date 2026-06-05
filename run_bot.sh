#!/bin/bash
# Enhanced Bangalore Instagram Bot Agent Launcher

cd "$(dirname "$0")"

echo "🚀 BANGALORE INSTAGRAM BOT AGENT"
echo "================================="
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    echo "📝 Setting up .env..."
    
    read -p "Enter your Instagram username: " INSTA_USER
    read -sp "Enter your Instagram password (hidden): " INSTA_PASS
    echo ""
    read -p "Enter your NewsAPI key (from https://newsapi.org/): " NEWSAPI_KEY
    read -p "Enter your OpenWeather API key (from https://openweathermap.org/api): " WEATHER_KEY
    
    cat > .env << EOF
INSTAGRAM_USERNAME=$INSTA_USER
INSTAGRAM_PASSWORD=$INSTA_PASS

NEWSAPI_KEY=$NEWSAPI_KEY
OPENWEATHER_API_KEY=$WEATHER_KEY

BANGALORE_LAT=12.9716
BANGALORE_LNG=77.5946
BANGALORE_CITY=Bangalore

POST_INTERVAL_MINUTES=30
IMAGE_WIDTH=1080
IMAGE_HEIGHT=1350
REPLY_TO_COMMENTS=true
MAX_REPLIES_PER_POST=5
EOF
    
    echo "✅ .env configured!"
fi

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Python $python_version"

# Create virtual environment if needed
if [ ! -d venv ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt 2>/dev/null || pip install -r requirements.txt

# Create posts directory
mkdir -p posts

# Run the bot
echo ""
echo "✨ Starting Bangalore Instagram Bot Agent..."
echo ""
python3 bot_agent.py
