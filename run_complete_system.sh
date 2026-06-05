#!/bin/bash
# Run both Bot Agent + Web Dashboard together

cd "$(dirname "$0")"

echo "🚀 LAUNCHING INSTAGRAM BOT + WEB DASHBOARD"
echo "=========================================="
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    echo "Please configure .env first"
    exit 1
fi

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
pip install -q -r web_requirements.txt 2>/dev/null || pip install -r web_requirements.txt

# Create posts directory
mkdir -p posts

echo ""
echo "✨ Starting services..."
echo ""

# Start web app in background
echo "Starting Web Dashboard on http://localhost:5000..."
python3 web_app.py &
WEB_PID=$!

sleep 2

# Start bot agent
echo "Starting Bot Agent..."
python3 bot_agent_with_web.py &
BOT_PID=$!

# Wait for both processes
wait $WEB_PID $BOT_PID

echo ""
echo "✅ Services stopped"
