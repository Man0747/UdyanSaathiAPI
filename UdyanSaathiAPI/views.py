from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import pollutionModel, FleetAsset, DispatchTicket, InterventionLog
from .serializer import *
from .DBOPS import PollutionDAO
from .mock_data_generator import MockDataGenerator
from django.db.models import Avg, Sum
from datetime import datetime
import random

# ALL VIEWS OF THE REST API

#THIS VIEW RETURNS POLLUTION DATA FOR A STATION
@api_view(['GET']) #TYPE OF VIEW
def get_PollutionData_By_Station(request): 
    pol_Station = request.GET.get('pol_Station') #THIS GETS THE QUERY PARAMAETER
    pollutiondata = PollutionDAO.find_PollutionData_By_Station(pol_Station) #THIS GETS DATA FROM DATABASE
    serializer = PollutionSerializer(pollutiondata, many=True) #USED DO CONVERT DATA TO JSON
    return Response(serializer.data,status=status.HTTP_200_OK) #RETURNS THE DATA 

#THIS VIEW RETURNS ALL STATIONS FOR A CITY
@api_view(['GET']) #TYPE OF VIEW
def get_Stations_By_City(request):
    pol_Station = request.GET.get('pol_Station') #THIS GETS THE QUERY PARAMAETER
    stationdata = PollutionDAO.find_Stations_By_City(pol_Station) #THIS GETS DATA FROM DATABASE
    serializer = StationSerializer(stationdata, many=True) #USED DO CONVERT DATA TO JSON
    return Response(serializer.data,status=status.HTTP_200_OK) #RETURNS THE DATA 

#THIS VIEW RETURNS ALL STATIONS IN OUR DATABASE
@api_view(['GET']) #TYPE OF VIEW
def get_All_Stations(request):
    stationdata = PollutionDAO.find_All_Stations() #THIS GETS DATA FROM DATABASE
    serializer = StationSerializer(stationdata, many=True) #USED DO CONVERT DATA TO JSON
    return Response(serializer.data,status=status.HTTP_200_OK) #RETURNS THE DATA 

#THIS VIEW RETURNS TOP 6 CITIES WITH MOST POLLUTION
@api_view(['GET']) #TYPE OF VIEW
def get_Top6_Most_Polluted_Cities(request):
    todate = request.GET.get('to_date') #THIS GETS THE QUERY PARAMAETER
    Top6CityData = PollutionDAO.find_Top6_Most_Polluted_Cities(todate) #THIS GETS DATA FROM DATABASE
    serializer = Top6CitiesSerializer(Top6CityData, many=True) #USED DO CONVERT DATA TO JSON
    return Response(serializer.data,status=status.HTTP_200_OK) #RETURNS THE DATA 

#THIS VIEW RETURNS TOP 6 CITIES WITH LEAST POLLUTION
@api_view(['GET']) #TYPE OF VIEW
def get_Top6_Least_Polluted_Cities(request):
    todate = request.GET.get('to_date') #THIS GETS THE QUERY PARAMAETER
    Least6CityData = PollutionDAO.find_Top6_Least_Polluted_Cities(todate) #THIS GETS DATA FROM DATABASE
    serializer = Top6LeastCitiesSerializer(Least6CityData, many=True) #USED DO CONVERT DATA TO JSON
    return Response(serializer.data,status=status.HTTP_200_OK) #RETURNS THE DATA 

#THIS VIEW RETURNS GRAPH DATA FOR A CITY 
@api_view(['GET']) #TYPE OF VIEW
def get_GraphData(request):
    todate = request.GET.get('to_date') #THIS GETS THE QUERY PARAMAETER
    pol_City = request.GET.get('pol_City') #THIS GETS THE QUERY PARAMAETER
    GraphData = PollutionDAO.find_GraphData(pol_City,todate)  #THIS GETS DATA FROM DATABASE
    serializer = GraphSerializer(GraphData, many=True) #USED DO CONVERT DATA TO JSON
    return Response(serializer.data,status=status.HTTP_200_OK)  #RETURNS THE DATA 

#THIS VIEW RETURNS DATA FOR ALl MAJOR METRO CITIES 
@api_view(['GET']) #TYPE OF VIEW
def get_MetroCities_Data(request):
    todate = request.GET.get('to_date') #THIS GETS THE QUERY PARAMAETER
    metroData = PollutionDAO.find_MetroCities_Data(todate) #THIS GETS DATA FROM DATABASE
    serializer = TopMetroCitiesSerializer(metroData, many=True)  #USED DO CONVERT DATA TO JSON
    return Response(serializer.data,status=status.HTTP_200_OK) #RETURNS THE DATA 

#THIS VIEW RETURNS DATA FOR THE AQI CALENDAR/HEATMAP
@api_view(['GET']) #TYPE OF VIEW
def get_Aqi_Calendar_Data(request):
    pol_Station = request.GET.get('pol_Station') #THIS GETS THE QUERY PARAMAETER
    aqicalData = PollutionDAO.find_Aqi_Calendar_Data(pol_Station) #THIS GETS DATA FROM DATABASE
    serializer = AqiCalendarSerializer(aqicalData, many=True) #USED DO CONVERT DATA TO JSON
    return Response(serializer.data,status=status.HTTP_200_OK) #RETURNS THE DATA 

#THIS VIEW RETURNS ML DATA FOR STATION
@api_view(['GET']) #TYPE OF VIEW
def get_ML_Data(request):
    pol_Station = request.GET.get('pol_Station') #THIS GETS THE QUERY PARAMAETER
    Mldata =  PollutionDAO.find_ML_Data(pol_Station) #THIS GETS DATA FROM DATABASE
    serializer = MlSerializer(Mldata, many=True) #USED DO CONVERT DATA TO JSON
    return Response(serializer.data,status=status.HTTP_200_OK)

#THIS VIEW RETURNS MAP DATA FOR ALL STATIONS
@api_view(['GET']) #TYPE OF VIEW
def get_Map_Data(request):
    Mapdata =  PollutionDAO.find_Map_Data() #THIS GETS DATA FROM DATABASE
    serializer = MapSerializer(Mapdata, many=True) #USED DO CONVERT DATA TO JSON
    return Response(serializer.data,status=status.HTTP_200_OK) #RETURNS THE DATA 

