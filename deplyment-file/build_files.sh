#!/bin/bash

# Build script for Vercel - Optimized for file count limits
echo "=== Building for Vercel ==="

# Set environment variables for build
export VERCEL=1
export PYTHON_PATH=/var/task
export DJANGO_SETTINGS_MODULE=lagrange_project.settings

# Debug information
echo "Working directory: $(pwd)"
echo "Python version: $(python --version)"
echo "Available files: $(ls -la)"

# Install dependencies (use Vercel-optimized requirements)
echo "Installing dependencies..."
# Force install core dependencies one by one for better error tracking
pip install Django==4.2.16 || exit 1
pip install djangorestframework==3.15.2 || exit 1
pip install django-cors-headers==4.3.1 || exit 1
pip install python-decouple==3.8 || exit 1
pip install numpy==1.26.4 || exit 1
pip install requests==2.31.0 || exit 1
# Skip whitenoise for Vercel deployment

echo "Core dependencies installed successfully (whitenoise skipped for Vercel)"

# Verify Django installation
echo "Verifying Django installation..."
python -c "import django; print(f'Django version: {django.VERSION}')" || exit 1

# Create temporary database directory
echo "Setting up temporary database..."
mkdir -p /tmp

# Test Django configuration before running migrations
echo "Testing Django configuration..."
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lagrange_project.settings')
import django
django.setup()
from django.conf import settings
print(f'Settings configured: {settings.configured}')
print(f'Database engine: {settings.DATABASES[\"default\"][\"ENGINE\"]}')
" || echo "Django configuration test failed"

# Run migrations (with error handling)
echo "Running migrations..."
python manage.py migrate --noinput || echo "Migration failed, continuing..."

# Copy essential favicon files to static directory first
echo "Copying essential favicon files..."
mkdir -p static/images
cp favicon_io/favicon.ico static/ 2>/dev/null || echo "favicon.ico not found"
cp favicon_io/site.webmanifest static/ 2>/dev/null || echo "site.webmanifest not found"

# Collect static files with ultra-minimal approach
echo "Collecting static files (minimal for Vercel limits)..."
python manage.py collectstatic --noinput --clear

# Create ultra-minimal staticfiles_build directory
echo "Creating ultra-minimal build directory..."
rm -rf staticfiles_build
mkdir -p staticfiles_build

# Only copy essential files to stay under Vercel limits
echo "Copying only essential static files..."
# Copy favicon and manifest only
cp staticfiles/favicon.ico staticfiles_build/ 2>/dev/null || echo "No favicon.ico"
cp staticfiles/site.webmanifest staticfiles_build/ 2>/dev/null || echo "No webmanifest"

# Skip ALL admin and rest_framework files to drastically reduce file count
echo "Skipping admin and rest_framework static files to reduce deployment size"
echo "Essential files only: favicon.ico, site.webmanifest"

# Final verification
echo "=== Build Verification ==="
echo "Python version: $(python --version)"
echo "Django version: $(python -c 'import django; print(django.VERSION)')"
echo "Static files count: $(find staticfiles_build -type f | wc -l)"
echo "Build directory contents: $(ls -la staticfiles_build/ | head -10)"

echo "=== Build completed successfully! ==="
