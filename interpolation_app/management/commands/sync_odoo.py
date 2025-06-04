from django.core.management.base import BaseCommand
from django.conf import settings
from decouple import config
import requests
import json
from interpolation_app.models import InterpolationSet, LagrangeResult


class Command(BaseCommand):
    help = 'Sync interpolation data with Odoo'

    def add_arguments(self, parser):
        parser.add_argument(
            '--set-id',
            type=int,
            help='Sync specific interpolation set by ID',
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Sync all interpolation sets',
        )
        parser.add_argument(
            '--check-connection',
            action='store_true',
            help='Check Odoo connection status',
        )

    def handle(self, *args, **options):
        if options['check_connection']:
            self.check_odoo_connection()
        elif options['all']:
            self.sync_all_sets()
        elif options['set_id']:
            self.sync_specific_set(options['set_id'])
        else:
            self.stdout.write(
                self.style.ERROR('Please specify --all, --set-id, or --check-connection')
            )

    def check_odoo_connection(self):
        """Check if Odoo is accessible"""
        try:
            odoo_config = settings.ODOO_CONFIG
            odoo_url = f"http://{odoo_config['host']}:{odoo_config['port']}"
            
            self.stdout.write(f"Checking Odoo connection at {odoo_url}...")
            
            # Try to access Odoo web interface
            response = requests.get(f"{odoo_url}/web/database/selector", timeout=5)
            
            if response.status_code == 200:
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Odoo is accessible at {odoo_url}')
                )
                self.stdout.write(f"Database: {odoo_config['database']}")
                self.stdout.write(f"User: {odoo_config['username']}")
            else:
                self.stdout.write(
                    self.style.ERROR(f'✗ Odoo returned status code: {response.status_code}')
                )
                
        except requests.exceptions.ConnectionError:
            self.stdout.write(
                self.style.ERROR('✗ Cannot connect to Odoo. Make sure it\'s running with: docker-compose up -d')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'✗ Error checking Odoo: {str(e)}')
            )

    def sync_all_sets(self):
        """Sync all interpolation sets to Odoo"""
        sets = InterpolationSet.objects.all()
        
        if not sets.exists():
            self.stdout.write(
                self.style.WARNING('No interpolation sets found to sync')
            )
            return
        
        self.stdout.write(f"Syncing {sets.count()} interpolation sets...")
        
        for interpolation_set in sets:
            self.sync_set_to_odoo(interpolation_set)

    def sync_specific_set(self, set_id):
        """Sync specific interpolation set to Odoo"""
        try:
            interpolation_set = InterpolationSet.objects.get(id=set_id)
            self.stdout.write(f"Syncing set: {interpolation_set.name}")
            self.sync_set_to_odoo(interpolation_set)
        except InterpolationSet.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'Interpolation set with ID {set_id} not found')
            )

    def sync_set_to_odoo(self, interpolation_set):
        """Sync a single interpolation set to Odoo"""
        try:
            # Prepare data for Odoo
            points_data = []
            for point in interpolation_set.points.all():
                points_data.append({
                    'x_coordinate': point.x,
                    'y_coordinate': point.y
                })

            # Get latest result if exists
            latest_result = interpolation_set.result_ids.order_by('-created_at').first()
            
            odoo_data = {
                'interpolation_set': {
                    'name': interpolation_set.name,
                    'description': interpolation_set.description,
                    'points': points_data,
                    'points_count': len(points_data)
                }
            }

            if latest_result:
                odoo_data['interpolation_result'] = {
                    'polynomial_coefficients': latest_result.polynomial_coefficients,
                    'evaluation_points': latest_result.evaluation_points,
                    'evaluation_results': latest_result.evaluation_results,
                }

            # In a real implementation, you would make actual Odoo API calls here
            # For now, we'll simulate the process
            
            self.stdout.write(
                self.style.SUCCESS(f'✓ Prepared data for Odoo integration: {interpolation_set.name}')
            )
            
            # Display what would be sent
            self.stdout.write("Data prepared for Odoo:")
            self.stdout.write(json.dumps(odoo_data, indent=2))
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'✗ Error syncing {interpolation_set.name}: {str(e)}')
            )

    def get_odoo_api_client(self):
        """Get Odoo API client (placeholder for actual implementation)"""
        # In a real implementation, you would use xmlrpc or JSON-RPC
        # to connect to Odoo's API
        pass