@api_view(['GET'])
def get_Stations_Coordinates(request):
    pol_Station = request.GET.get('pol_Station') #THIS GETS THE QUERY PARAMAETER
    StationCoordinatesData = PollutionDAO.find_StationsCoordinates(pol_Station)
    serializer = StationsCoordinatesSerializer(StationCoordinatesData, many=True) #USED DO CONVERT DATA TO JSON
    return Response(serializer.data,status=status.HTTP_200_OK) #RETURNS THE DATA 

@api_view(['GET'])
def get_HealthOfApi(request):
    return Response({"status":"UdyanSaathiAPI is running fine"},status=status.HTTP_200_OK)

# DISPATCH SYSTEM API VIEWS

@api_view(['POST'])
def initialize_dispatch_demo(request):
    """Initialize complete dispatch system with mock data"""
    result = MockDataGenerator.initialize_complete_demo()
    return Response(result)

@api_view(['GET'])
def get_fleet_status(request):
    """Get all fleet assets with their status"""
    assets = FleetAsset.objects.all()
    
    fleet_data = {
        'total_assets': assets.count(),
        'idle': assets.filter(status='IDLE').count(),
        'active': assets.filter(status='ACTIVE').count(),
        'dispatched': assets.filter(status='DISPATCHED').count(),
        'returning': assets.filter(status='RETURNING').count(),
        'maintenance': assets.filter(status='MAINTENANCE').count(),
        'assets': []
    }
    
    for asset in assets:
        fleet_data['assets'].append({
            'asset_id': asset.asset_id,
            'type': asset.asset_type,
            'status': asset.status,
            'location': [asset.current_lat, asset.current_lon],
            'water_level': asset.water_level_pct,
            'fuel_level': asset.fuel_level_pct,
            'home_station': asset.home_station,
            'operational_hours': asset.operational_hours
        })
    
    return Response(fleet_data)

@api_view(['GET'])
def get_active_missions(request):
    """Get all active dispatch missions"""
    missions = DispatchTicket.objects.filter(
        is_completed=False
    ).select_related('asset').order_by('-urgency_level', 'estimated_arrival')
    
    missions_data = []
    for mission in missions:
        missions_data.append({
            'ticket_id': mission.ticket_id,
            'asset_id': mission.asset.asset_id,
            'asset_type': mission.asset.asset_type,
            'asset_status': mission.asset.status,
            'asset_current_lat': mission.asset.current_lat,
            'asset_current_lon': mission.asset.current_lon,
            'target_station': mission.target_station,
            'target_lat': mission.target_lat,
            'target_lon': mission.target_lon,
            'predicted_pm25': mission.predicted_pm25,
            'predicted_aqi': mission.predicted_aqi,
            'urgency_level': mission.urgency_level,
            'mission_brief': mission.mission_brief,
            'dispatch_time': mission.dispatch_time.isoformat(),
            'estimated_arrival': mission.estimated_arrival.isoformat(),
        })
    
    return Response({
        'total_missions': len(missions_data),
        'missions': missions_data
    })

@api_view(['GET'])
def get_intervention_stats(request):
    """Get intervention effectiveness statistics"""
    logs = InterventionLog.objects.all()
    
    # Calculate aggregates
    total_interventions = logs.count()
    avg_reduction = logs.aggregate(Avg('reduction_percentage'))['reduction_percentage__avg'] or 0
    total_water = logs.aggregate(Sum('water_used_liters'))['water_used_liters__sum'] or 0
    
    # Recent interventions
    recent = logs.select_related('ticket').order_by('-timestamp')[:10]
    recent_data = []
    
    for log in recent:
        recent_data.append({
            'ticket_id': log.ticket.ticket_id,
            'station': log.ticket.target_station,
            'pre_pm25': log.pre_intervention_pm25,
            'pre_aqi': log.pre_intervention_aqi,
            'post_pm25': log.post_intervention_pm25,
            'post_aqi': log.post_intervention_aqi,
            'reduction_percentage': log.reduction_percentage,
            'water_used_liters': log.water_used_liters,
            'duration_hours': log.intervention_duration_hours,
            'timestamp': log.timestamp.isoformat()
        })
    
    return Response({
        'summary': {
            'total_interventions': total_interventions,
            'average_reduction_percentage': round(avg_reduction, 2),
            'total_water_used_liters': total_water,
            'total_water_used_kl': round(total_water / 1000, 2) if total_water else 0
        },
        'recent_interventions': recent_data
    })

@api_view(['GET'])
def get_dispatch_dashboard_summary(request):
    """Get complete dashboard summary"""
    fleet = FleetAsset.objects.all()
    missions = DispatchTicket.objects.filter(is_completed=False)
    logs = InterventionLog.objects.all()
    
    avg_reduction = logs.aggregate(Avg('reduction_percentage'))['reduction_percentage__avg'] or 0
    
    return Response({
        'fleet_summary': {
            'total': fleet.count(),
            'operational': fleet.exclude(status='MAINTENANCE').count(),
            'idle': fleet.filter(status='IDLE').count(),
            'deployed': fleet.filter(status__in=['ACTIVE', 'DISPATCHED']).count()
        },
        'mission_summary': {
            'active': missions.count(),
            'critical': missions.filter(urgency_level='CRITICAL').count(),
            'high': missions.filter(urgency_level='HIGH').count(),
            'medium': missions.filter(urgency_level='MEDIUM').count()
        },
        'effectiveness': {
            'avg_reduction': round(avg_reduction, 2),
            'total_interventions': logs.count()
        }
    })


# ==================== WARD-BASED POLLUTION VIEWS (REAL DATA) ====================

