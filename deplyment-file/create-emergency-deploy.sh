#!/bin/bash

echo "🚨 EMERGENCY VERCEL DEPLOYMENT 🚨"
echo "This creates a minimal deployment package to bypass file limits"

# Create emergency deployment directory
rm -rf emergency-deploy
mkdir emergency-deploy

# Copy only essential files
echo "Copying essential files..."

# Core Python files
cp -r lagrange_project emergency-deploy/
cp -r interpolation_app emergency-deploy/
cp manage.py emergency-deploy/

# Remove unnecessary files from interpolation_app
rm -rf emergency-deploy/interpolation_app/templates
rm -rf emergency-deploy/interpolation_app/migrations
rm -rf emergency-deploy/interpolation_app/management
touch emergency-deploy/interpolation_app/migrations/__init__.py

# API directory
mkdir emergency-deploy/api
cp api/emergency.py emergency-deploy/api/index.py

# Minimal requirements
cp requirements-emergency.txt emergency-deploy/requirements.txt

# Settings
cp emergency_settings.py emergency-deploy/settings.py

# Vercel config
cat > emergency-deploy/vercel.json << 'EOF'
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python",
      "config": { 
        "maxLambdaSize": "15mb", 
        "runtime": "python3.9"
      }
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/api/index.py"
    }
  ]
}
EOF

# Build script
cat > emergency-deploy/build_files.sh << 'EOF'
#!/bin/bash
pip install Django==4.2.16
pip install djangorestframework==3.15.2
pip install django-cors-headers==4.3.1
pip install whitenoise==6.6.0
echo "Emergency build complete"
EOF

chmod +x emergency-deploy/build_files.sh

echo "📊 File count: $(find emergency-deploy -type f | wc -l)"
echo "📦 Directory size: $(du -sh emergency-deploy)"

echo ""
echo "🚀 To deploy this emergency package:"
echo "1. cd emergency-deploy"
echo "2. vercel --prod"
echo ""
echo "⚠️  This is a minimal deployment for testing connectivity only!"
echo "   Many features will be missing until full deployment."
