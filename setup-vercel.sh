#!/bin/bash

echo "🚀 Starting Vercel deployment setup..."

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    echo "❌ Error: manage.py not found. Please run this script from the Django project root."
    exit 1
fi

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "❌ Error: Git repository not found. Please initialize git first."
    echo "Run: git init && git add . && git commit -m 'Initial commit'"
    exit 1
fi

# Install Vercel CLI if not already installed
if ! command -v vercel &> /dev/null; then
    echo "📦 Installing Vercel CLI..."
    npm install -g vercel
fi

# Check if we're logged into Vercel
echo "🔑 Please ensure you're logged into Vercel..."
vercel whoami || {
    echo "Please log in to Vercel:"
    vercel login
}

# Initialize Vercel project
echo "🔧 Setting up Vercel project..."
vercel --yes

# Get project details
echo "📋 Getting project information..."
echo "Your project details are now saved in .vercel/project.json"
echo "Please copy the orgId and projectId to your GitHub repository secrets."

# Show next steps
echo ""
echo "✅ Vercel setup complete!"
echo ""
echo "📝 Next steps:"
echo "1. Go to your GitHub repository → Settings → Secrets and variables → Actions"
echo "2. Add these secrets:"
echo "   - VERCEL_TOKEN: Get from https://vercel.com/account/tokens"
echo "   - VERCEL_ORG_ID: Found in .vercel/project.json"
echo "   - VERCEL_PROJECT_ID: Found in .vercel/project.json"
echo "3. Push your code to GitHub:"
echo "   git add ."
echo "   git commit -m 'Add Vercel deployment configuration'"
echo "   git push origin main"
echo "4. Your app will be automatically deployed!"
echo ""
echo "🌐 Once deployed, don't forget to:"
echo "- Update CORS_ALLOWED_ORIGINS in Vercel environment variables"
echo "- Set up proper SECRET_KEY in production"
echo "- Configure your custom domain if needed"