@api_view(['GET'])
def get_ward_rankings(request):
    """
    Get all Delhi wards ranked by pollution level
    Uses REAL pollution data from production API
    """
    from .ward_data import get_ward_data
    from .ward_utils import calculate_ward_pollution, get_urgency_level
    from datetime import datetime
    import random
    
    wards_data = get_ward_data()
    ward_rankings = []
    
    # HYBRID APPROACH: Try cache → production DB → API (fastest to slowest)
    from django.core.cache import cache
    
    # Try cache first (fastest ~5ms)
    cached = cache.get('ward_rankings')
    if cached:
        print("✅ Using cached ward rankings")
        return Response(cached)
    
    # Method 1: Try production database (fast ~50ms)
    try:
        from .models import StationsCoordinatesModel, pollutionModel
        from django.db.models import Max
        
        # Get all stations from production DB
        stations_queryset = StationsCoordinatesModel.objects.using('production').all()
        print(f"✅ Found {stations_queryset.count()} stations from production DB")
        
        # Get latest pollution data
        latest_date = pollutionModel.objects.using('production').aggregate(
            max_date=Max('Pol_Date')
        )['max_date']
        
        pollution_data = {}
        if latest_date:
            pollution_queryset = pollutionModel.objects.using('production').filter(
                Pol_Date=latest_date
            )
            for record in pollution_queryset:
                pollution_data[record.pol_Station] = {
                    'AQI': record.AQI,
                    'PM25': record.PM25,
                    'PM10': record.PM10,
                }
        
        stations_data = []
        for station in stations_queryset:
            pollution = pollution_data.get(station.Station, {})
            stations_data.append({
                'Station': station.Station,
                'Latitude': float(station.Latitude),
                'Longitude': float(station.Longitude),
                'AQI': pollution.get('AQI', 0),
                'PM25': pollution.get('PM25', 0),
                'PM10': pollution.get('PM10', 0),
            })
        
        data_source = 'production_database'
        
    except Exception as db_error:
        # Method 2: Fall back to production API (slower ~300ms)
        print(f"⚠️ DB query failed, falling back to API: {db_error}")
        try:
            import requests
            response = requests.get('https://apiudyansaathi.azurewebsites.net/api/get-MapData/', timeout=10)
            stations_data = response.json()
            print(f"✅ Found {len(stations_data)} stations from production API")
            data_source = 'production_api'
        except Exception as api_error:
            print(f"❌ API call also failed: {api_error}")
            return Response({
                'total_wards': 0,
                'wards': [],
                'error': 'Could not fetch station data from database or API',
                'timestamp': datetime.now().isoformat()
            })
    
    # Assign stations to wards based on location
    for ward_id, ward_info in wards_data.items():
        ward_stations = []
        ward_center = ward_info['center']
        
        # Find stations within this ward's area
        for station in stations_data:
            try:
                # Simple distance check - assign station to nearest ward
                station_lat = float(station.get('Latitude', 0))
                station_lon = float(station.get('Longitude', 0))
                
                # Calculate simple distance
                lat_diff = abs(station_lat - ward_center[0])
                lon_diff = abs(station_lon - ward_center[1])
                distance = (lat_diff ** 2 + lon_diff ** 2) ** 0.5
                
                # If within ~0.15 degrees (~15km), assign to ward
                if distance < 0.15:
                    # Get pollutant values
                    aqi_val = int(station.get('AQI', 0))
                    pm25_val = float(station.get('PM25', 0))
                    pm10_val = float(station.get('PM10', 0))
                    
                    # Estimate from AQI if missing
                    if pm25_val == 0 and aqi_val > 0:
                        pm25_val = aqi_val * 0.6
                    if pm10_val == 0 and aqi_val > 0:
                        pm10_val = aqi_val * 0.8
                    
                    ward_stations.append({
                        'station_name': station.get('Station', 'Unknown'),
                        'AQI': aqi_val,
                        'PM25': pm25_val,
                        'PM10': pm10_val
                    })
            except Exception as e:
                continue
        
        if ward_stations:
            pollution_summary = calculate_ward_pollution(ward_stations)
            
            ward_rankings.append({
                'ward_id': ward_id,
                'ward_name': ward_info['name'],
                'avg_aqi': pollution_summary['avg_aqi'],
                'avg_pm25': pollution_summary['avg_pm25'],
                'avg_pm10': pollution_summary['avg_pm10'],
                'max_aqi': pollution_summary['max_aqi'],
                'min_aqi': pollution_summary['min_aqi'],
                'station_count': pollution_summary['station_count'],
                'urgency': get_urgency_level(pollution_summary['avg_aqi'], 0)
            })
    
    # Sort by AQI (worst first)
    ward_rankings.sort(key=lambda x: x['avg_aqi'], reverse=True)
    
    # Add rankings
    for idx, ward in enumerate(ward_rankings, 1):
        ward['rank'] = idx
    
    result = {
        'total_wards': len(ward_rankings),
        'wards': ward_rankings,
        'timestamp': datetime.now().isoformat(),
        'data_source': data_source,
        'cache_status': 'miss'
    }
    
    # Cache for 5 minutes
    cache.set('ward_rankings', result, 300)
    
    return Response(result)


