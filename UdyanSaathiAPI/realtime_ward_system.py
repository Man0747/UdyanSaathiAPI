"""
Real-Time Delhi Ward Pollution System
Integrates official Delhi ward boundaries with LIVE pollution data from production database

This system:
1. Maps monitoring stations to official Delhi wards
2. Aggregates real-time pollution data per ward
3. Calculates health impacts using WHO methodology
4. Provides zone-wise and corporation-wise summaries
"""

import requests
from datetime import datetime
from math import sqrt
from django.core.cache import cache

from .delhi_ward_boundaries import (
    DELHI_WARDS_OFFICIAL,
    DELHI_ZONES,
    WARD_TYPE_POLLUTION_SOURCES,
    get_ward_by_id,
    get_pollution_sources_for_ward,
    get_all_delhi_wards,
    haversine_distance,
    find_nearest_ward
)


class RealTimeWardPollutionSystem:
    """
    Production-grade system for real-time ward pollution data
    Uses actual monitoring station data mapped to official ward boundaries
    """
    
    PRODUCTION_API = "https://apiudyansaathi.azurewebsites.net/api"
    CACHE_TIMEOUT = 300  # 5 minutes
    
    @classmethod
    def get_all_stations_realtime(cls):
        """
        Fetch real-time data from ALL Delhi monitoring stations
        Uses production API with caching
        """
        cache_key = "delhi_all_stations_realtime"
        cached = cache.get(cache_key)
        
        if cached:
            return cached
        
        try:
            # Try production API
            response = requests.get(f"{cls.PRODUCTION_API}/get-MapData/", timeout=10)
            
            if response.status_code == 200:
                stations = response.json()
                cache.set(cache_key, stations, cls.CACHE_TIMEOUT)
                return stations
        except Exception as api_error:
            print(f"API error: {api_error}")
        
        # Fallback to production database
        try:
            from .models import StationsCoordinatesModel, pollutionModel
            from django.db.models import Max
            
            stations = StationsCoordinatesModel.objects.using('production').all()
            latest_date = pollutionModel.objects.using('production').aggregate(
                max_date=Max('Pol_Date')
            )['max_date']
            
            if latest_date:
                pollution = pollutionModel.objects.using('production').filter(
                    Pol_Date=latest_date
                )
                
                pollution_dict = {p.pol_Station: p for p in pollution}
                
                result = []
                for station in stations:
                    pol = pollution_dict.get(station.Station)
                    result.append({
                        "Station": station.Station,
                        "Latitude": float(station.Latitude),
                        "Longitude": float(station.Longitude),
                        "AQI": pol.AQI if pol else 0,
                        "PM25": pol.PM25 if pol else 0,
                        "PM10": pol.PM10 if pol else 0,
                    })
                
                cache.set(cache_key, result, cls.CACHE_TIMEOUT)
                return result
                
        except Exception as db_error:
            print(f"Database error: {db_error}")
        
        return []
    
    @classmethod
    def map_stations_to_wards(cls):
        """
        Map all monitoring stations to their nearest wards
        Returns dict: {ward_id: [list of stations]}
        """
        stations = cls.get_all_stations_realtime()
        ward_station_map = {ward_id: [] for ward_id in DELHI_WARDS_OFFICIAL.keys()}
        
        for station in stations:
            lat = station.get("Latitude", 0)
            lon = station.get("Longitude", 0)
            
            if lat == 0 or lon == 0:
                continue
            
            # Find nearest ward
            nearest_ward_id, distance = find_nearest_ward(lat, lon)
            
            if nearest_ward_id and distance <= 10:  # Within 10km
                ward_station_map[nearest_ward_id].append({
                    **station,
                    "distance_km": round(distance, 2)
                })
        
        return ward_station_map
    
    @classmethod
    def get_ward_realtime_pollution(cls, ward_id):
        """
        Get real-time pollution data for a specific Delhi ward
        """
        ward = get_ward_by_id(ward_id)
        if not ward:
            return {"error": f"Ward {ward_id} not found"}
        
        ward_center = ward["center"]
        ward_radius_km = sqrt(ward.get("area_km2", 4)) * 1.5
        
        # Get all stations
        stations = cls.get_all_stations_realtime()
        stations_in_ward = []
        
        for station in stations:
            lat = station.get("Latitude", 0)
            lon = station.get("Longitude", 0)
            
            if lat == 0 or lon == 0:
                continue
            
            distance = haversine_distance(ward_center[0], ward_center[1], lat, lon)
            
            if distance <= ward_radius_km:
                stations_in_ward.append({
                    **station,
                    "distance_km": round(distance, 2)
                })
        
        # If no stations in ward, get nearest 3 stations
        if not stations_in_ward:
            all_with_distance = []
            for station in stations:
                lat = station.get("Latitude", 0)
                lon = station.get("Longitude", 0)
                if lat != 0 and lon != 0:
                    distance = haversine_distance(ward_center[0], ward_center[1], lat, lon)
                    all_with_distance.append({**station, "distance_km": round(distance, 2)})
            
            all_with_distance.sort(key=lambda x: x["distance_km"])
            stations_in_ward = all_with_distance[:3]  # Nearest 3
        
        if not stations_in_ward:
            return {
                "ward_id": ward_id,
                "ward_name": ward["name"],
                "error": "No monitoring stations available"
            }
        
        # Calculate ward-level aggregates
        avg_aqi = sum([s.get("AQI", 0) for s in stations_in_ward]) / len(stations_in_ward)
        avg_pm25 = sum([s.get("PM25", 0) or s.get("AQI", 0) * 0.6 for s in stations_in_ward]) / len(stations_in_ward)
        avg_pm10 = sum([s.get("PM10", 0) or s.get("AQI", 0) * 0.8 for s in stations_in_ward]) / len(stations_in_ward)
        
        # Get pollution sources
        pollution_sources = get_pollution_sources_for_ward(ward_id)
        
        # Determine AQI category
        aqi_category = cls.get_aqi_category(avg_aqi)
        
        # Calculate health impact
        health_impact = cls.calculate_health_impact(avg_pm25, ward.get("population_2024_est", 50000))
        
        return {
            "ward_id": ward_id,
            "ward_name": ward["name"],
            "zone": ward["zone"],
            "corporation": ward["corporation"],
            "type": ward["type"],
            
            "realtime_pollution": {
                "aqi": round(avg_aqi, 1),
                "pm25": round(avg_pm25, 1),
                "pm10": round(avg_pm10, 1),
                "category": aqi_category["category"],
                "color": aqi_category["color"],
                "urgency": cls.get_urgency_level(avg_aqi)
            },
            
            "monitoring_stations": {
                "count": len(stations_in_ward),
                "stations": [
                    {
                        "name": s["Station"],
                        "aqi": s.get("AQI", 0),
                        "distance_km": s.get("distance_km", 0)
                    }
                    for s in stations_in_ward
                ]
            },
            
            "pollution_sources": {
                source: f"{contribution*100:.1f}%"
                for source, contribution in sorted(
                    pollution_sources.items(),
                    key=lambda x: x[1],
                    reverse=True
                )
            },
            
            "ward_info": {
                "population": ward.get("population_2024_est", 0),
                "area_km2": ward.get("area_km2", 0),
                "is_hotspot": ward.get("pollution_hotspot", False),
                "major_roads": ward.get("major_roads", []),
                "industrial_areas": ward.get("industrial_areas", []),
                "metro_stations": ward.get("metro_stations", [])
            },
            
            "health_impact": health_impact,
            
            "timestamp": datetime.now().isoformat(),
            "data_source": "real_time_production"
        }
    
    @classmethod
    def get_all_wards_ranked(cls):
        """
        Get all Delhi wards ranked by pollution level
        Uses real-time data from all monitoring stations
        """
        cache_key = "all_wards_ranked_realtime"
        cached = cache.get(cache_key)
        
        if cached:
            return cached
        
        stations = cls.get_all_stations_realtime()
        ward_rankings = []
        
        for ward_id, ward in DELHI_WARDS_OFFICIAL.items():
            ward_center = ward["center"]
            ward_radius_km = sqrt(ward.get("area_km2", 4)) * 1.5
            
            # Find stations for this ward
            ward_stations = []
            for station in stations:
                lat = station.get("Latitude", 0)
                lon = station.get("Longitude", 0)
                
                if lat == 0 or lon == 0:
                    continue
                
                distance = haversine_distance(ward_center[0], ward_center[1], lat, lon)
                
                if distance <= ward_radius_km:
                    ward_stations.append(station)
            
            # Use nearest stations if none in radius
            if not ward_stations:
                all_with_distance = []
                for station in stations:
                    lat = station.get("Latitude", 0)
                    lon = station.get("Longitude", 0)
                    if lat != 0 and lon != 0:
                        distance = haversine_distance(ward_center[0], ward_center[1], lat, lon)
                        all_with_distance.append({**station, "distance": distance})
                
                if all_with_distance:
                    all_with_distance.sort(key=lambda x: x["distance"])
                    ward_stations = all_with_distance[:2]  # Nearest 2
            
            if not ward_stations:
                continue
            
            # Calculate averages
            avg_aqi = sum([s.get("AQI", 0) for s in ward_stations]) / len(ward_stations)
            avg_pm25 = sum([s.get("PM25", 0) or s.get("AQI", 0) * 0.6 for s in ward_stations]) / len(ward_stations)
            avg_pm10 = sum([s.get("PM10", 0) or s.get("AQI", 0) * 0.8 for s in ward_stations]) / len(ward_stations)
            
            aqi_category = cls.get_aqi_category(avg_aqi)
            
            ward_rankings.append({
                "ward_id": ward_id,
                "ward_name": ward["name"],
                "zone": ward["zone"],
                "type": ward["type"],
                "avg_aqi": round(avg_aqi, 1),
                "avg_pm25": round(avg_pm25, 1),
                "avg_pm10": round(avg_pm10, 1),
                "aqi_category": aqi_category["category"],
                "aqi_color": aqi_category["color"],
                "station_count": len(ward_stations),
                "population": ward.get("population_2024_est", 0),
                "is_hotspot": ward.get("pollution_hotspot", False)
            })
        
        # Sort by AQI (worst first)
        ward_rankings.sort(key=lambda x: x["avg_aqi"], reverse=True)
        
        # Add ranks and urgency
        for idx, ward in enumerate(ward_rankings, 1):
            ward["rank"] = idx
            ward["urgency"] = cls.get_urgency_level(ward["avg_aqi"])
        
        # Calculate summary
        total_population_at_risk = sum([
            w["population"] for w in ward_rankings 
            if w["urgency"] in ["CRITICAL", "SEVERE"]
        ])
        
        result = {
            "timestamp": datetime.now().isoformat(),
            "total_wards": len(ward_rankings),
            "data_source": "real_time_production",
            
            "summary": {
                "critical_wards": len([w for w in ward_rankings if w["urgency"] == "CRITICAL"]),
                "severe_wards": len([w for w in ward_rankings if w["urgency"] == "SEVERE"]),
                "poor_wards": len([w for w in ward_rankings if w["urgency"] == "POOR"]),
                "moderate_wards": len([w for w in ward_rankings if w["urgency"] == "MODERATE"]),
                "good_wards": len([w for w in ward_rankings if w["urgency"] == "GOOD"]),
                "population_at_risk": total_population_at_risk,
                "avg_delhi_aqi": round(sum([w["avg_aqi"] for w in ward_rankings]) / len(ward_rankings), 1) if ward_rankings else 0
            },
            
            "wards": ward_rankings,
            "worst_5": ward_rankings[:5],
            "best_5": ward_rankings[-5:][::-1] if len(ward_rankings) >= 5 else ward_rankings[::-1],
            
            "zones_summary": cls.get_zones_summary(ward_rankings)
        }
        
        cache.set(cache_key, result, cls.CACHE_TIMEOUT)
        return result
    
    @classmethod
    def get_zones_summary(cls, ward_rankings):
        """Get pollution summary by zone"""
        zone_data = {}
        
        for ward in ward_rankings:
            zone = ward["zone"]
            
            if zone not in zone_data:
                zone_data[zone] = {
                    "wards": [],
                    "total_aqi": 0,
                    "count": 0,
                    "total_population": 0
                }
            
            zone_data[zone]["wards"].append(ward["ward_name"])
            zone_data[zone]["total_aqi"] += ward["avg_aqi"]
            zone_data[zone]["count"] += 1
            zone_data[zone]["total_population"] += ward["population"]
        
        zones_summary = []
        for zone_name, data in zone_data.items():
            zone_info = DELHI_ZONES.get(zone_name, {})
            avg_aqi = data["total_aqi"] / data["count"] if data["count"] > 0 else 0
            
            zones_summary.append({
                "zone": zone_name,
                "zone_full_name": zone_info.get("name", zone_name),
                "description": zone_info.get("description", ""),
                "avg_aqi": round(avg_aqi, 1),
                "ward_count": data["count"],
                "population": data["total_population"],
                "urgency": cls.get_urgency_level(avg_aqi),
                "characteristics": zone_info.get("characteristics", "")
            })
        
        zones_summary.sort(key=lambda x: x["avg_aqi"], reverse=True)
        return zones_summary
    
    @classmethod
    def get_aqi_category(cls, aqi):
        """Get AQI category and color based on Indian AQI standards"""
        if aqi <= 50:
            return {"category": "Good", "color": "#00e400"}
        elif aqi <= 100:
            return {"category": "Satisfactory", "color": "#92d050"}
        elif aqi <= 200:
            return {"category": "Moderate", "color": "#ffff00"}
        elif aqi <= 300:
            return {"category": "Poor", "color": "#ff7e00"}
        elif aqi <= 400:
            return {"category": "Very Poor", "color": "#ff0000"}
        else:
            return {"category": "Severe", "color": "#7e0023"}
    
    @classmethod
    def get_urgency_level(cls, aqi):
        """Get urgency level for action"""
        if aqi > 400:
            return "CRITICAL"
        elif aqi > 300:
            return "SEVERE"
        elif aqi > 200:
            return "POOR"
        elif aqi > 100:
            return "MODERATE"
        else:
            return "GOOD"
    
    @classmethod
    def calculate_health_impact(cls, pm25, population):
        """
        Calculate health impact using WHO methodology
        """
        who_guideline = 15  # µg/m³
        excess_pm25 = max(0, pm25 - who_guideline)
        
        # WHO estimates: 8% mortality increase per 10 µg/m³
        mortality_increase = (excess_pm25 / 10) * 0.08
        respiratory_increase = (excess_pm25 / 10) * 0.10
        
        # Cigarette equivalent (1 cigarette = 22 µg PM2.5 for 24h)
        cigarettes_per_day = (pm25 * 24) / 22
        
        # Lung age calculation (Gauderman et al. 2015)
        biological_age = 35
        lung_age_increase = (excess_pm25 / 10) * 2.5
        estimated_lung_age = biological_age + lung_age_increase
        
        # Population at elevated risk
        lives_at_risk = int(population * mortality_increase * 0.001)
        
        return {
            "who_guideline_exceeded_by": round(excess_pm25, 1),
            "cigarette_equivalent_per_day": round(cigarettes_per_day, 1),
            "mortality_risk_increase": f"{mortality_increase*100:.1f}%",
            "respiratory_risk_increase": f"{respiratory_increase*100:.1f}%",
            "lung_age": {
                "biological": biological_age,
                "estimated": round(estimated_lung_age, 1),
                "excess_years": round(lung_age_increase, 1)
            },
            "lives_at_elevated_risk": lives_at_risk,
            "recommendation": cls.get_health_recommendation(pm25)
        }
    
    @classmethod
    def get_health_recommendation(cls, pm25):
        """Get health recommendation based on PM2.5 level"""
        if pm25 <= 30:
            return "Air quality acceptable. Enjoy outdoor activities."
        elif pm25 <= 60:
            return "Sensitive individuals should limit prolonged outdoor exertion."
        elif pm25 <= 90:
            return "Everyone should reduce prolonged outdoor exertion."
        elif pm25 <= 120:
            return "Everyone should avoid prolonged outdoor exertion. Consider wearing N95 mask."
        elif pm25 <= 250:
            return "Avoid all outdoor activities. Use air purifiers indoors. Wear N95 mask if going out."
        else:
            return "EMERGENCY: Stay indoors. Close all windows. Use air purifiers. Seek medical attention if breathing difficulty."
