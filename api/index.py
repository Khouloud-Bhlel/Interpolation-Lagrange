"""
Vercel WSGI entry point for Django application
"""
import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lagrange_project.settings')

# Ensure VERCEL environment is set
os.environ.setdefault('VERCEL', '1')

try:
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
except Exception as e:
    # If there's an error, create a simple WSGI app that returns the error
    def application(environ, start_response):
        status = '500 Internal Server Error'
        headers = [('Content-type', 'text/plain')]
        start_response(status, headers)
        return [f'Django Error: {str(e)}'.encode('utf-8')]

# Vercel needs the app to be available at module level
app = application