@api_view(['GET'])
def get_ward_health_report(request):
    """
    Get detailed health report for a specific ward
    Uses REAL pollution data from production API
    """
    ward_id = request.GET.get('ward_id')
    
    if not ward_id:
        return Response({'error': 'ward_id parameter required'}, status=400)
    
    try:
        ward_id = int(ward_id)
    except ValueError:
        return Response({'error': 'ward_id must be an integer'}, status=400)
    
    from .ward_data import get_ward_data
    from .ward_utils import calculate_ward_pollution, calculate_health_metrics
    from datetime import datetime
    import requests
    
    wards_data = get_ward_data()
    
    if ward_id not in wards_data:
        return Response({'error': f'Ward {ward_id} not found'}, status=404)
    
    ward_info = wards_data[ward_id]
    
    # Fetch real pollution data from production API
    try:
        response = requests.get('https://apiudyansaathi.azurewebsites.net/api/get-MapData/')
        stations_data = response.json()
    except Exception as e:
        return Response({
            'error': 'Could not fetch station data from production API',
            'ward_name': ward_info['name']
        }, status=500)
    
    # Find stations in this ward
    ward_stations = []
    station_names = []
    ward_center = ward_info['center']
    
    for station in stations_data:
        try:
            station_lat = float(station.get('Latitude', 0))
            station_lon = float(station.get('Longitude', 0))
            
            lat_diff = abs(station_lat - ward_center[0])
            lon_diff = abs(station_lon - ward_center[1])
            distance = (lat_diff ** 2 + lon_diff ** 2) ** 0.5
            
            if distance < 0.15:
                aqi_val = int(station.get('AQI', 0))
                estimated_pm25 = aqi_val * 0.6
                
                ward_stations.append({
                    'station_name': station.get('Station', 'Unknown'),
                    'AQI': aqi_val,
                    'PM25': estimated_pm25,
                    'PM10': estimated_pm25 * 1.5,
                    'timestamp': station.get('Pol_Date', datetime.now().isoformat())
                })
                station_names.append(station.get('Station', 'Unknown'))
        except Exception as e:
            continue
    
    if not ward_stations:
        return Response({
            'error': f'No monitoring stations found in Ward {ward_id}',
            'ward_name': ward_info['name']
        }, status=404)
    
    # Calculate ward pollution
    pollution_summary = calculate_ward_pollution(ward_stations)
    
    # Calculate health metrics
    health_metrics = calculate_health_metrics(pollution_summary['avg_pm25'])
    
    # Get all ward rankings for comparison  
    from django.test import RequestFactory
    factory = RequestFactory()
    rankings_request = factory.get('/api/wards/rankings/')
    rankings_response = get_ward_rankings(rankings_request)
    all_wards = rankings_response.data.get('wards', [])
    
    current_ward = next((w for w in all_wards if w['ward_id'] == ward_id), None)
    best_ward = min(all_wards, key=lambda x: x['avg_aqi']) if all_wards else None
    worst_ward = max(all_wards, key=lambda x: x['avg_aqi']) if all_wards else None
    
    return Response({
        'ward_id': ward_id,
        'ward_name': ward_info['name'],
        'health_metrics': health_metrics,
        'current_pollution': {
            'avg_aqi': pollution_summary['avg_aqi'],
            'avg_pm25': pollution_summary['avg_pm25'],
            'avg_pm10': pollution_summary['avg_pm10'],
            'max_aqi': pollution_summary['max_aqi'],
            'min_aqi': pollution_summary['min_aqi']
        },
        'rankings': {
            'your_rank': current_ward['rank'] if current_ward else None,
            'total_wards': len(all_wards),
            'percentile': round((1 - (current_ward['rank'] / len(all_wards))) * 100, 1) if current_ward else None,
            'urgency': current_ward['urgency'] if current_ward else 'UNKNOWN'
        },
        'comparison': {
            'city_average': round(sum(w['avg_aqi'] for w in all_wards) / len(all_wards), 2),
            'best_ward': {
                'name': best_ward['ward_name'],
                'aqi': best_ward['avg_aqi']
            },
            'worst_ward': {
                'name': worst_ward['ward_name'],
                'aqi': worst_ward['avg_aqi']
            }
        },
        'data_sources': {
            'monitoring_stations': len(station_names),
            'stations': station_names,
            'last_updated': ward_stations[0]['timestamp'] if ward_stations else None,
            'data_type': 'REAL - Live station data'
        },
        'citizen_actions': [
            '🚴 Use public transport or bike to work',
            '🌳 Participate in tree plantation drives',
            '🚫 Report visible polluters: 1800-11-0093',
            '💡 Use air purifiers indoors',
            '😷 Wear N95 masks when AQI > 200'
        ],
        'council_actions': [
            'Last Action: Monitoring ongoing',
            'Pending: Source identification survey',
            'Recommendation: Deploy smog guns if AQI > 300'
        ]
    })


@api_view(['GET'])
def get_ward_map_data(request):
    """
    Get ward boundaries and pollution data for map visualization
    """
    from .ward_data import get_ward_data, create_geojson_feature
    from .ward_utils import map_station_to_ward, calculate_ward_pollution, get_urgency_level
    from .models import StationsCoordinatesModel
    
    wards_data = get_ward_data()
    features = []
    
    all_stations = StationsCoordinatesModel.objects.all()
    
    for ward_id, ward_info in wards_data.items():
        ward_stations = []
        
        for station in all_stations:
            mapped_ward = map_station_to_ward(
                station.Latitude,
                station.Longitude,
                wards_data
            )
            
            if mapped_ward == ward_id:
                try:
                    pollution_data = PollutionDAO.find_PollutionData_By_Station(station.Station)
                    if pollution_data:
                        latest = pollution_data[0]
                        ward_stations.append({
                            'AQI': latest.AQI,
                            'PM25': latest.PM25,
                            'PM10': latest.PM10
                        })
                except:
                    continue
        
        pollution_summary = calculate_ward_pollution(ward_stations) if ward_stations else None
        
        feature = create_geojson_feature(ward_id, ward_info)
        
        if pollution_summary:
            feature['properties'].update({
                'avg_aqi': pollution_summary['avg_aqi'],
                'avg_pm25': pollution_summary['avg_pm25'],
                'urgency': get_urgency_level(pollution_summary['avg_aqi'], 0),
                'station_count': len(ward_stations)
            })
        else:
            feature['properties'].update({
                'avg_aqi': None,
                'avg_pm25': None,
                'urgency': 'NO_DATA',
                'station_count': 0
            })
        
        features.append(feature)
    
    return Response({
        'type': 'FeatureCollection',
        'features': features
    })


# ==================== DELHI OFFICIAL WARD SYSTEM (40 WARDS - REAL-TIME DATA) ====================

@api_view(['GET'])
def get_delhi_ward_list(request):
    """
    Get complete list of all 40 official Delhi wards with metadata
    Real-time data from production monitoring stations
    """
    from .delhi_ward_boundaries import (
        DELHI_WARDS_OFFICIAL,
        DELHI_ZONES,
        get_all_delhi_wards
    )
    
    wards = []
    for ward_id, ward in DELHI_WARDS_OFFICIAL.items():
        wards.append({
            "ward_id": ward_id,
            "name": ward["name"],
            "zone": ward["zone"],
            "zone_info": DELHI_ZONES.get(ward["zone"], {}).get("description", ""),
            "corporation": ward["corporation"],
            "type": ward["type"],
            "population_2024": ward.get("population_2024_est", 0),
            "area_km2": ward.get("area_km2", 0),
            "center": ward["center"],
            "is_hotspot": ward.get("pollution_hotspot", False),
            "metro_stations": ward.get("metro_stations", []),
            "industrial_areas": ward.get("industrial_areas", [])
        })
    
    # Group by zone
    zones_summary = {}
    for ward in wards:
        zone = ward["zone"]
        if zone not in zones_summary:
            zones_summary[zone] = {
                "name": DELHI_ZONES.get(zone, {}).get("name", zone),
                "ward_count": 0,
                "total_population": 0
            }
        zones_summary[zone]["ward_count"] += 1
        zones_summary[zone]["total_population"] += ward["population_2024"]
    
    return Response({
        "total_wards": len(wards),
        "total_zones": len(zones_summary),
        "zones": zones_summary,
        "wards": wards,
        "data_source": "official_delhi_boundaries"
    })


