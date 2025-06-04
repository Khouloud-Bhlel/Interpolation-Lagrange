#!/bin/bash

# Build script for Vercel
echo "Building for Vercel..."

# Set environment variables for build
export VERCEL=1
export PYTHON_PATH=/var/task

# Install dependencies (use minimal requirements for Vercel)
echo "Installing dependencies..."
pip install -r requirements-minimal.txt

# Set Django settings module
export DJANGO_SETTINGS_MODULE=lagrange_project.settings

# Create temporary database directory
mkdir -p /tmp

# Run migrations (with error handling)
echo "Running migrations..."
python manage.py migrate --noinput || echo "Migration failed, continuing..."

# Copy favicon files to static directory
echo "Copying favicon files..."
mkdir -p static/images
cp favicon_io/favicon.ico static/ 2>/dev/null || echo "favicon.ico not found"
cp favicon_io/*.png static/images/ 2>/dev/null || echo "PNG favicons not found"
cp favicon_io/site.webmanifest static/ 2>/dev/null || echo "site.webmanifest not found"

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Copy favicon files to staticfiles directory (backup)
echo "Copying favicon files to staticfiles..."
mkdir -p staticfiles/images
cp favicon_io/favicon.ico staticfiles/ 2>/dev/null || echo "favicon.ico not found"
cp favicon_io/*.png staticfiles/images/ 2>/dev/null || echo "PNG favicons not found"
cp favicon_io/site.webmanifest staticfiles/ 2>/dev/null || echo "site.webmanifest not found"

# Create staticfiles_build directory for Vercel
mkdir -p staticfiles_build
cp -r staticfiles/* staticfiles_build/ 2>/dev/null || echo "No static files to copy"

echo "Build completed!"
