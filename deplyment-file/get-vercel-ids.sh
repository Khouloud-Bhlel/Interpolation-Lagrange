#!/bin/bash

echo "🔧 Vercel Project Setup Helper"
echo "================================"

# Check if vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI not found. Installing..."
    npm install -g vercel
fi

# Check if logged in
echo "🔑 Checking Vercel authentication..."
if ! vercel whoami &> /dev/null; then
    echo "Please log in to Vercel:"
    vercel login
fi

# Link project (this will create .vercel/project.json)
echo "🔗 Linking Vercel project..."
vercel link

# Show project details
if [ -f ".vercel/project.json" ]; then
    echo ""
    echo "✅ Project linked successfully!"
    echo ""
    echo "📋 Copy these values to your GitHub Secrets:"
    echo "============================================="
    echo "VERCEL_ORG_ID: $(cat .vercel/project.json | jq -r '.orgId')"
    echo "VERCEL_PROJECT_ID: $(cat .vercel/project.json | jq -r '.projectId')"
    echo ""
    echo "🔗 GitHub Secrets URL:"
    echo "https://github.com/yourusername/yourrepo/settings/secrets/actions"
    echo ""
    echo "🌐 Vercel Dashboard:"
    echo "https://vercel.com/dashboard"
else
    echo "❌ Failed to link project. Please run 'vercel link' manually."
fi

echo ""
echo "🚀 Next steps:"
echo "1. Copy the ORG_ID and PROJECT_ID to GitHub Secrets"
echo "2. Set environment variables in Vercel dashboard"
echo "3. Push your code to trigger deployment"
echo "4. Check deployment status in GitHub Actions"