@api_view(['GET'])
def get_delhi_ward_pollution(request):
    """
    Get real-time pollution data for a specific Delhi ward
    Maps monitoring stations to ward and calculates aggregates
    """
    ward_id = request.GET.get('ward_id')
    
    if not ward_id:
        return Response({'error': 'ward_id parameter required'}, status=400)
    
    try:
        ward_id = int(ward_id)
    except ValueError:
        return Response({'error': 'ward_id must be an integer'}, status=400)
    
    from .realtime_ward_system import RealTimeWardPollutionSystem
    
    result = RealTimeWardPollutionSystem.get_ward_realtime_pollution(ward_id)
    
    if "error" in result:
        return Response(result, status=404)
    
    return Response(result)


@api_view(['GET'])
def get_delhi_all_wards_pollution(request):
    """
    Get real-time pollution for ALL Delhi wards ranked by severity
    Complete dashboard-ready data with zone summaries
    """
    from .realtime_ward_system import RealTimeWardPollutionSystem
    
    result = RealTimeWardPollutionSystem.get_all_wards_ranked()
    return Response(result)


@api_view(['GET'])
def get_delhi_zones_summary(request):
    """
    Get pollution summary grouped by Delhi zones
    Useful for zone-level policy decisions
    """
    from .realtime_ward_system import RealTimeWardPollutionSystem
    
    all_wards_data = RealTimeWardPollutionSystem.get_all_wards_ranked()
    
    return Response({
        "total_zones": len(all_wards_data.get("zones_summary", [])),
        "zones": all_wards_data.get("zones_summary", []),
        "summary": all_wards_data.get("summary", {}),
        "timestamp": all_wards_data.get("timestamp", ""),
        "data_source": "real_time_production"
    })


@api_view(['GET'])
def get_delhi_hotspots(request):
    """
    Get all pollution hotspot wards in Delhi
    Critical for targeted intervention planning
    """
    from .delhi_ward_boundaries import get_pollution_hotspot_wards, get_industrial_wards
    from .realtime_ward_system import RealTimeWardPollutionSystem
    
    # Get static hotspots (known industrial/high pollution areas)
    static_hotspots = get_pollution_hotspot_wards()
    industrial_wards = get_industrial_wards()
    
    # Get real-time data
    all_wards_data = RealTimeWardPollutionSystem.get_all_wards_ranked()
    
    # Find current hotspots (AQI > 200)
    current_hotspots = [
        w for w in all_wards_data.get("wards", [])
        if w.get("avg_aqi", 0) > 200
    ]
    
    return Response({
        "static_hotspots": [
            {"ward_id": w_id, "name": w["name"], "type": w["type"]}
            for w_id, w in static_hotspots.items()
        ],
        "industrial_wards": [
            {"ward_id": w_id, "name": w["name"], "industrial_areas": w.get("industrial_areas", [])}
            for w_id, w in industrial_wards.items()
        ],
        "current_hotspots": current_hotspots[:10],  # Top 10 current worst
        "total_high_pollution_wards": len(current_hotspots),
        "population_affected": sum(w.get("population", 0) for w in current_hotspots),
        "timestamp": all_wards_data.get("timestamp", ""),
        "data_source": "real_time_production"
    })


@api_view(['GET'])
def get_delhi_ward_geojson(request):
    """
    Get GeoJSON data for all Delhi wards with real-time pollution
    For map visualization with ward boundaries
    """
    from .delhi_ward_boundaries import DELHI_WARDS_OFFICIAL
    from .realtime_ward_system import RealTimeWardPollutionSystem
    
    all_wards_data = RealTimeWardPollutionSystem.get_all_wards_ranked()
    wards_pollution = {w["ward_id"]: w for w in all_wards_data.get("wards", [])}
    
    features = []
    
    for ward_id, ward in DELHI_WARDS_OFFICIAL.items():
        pollution = wards_pollution.get(ward_id, {})
        
        feature = {
            "type": "Feature",
            "properties": {
                "ward_id": ward_id,
                "name": ward["name"],
                "zone": ward["zone"],
                "corporation": ward["corporation"],
                "type": ward["type"],
                "population": ward.get("population_2024_est", 0),
                "aqi": pollution.get("avg_aqi", 0),
                "pm25": pollution.get("avg_pm25", 0),
                "urgency": pollution.get("urgency", "NO_DATA"),
                "aqi_category": pollution.get("aqi_category", "Unknown"),
                "aqi_color": pollution.get("aqi_color", "#888888"),
                "is_hotspot": ward.get("pollution_hotspot", False)
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [ward.get("boundary", [])]
            }
        }
        features.append(feature)
    
    return Response({
        "type": "FeatureCollection",
        "features": features,
        "timestamp": all_wards_data.get("timestamp", ""),
        "crs": {
            "type": "name",
            "properties": {"name": "urn:ogc:def:crs:EPSG::4326"}
        }
    })


