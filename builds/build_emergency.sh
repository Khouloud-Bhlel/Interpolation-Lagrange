#!/bin/bash

# Ultra-minimal build script for Vercel emergency deployment
echo "=== EMERGENCY BUILD FOR VERCEL ==="

# Set minimal environment
export VERCEL=1
export DJANGO_SETTINGS_MODULE=lagrange_project.settings

# Install only core dependencies
echo "Installing minimal dependencies..."
pip install Django==4.2.16
pip install djangorestframework==3.15.2
pip install django-cors-headers==4.3.1
pip install whitenoise==6.6.0

# Skip migrations and static files for now
echo "Skipping migrations and static files for emergency deployment"

# Create minimal static directory
mkdir -p staticfiles_build
echo "/* Emergency deployment - static files skipped */" > staticfiles_build/emergency.css

echo "=== EMERGENCY BUILD COMPLETE ==="
