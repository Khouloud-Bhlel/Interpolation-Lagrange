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
pip install whitenoise==6.6.0 || exit 1

echo "Core dependencies installed successfully"

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

# Final verification
echo "=== Build Verification ==="
echo "Python version: $(python --version)"
echo "Django version: $(python -c 'import django; print(django.VERSION)')"
echo "Static files count: $(find staticfiles_build -type f | wc -l)"
echo "Build directory contents: $(ls -la staticfiles_build/ | head -10)"

echo "=== Build completed successfully! ==="
