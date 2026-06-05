#!/bin/bash
# Instagram News Agent Startup Script

cd "$(dirname "$0")"

echo "🚀 Instagram News Agent Launcher"
echo "================================="
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    echo "📝 Creating .env from template..."
    cp .env.example .env
    echo "✅ .env created. Please edit it with your credentials."
    echo ""
    echo "Get your API keys:"
    echo "  - NewsAPI: https://newsapi.org/"
    echo "  - Anthropic: https://console.anthropic.com/"
    echo "  - Instagram: Meta Developers or your credentials"
    echo ""
    echo "Then run this script again."
    exit 1
fi

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Python $python_version"

# Check if venv exists, if not create it
if [ ! -d venv ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt -q

# Run agent
echo ""
echo "✨ Starting Instagram News Agent..."
echo ""
python3 main_agent.py
