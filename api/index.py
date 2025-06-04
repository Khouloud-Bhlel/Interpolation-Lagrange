"""
Vercel WSGI entry point for Django application - Simplified for debugging
"""
import os
import sys
from pathlib import Path

def debug_print(message):
    """Print debug message with timestamp"""
    import datetime
    timestamp = datetime.datetime.now().isoformat()
    print(f"[{timestamp}] {message}")

# Debug: Print initial environment
debug_print("=== VERCEL WSGI STARTUP ===")
debug_print(f"Working directory: {os.getcwd()}")
debug_print(f"Python version: {sys.version}")
debug_print(f"Python executable: {sys.executable}")
debug_print(f"Python path initial: {sys.path[:3]}")

# Set up Python path more aggressively
current_file = Path(__file__).resolve()
current_dir = current_file.parent
project_root = current_dir.parent

# Multiple strategies to ensure project is in path
paths_to_add = [
    str(project_root),          # Main project directory
    str(current_dir),           # API directory
    str(Path.cwd()),            # Current working directory
    '/var/task',                # Vercel's default task directory
]

for path in paths_to_add:
    if path not in sys.path:
        sys.path.insert(0, path)
        debug_print(f"Added to Python path: {path}")

debug_print(f"Final Python path: {sys.path[:6]}")

# Set environment variables before importing Django
env_vars = {
    'DJANGO_SETTINGS_MODULE': 'lagrange_project.settings',
    'VERCEL': '1',
    'SECRET_KEY': 'vercel-default-secret-key-not-for-production-use-only-12345678901234567890',
    'DEBUG': 'False',
    'ALLOWED_HOSTS': '.vercel.app,.now.sh'
}

for key, value in env_vars.items():
    os.environ.setdefault(key, value)
    debug_print(f"Environment variable {key}: {os.environ.get(key)}")

debug_print("Environment setup complete")

def create_error_response(error_message, details=None):
    """Create a comprehensive WSGI error response"""
    def application(environ, start_response):
        status = '500 Internal Server Error'
        headers = [
            ('Content-type', 'text/html; charset=utf-8'),
            ('Access-Control-Allow-Origin', '*'),
        ]
        start_response(status, headers)
        
        # Get request info for debugging
        request_info = {
            'method': environ.get('REQUEST_METHOD', 'Unknown'),
            'path': environ.get('PATH_INFO', 'Unknown'),
            'query': environ.get('QUERY_STRING', ''),
            'user_agent': environ.get('HTTP_USER_AGENT', 'Unknown'),
        }
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Django Error - Lagrange Animator</title>
            <link rel="icon" type="image/x-icon" href="/static/favicon.ico">
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }}
                .container {{ max-width: 900px; margin: 0 auto; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 8px 32px rgba(0,0,0,0.1); }}
                .error {{ color: #d32f2f; background: #ffebee; padding: 20px; border-radius: 8px; border-left: 4px solid #d32f2f; margin: 20px 0; }}
                .info {{ color: #1976d2; margin-top: 20px; background: #e3f2fd; padding: 15px; border-radius: 8px; }}
                .success {{ color: #388e3c; background: #e8f5e8; padding: 15px; border-radius: 8px; margin: 20px 0; }}
                pre {{ background: #f5f5f5; padding: 15px; overflow: auto; border-radius: 8px; font-size: 12px; border: 1px solid #ddd; }}
                h1 {{ color: #1976d2; margin-bottom: 10px; }}
                h3 {{ color: #333; margin-top: 25px; }}
                .request-info {{ background: #fff3e0; padding: 15px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #ff9800; }}
                .badge {{ display: inline-block; background: #1976d2; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px; margin: 2px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🚀 Lagrange Interpolation Animator</h1>
                <div class="success">
                    <strong>✅ Vercel Function Active:</strong> This error page confirms the Python function is running correctly.
                </div>
                
                <div class="request-info">
                    <h3>📝 Request Information:</h3>
                    <span class="badge">{request_info['method']}</span>
                    <span class="badge">{request_info['path']}</span>
                    {f'<span class="badge">?{request_info["query"]}</span>' if request_info['query'] else ''}
                </div>
                
                <div class="error">
                    <h3>⚠️ Application Error:</h3>
                    <pre>{error_message}</pre>
                </div>
                
                {f'<div class="info"><h3>🔍 Additional Details:</h3><pre>{details}</pre></div>' if details else ''}
                
                <div class="info">
                    <h3>🛠️ Environment Debug Information:</h3>
                    <pre>
Python Version: {sys.version}
Working Directory: {os.getcwd()}
Python Path (first 5): {sys.path[:5]}
Environment Variables:
  - DJANGO_SETTINGS_MODULE: {os.environ.get('DJANGO_SETTINGS_MODULE')}
  - VERCEL: {os.environ.get('VERCEL')}
  - DEBUG: {os.environ.get('DEBUG')}
  - ALLOWED_HOSTS: {os.environ.get('ALLOWED_HOSTS')}
                    </pre>
                </div>
                
                <div class="info">
                    <h3>🎯 Debugging Steps:</h3>
                    <ol>
                        <li>Try accessing <strong>/debug/</strong> endpoint for detailed Django info</li>
                        <li>Check Vercel function logs for detailed error messages</li>
                        <li>Verify all dependencies are installed correctly</li>
                        <li>Ensure Django settings module can be imported</li>
                    </ol>
                </div>
            </div>
        </body>
        </html>
        """
        return [html_content.encode('utf-8')]
    return application

try:
    debug_print("=== DJANGO IMPORT PHASE ===")
    
    # Step 1: Try to import Django
    debug_print("Importing Django...")
    import django
    debug_print(f"✅ Django imported successfully (version: {django.VERSION})")
    
    # Step 2: Import settings
    debug_print("Importing Django settings...")
    from django.conf import settings
    debug_print(f"✅ Settings imported, configured: {settings.configured}")
    
    # Step 3: Setup Django if needed
    if not settings.configured:
        debug_print("Setting up Django...")
        django.setup()
        debug_print("✅ Django setup completed")
    else:
        debug_print("✅ Django already configured")
    
    # Step 4: Test basic settings access
    debug_print("Testing settings access...")
    debug_print(f"   - DEBUG: {settings.DEBUG}")
    debug_print(f"   - ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
    debug_print(f"   - INSTALLED_APPS count: {len(settings.INSTALLED_APPS)}")
    
    # Step 5: Import WSGI application
    debug_print("Importing WSGI application...")
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    debug_print("✅ WSGI application created successfully")
    
    debug_print("=== DJANGO SETUP COMPLETE ===")
    
except ImportError as e:
    error_msg = f"Import Error: {str(e)}"
    debug_print(f"❌ {error_msg}")
    
    # Try to give more specific import error info
    import_details = f"""
Module that failed to import: {e.name if hasattr(e, 'name') else 'Unknown'}
Import path attempted: {e.path if hasattr(e, 'path') else 'Unknown'}
Available modules in current directory: {list(Path('.').glob('*.py'))}
Available packages: {[p for p in sys.path if Path(p).exists()]}
    """
    
    application = create_error_response(error_msg, import_details)
    
except Exception as e:
    import traceback
    error_msg = f"Django Configuration Error: {str(e)}"
    full_traceback = traceback.format_exc()
    debug_print(f"❌ {error_msg}")
    debug_print(f"Full traceback: {full_traceback}")
    
    application = create_error_response(error_msg, full_traceback)

# Vercel expects the app at module level
app = application
