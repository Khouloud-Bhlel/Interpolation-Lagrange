"""
Minimal test view for debugging Vercel deployment
"""
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import sys
import os
import django

@csrf_exempt
@require_http_methods(["GET"])
def debug_info(request):
    """Return debug information about the Django environment"""
    
    debug_data = {
        "status": "Django is working!",
        "django_version": django.VERSION,
        "python_version": sys.version,
        "python_path": sys.path[:5],  # First 5 entries
        "working_directory": os.getcwd(),
        "environment_variables": {
            "VERCEL": os.environ.get("VERCEL"),
            "DEBUG": os.environ.get("DEBUG"),
            "DJANGO_SETTINGS_MODULE": os.environ.get("DJANGO_SETTINGS_MODULE"),
            "ALLOWED_HOSTS": os.environ.get("ALLOWED_HOSTS"),
        },
        "settings_info": {
            "debug": None,
            "allowed_hosts": None,
            "static_url": None,
            "database_engine": None,
        }
    }
    
    try:
        from django.conf import settings
        debug_data["settings_info"] = {
            "debug": settings.DEBUG,
            "allowed_hosts": settings.ALLOWED_HOSTS,
            "static_url": settings.STATIC_URL,
            "database_engine": settings.DATABASES["default"]["ENGINE"],
            "installed_apps_count": len(settings.INSTALLED_APPS),
            "middleware_count": len(settings.MIDDLEWARE),
        }
    except Exception as e:
        debug_data["settings_error"] = str(e)
    
    return JsonResponse(debug_data, safe=False)
