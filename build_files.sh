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

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Create staticfiles_build directory for Vercel
mkdir -p staticfiles_build
cp -r staticfiles/* staticfiles_build/ 2>/dev/null || echo "No static files to copy"

echo "Build completed!"
