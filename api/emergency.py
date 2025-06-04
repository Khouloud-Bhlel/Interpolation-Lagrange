"""
Emergency Vercel WSGI entry point - Ultra minimal
"""
import os
import sys
from pathlib import Path

# Simple Python path setup
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Minimal environment setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'emergency_settings')
os.environ.setdefault('VERCEL', '1')

def create_error_response(error_msg):
    """Create simple error response"""
    def app(environ, start_response):
        start_response('500 Internal Server Error', [('Content-Type', 'text/html')])
        return [f"""
        <html><body>
        <h1>Emergency Deployment</h1>
        <p>Error: {error_msg}</p>
        <p>This is a minimal deployment to test Vercel connectivity.</p>
        </body></html>
        """.encode()]
    return app

try:
    import django
    django.setup()
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
except Exception as e:
    application = create_error_response(str(e))

# Vercel expects 'app'
app = application
