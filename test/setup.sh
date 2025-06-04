#!/bin/bash

# Lagrange Interpolation Animator Setup Script
echo "Setting up Lagrange Interpolation Animator..."

# Check if virtual environment exists
if [ ! -d "lagrange_env" ]; then
    echo "Creating virtual environment..."
    python3 -m venv lagrange_env
fi

# Activate virtual environment
source lagrange_env/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Set up environment variables
if [ ! -f ".env" ]; then
    echo "Environment file already exists, skipping creation..."
else
    echo "Environment file found."
fi

# Create database (PostgreSQL)
echo "Setting up database..."
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
echo "Do you want to create a Django superuser? (y/n)"
read -r response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    python manage.py createsuperuser
fi

# Collect static files
python manage.py collectstatic --noinput

echo "Setup complete!"
echo ""
echo "To start the Django development server:"
echo "  source lagrange_env/bin/activate"
echo "  python manage.py runserver"
echo ""
echo "To start Odoo with Docker:"
echo "  docker-compose up -d"
echo ""
echo "Access points:"
echo "  Django App: http://localhost:8000"
echo "  Odoo: http://localhost:8069"