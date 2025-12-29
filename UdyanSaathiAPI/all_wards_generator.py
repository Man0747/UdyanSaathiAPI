"""
ALL 272 DELHI WARDS DATA GENERATOR
Generates complete ward data for all 272 Delhi Municipal Corporation wards
- 40 wards with real CPCB monitoring stations (real data)
- 232 wards with interpolated/estimated data (based on nearest stations)
"""

import random
from datetime import datetime, timedelta

# All 272 Delhi Wards organized by Municipal Corporation
ALL_DELHI_WARDS = {
    # NORTH DELHI MUNICIPAL CORPORATION (NDMC) - 104 wards
    **{f"NDMC-{i:03d}": {
        "ward_id": f"NDMC-{i:03d}",
        "ward_number": i,
        "ward_name": f"NDMC Ward {i}",
        "zone": "north",
        "corporation": "NDMC",
        "has_monitoring_station": False,
        "centroid": [28.7 + (random.random() * 0.2 - 0.1), 77.1 + (random.random() * 0.2 - 0.1)],
        "area_km2": random.uniform(1.0, 5.0),
        "population": random.randint(15000, 50000)
    } for i in range(1, 105)},
    
    # SOUTH DELHI MUNICIPAL CORPORATION (SDMC) - 104 wards
    **{f"SDMC-{i:03d}": {
        "ward_id": f"SDMC-{i:03d}",
        "ward_number": i + 104,
        "ward_name": f"SDMC Ward {i}",
        "zone": "south",
        "corporation": "SDMC",
        "has_monitoring_station": False,
        "centroid": [28.5 + (random.random() * 0.2 - 0.1), 77.2 + (random.random() * 0.2 - 0.1)],
        "area_km2": random.uniform(1.0, 5.0),
        "population": random.randint(15000, 50000)
    } for i in range(1, 105)},
    
    # EAST DELHI MUNICIPAL CORPORATION (EDMC) - 64 wards
    **{f"EDMC-{i:03d}": {
        "ward_id": f"EDMC-{i:03d}",
        "ward_number": i + 208,
        "ward_name": f"EDMC Ward {i}",
        "zone": "east",
        "corporation": "EDMC",
        "has_monitoring_station": False,
        "centroid": [28.6 + (random.random() * 0.2 - 0.1), 77.3 + (random.random() * 0.2 - 0.1)],
        "area_km2": random.uniform(1.0, 5.0),
        "population": random.randint(15000, 50000)
    } for i in range(1, 65)},
}

# Map your 40 monitored stations to specific wards
MONITORED_WARDS = {
    "NDMC-001": {"station": "Anand Vihar", "ward_name": "Anand Vihar", "has_monitoring_station": True},
    "NDMC-002": {"station": "Ashok Vihar", "ward_name": "Ashok Vihar", "has_monitoring_station": True},
    "NDMC-003": {"station": "Bawana", "ward_name": "Bawana", "has_monitoring_station": True},
    "NDMC-004": {"station": "Dwarka", "ward_name": "Dwarka", "has_monitoring_station": True},
    "NDMC-005": {"station": "Mundka", "ward_name": "Mundka", "has_monitoring_station": True},
    "NDMC-006": {"station": "Narela", "ward_name": "Narela", "has_monitoring_station": True},
    "NDMC-007": {"station": "Rohini", "ward_name": "Rohini", "has_monitoring_station": True},
    "NDMC-008": {"station": "Wazirpur", "ward_name": "Wazirpur", "has_monitoring_station": True},
    
    "SDMC-001": {"station": "IGI Airport (T3)", "ward_name": "IGI Airport", "has_monitoring_station": True},
    "SDMC-002": {"station": "RK Puram", "ward_name": "RK Puram", "has_monitoring_station": True},
    "SDMC-003": {"station": "Punjabi Bagh", "ward_name": "Punjabi Bagh", "has_monitoring_station": True},
    "SDMC-004": {"station": "Pusa", "ward_name": "Pusa", "has_monitoring_station": True},
    "SDMC-005": {"station": "Lodhi Road", "ward_name": "Lodhi Road", "has_monitoring_station": True},
    "SDMC-006": {"station": "Nehru Nagar", "ward_name": "Nehru Nagar", "has_monitoring_station": True},
    "SDMC-007": {"station": "Patparganj", "ward_name": "Patparganj", "has_monitoring_station": True},
    "SDMC-008": {"station": "Punjabi Bagh West", "ward_name": "Punjabi Bagh West", "has_monitoring_station": True},
    
    "EDMC-001": {"station": "Anand Vihar", "ward_name": "Anand Vihar East", "has_monitoring_station": True},
    "EDMC-002": {"station": "Vivek Vihar", "ward_name": "Vivek Vihar", "has_monitoring_station": True},
    "EDMC-003": {"station": "Jahangirpuri", "ward_name": "Jahangirpuri", "has_monitoring_station": True},
    "EDMC-004": {"station": "Sonia Vihar", "ward_name": "Sonia Vihar", "has_monitoring_station": True},
    "EDMC-005": {"station": "Shahdara", "ward_name": "Shahdara", "has_monitoring_station": True},
    "EDMC-006": {"station": "Mayur Vihar", "ward_name": "Mayur Vihar", "has_monitoring_station": True},
    "EDMC-007": {"station": "East Arjun Nagar", "ward_name": "East Arjun Nagar", "has_monitoring_station": True},
    "EDMC-008": {"station": "Dilshad Garden", "ward_name": "Dilshad Garden", "has_monitoring_station": True},
    
    # Add more mappings for your 40 monitored wards
    "NDMC-009": {"station": "North Campus, DU", "ward_name": "North Campus", "has_monitoring_station": True},
    "NDMC-010": {"station": "Civil Lines", "ward_name": "Civil Lines", "has_monitoring_station": True},
    "NDMC-011": {"station": "Chandni Chowk", "ward_name": "Chandni Chowk", "has_monitoring_station": True},
    "NDMC-012": {"station": "Karol Bagh", "ward_name": "Karol Bagh", "has_monitoring_station": True},
    
    "SDMC-009": {"station": "Greater Kailash", "ward_name": "Greater Kailash", "has_monitoring_station": True},
    "SDMC-010": {"station": "Defence Colony", "ward_name": "Defence Colony", "has_monitoring_station": True},
    "SDMC-011": {"station": "Hauz Khas", "ward_name": "Hauz Khas", "has_monitoring_station": True},
    "SDMC-012": {"station": "Vasant Kunj", "ward_name": "Vasant Kunj", "has_monitoring_station": True},
    "SDMC-013": {"station": "Saket", "ward_name": "Saket", "has_monitoring_station": True},
    "SDMC-014": {"station": "Mehrauli", "ward_name": "Mehrauli", "has_monitoring_station": True},
    "SDMC-015": {"station": "Lajpat Nagar", "ward_name": "Lajpat Nagar", "has_monitoring_station": True},
    "SDMC-016": {"station": "South Campus, DU", "ward_name": "South Campus", "has_monitoring_station": True},
    
    "EDMC-009": {"station": "Preet Vihar", "ward_name": "Preet Vihar", "has_monitoring_station": True},
    "EDMC-010": {"station": "Laxmi Nagar", "ward_name": "Laxmi Nagar", "has_monitoring_station": True},
    "EDMC-011": {"station": "Gandhi Nagar", "ward_name": "Gandhi Nagar", "has_monitoring_station": True},
    "EDMC-012": {"station": "Krishna Nagar", "ward_name": "Krishna Nagar", "has_monitoring_station": True},
}

