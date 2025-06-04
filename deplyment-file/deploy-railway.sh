#!/bin/bash

# 🚄 RAILWAY DEPLOYMENT SCRIPT
# Complete deployment for Lagrange Interpolation Animator

echo "🚄 RAILWAY DEPLOYMENT - LAGRANGE INTERPOLATION ANIMATOR"
echo "======================================================="

# Check if Railway CLI is available
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found. Installing..."
    npm install -g @railway/cli
fi

echo "✅ Railway CLI ready"
echo ""

# Check login status
echo "🔐 Checking Railway login status..."
if railway whoami &> /dev/null; then
    echo "✅ Already logged in to Railway"
    railway whoami
else
    echo "🔐 Please log in to Railway..."
    railway login
fi

echo ""
echo "📁 Current project directory: $(pwd)"
echo "📊 Project files:"
ls -la | head -10

echo ""
echo "🔧 DEPLOYMENT OPTIONS:"
echo ""
echo "1. 🚀 Deploy with existing files (Recommended)"
echo "2. 🔄 Initialize new Railway project first"
echo "3. 📖 Show manual deployment instructions"
echo ""

read -p "Choose option (1/2/3): " choice

case $choice in
    1)
        echo ""
        echo "🚀 DEPLOYING TO RAILWAY..."
        echo ""
        
        # Try to deploy directly
        echo "📤 Attempting deployment..."
        railway up --detach
        
        if [ $? -eq 0 ]; then
            echo ""
            echo "✅ DEPLOYMENT SUCCESSFUL!"
            echo ""
            echo "🌐 Getting deployment URL..."
            railway domain
            echo ""
            echo "📊 Deployment status:"
            railway status
            echo ""
            echo "🎉 Your Lagrange Interpolation Animator is now live!"
            echo "📱 You can access it using the URL shown above."
        else
            echo ""
            echo "⚠️  Direct deployment failed. Trying to initialize project first..."
            railway new
            railway up --detach
        fi
        ;;
        
    2)
        echo ""
        echo "🔄 INITIALIZING NEW RAILWAY PROJECT..."
        echo ""
        
        # Initialize new project
        railway new
        
        if [ $? -eq 0 ]; then
            echo "✅ Project initialized successfully"
            echo ""
            echo "🚀 Now deploying..."
            railway up --detach
            
            echo ""
            echo "🌐 Setting up domain..."
            railway domain
            
            echo ""
            echo "✅ DEPLOYMENT COMPLETE!"
            railway status
        else
            echo "❌ Project initialization failed"
            echo "Please try manual deployment (option 3)"
        fi
        ;;
        
    3)
        echo ""
        echo "📖 MANUAL RAILWAY DEPLOYMENT INSTRUCTIONS"
        echo "======================================="
        echo ""
        echo "1. 🌐 Go to railway.app and create account"
        echo "2. 🆕 Click 'New Project' -> 'Deploy from GitHub repo'"
        echo "3. 🔗 Connect your GitHub account"
        echo "4. 📂 Select this repository"
        echo "5. ⚙️  Railway will auto-detect Django and deploy"
        echo ""
        echo "OR use CLI:"
        echo "1. railway new"
        echo "2. railway up"
        echo ""
        echo "🔧 Environment Variables to set in Railway dashboard:"
        echo "   DEBUG=False"
        echo "   SECRET_KEY=your-secret-key-here"
        echo "   ALLOWED_HOSTS=your-app.railway.app"
        echo "   CORS_ALLOWED_ORIGINS=https://your-app.railway.app"
        echo ""
        echo "📋 Railway will automatically:"
        echo "   ✅ Install requirements.txt"
        echo "   ✅ Run database migrations"
        echo "   ✅ Collect static files"
        echo "   ✅ Start with gunicorn"
        echo ""
        ;;
        
    *)
        echo "Invalid option. Please run the script again."
        ;;
esac

echo ""
echo "📋 NEXT STEPS AFTER DEPLOYMENT:"
echo "1. ✅ Test your app at the Railway URL"
echo "2. ⚙️  Configure environment variables in Railway dashboard"
echo "3. 🔗 Set up custom domain (optional)"
echo "4. 📊 Monitor logs: railway logs"
echo ""
echo "🚄 Railway provides excellent Django support with:"
echo "   • Automatic builds and deployments"
echo "   • Built-in PostgreSQL database option"
echo "   • SSL certificates"
echo "   • Easy scaling"
echo "   • WebSocket support"
echo ""
echo "🎉 Your Lagrange Interpolation Animator deployment is ready!"
