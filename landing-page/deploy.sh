#!/bin/bash

# The Facility - Landing Page Deploy Script
# Usage: ./deploy.sh [vercel|netlify|cloudflare|github]

cd "$(dirname "$0")"

echo "🚀 The Facility Landing Page Deploy"
echo "===================================="

case "${1:-vercel}" in
    vercel)
        echo "📦 Deploying to Vercel..."
        npx vercel --prod
        ;;
    netlify)
        echo "📦 Deploying to Netlify..."
        npx netlify deploy --prod --dir=.
        ;;
    cloudflare)
        echo "📦 Deploying to Cloudflare Pages..."
        npx wrangler pages deploy .
        ;;
    github)
        echo "📦 GitHub Pages instructions:"
        echo "1. Create a new GitHub repository"
        echo "2. Push this folder to main branch"
        echo "3. Go to Settings > Pages > Enable from main"
        echo "4. Add custom domain in Settings > Pages"
        ;;
    *)
        echo "Usage: ./deploy.sh [vercel|netlify|cloudflare|github]"
        exit 1
        ;;
esac

echo ""
echo "✅ Deployment complete!"
echo "🌐 Don't forget to update DNS for thefacility.xyz"
