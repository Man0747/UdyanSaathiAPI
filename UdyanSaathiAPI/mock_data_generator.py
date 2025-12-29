"""
Mock Data Generator for Dispatch System
Creates realistic sample data for demonstration
"""

from datetime import datetime, timedelta
import random
from .models import FleetAsset, DispatchTicket, InterventionLog
import uuid


class MockDataGenerator:
    
    # Sample fleet locations (major Indian cities)
    MOCK_FLEET_DATA = [
        {
            'asset_id': 'SG-DEL-001',
            'asset_type': 'SMOG_GUN',
            'status': 'IDLE',
            'current_lat': 28.7041,
            'current_lon': 77.1025,
            'home_station': 'Connaught Place, Delhi',
            'water_level_pct': 100,
            'fuel_level_pct': 85
        },
        {
            'asset_id': 'SG-DEL-002',
            'asset_type': 'SMOG_GUN',
            'status': 'ACTIVE',
            'current_lat': 28.5355,
            'current_lon': 77.3910,
            'home_station': 'Noida, Sector 62',
            'water_level_pct': 65,
            'fuel_level_pct': 45
        },
        {
            'asset_id': 'SG-GGN-001',
            'asset_type': 'SMOG_GUN',
            'status': 'DISPATCHED',
            'current_lat': 28.4595,
            'current_lon': 77.0266,
            'home_station': 'Gurugram, Cyber City',
            'water_level_pct': 88,
            'fuel_level_pct': 72
        },
        {
            'asset_id': 'SG-MUM-001',
            'asset_type': 'SMOG_GUN',
            'status': 'IDLE',
            'current_lat': 19.0760,
            'current_lon': 72.8777,
            'home_station': 'Mumbai, Andheri',
            'water_level_pct': 100,
            'fuel_level_pct': 90
        },
        {
            'asset_id': 'SG-BLR-001',
            'asset_type': 'SMOG_GUN',
            'status': 'IDLE',
            'current_lat': 12.9716,
            'current_lon': 77.5946,
            'home_station': 'Bangalore, Whitefield',
            'water_level_pct': 95,
            'fuel_level_pct': 88
        },
        {
            'asset_id': 'SG-KOL-001',
            'asset_type': 'SMOG_GUN',
            'status': 'RETURNING',
            'current_lat': 22.5726,
            'current_lon': 88.3639,
            'home_station': 'Kolkata, Salt Lake',
            'water_level_pct': 42,
            'fuel_level_pct': 38
        },
        {
            'asset_id': 'SG-HYD-001',
            'asset_type': 'SMOG_GUN',
            'status': 'IDLE',
            'current_lat': 17.3850,
            'current_lon': 78.4867,
            'home_station': 'Hyderabad, Hitech City',
            'water_level_pct': 78,
            'fuel_level_pct': 65
        },
        {
            'asset_id': 'SG-CHE-001',
            'asset_type': 'SMOG_GUN',
            'status': 'MAINTENANCE',
            'current_lat': 13.0827,
            'current_lon': 80.2707,
            'home_station': 'Chennai, Anna Nagar',
            'water_level_pct': 0,
            'fuel_level_pct': 0
        },
        {
            'asset_id': 'SG-PUN-001',
            'asset_type': 'SMOG_GUN',
            'status': 'IDLE',
            'current_lat': 18.5204,
            'current_lon': 73.8567,
            'home_station': 'Pune, Hinjewadi',
            'water_level_pct': 92,
            'fuel_level_pct': 80
        },
        {
            'asset_id': 'SG-AHM-001',
            'asset_type': 'SMOG_GUN',
            'status': 'ACTIVE',
            'current_lat': 23.0225,
            'current_lon': 72.5714,
            'home_station': 'Ahmedabad, Satellite',
            'water_level_pct': 55,
            'fuel_level_pct': 48
        },
        {
            'asset_id': 'SP-DEL-001',
            'asset_type': 'SPRINKLER',
            'status': 'ACTIVE',
            'current_lat': 28.6139,
            'current_lon': 77.2090,
            'home_station': 'India Gate, Delhi',
            'water_level_pct': 70,
            'fuel_level_pct': 100
        },
        {
            'asset_id': 'SP-MUM-001',
            'asset_type': 'SPRINKLER',
            'status': 'ACTIVE',
            'current_lat': 18.9220,
            'current_lon': 72.8347,
            'home_station': 'Marine Drive, Mumbai',
            'water_level_pct': 85,
            'fuel_level_pct': 100
        }
    ]
    
    # Sample mission scenarios
    MOCK_MISSION_SCENARIOS = [
        {
            'target_station': 'Anand Vihar, Delhi',
            'target_lat': 28.6469,
            'target_lon': 77.3169,
            'predicted_pm25': 420,
            'urgency_level': 'CRITICAL',
            'mission_brief': 'Deploy to Anand Vihar. Predicted PM2.5 spike: 420 µg/m³ (AQI 470). Critical crop burning detected. ETA: 15 mins.',
            'asset_id': 'SG-DEL-002'
        },
        {
            'target_station': 'Dwarka, Delhi',
            'target_lat': 28.5921,
            'target_lon': 77.0460,
            'predicted_pm25': 365,
            'urgency_level': 'HIGH',
            'mission_brief': 'Deploy to Dwarka. Predicted PM2.5 spike: 365 µg/m³ (AQI 415). Industrial emissions increasing. ETA: 22 mins.',
            'asset_id': 'SG-GGN-001'
        },
        {
            'target_station': 'Thane, Mumbai',
            'target_lat': 19.2183,
            'target_lon': 72.9781,
            'predicted_pm25': 285,
            'urgency_level': 'MEDIUM',
            'mission_brief': 'Deploy to Thane. Predicted PM2.5 spike: 285 µg/m³ (AQI 335). Construction dust mitigation. ETA: 35 mins.',
            'asset_id': 'SG-MUM-001'
        },
        {
            'target_station': 'Ahmedabad, Gujarat',
            'target_lat': 23.0225,
            'target_lon': 72.5714,
            'predicted_pm25': 310,
            'urgency_level': 'HIGH',
            'mission_brief': 'Deploy to Ahmedabad. Predicted PM2.5 spike: 310 µg/m³ (AQI 360). Festival pollution control. ETA: 18 mins.',
            'asset_id': 'SG-AHM-001'
        }
    ]
    
    # Sample intervention results (completed missions)
    MOCK_INTERVENTION_LOGS = [
        {
            'station': 'Rohini, Delhi',
            'pre_pm25': 450,
            'post_pm25': 285,
            'reduction': 36.7,
            'water_used': 15000,
            'duration': 4.5
        },
        {
            'station': 'Bandra, Mumbai',
            'pre_pm25': 320,
            'post_pm25': 215,
            'reduction': 32.8,
            'water_used': 12000,
            'duration': 3.2
        },
        {
            'station': 'Electronic City, Bangalore',
            'pre_pm25': 280,
            'post_pm25': 195,
            'reduction': 30.4,
            'water_used': 10000,
            'duration': 3.8
        },
        {
            'station': 'Salt Lake, Kolkata',
            'pre_pm25': 395,
            'post_pm25': 240,
            'reduction': 39.2,
            'water_used': 14500,
            'duration': 5.1
        },
        {
            'station': 'Hitech City, Hyderabad',
            'pre_pm25': 305,
            'post_pm25': 210,
            'reduction': 31.1,
            'water_used': 11000,
            'duration': 3.5
        }
    ]
    
    @classmethod
    def create_mock_fleet(cls):
        """Create sample fleet assets"""
        created_count = 0
        
        for asset_data in cls.MOCK_FLEET_DATA:
            asset, created = FleetAsset.objects.update_or_create(
                asset_id=asset_data['asset_id'],
                defaults=asset_data
            )
            if created:
                created_count += 1
        
        return {
            'status': 'SUCCESS',
            'created': created_count,
            'total': len(cls.MOCK_FLEET_DATA),
            'message': f'Created {created_count} fleet assets, updated {len(cls.MOCK_FLEET_DATA) - created_count}'
        }
    
    @classmethod
    def create_mock_missions(cls):
        """Create sample active dispatch missions"""
        created_count = 0
        
        for scenario in cls.MOCK_MISSION_SCENARIOS:
            try:
                asset = FleetAsset.objects.get(asset_id=scenario['asset_id'])
                
                # Check if mission already exists for this asset
                existing = DispatchTicket.objects.filter(
                    asset=asset,
                    is_completed=False
                ).first()
                
                if existing:
                    continue
                
                # Generate unique ticket ID
                ticket_id = f"DSP-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
                
                # Calculate predicted AQI
                predicted_aqi = cls._pm25_to_aqi(scenario['predicted_pm25'])
                
                # Create mission
                mission = DispatchTicket.objects.create(
                    ticket_id=ticket_id,
                    asset=asset,
                    target_station=scenario['target_station'],
                    target_lat=scenario['target_lat'],
                    target_lon=scenario['target_lon'],
                    predicted_pm25=scenario['predicted_pm25'],
                    predicted_aqi=predicted_aqi,
                    forecast_time=datetime.now() + timedelta(hours=random.randint(2, 6)),
                    urgency_level=scenario['urgency_level'],
                    mission_brief=scenario['mission_brief'],
                    estimated_arrival=datetime.now() + timedelta(minutes=random.randint(15, 45)),
                    is_completed=False
                )
                
                created_count += 1
                
                # Update asset status
                asset.status = 'DISPATCHED' if scenario['urgency_level'] in ['HIGH', 'CRITICAL'] else 'ACTIVE'
                asset.save()
            
            except FleetAsset.DoesNotExist:
                continue
        
        return {
            'status': 'SUCCESS',
            'created': created_count,
            'total': len(cls.MOCK_MISSION_SCENARIOS)
        }
    
    @classmethod
    def create_mock_intervention_logs(cls):
        """Create sample intervention effectiveness logs"""
        created_count = 0
        
        for log_data in cls.MOCK_INTERVENTION_LOGS:
            # Create a completed dummy mission first
            ticket_id = f"DSP-HIST-{uuid.uuid4().hex[:6].upper()}"
            
            # Get a random idle asset
            asset = FleetAsset.objects.filter(status='IDLE').first()
            if not asset:
                asset = FleetAsset.objects.first()
            
            if not asset:
                continue
            
            # Create completed mission
            mission = DispatchTicket.objects.create(
                ticket_id=ticket_id,
                asset=asset,
                target_station=log_data['station'],
                target_lat=28.0 + random.uniform(-5, 5),
                target_lon=77.0 + random.uniform(-5, 5),
                predicted_pm25=log_data['pre_pm25'],
                predicted_aqi=cls._pm25_to_aqi(log_data['pre_pm25']),
                forecast_time=datetime.now() - timedelta(days=random.randint(1, 7)),
                urgency_level='HIGH',
                mission_brief=f"Historical mission at {log_data['station']}",
                dispatch_time=datetime.now() - timedelta(days=random.randint(1, 7), hours=random.randint(1, 5)),
                estimated_arrival=datetime.now() - timedelta(days=random.randint(1, 7), hours=random.randint(0, 4)),
                actual_arrival=datetime.now() - timedelta(days=random.randint(1, 7), hours=random.randint(0, 3)),
                is_completed=True,
                completion_time=datetime.now() - timedelta(days=random.randint(0, 7))
            )
            
            # Create intervention log
            log = InterventionLog.objects.create(
                ticket=mission,
                pre_intervention_pm25=log_data['pre_pm25'],
                pre_intervention_aqi=cls._pm25_to_aqi(log_data['pre_pm25']),
                post_intervention_pm25=log_data['post_pm25'],
                post_intervention_aqi=cls._pm25_to_aqi(log_data['post_pm25']),
                reduction_percentage=log_data['reduction'],
                intervention_duration_hours=log_data['duration'],
                water_used_liters=log_data['water_used']
            )
            
            created_count += 1
        
        return {
            'status': 'SUCCESS',
            'created': created_count,
            'total': len(cls.MOCK_INTERVENTION_LOGS)
        }
    
    @staticmethod
    def _pm25_to_aqi(pm25):
        """Convert PM2.5 to AQI"""
        if pm25 <= 30:
            return int((pm25 / 30) * 50)
        elif pm25 <= 60:
            return int(50 + ((pm25 - 30) / 30) * 50)
        elif pm25 <= 90:
            return int(100 + ((pm25 - 60) / 30) * 100)
        elif pm25 <= 120:
            return int(200 + ((pm25 - 90) / 30) * 100)
        elif pm25 <= 250:
            return int(300 + ((pm25 - 120) / 130) * 100)
        else:
            return int(400 + ((pm25 - 250) / 130) * 100)
    
    @classmethod
    def initialize_complete_demo(cls):
        """One-click initialization of entire dispatch demo"""
        results = {}
        
        # Step 1: Create fleet
        results['fleet'] = cls.create_mock_fleet()
        
        # Step 2: Create active missions
        results['missions'] = cls.create_mock_missions()
        
        # Step 3: Create historical logs
        results['logs'] = cls.create_mock_intervention_logs()
        
        return {
            'status': 'DEMO_COMPLETE',
            'results': results,
            'summary': {
                'fleet_assets': results['fleet']['total'],
                'active_missions': results['missions']['created'],
                'historical_interventions': results['logs']['created']
            }
        }
