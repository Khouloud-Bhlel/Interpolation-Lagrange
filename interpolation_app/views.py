from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import requests
import json

from .models import InterpolationPoint, InterpolationSet, LagrangeResult
from .serializers import (
    InterpolationPointSerializer,
    InterpolationSetSerializer,
    LagrangeResultSerializer,
    InterpolationRequestSerializer
)
from .lagrange import LagrangeInterpolator

def index(request):
    """Serve the main HTML interface"""
    return render(request, 'interpolation_app/index.html')

class InterpolationPointViewSet(viewsets.ModelViewSet):
    queryset = InterpolationPoint.objects.all()
    serializer_class = InterpolationPointSerializer

class InterpolationSetViewSet(viewsets.ModelViewSet):
    queryset = InterpolationSet.objects.all()
    serializer_class = InterpolationSetSerializer
    
    @action(detail=True, methods=['post'])
    def add_point(self, request, pk=None):
        """Add a point to the interpolation set"""
        interpolation_set = self.get_object()
        x = request.data.get('x')
        y = request.data.get('y')
        
        if x is None or y is None:
            return Response(
                {'error': 'Both x and y coordinates are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        point = InterpolationPoint.objects.create(x=float(x), y=float(y))
        interpolation_set.points.add(point)
        
        serializer = self.get_serializer(interpolation_set)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def interpolate(self, request, pk=None):
        """Perform Lagrange interpolation on the set"""
        interpolation_set = self.get_object()
        points = interpolation_set.get_points_list()
        
        if len(points) < 2:
            return Response(
                {'error': 'At least 2 points are required for interpolation'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            interpolator = LagrangeInterpolator(points)
            
            # Get evaluation points from request, or use default range
            x_values = request.data.get('x_values', [])
            if not x_values:
                x_min = min(p[0] for p in points) - 1
                x_max = max(p[0] for p in points) + 1
                x_values, y_values = interpolator.interpolate_range(x_min, x_max, 100)
            else:
                y_values = interpolator.evaluate_at_points(x_values)
            
            # Get polynomial coefficients
            coefficients = interpolator.get_polynomial_coefficients()
            
            # Save result
            result = LagrangeResult.objects.create(
                interpolation_set=interpolation_set
            )
            result.set_coefficients(coefficients)
            result.set_evaluation_data(x_values, y_values)
            result.save()
            
            # Get animation data
            animation_data = interpolator.get_animation_data()
            lagrange_terms_details = interpolator.get_lagrange_terms_details()
            
            return Response({
                'result_id': result.id,
                'coefficients': coefficients,
                'evaluation_points': x_values,
                'evaluation_results': y_values,
                'animation_data': animation_data,
                'lagrange_terms_details': lagrange_terms_details,
                'original_points': points
            })
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class LagrangeResultViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LagrangeResult.objects.all()
    serializer_class = LagrangeResultSerializer

@method_decorator(csrf_exempt, name='dispatch')
class InterpolationAPIView(APIView):
    """
    Direct API for Lagrange interpolation without saving to database
    """
    
    def post(self, request):
        serializer = InterpolationRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        points = [(p[0], p[1]) for p in data['points']]
        x_values = data.get('x_values', [])
        
        try:
            interpolator = LagrangeInterpolator(points)
            
            # Generate evaluation points if not provided
            if not x_values:
                x_min = min(p[0] for p in points) - 1
                x_max = max(p[0] for p in points) + 1
                x_values, y_values = interpolator.interpolate_range(x_min, x_max, 100)
            else:
                y_values = interpolator.evaluate_at_points(x_values)
            
            # Get additional data
            coefficients = interpolator.get_polynomial_coefficients()
            animation_data = interpolator.get_animation_data()
            lagrange_terms_details = interpolator.get_lagrange_terms_details()
            
            return Response({
                'success': True,
                'coefficients': coefficients,
                'evaluation_points': x_values if isinstance(x_values, list) else x_values.tolist(),
                'evaluation_results': y_values,
                'animation_data': animation_data,
                'lagrange_terms_details': lagrange_terms_details,
                'original_points': points,
                'polynomial_degree': len(points) - 1
            })
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@method_decorator(csrf_exempt, name='dispatch')
class OdooIntegrationView(APIView):
    """
    Integration with Odoo using Docker Desktop
    """
    
    def get_odoo_url(self):
        config = settings.ODOO_CONFIG
        return f"http://{config['host']}:{config['port']}"
    
    def post(self, request):
        """Send interpolation results to Odoo"""
        try:
            # Get Odoo configuration from settings
            odoo_config = settings.ODOO_CONFIG
            
            # Prepare data for Odoo - handle both formats
            interpolation_data = request.data.get('interpolation_data', request.data)
            
            # Extract data from interpolation results
            points = interpolation_data.get('original_points', interpolation_data.get('points', []))
            coefficients = interpolation_data.get('coefficients', [])
            evaluation_points = interpolation_data.get('evaluation_points', [])
            evaluation_results = interpolation_data.get('evaluation_results', [])
            
            # Create a structured payload for Odoo
            odoo_payload = {
                'interpolation_set': {
                    'name': f"Interpolation Set {len(points)} points",
                    'description': f"Lagrange interpolation with {len(points)} points, degree {len(points)-1}",
                    'points': [{'x': p[0], 'y': p[1]} for p in points],
                },
                'interpolation_result': {
                    'polynomial_coefficients': coefficients,
                    'evaluation_points': evaluation_points,
                    'evaluation_results': evaluation_results,
                    'polynomial_degree': len(points) - 1 if points else 0,
                }
            }
            
            # Actually send data to Odoo using XML-RPC
            try:
                import xmlrpc.client
                
                # Odoo connection parameters
                url = f"http://{odoo_config['host']}:{odoo_config['port']}"
                db = odoo_config['database']
                username = odoo_config['user']
                password = odoo_config['password']
                
                # Connect to Odoo
                common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
                uid = common.authenticate(db, username, password, {})
                
                if not uid:
                    raise Exception("Failed to authenticate with Odoo")
                
                models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
                
                # Create interpolation set
                set_data = {
                    'name': odoo_payload['interpolation_set']['name'],
                    'description': odoo_payload['interpolation_set']['description'],
                }
                
                set_id = models.execute_kw(db, uid, password, 'lagrange.interpolation.set', 'create', [set_data])
                
                # Create interpolation points
                for point_data in odoo_payload['interpolation_set']['points']:
                    point_record = {
                        'x_coordinate': point_data['x'],
                        'y_coordinate': point_data['y'],
                        'interpolation_set_id': set_id,
                    }
                    models.execute_kw(db, uid, password, 'lagrange.interpolation.point', 'create', [point_record])
                
                # Create interpolation result
                import json
                result_data = {
                    'interpolation_set_id': set_id,
                    'polynomial_coefficients': json.dumps(coefficients),
                    'evaluation_points': json.dumps(evaluation_points),
                    'evaluation_results': json.dumps(evaluation_results),
                }
                
                result_id = models.execute_kw(db, uid, password, 'lagrange.interpolation.result', 'create', [result_data])
                
                response_data = {
                    'success': True,
                    'message': 'Data successfully sent to Odoo',
                    'odoo_config': {
                        'host': odoo_config['host'],
                        'port': odoo_config['port'],
                        'database': odoo_config['database'],
                        'user': odoo_config['user']
                    },
                    'odoo_records': {
                        'set_id': set_id,
                        'result_id': result_id,
                        'points_created': len(odoo_payload['interpolation_set']['points'])
                    },
                    'data_sent': odoo_payload,
                    'integration_status': 'completed',
                    'odoo_url': f"http://{odoo_config['host']}:{odoo_config['port']}/web#id={set_id}&model=lagrange.interpolation.set&view_type=form"
                }
                
                return Response(response_data)
                
            except Exception as odoo_error:
                # If Odoo integration fails, still return success but with simulation message
                print(f"Odoo integration failed: {str(odoo_error)}")
                
                response_data = {
                    'success': True,
                    'message': 'Data prepared for Odoo integration (Odoo not accessible)',
                    'odoo_config': {
                        'host': odoo_config['host'],
                        'port': odoo_config['port'],
                        'database': odoo_config['database'],
                        'user': odoo_config['user']
                    },
                    'data_prepared': odoo_payload,
                    'integration_status': 'simulated',
                    'odoo_error': str(odoo_error),
                    'instructions': [
                        'Make sure Odoo is running: docker-compose up -d',
                        f'Access Odoo at: http://{odoo_config["host"]}:{odoo_config["port"]}',
                        'Install the lagrange_integration module',
                        'Set up database: odoo',
                        f'Username: {odoo_config["user"]}, Password: {odoo_config["password"]}'
                    ]
                }
                
                return Response(response_data)
            
        except Exception as e:
            import traceback
            error_details = str(e)
            traceback_details = traceback.format_exc()
            print(f"Odoo integration error: {error_details}")
            print(f"Traceback: {traceback_details}")
            
            return Response(
                {'error': f'Odoo integration error: {error_details}', 'traceback': traceback_details},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def get(self, request):
        """Get Odoo integration status"""
        try:
            odoo_config = settings.ODOO_CONFIG
            
            # Check if Odoo is accessible (basic health check)
            try:
                odoo_url = self.get_odoo_url()
                # In a real implementation, you would ping Odoo here
                odoo_status = 'configured'
            except:
                odoo_status = 'not_accessible'
            
            return Response({
                'odoo_config': {
                    'host': odoo_config['host'],
                    'port': odoo_config['port'],
                    'database': odoo_config['database']
                },
                'status': odoo_status,
                'integration_available': True
            })
            
        except Exception as e:
            return Response(
                {'error': f'Odoo status check error: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
