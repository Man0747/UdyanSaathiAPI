"""
Management command to sync production data to local cache
Usage: python manage.py sync_production_data
"""

from django.core.management.base import BaseCommand
from django.core.cache import cache
from UdyanSaathiAPI.models import StationsCoordinatesModel, pollutionModel
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Sync production data to local cache for faster access'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force sync even if cache exists',
        )
    
    def handle(self, *args, **options):
        force = options.get('force', False)
        
        self.stdout.write('🚀 Starting production data sync...')
        self.stdout.write('')
        
        # Check if cache exists
        if not force and cache.get('all_stations'):
            self.stdout.write(self.style.WARNING('⚠️  Cache already exists. Use --force to override.'))
            return
        
        # Sync station coordinates
        self.sync_stations()
        
        # Sync latest pollution data
        self.sync_pollution_data()
        
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('✅ Sync complete!'))
        self.stdout.write('')
        self.stdout.write('📊 Cache configured for:')
        self.stdout.write('  - Station data: 24 hours')
        self.stdout.write('  - Pollution data: 1 hour')
        self.stdout.write('  - Ward rankings: 5 minutes')
    
    def sync_stations(self):
        """Sync all station coordinates from production"""
        self.stdout.write('📍 Syncing station coordinates...')
        
        try:
            # Query production database directly using router
            stations = StationsCoordinatesModel.objects.using('production').all()
            
            # Convert to list of dicts for caching
            station_data = []
            for station in stations:
                station_data.append({
                    'Station': station.Station,
                    'City': station.City,
                    'State': station.State,
                    'Latitude': float(station.Latitude),
                    'Longitude': float(station.Longitude),
                })
            
            if not station_data:
                self.stdout.write(self.style.WARNING('⚠️  No stations found in production DB'))
                return
            
            # Cache for 24 hours
            cache.set('all_stations', station_data, 86400)
            
            self.stdout.write(self.style.SUCCESS(f'✅ Synced {len(station_data)} stations'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error syncing stations: {e}'))
            self.stdout.write('   Make sure production database is configured in settings.py')
    
    def sync_pollution_data(self):
        """Sync latest pollution readings from production"""
        self.stdout.write('💨 Syncing pollution data...')
        
        try:
            # Get latest record for each station from production
            from django.db.models import Max
            
            # Get the most recent date
            latest_date = pollutionModel.objects.using('production').aggregate(
                max_date=Max('Pol_Date')
            )['max_date']
            
            if not latest_date:
                self.stdout.write(self.style.WARNING('⚠️  No pollution data found'))
                return
            
            # Get latest data for each station
            pollution = pollutionModel.objects.using('production').filter(
                Pol_Date=latest_date
            ).values(
                'pol_Station', 'AQI', 'PM25', 'PM10', 
                'CO', 'NO2', 'SO2', 'O3', 'Pol_Date'
            )
            
            # Cache for 1 hour
            pollution_data = list(pollution)
            cache.set('latest_pollution', pollution_data, 3600)
            cache.set('latest_pollution_date', latest_date.isoformat(), 3600)
            
            self.stdout.write(self.style.SUCCESS(
                f'✅ Synced {len(pollution_data)} pollution records from {latest_date}'
            ))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error syncing pollution: {e}'))
            self.stdout.write('   Make sure production database is configured in settings.py')
