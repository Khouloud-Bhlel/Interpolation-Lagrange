from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'points', views.InterpolationPointViewSet)
router.register(r'sets', views.InterpolationSetViewSet)
router.register(r'results', views.LagrangeResultViewSet)

urlpatterns = [
    # Main web interface
    path('', views.index, name='index'),
    
    # Include the router URLs
    path('api/', include(router.urls)),
    
    # Direct interpolation API
    path('api/interpolate/', views.InterpolationAPIView.as_view(), name='interpolate'),
    
    # Odoo integration
    path('api/odoo/send/', views.OdooIntegrationView.as_view(), name='odoo-integration'),
]
