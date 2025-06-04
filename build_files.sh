#!/bin/bash

# Build script for Vercel
echo "Building for Vercel..."

# Install dependencies (use optimized requirements for Vercel)
pip install -r requirements.txt

# Run migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput --clear

# Create staticfiles_build directory for Vercel
mkdir -p staticfiles_build
cp -r staticfiles/* staticfiles_build/ 2>/dev/null || echo "No static files to copy"

echo "Build completed!"
