"""
Vercel WSGI entry point for Django application
"""
import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Set environment variables before importing Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lagrange_project.settings')
os.environ.setdefault('VERCEL', '1')
os.environ.setdefault('SECRET_KEY', 'vercel-default-secret-key-not-for-production-use-only-12345678901234567890')
os.environ.setdefault('DEBUG', 'False')
os.environ.setdefault('ALLOWED_HOSTS', '.vercel.app,.now.sh')

def create_error_response(error_message):
    """Create a simple WSGI error response"""
    def application(environ, start_response):
        status = '500 Internal Server Error'
        headers = [
            ('Content-type', 'text/html; charset=utf-8'),
            ('Access-Control-Allow-Origin', '*'),
        ]
        start_response(status, headers)
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Django Error - Lagrange Animator</title>
            <link rel="icon" type="image/x-icon" href="/static/favicon.ico">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
                .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                .error {{ color: #d32f2f; background: #ffebee; padding: 20px; border-radius: 4px; border-left: 4px solid #d32f2f; }}
                .info {{ color: #1976d2; margin-top: 20px; background: #e3f2fd; padding: 15px; border-radius: 4px; }}
                pre {{ background: #f5f5f5; padding: 15px; overflow: auto; border-radius: 4px; font-size: 12px; }}
                h1 {{ color: #1976d2; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🚀 Lagrange Interpolation Animator</h1>
                <div class="error">
                    <h3>Application Error:</h3>
                    <pre>{error_message}</pre>
                </div>
                <div class="info">
                    <h3>Debug Information:</h3>
                    <pre>
Python Version: {sys.version}
Python Path: {sys.path[:3]}
Project Root: {project_root}
Django Settings: {os.environ.get('DJANGO_SETTINGS_MODULE')}
Vercel Environment: {os.environ.get('VERCEL')}
Debug Mode: {os.environ.get('DEBUG')}
Working Directory: {os.getcwd()}
                    </pre>
                </div>
                <div class="info">
                    <p><strong>Note:</strong> This is a development error page. In production, detailed error information would be logged securely.</p>
                </div>
            </div>
        </body>
        </html>
        """
        return [html_content.encode('utf-8')]
    return application

try:
    # Configure Django
    import django
    from django.conf import settings
    
    # Setup Django if not configured
    if not settings.configured:
        django.setup()
    
    # Import the WSGI application
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    
except ImportError as e:
    application = create_error_response(f"Import Error: {str(e)}\n\nThis usually means a required package is missing.")
except Exception as e:
    import traceback
    application = create_error_response(f"Django Configuration Error: {str(e)}\n\nFull traceback:\n{traceback.format_exc()}")

# Vercel expects the app at module level
app = application
