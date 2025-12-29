"""
Ward boundary data for Delhi
Source: https://github.com/datameet/Municipal_Spatial_Data
Simplified sample data for demonstration - full data would come from GeoJSON files
"""

"""
Ward boundary data for Delhi
Source: https://github.com/datameet/Municipal_Spatial_Data
Adjusted to cover actual monitoring station locations in Delhi
"""

# Delhi ward boundaries covering actual monitoring station areas
# Coordinates adjusted to encompass real pollution monitoring stations
DELHI_WARDS_SAMPLE = {
    1: {
        "name": "North Delhi (Rohini, Narela area)",
        "center": [28.7500, 77.1000],
        "boundary": [
            [28.6500, 76.9500],
            [28.8500, 76.9500],
            [28.8500, 77.2500],
            [28.6500, 77.2500],
            [28.6500, 76.9500]
        ]
    },
    2: {
        "name": "Central Delhi (Connaught Place, ITO area)",
        "center": [28.6350, 77.2200],
        "boundary": [
            [28.6000, 77.1900],
            [28.6700, 77.1900],
            [28.6700, 77.2500],
            [28.6000, 77.2500],
            [28.6000, 77.1900]
        ]
    },
    3: {
        "name": "East Delhi (Anand Vihar, IP Extension)",
        "center": [28.6450, 77.3150],
        "boundary": [
            [28.6000, 77.2500],
            [28.7000, 77.2500],
            [28.7000, 77.3800],
            [28.6000, 77.3800],
            [28.6000, 77.2500]
        ]
    },
    4: {
        "name": "South Delhi (Lodhi Road, RK Puram)",
        "center": [28.5700, 77.2000],
        "boundary": [
            [28.5200, 77.1500],
            [28.6200, 77.1500],
            [28.6200, 77.2500],
            [28.5200, 77.2500],
            [28.5200, 77.1500]
        ]
    },
    5: {
        "name": "West Delhi (Dwarka, Punjabi Bagh)",
        "center": [28.6200, 77.0500],
        "boundary": [
            [28.5500, 76.9500],
            [28.6900, 76.9500],
            [28.6900, 77.1500],
            [28.5500, 77.1500],
            [28.5500, 76.9500]
        ]
    },
    6: {
        "name": "Southwest Delhi (Palam, RK Puram)",
        "center": [28.5500, 77.1200],
        "boundary": [
            [28.5000, 77.0500],
            [28.6000, 77.0500],
            [28.6000, 77.1900],
            [28.5000, 77.1900],
            [28.5000, 77.0500]
        ]
    },
    7: {
        "name": "Northeast Delhi (Shahdara, Vivek Vihar)",
        "center": [28.6800, 77.2800],
        "boundary": [
            [28.6500, 77.2500],
            [28.7100, 77.2500],
            [28.7100, 77.3100],
            [28.6500, 77.3100],
            [28.6500, 77.2500]
        ]
    },
    8: {
        "name": "Northwest Delhi (Rohini, Pitampura)",
        "center": [28.7200, 77.1100],
        "boundary": [
            [28.6800, 77.0500],
            [28.7600, 77.0500],
            [28.7600, 77.1700],
            [28.6800, 77.1700],
            [28.6800, 77.0500]
        ]
    },
    9: {
        "name": "New Delhi (Diplomatic Enclave)",
        "center": [28.6100, 77.2100],
        "boundary": [
            [28.5800, 77.1800],
            [28.6400, 77.1800],
            [28.6400, 77.2400],
            [28.5800, 77.2400],
            [28.5800, 77.1800]
        ]
    },
    10: {
        "name": "South Delhi Extension (Mehrauli, Vasant Vihar)",
        "center": [28.5300, 77.1600],
        "boundary": [
            [28.4800, 77.1200],
            [28.5800, 77.1200],
            [28.5800, 77.2000],
            [28.4800, 77.2000],
            [28.4800, 77.1200]
        ]
    }
}

def get_ward_data():
    """
    Returns ward boundary data
    In production, this would load from the GitHub repo's GeoJSON files
    """
    return DELHI_WARDS_SAMPLE


def create_geojson_feature(ward_id, ward_data):
    """Convert ward data to GeoJSON format"""
    return {
        "type": "Feature",
        "properties": {
            "ward_id": ward_id,
            "name": ward_data["name"]
        },
        "geometry": {
            "type": "Polygon",
            "coordinates": [ward_data["boundary"]]
        }
    }
