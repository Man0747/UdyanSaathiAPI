from django.urls import path
from . import views

# # ONLY FOR DEBUG 
# #**************START*********************
# from .DBOPS import PollutionDAO
# from .serializer import *
# # pollutiondata = PollutionDAO.get_pollution_by_date_station("Knowledge Park - III, Greater Noida - UPPCB")
# Mldata =  PollutionDAO.get_mldata("Knowledge Park - III, Greater Noida - UPPCB")
# serializer = MlSerializer(Mldata, many=True)
# # serializer = MlSerializer(pollutiondata, many=True)


# #*************END**********************

urlpatterns = [
    path('get-pollution-by-date-station/', views.get_PollutionData_By_Station, name="routes"),
    path('get-stations/', views.get_Stations_By_City, name="routes"),
    path('get-Top10Cities/', views.get_Top6_Most_Polluted_Cities, name="routes"),
    path('get-Top10LeastPollutedCities/', views.get_Top6_Least_Polluted_Cities, name="routes"),
    path('get-GraphData/', views.get_GraphData, name="routes"),
    path('get-MetroCityData/', views.get_MetroCities_Data, name="routes"),
    path('get-AqiCalData/', views.get_Aqi_Calendar_Data, name="routes"),
    path('get-MLData/', views.get_ML_Data, name="routes"),
    path('get-MapData/', views.get_Map_Data, name="routes"),
    path('get-allStations/', views.get_All_Stations, name="routes"),
    path('get-stations_coordinates/', views.get_Stations_Coordinates, name="routes"),
    path('health/', views.get_HealthOfApi, name="routes"),
    
    # Dispatch System
    path('dispatch/initialize-demo/', views.initialize_dispatch_demo, name='init_dispatch'),
    path('dispatch/fleet-status/', views.get_fleet_status, name='fleet_status'),
    path('dispatch/active-missions/', views.get_active_missions, name='active_missions'),
    path('dispatch/stats/', views.get_intervention_stats, name='intervention_stats'),
    path('dispatch/dashboard-summary/', views.get_dispatch_dashboard_summary, name='dashboard_summary'),
    
    # Ward-based Pollution Analysis (REAL DATA - Legacy 10 Wards)
    path('wards/rankings/', views.get_ward_rankings, name='ward_rankings'),
    path('ward/health/', views.get_ward_health_report, name='ward_health'),
    path('wards/map-data/', views.get_ward_map_data, name='ward_map'),
    
    # ===== DELHI OFFICIAL WARD SYSTEM (40 WARDS - REAL-TIME) =====
    # Complete list of all 40 Delhi wards with metadata
    path('delhi/wards/', views.get_delhi_ward_list, name='delhi_ward_list'),
    
    # Real-time pollution for specific ward
    path('delhi/ward/pollution/', views.get_delhi_ward_pollution, name='delhi_ward_pollution'),
    
    # All wards ranked by pollution (dashboard view)
    path('delhi/wards/pollution/', views.get_delhi_all_wards_pollution, name='delhi_all_wards_pollution'),
    
    # Zone-wise pollution summary
    path('delhi/zones/', views.get_delhi_zones_summary, name='delhi_zones'),
    
    # Pollution hotspots (critical areas)
    path('delhi/hotspots/', views.get_delhi_hotspots, name='delhi_hotspots'),
    
    # GeoJSON for map visualization with ward boundaries
    path('delhi/wards/geojson/', views.get_delhi_ward_geojson, name='delhi_geojson'),
    
    # Comprehensive health report for a ward
    path('delhi/ward/health/', views.get_delhi_health_report, name='delhi_health'),
    
    # ===== WARD POLICY SIMULATOR (What-If Analysis) =====
    # List all available policies
    path('policy/available/', views.get_available_policies, name='policy_available'),
    
    # Analyze ward pollution sources and get policy recommendations
    path('policy/analyze/', views.analyze_ward_for_policy, name='policy_analyze'),
    
    # Simulate single policy impact
    path('policy/simulate/', views.simulate_single_policy, name='policy_simulate'),
    
    # Simulate multiple policies together
    path('policy/simulate-multiple/', views.simulate_multiple_policies, name='policy_simulate_multiple'),
    
    # AI-powered policy recommendation
    path('policy/ai-recommend/', views.get_ai_policy_recommendation, name='policy_ai_recommend'),
    
    # Get ward with real-time data ready for simulation
    path('policy/ward-realtime/', views.get_ward_with_realtime_for_simulation, name='policy_ward_realtime'),
    
    # ===== ALL 272 DELHI WARDS SYSTEM (COMPLETE COVERAGE) =====
    # Summary of all 272 wards (40 monitored + 232 estimated)
    path('delhi/all-wards/summary/', views.get_all_272_wards_summary, name='all_272_summary'),
    
    # Complete pollution data for all 272 wards
    path('delhi/all-wards/pollution/', views.get_all_272_wards_pollution, name='all_272_pollution'),
]