@api_view(['GET'])
def get_delhi_health_report(request):
    """
    Get comprehensive health impact report for a Delhi ward
    Uses WHO methodology for health impact calculation
    """
    ward_id = request.GET.get('ward_id')
    
    if not ward_id:
        return Response({'error': 'ward_id parameter required'}, status=400)
    
    try:
        ward_id = int(ward_id)
    except ValueError:
        return Response({'error': 'ward_id must be an integer'}, status=400)
    
    from .realtime_ward_system import RealTimeWardPollutionSystem
    from .delhi_ward_boundaries import get_pollution_sources_for_ward
    
    # Get ward pollution data
    ward_data = RealTimeWardPollutionSystem.get_ward_realtime_pollution(ward_id)
    
    if "error" in ward_data:
        return Response(ward_data, status=404)
    
    # Get all wards for comparison
    all_wards = RealTimeWardPollutionSystem.get_all_wards_ranked()
    
    # Find current ward rank
    current_rank = None
    for w in all_wards.get("wards", []):
        if w["ward_id"] == ward_id:
            current_rank = w.get("rank", None)
            break
    
    # Calculate Delhi-wide average
    delhi_avg_aqi = all_wards.get("summary", {}).get("avg_delhi_aqi", 0)
    
    return Response({
        "ward_id": ward_id,
        "ward_name": ward_data.get("ward_name", ""),
        "zone": ward_data.get("zone", ""),
        "corporation": ward_data.get("corporation", ""),
        
        "current_pollution": ward_data.get("realtime_pollution", {}),
        "health_impact": ward_data.get("health_impact", {}),
        "pollution_sources": ward_data.get("pollution_sources", {}),
        
        "rankings": {
            "current_rank": current_rank,
            "total_wards": all_wards.get("total_wards", 0),
            "percentile": round((1 - (current_rank / all_wards.get("total_wards", 40))) * 100, 1) if current_rank else None,
            "comparison_to_delhi_avg": {
                "delhi_avg_aqi": delhi_avg_aqi,
                "ward_aqi": ward_data.get("realtime_pollution", {}).get("aqi", 0),
                "difference": round(ward_data.get("realtime_pollution", {}).get("aqi", 0) - delhi_avg_aqi, 1)
            }
        },
        
        "ward_details": ward_data.get("ward_info", {}),
        "monitoring_stations": ward_data.get("monitoring_stations", {}),
        
        "citizen_actions": [
            "🚴 Use public transport or cycle instead of personal vehicles",
            "🌳 Participate in tree plantation drives in your area",
            "🚫 Report visible polluters to Delhi Pollution Control: 1800-11-0093",
            "💨 Use HEPA air purifiers indoors on high AQI days",
            "😷 Wear N95 masks when going outdoors if AQI > 200",
            "🌾 Report stubble burning to authorities",
            "🍃 Keep indoor plants like snake plant, aloe vera for air purification"
        ],
        
        "council_recommendations": [
            f"Priority Level: {ward_data.get('realtime_pollution', {}).get('urgency', 'UNKNOWN')}",
            "Deploy anti-smog guns if AQI > 300",
            "Increase road water sprinkling frequency",
            "Strict enforcement on construction dust control",
            "Promote EV adoption with charging infrastructure"
        ],
        
        "timestamp": ward_data.get("timestamp", ""),
        "data_source": "real_time_production"
    })


# ==================== WARD POLICY SIMULATOR (What-If Analysis) ====================

@api_view(['GET'])
def get_available_policies(request):
    """
    GET /api/policy/available/
    
    Returns list of all available policies that can be simulated
    """
    from .ward_policy_simulator import WardPolicySimulator
    
    policies = WardPolicySimulator.get_available_policies()
    
    return Response({
        "total_policies": len(policies),
        "policies": policies,
        "usage": "Use these policy IDs with /api/policy/simulate/ endpoint"
    })


@api_view(['GET'])
def analyze_ward_for_policy(request):
    """
    GET /api/policy/analyze/?ward_id=20&pm25=185
    
    Analyze a ward's pollution sources and get recommended policies
    """
    from .ward_policy_simulator import WardPolicySimulator
    
    ward_id = request.GET.get('ward_id')
    pm25 = request.GET.get('pm25')
    
    if not ward_id or not pm25:
        return Response({
            "error": "Both ward_id and pm25 parameters are required",
            "example": "/api/policy/analyze/?ward_id=20&pm25=185"
        }, status=400)
    
    try:
        ward_id = int(ward_id)
        pm25 = float(pm25)
    except ValueError:
        return Response({"error": "ward_id must be integer, pm25 must be number"}, status=400)
    
    result = WardPolicySimulator.analyze_ward_pollution(ward_id, pm25)
    
    if "error" in result:
        return Response(result, status=404)
    
    return Response(result)


@api_view(['POST'])
def simulate_single_policy(request):
    """
    POST /api/policy/simulate/
    
    Simulate a single policy's impact on a ward
    
    Request Body:
    {
        "ward_id": 20,
        "current_pm25": 185,
        "policy_type": "construction_ban",
        "policy_params": {"days": 3}
    }
    
    Available policy_types:
    - construction_ban: {"days": 1-7}
    - odd_even: {"enabled": true}
    - industrial_shutdown: {"capacity_reduction_pct": 10-100}
    - dust_control: {"road_km": 5-50}
    - traffic_rerouting: {"enabled": true}
    - smog_tower: {"units": 1-5}
    - green_barrier: {}
    - public_transport_boost: {}
    """
    from .ward_policy_simulator import WardPolicySimulator
    
    ward_id = request.data.get('ward_id')
    current_pm25 = request.data.get('current_pm25')
    policy_type = request.data.get('policy_type')
    policy_params = request.data.get('policy_params', {})
    
    if not all([ward_id, current_pm25, policy_type]):
        return Response({
            "error": "ward_id, current_pm25, and policy_type are required",
            "example": {
                "ward_id": 20,
                "current_pm25": 185,
                "policy_type": "construction_ban",
                "policy_params": {"days": 3}
            }
        }, status=400)
    
    try:
        ward_id = int(ward_id)
        current_pm25 = float(current_pm25)
    except ValueError:
        return Response({"error": "Invalid numeric values"}, status=400)
    
    result = WardPolicySimulator.simulate_policy(
        ward_id,
        current_pm25,
        policy_type,
        policy_params
    )
    
    if "error" in result:
        return Response(result, status=400)
    
    return Response(result)


@api_view(['POST'])
def simulate_multiple_policies(request):
    """
    POST /api/policy/simulate-multiple/
    
    Simulate multiple policies together with diminishing returns
    
    Request Body:
    {
        "ward_id": 20,
        "current_pm25": 185,
        "policies": [
            {"type": "construction_ban", "params": {"days": 3}},
            {"type": "dust_control", "params": {"road_km": 15}},
            {"type": "traffic_rerouting", "params": {"enabled": true}}
        ]
    }
    """
    from .ward_policy_simulator import WardPolicySimulator
    
    ward_id = request.data.get('ward_id')
    current_pm25 = request.data.get('current_pm25')
    policies = request.data.get('policies', [])
    
    if not all([ward_id, current_pm25]) or not policies:
        return Response({
            "error": "ward_id, current_pm25, and policies array are required",
            "example": {
                "ward_id": 20,
                "current_pm25": 185,
                "policies": [
                    {"type": "construction_ban", "params": {"days": 3}},
                    {"type": "odd_even", "params": {"enabled": True}}
                ]
            }
        }, status=400)
    
    try:
        ward_id = int(ward_id)
        current_pm25 = float(current_pm25)
    except ValueError:
        return Response({"error": "Invalid numeric values"}, status=400)
    
    result = WardPolicySimulator.simulate_multiple_policies(
        ward_id,
        current_pm25,
        policies
    )
    
    if "error" in result:
        return Response(result, status=400)
    
    return Response(result)