# Update the ward data with monitoring stations
for ward_id, station_info in MONITORED_WARDS.items():
    if ward_id in ALL_DELHI_WARDS:
        ALL_DELHI_WARDS[ward_id].update(station_info)


def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two points in km"""
    from math import radians, cos, sin, asin, sqrt
    
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    km = 6371 * c
    return km


def find_nearest_monitored_ward(ward_lat, ward_lon):
    """Find the nearest ward with a monitoring station"""
    min_distance = float('inf')
    nearest_ward = None
    
    for ward_id, ward_data in ALL_DELHI_WARDS.items():
        if ward_data.get('has_monitoring_station'):
            centroid = ward_data['centroid']
            distance = calculate_distance(ward_lat, ward_lon, centroid[0], centroid[1])
            if distance < min_distance:
                min_distance = distance
                nearest_ward = (ward_id, ward_data)
    
    return nearest_ward, min_distance


def estimate_ward_pollution(ward_data, pollution_data_from_db):
    """
    Estimate pollution for wards without monitoring stations
    Uses nearest neighbor interpolation
    
    Args:
        ward_data: Ward information dict
        pollution_data_from_db: Real pollution data from your CPCB database
    
    Returns:
        Estimated pollution metrics
    """
    if ward_data.get('has_monitoring_station'):
        # This ward has real data - fetch from database
        station_name = ward_data.get('station')
        # You'll connect this to your actual database query
        return None  # Will be filled with real data
    
    # For wards without stations, interpolate
    centroid = ward_data['centroid']
    nearest_ward, distance = find_nearest_monitored_ward(centroid[0], centroid[1])
    
    if nearest_ward:
        # Add distance-based uncertainty
        # Farther wards get more uncertainty added
        uncertainty_factor = 1 + (distance / 20)  # 20km = significant uncertainty
        
        # You'll get real data from the nearest monitored ward
        # and apply uncertainty factor
        return {
            "estimated": True,
            "nearest_station": nearest_ward[1].get('station'),
            "distance_km": round(distance, 2),
            "uncertainty_factor": round(uncertainty_factor, 2),
            "data_source": "interpolated"
        }
    
    return None


def get_all_272_wards():
    """Return all 272 wards"""
    return ALL_DELHI_WARDS


def get_wards_by_corporation(corporation):
    """Get wards by corporation (NDMC/SDMC/EDMC)"""
    return {k: v for k, v in ALL_DELHI_WARDS.items() if v['corporation'] == corporation}


def get_wards_by_zone(zone):
    """Get wards by zone"""
    return {k: v for k, v in ALL_DELHI_WARDS.items() if v['zone'] == zone}


def get_monitored_wards_only():
    """Get only the 40 wards with real monitoring stations"""
    return {k: v for k, v in ALL_DELHI_WARDS.items() if v.get('has_monitoring_station')}


def get_wards_summary():
    """Get summary statistics"""
    total = len(ALL_DELHI_WARDS)
    monitored = len([w for w in ALL_DELHI_WARDS.values() if w.get('has_monitoring_station')])
    estimated = total - monitored
    
    by_corporation = {
        "NDMC": len(get_wards_by_corporation("NDMC")),
        "SDMC": len(get_wards_by_corporation("SDMC")),
        "EDMC": len(get_wards_by_corporation("EDMC"))
    }
    
    return {
        "total_wards": total,
        "monitored_wards": monitored,
        "estimated_wards": estimated,
        "coverage_percentage": round((monitored / total) * 100, 2),
        "by_corporation": by_corporation
    }
