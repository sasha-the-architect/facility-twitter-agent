#!/bin/bash
# Facility Twitter Agent - Railway Deployment Script
# Run this from the facility project directory

set -e

echo "🏛️ Deploying Facility Twitter Agent to Railway..."
echo ""

# Check if linked
if ! railway status &>/dev/null; then
    echo "📦 Linking to Railway project..."
    railway link --project 3e2d8145-0dbb-468f-b407-c29860340a1d
fi

# Get service
echo ""
echo "📋 Available services:"
railway service status 2>/dev/null || railway status

# Prompt for Twitter cookies
echo ""
echo "🔐 Twitter Authentication Required:"
echo "1. Open x.com in browser (Chrome/Arc)"
echo "2. Open DevTools (Cmd+Option+I)"
echo "3. Go to Application → Cookies → https://x.com"
echo "4. Copy 'auth_token' and 'ct0' values"
echo ""

read -p "Enter Twitter auth_token: " AUTH_TOKEN
read -p "Enter Twitter ct0: " CT0

# Set environment variables
echo ""
echo "🔧 Setting environment variables..."
railway vars set TWITTER_AUTH_TOKEN="$AUTH_TOKEN"
railway vars set TWITTER_CT0="$CT0"

# Deploy
echo ""
echo "🚀 Deploying to Railway..."
railway up -d

echo ""
echo "✅ Deployment started!"
echo "📊 Monitor at: https://railway.com/project/3e2d8145-0dbb-468f-b407-c29860340a1d"
echo ""
echo "📝 Next steps:"
echo "1. Wait for deployment to complete"
echo "2. Check logs: railway logs"
echo "3. The agent will start running in daemon mode"