@api_view(['GET'])
def get_ai_policy_recommendation(request):
    """
    GET /api/policy/ai-recommend/?ward_id=20&pm25=185&budget=500
    
    Get AI-powered policy recommendation for a ward
    
    Parameters:
    - ward_id: Ward ID (1-40)
    - pm25: Current PM2.5 level
    - budget: (Optional) Budget constraint in lakhs
    """
    from .ward_policy_simulator import WardPolicySimulator
    
    ward_id = request.GET.get('ward_id')
    pm25 = request.GET.get('pm25')
    budget = request.GET.get('budget')
    
    if not ward_id or not pm25:
        return Response({
            "error": "ward_id and pm25 parameters are required",
            "example": "/api/policy/ai-recommend/?ward_id=20&pm25=185&budget=500"
        }, status=400)
    
    try:
        ward_id = int(ward_id)
        pm25 = float(pm25)
        budget = float(budget) if budget else None
    except ValueError:
        return Response({"error": "Invalid numeric values"}, status=400)
    
    result = WardPolicySimulator.get_ai_recommendation(ward_id, pm25, budget)
    
    if "error" in result:
        return Response(result, status=404)
    
    return Response(result)


@api_view(['GET'])
def get_ward_with_realtime_for_simulation(request):
    """
    GET /api/policy/ward-realtime/?ward_id=20
    
    Get real-time pollution data for a ward ready for simulation
    Combines current pollution with analysis
    """
    from .realtime_ward_system import RealTimeWardPollutionSystem
    from .ward_policy_simulator import WardPolicySimulator
    
    ward_id = request.GET.get('ward_id')
    
    if not ward_id:
        return Response({"error": "ward_id parameter required"}, status=400)
    
    try:
        ward_id = int(ward_id)
    except ValueError:
        return Response({"error": "ward_id must be integer"}, status=400)
    
    # Get real-time pollution
    realtime_data = RealTimeWardPollutionSystem.get_ward_realtime_pollution(ward_id)
    
    if "error" in realtime_data:
        return Response(realtime_data, status=404)
    
    # Get current PM2.5
    current_pm25 = realtime_data.get("realtime_pollution", {}).get("pm25", 0)
    
    if current_pm25 == 0:
        # Estimate from AQI if PM2.5 not available
        current_aqi = realtime_data.get("realtime_pollution", {}).get("aqi", 0)
        current_pm25 = current_aqi * 0.6  # Rough estimation
    
    # Analyze pollution sources
    analysis = WardPolicySimulator.analyze_ward_pollution(ward_id, current_pm25)
    
    return Response({
        "ward_id": ward_id,
        "ward_name": realtime_data.get("ward_name"),
        "zone": realtime_data.get("zone"),
        "ward_type": realtime_data.get("type"),
        
        "current_pollution": {
            "aqi": realtime_data.get("realtime_pollution", {}).get("aqi"),
            "pm25": round(current_pm25, 1),
            "pm10": realtime_data.get("realtime_pollution", {}).get("pm10"),
            "category": realtime_data.get("realtime_pollution", {}).get("category"),
            "urgency": realtime_data.get("realtime_pollution", {}).get("urgency")
        },
        
        "pollution_analysis": {
            "source_breakdown": analysis.get("source_breakdown", {}),
            "top_sources": analysis.get("top_sources", []),
            "recommended_policies": analysis.get("recommended_policies", [])
        },
        
        "ward_info": realtime_data.get("ward_info", {}),
        "monitoring_stations": realtime_data.get("monitoring_stations", {}),
        
        "simulator_ready": {
            "ward_id": ward_id,
            "current_pm25": round(current_pm25, 1),
            "use_with": "/api/policy/simulate/ or /api/policy/ai-recommend/"
        },
        
        "timestamp": realtime_data.get("timestamp"),
        "data_source": "real_time_production"
    })


# ==================== ALL 272 DELHI WARDS SYSTEM ====================

@api_view(['GET'])
def get_all_272_wards_summary(request):
    """
    Get summary of all 272 Delhi Municipal Corporation wards
    40 monitored + 232 estimated
    """
    from .all_wards_generator import get_wards_summary
    
    summary = get_wards_summary()
    
    return Response({
        "status": "success",
        "data": summary,
        "message": "Complete Delhi ward coverage: 272 total wards"
    })


