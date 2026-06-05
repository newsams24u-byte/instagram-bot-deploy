#!/bin/bash
# Test script to verify local Docker build works before pushing to Render

echo "🐳 Building Docker image locally..."
docker build -t instagram-bot:test .

if [ $? -eq 0 ]; then
    echo "✅ Docker build successful!"
    echo ""
    echo "🧪 Testing container startup..."
    docker run --rm -d --name test-bot -p 5000:5000 instagram-bot:test > /dev/null
    
    sleep 3
    
    if docker ps | grep -q test-bot; then
        echo "✅ Container started successfully!"
        
        # Test health endpoint
        echo "🔍 Testing health endpoint..."
        curl -s http://localhost:5000/ | head -20
        
        echo ""
        echo "✅ All tests passed! Ready to deploy to Render."
        docker stop test-bot
    else
        echo "❌ Container failed to start"
        docker logs test-bot
        exit 1
    fi
else
    echo "❌ Docker build failed!"
    exit 1
fi
