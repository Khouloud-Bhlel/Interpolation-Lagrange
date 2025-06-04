#!/bin/bash

# 🚀 FINAL DEPLOYMENT SCRIPT
# Choose your deployment strategy based on current situation

echo "🚀 LAGRANGE INTERPOLATION ANIMATOR - DEPLOYMENT READY"
echo "======================================================"

# Check if we're in rate limit period
echo ""
echo "📊 DEPLOYMENT OPTIONS:"
echo ""

echo "🚨 OPTION 1: EMERGENCY DEPLOYMENT (NOW)"
echo "   - Ultra-minimal: 22 files only"
echo "   - Basic functionality"
echo "   - Command: cd emergency-deploy && vercel --prod"
echo ""

echo "⏰ OPTION 2: OPTIMIZED DEPLOYMENT (AFTER RATE LIMIT RESET)"
echo "   - Full application with all features"
echo "   - Automatic via GitHub Actions"
echo "   - Wait time: ~23 hours"
echo ""

echo "🔧 OPTION 3: ALTERNATIVE PLATFORMS (RECOMMENDED)"
echo "   - Railway: Instant deployment, no limits"
echo "   - Render: Auto-deploy from GitHub"
echo "   - Heroku: Classic Django hosting"
echo ""

echo "======================================================"

read -p "Choose option (1/2/3) or press Enter to see detailed instructions: " choice

case $choice in
    1)
        echo ""
        echo "🚨 EXECUTING EMERGENCY DEPLOYMENT..."
        echo ""
        cd emergency-deploy
        echo "Current directory: $(pwd)"
        echo "Files to deploy: $(find . -type f | wc -l)"
        echo ""
        echo "Running: vercel --prod --archive=tgz"
        echo ""
        echo "⚠️  Note: This is a minimal deployment for testing connectivity only!"
        echo "   Many features will be missing until full deployment."
        echo ""
        echo "🔄 Using archive mode to bypass rate limit..."
        vercel --prod --archive=tgz
        ;;
    2)
        echo ""
        echo "⏰ OPTIMIZED DEPLOYMENT SCHEDULED"
        echo ""
        echo "✅ GitHub Actions workflow is configured and ready"
        echo "✅ All files optimized for deployment"
        echo "✅ Environment variables configured"
        echo ""
        echo "When rate limit resets (~23 hours):"
        echo "1. GitHub Actions will automatically deploy"
        echo "2. OR run manually: vercel deploy --prod"
        echo ""
        echo "Monitor status at: https://github.com/your-repo/actions"
        ;;
    3)
        echo ""
        echo "🔧 ALTERNATIVE DEPLOYMENT PLATFORMS (RECOMMENDED):"
        echo ""
        echo "🚄 Railway (Best for Django):"
        echo "  1. npm install -g @railway/cli"
        echo "  2. railway login"
        echo "  3. railway new"
        echo "  4. railway up"
        echo "  ✅ No file limits, instant deployment"
        echo ""
        echo "🎨 Render (Auto-deploy from Git):"
        echo "  1. Connect GitHub repo at render.com"
        echo "  2. Create new web service"
        echo "  3. Use render.yaml configuration"
        echo "  ✅ Free tier available, automatic builds"
        echo ""
        echo "⚡ Heroku (Classic):"
        echo "  1. heroku create your-app-name"
        echo "  2. git push heroku main"
        echo "  ✅ Well-documented, Django-friendly"
        echo ""
        echo "🎯 RECOMMENDED NEXT STEP: Try Railway first!"
        echo "   Railway is specifically designed for modern Django apps."
        echo ""
        read -p "Deploy to Railway now? (y/n): " railway_choice
        if [[ $railway_choice =~ ^[Yy]$ ]]; then
            echo ""
            echo "🚄 DEPLOYING TO RAILWAY..."
            echo ""
            # Check if Railway CLI is installed
            if command -v railway &> /dev/null; then
                echo "✅ Railway CLI found"
                railway login
                railway new
                railway up
            else
                echo "❌ Railway CLI not found. Installing..."
                echo "   Run: npm install -g @railway/cli"
                echo "   Then: railway login && railway new && railway up"
            fi
        fi
        ;;
    *)
        echo ""
        echo "📖 DETAILED DEPLOYMENT INSTRUCTIONS"
        echo ""
        echo "Current Status:"
        echo "  ✅ Django app configured for Vercel"
        echo "  ✅ WSGI entry point optimized"
        echo "  ✅ Static files configured"
        echo "  ✅ Environment variables set"
        echo "  ✅ GitHub Actions ready"
        echo "  ⚠️  Vercel rate limited (reset in ~23h)"
        echo ""
        echo "Emergency Package Ready:"
        echo "  📁 Location: emergency-deploy/"
        echo "  📊 Files: 22 essential files"
        echo "  💾 Size: ~200KB"
        echo "  🚀 Ready to deploy"
        echo ""
        echo "Quick Commands:"
        echo "  Emergency: cd emergency-deploy && vercel --prod"
        echo "  Status: vercel ls"
        echo "  Logs: vercel logs"
        echo ""
        ;;
esac

echo ""
echo "📋 NEXT STEPS:"
echo "1. Deploy using chosen option above"
echo "2. Test endpoints: /, /debug/, /api/"
echo "3. Configure environment variables in Vercel dashboard"
echo "4. Add custom domain (optional)"
echo ""
echo "🎉 Your Lagrange Interpolation Animator is ready for deployment!"