@api_view(['GET'])
def get_all_272_wards_pollution(request):
    """
    Get pollution data for all 272 wards
    - 40 wards with real monitoring station data
    - 232 wards with interpolated/estimated data
    """
    try:
        from .all_wards_generator import (
            get_all_272_wards,
            find_nearest_monitored_ward
        )
    except ImportError as e:
        return Response({
            "status": "error",
            "message": f"Import error: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    try:
        all_wards = get_all_272_wards()
        wards_with_pollution = []
        
        for ward_id, ward_data in all_wards.items():
            ward_info = {
                "ward_id": ward_id,
                "ward_number": ward_data['ward_number'],
                "ward_name": ward_data['ward_name'],
                "zone": ward_data['zone'],
                "corporation": ward_data['corporation'],
                "centroid": ward_data['centroid'],
                "has_real_data": ward_data.get('has_monitoring_station', False)
            }
            
            if ward_data.get('has_monitoring_station'):
                # Get real data from monitoring station
                station_name = ward_data.get('station')
                try:
                    pollution_data = PollutionDAO.find_PollutionData_By_Station(station_name)
                    if pollution_data and len(pollution_data) > 0:
                        latest = pollution_data[0]
                        ward_info.update({
                            "aqi": latest.AQI,
                            "pm25": latest.PM25,
                            "pm10": latest.PM10,
                            "no2": latest.NO2,
                            "so2": latest.SO2,
                            "co": latest.CO,
                            "ozone": latest.OZONE,
                            "category": get_aqi_category(latest.AQI),
                            "station_name": station_name,
                            "data_source": "real_time_cpcb",
                            "last_updated": str(latest.pol_date) if hasattr(latest, 'pol_date') else None
                        })
                    else:
                        # No data available - use defaults
                        ward_info.update({
                            "aqi": 150,
                            "pm25": 75,
                            "pm10": 100,
                            "no2": 40,
                            "so2": 15,
                            "co": 1.5,
                            "ozone": 45,
                            "category": "Moderate",
                            "data_source": "no_data",
                            "station_name": station_name
                        })
                except Exception as e:
                    print(f"Error fetching data for {station_name}: {e}")
                    ward_info.update({
                        "aqi": 150,
                        "pm25": 75,
                        "pm10": 100,
                        "no2": 40,
                        "so2": 15,
                        "co": 1.5,
                        "ozone": 45,
                        "category": "Moderate",
                        "data_source": "error"
                    })
            else:
                # Estimate pollution from nearest monitored ward
                centroid = ward_data['centroid']
                nearest_ward, distance = find_nearest_monitored_ward(centroid[0], centroid[1])
                
                if nearest_ward:
                    station_name = nearest_ward[1].get('station')
                    
                    try:
                        # Get pollution from nearest station
                        pollution_data = PollutionDAO.find_PollutionData_By_Station(station_name)
                        if pollution_data and len(pollution_data) > 0:
                            latest = pollution_data[0]
                            
                            # Apply distance-based adjustment
                            # Farther wards get slightly degraded interpolation
                            uncertainty = 1 + (distance / 20)  # 20km = max uncertainty
                            
                            estimated_aqi = min(500, int(latest.AQI * uncertainty * (0.95 + random.random() * 0.1)))
                            estimated_pm25 = min(500, int(latest.PM25 * uncertainty * (0.95 + random.random() * 0.1)))
                            
                            ward_info.update({
                                "aqi": estimated_aqi,
                                "pm25": estimated_pm25,
                                "pm10": min(500, int(latest.PM10 * uncertainty)),
                                "no2": min(500, int(latest.NO2 * uncertainty)) if hasattr(latest, 'NO2') and latest.NO2 else 40,
                                "so2": min(500, int(latest.SO2 * uncertainty)) if hasattr(latest, 'SO2') and latest.SO2 else 15,
                                "co": round(latest.CO * uncertainty, 2) if hasattr(latest, 'CO') and latest.CO else 1.5,
                                "ozone": min(300, int(latest.OZONE * uncertainty)) if hasattr(latest, 'OZONE') and latest.OZONE else 45,
                                "category": get_aqi_category(estimated_aqi),
                                "data_source": "interpolated",
                                "nearest_station": station_name,
                                "distance_to_station_km": round(distance, 2),
                                "uncertainty_factor": round(uncertainty, 2)
                            })
                        else:
                            # Default estimate
                            ward_info.update({
                                "aqi": 150,
                                "pm25": 75,
                                "pm10": 100,
                                "no2": 40,
                                "so2": 15,
                                "co": 1.5,
                                "ozone": 45,
                                "category": "Moderate",
                                "data_source": "default_estimate"
                            })
                    except Exception as e:
                        print(f"Error interpolating for {ward_id}: {e}")
                        ward_info.update({
                            "aqi": 150,
                            "pm25": 75,
                            "pm10": 100,
                            "no2": 40,
                            "so2": 15,
                            "co": 1.5,
                            "ozone": 45,
                            "category": "Moderate",
                            "data_source": "fallback"
                        })
                else:
                    # No nearest ward found
                    ward_info.update({
                        "aqi": 150,
                        "pm25": 75,
                        "pm10": 100,
                        "no2": 40,
                        "so2": 15,
                        "co": 1.5,
                        "ozone": 45,
                        "category": "Moderate",
                        "data_source": "no_reference"
                    })
            
            wards_with_pollution.append(ward_info)
        
        # Sort by AQI (worst first)
        wards_with_pollution.sort(key=lambda x: x.get('aqi', 0), reverse=True)
        
        # Add rank, urgency, and other display fields
        for rank, ward in enumerate(wards_with_pollution, 1):
            ward['rank'] = rank
            ward['avg_aqi'] = ward.get('aqi', 150)
            ward['avg_pm25'] = ward.get('pm25', 75)
            ward['avg_pm10'] = ward.get('pm10', 100)
            ward['station_count'] = 1 if ward.get('has_real_data') else 0
            ward['population'] = all_wards.get(ward['ward_id'], {}).get('population', 30000)
            ward['is_hotspot'] = ward.get('aqi', 0) > 300
            
            # Set urgency level
            aqi = ward.get('aqi', 0)
            if aqi > 400:
                ward['urgency'] = 'CRITICAL'
            elif aqi > 300:
                ward['urgency'] = 'SEVERE'
            elif aqi > 200:
                ward['urgency'] = 'POOR'
            elif aqi > 100:
                ward['urgency'] = 'MODERATE'
            else:
                ward['urgency'] = 'GOOD'
            
            # Add type field
            ward['type'] = 'Monitored' if ward.get('has_real_data') else 'Estimated'
        
        # Calculate statistics
        real_data_count = len([w for w in wards_with_pollution if w['has_real_data']])
        estimated_count = len(wards_with_pollution) - real_data_count
        avg_aqi = sum(w.get('aqi', 0) for w in wards_with_pollution) / len(wards_with_pollution)
        
        return Response({
            "status": "success",
            "data": {
                "wards": wards_with_pollution,
                "total_wards": len(wards_with_pollution),
                "monitored_wards": real_data_count,
                "estimated_wards": estimated_count,
                "coverage_percentage": round((real_data_count / len(wards_with_pollution)) * 100, 2),
                "average_aqi": round(avg_aqi, 1),
                "timestamp": datetime.now().isoformat()
            }
        })
        
    except Exception as e:
        import traceback
        return Response({
            "status": "error",
            "message": str(e),
            "traceback": traceback.format_exc()
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def get_aqi_category(aqi):
    """Helper function to categorize AQI"""
    if aqi <= 50:
        return "Good"
    elif aqi <= 100:
        return "Satisfactory"
    elif aqi <= 200:
        return "Moderate"
    elif aqi <= 300:
        return "Poor"
    elif aqi <= 400:
        return "Very Poor"
    else:
        return "Severe"

