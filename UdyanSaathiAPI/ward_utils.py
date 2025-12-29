"""
Utility functions for ward-based pollution calculations
Uses REAL pollution data from monitoring stations
"""

from django.db.models import Avg, Max, Min, Count
from datetime import datetime, timedelta
import math


def point_in_polygon(lat, lon, polygon):
    """
    Check if a point (lat, lon) is inside a polygon
    Uses ray-casting algorithm
    """
    x, y = lon, lat
    n = len(polygon)
    inside = False

    p1x, p1y = polygon[0]
    for i in range(n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y

    return inside


def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate distance between two lat/lon points in kilometers
    Haversine formula
    """
    R = 6371  # Earth's radius in km
    
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    
    a = (math.sin(dlat / 2) ** 2 + 
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * 
         math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c


def map_station_to_ward(station_lat, station_lon, wards):
    """
    Find which ward a monitoring station belongs to
    """
    for ward_id, ward_data in wards.items():
        if point_in_polygon(station_lat, station_lon, ward_data['boundary']):
            return ward_id
    return None


def calculate_ward_pollution(stations_data):
    """
    Calculate aggregated pollution metrics for a ward
    Input: List of pollution data from stations within the ward
    """
    if not stations_data:
        return None
    
    total_aqi = sum(s['AQI'] for s in stations_data)
    total_pm25 = sum(s['PM25'] for s in stations_data)
    total_pm10 = sum(s['PM10'] for s in stations_data)
    count = len(stations_data)
    
    return {
        'avg_aqi': round(total_aqi / count, 2),
        'avg_pm25': round(total_pm25 / count, 2),
        'avg_pm10': round(total_pm10 / count, 2),
        'max_aqi': max(s['AQI'] for s in stations_data),
        'min_aqi': min(s['AQI'] for s in stations_data),
        'station_count': count
    }


def calculate_health_metrics(pm25_value):
    """
    Calculate health impact metrics from PM2.5 value
    Based on established medical research
    """
    # WHO guideline: 12 µg/m³ annual mean
    WHO_GUIDELINE = 12
    
    # Lung age calculation
    # Research: For every 10 µg/m³ increase, ~2-3 years lung aging
    biological_age = 35
    pm25_excess = max(0, pm25_value - WHO_GUIDELINE)
    lung_age_increase = (pm25_excess / 10) * 2.5
    lung_age = biological_age + lung_age_increase
    
    # Cigarette equivalent
    # EPA calculation: 1 cigarette = 22 µg PM2.5 exposure for 24 hours
    cigarettes_per_day = (pm25_value * 24) / 22
    
    # Life lost calculation (Berkeley Earth formula)
    # 22 µg/m³ = 11 minutes of life lost per day
    life_lost_minutes = (pm25_value / 22) * 11 * 365  # Annual
    life_lost_hours = life_lost_minutes / 60
    life_lost_days = life_lost_hours / 24
    
    return {
        'lung_age': round(lung_age, 1),
        'biological_age': biological_age,
        'lung_age_excess': round(lung_age - biological_age, 1),
        'cigarettes_per_day': round(cigarettes_per_day, 2),
        'life_lost_days_annual': round(life_lost_days, 1),
        'who_guideline_excess': round(pm25_excess, 2)
    }


def calculate_toxicity_velocity(current_aqi, historical_aqi, days):
    """
    Calculate how fast pollution is changing (velocity)
    Positive = getting worse, Negative = improving
    """
    if not historical_aqi or days == 0:
        return 0
    
    change = current_aqi - historical_aqi
    velocity_per_day = change / days
    
    return round(velocity_per_day, 2)


def get_urgency_level(aqi, velocity):
    """
    Determine urgency level based on AQI and velocity
    """
    if aqi > 300 or velocity > 20:
        return 'CRITICAL'
    elif aqi > 200 or velocity > 10:
        return 'HIGH'
    elif aqi > 100 or velocity > 5:
        return 'MEDIUM'
    else:
        return 'LOW'
