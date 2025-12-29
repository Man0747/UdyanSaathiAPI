"""
Ward boundary mapper for Delhi wards
Handles geospatial operations for ward assignment
"""

from .ward_data import get_ward_data


class WardMapper:
    """
    Utility class for mapping stations to wards based on coordinates
    """
    
    DELHI_WARDS = get_ward_data()
    
    @classmethod
    def is_station_in_ward(cls, lat, lon, ward_center, radius=0.15):
        """
        Check if a station coordinate is within a ward's radius
        Uses simple distance calculation (good enough for city-level)
        
        Args:
            lat: Station latitude
            lon: Station longitude
            ward_center: Tuple of (lat, lon) for ward center
            radius: Distance threshold in degrees (~15km for 0.15)
        
        Returns:
            bool: True if station is within ward radius
        """
        lat_diff = abs(lat - ward_center[0])
        lon_diff = abs(lon - ward_center[1])
        distance = (lat_diff ** 2 + lon_diff ** 2) ** 0.5
        
        return distance < radius
    
    @classmethod
    def find_ward_for_station(cls, lat, lon):
        """
        Find which ward a station belongs to
        
        Args:
            lat: Station latitude
            lon: Station longitude
        
        Returns:
            tuple: (ward_id, ward_name) or (None, None) if not found
        """
        for ward_id, ward_data in cls.DELHI_WARDS.items():
            if cls.is_station_in_ward(lat, lon, ward_data['center']):
                return ward_id, ward_data['name']
        
        return None, None
    
    @classmethod
    def get_stations_for_ward(cls, ward_id, all_stations):
        """
        Get all stations that belong to a specific ward
        
        Args:
            ward_id: Ward ID to filter by
            all_stations: List or queryset of stations with Latitude/Longitude
        
        Returns:
            list: Stations within the ward
        """
        if ward_id not in cls.DELHI_WARDS:
            return []
        
        ward_center = cls.DELHI_WARDS[ward_id]['center']
        stations_in_ward = []
        
        for station in all_stations:
            try:
                # Handle both dict and model object
                lat = station.get('Latitude') if isinstance(station, dict) else station.Latitude
                lon = station.get('Longitude') if isinstance(station, dict) else station.Longitude
                
                if cls.is_station_in_ward(float(lat), float(lon), ward_center):
                    stations_in_ward.append(station)
            except (ValueError, AttributeError, TypeError):
                continue
        
        return stations_in_ward
