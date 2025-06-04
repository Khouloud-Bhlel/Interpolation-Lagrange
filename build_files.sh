#!/bin/bash

# Build script for Vercel - Optimized for file count limits
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

# Copy essential favicon files to static directory first
echo "Copying essential favicon files..."
mkdir -p static/images
cp favicon_io/favicon.ico static/ 2>/dev/null || echo "favicon.ico not found"
cp favicon_io/favicon-32x32.png static/images/ 2>/dev/null || echo "favicon-32x32.png not found"
cp favicon_io/apple-touch-icon.png static/images/ 2>/dev/null || echo "apple-touch-icon.png not found"

# Collect static files with optimization
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Remove unnecessary static files to reduce file count
echo "Optimizing static files..."
# Remove admin static files for production (save space)
rm -rf staticfiles/admin/css/vendor/ 2>/dev/null || true
rm -rf staticfiles/admin/js/vendor/jquery/ 2>/dev/null || true
# Keep only essential favicon files
find staticfiles/images/ -name "*.png" -not -name "favicon-32x32.png" -not -name "apple-touch-icon.png" -delete 2>/dev/null || true

# Create optimized staticfiles_build directory for Vercel
echo "Creating optimized build directory..."
mkdir -p staticfiles_build
cp -r staticfiles/* staticfiles_build/ 2>/dev/null || echo "No static files to copy"

echo "Build completed successfully!"

echo "Build completed!"
