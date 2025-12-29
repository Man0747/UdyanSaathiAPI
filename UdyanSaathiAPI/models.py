# models.py
from django.db import models
from datetime import datetime
from datetime import date
import re

# ALL MODELS
class mapDataModel(models.Model):
    State = models.CharField(max_length=255, default=" ")
    City = models.CharField(max_length=255, default=" ")
    Station = models.CharField(max_length=500, default=" ")
    Pol_Date = models.CharField(max_length=500, default=" ")
    # CO = models.FloatField(max_length=10, default=0)
    # NH3 = models.FloatField(max_length=10, default=0)
    # NO2 = models.FloatField(max_length=10, default=0)
    # OZONE = models.FloatField(max_length=10, default=0)
    # PM25 = models.FloatField(max_length=10, default=0)
    # PM10 = models.FloatField(max_length=10, default=0)
    # SO2 = models.FloatField(max_length=10, default=0)
    AQI = models.IntegerField(default=0)
    AQI_Quality = models.CharField(max_length=100, default=" ")
    Longitude = models.FloatField(max_length=10,default=0)
    Latitude = models.FloatField(max_length=10,default=0)

class graphDataModel(models.Model):
    City = models.CharField(max_length=255,default=" ")
    Pol_Date = models.CharField(max_length=500, default=" ")
    AQI = models.IntegerField(default=0)
    NH3 = models.FloatField(max_length=10,default=0)   
    PM10 = models.FloatField(max_length=10,default=0)
    PM25 = models.FloatField(max_length=10,default=0)
    NO2 = models.FloatField(max_length=10,default=0)
    SO2 = models.FloatField(max_length=10,default=0)
    CO = models.FloatField(max_length=10,default=0)
    OZONE = models.FloatField(max_length=10,default=0)
    
class pollutionModel(models.Model):
    State = models.CharField(max_length=255, default=" ")
    City = models.CharField(max_length=255, default=" ")
    Station = models.CharField(max_length=500, default=" ")
    Pol_Date = models.CharField(max_length=500, default=" ")
    CO = models.FloatField(max_length=10, default=0)
    NH3 = models.FloatField(max_length=10, default=0)
    NO2 = models.FloatField(max_length=10, default=0)
    OZONE = models.FloatField(max_length=10, default=0)
    PM25 = models.FloatField(max_length=10, default=0)
    PM10 = models.FloatField(max_length=10, default=0)
    SO2 = models.FloatField(max_length=10, default=0)
    Checks = models.IntegerField(default=0)
    AQI = models.IntegerField(default=0)
    AQI_Quality = models.CharField(max_length=100, default=" ")

class stationModel(models.Model):
    Station = models.CharField(max_length=500,default=" ")

class Top10CitiesModel(models.Model):
    City = models.CharField(max_length=255,default=" ")
    AQI = models.IntegerField(default=0)
    PM25 = models.FloatField(max_length=10,default=0)
    PM10 = models.FloatField(max_length=10,default=0)
    CO = models.FloatField(max_length=10,default=0)
    OZONE = models.FloatField(max_length=10,default=0)
    SO2 = models.FloatField(max_length=10,default=0)
    NO2 = models.FloatField(max_length=10,default=0)
    NH3 = models.FloatField(max_length=10,default=0)

class Top10LeastCitiesModel(models.Model):
    City = models.CharField(max_length=255,default=" ")
    AQI = models.IntegerField(default=0)
    PM25 = models.FloatField(max_length=10,default=0)
    PM10 = models.FloatField(max_length=10,default=0)
    CO = models.FloatField(max_length=10,default=0)
    OZONE = models.FloatField(max_length=10,default=0)
    SO2 = models.FloatField(max_length=10,default=0)
    NO2 = models.FloatField(max_length=10,default=0)
    NH3 = models.FloatField(max_length=10,default=0)

class TopMetroCitiesModel(models.Model):
    City = models.CharField(max_length=255,default=" ")
    AQI = models.IntegerField(default=0)
    PM25 = models.FloatField(max_length=10,default=0)
    PM10 = models.FloatField(max_length=10,default=0)
    CO = models.FloatField(max_length=10,default=0)
    OZONE = models.FloatField(max_length=10,default=0)
    SO2 = models.FloatField(max_length=10,default=0)
    NO2 = models.FloatField(max_length=10,default=0)
    NH3 = models.FloatField(max_length=10,default=0)   

class AqiCalendarModel(models.Model):
    Station = models.CharField(max_length=500,default=" ")
    AQI = models.IntegerField(default=0)
    Pol_Date = models.CharField(max_length=500, default=" ")
    
class MlModel(models.Model):
    Station = models.CharField(max_length=255,default=" ")
    Day1 = models.FloatField(max_length=10,default=0)
    Day2 =models.FloatField(max_length=10,default=0)
    Day3 = models.FloatField(max_length=10,default=0)
    Day4 = models.FloatField(max_length=10,default=0)
    Day5 = models.FloatField(max_length=10,default=0)

class StationsCoordinatesModel(models.Model):
    Station = models.CharField(max_length=500, default=" ")
    Longitude = models.FloatField(max_length=10,default=0)
    Latitude = models.FloatField(max_length=10,default=0)

# DISPATCH SYSTEM MODELS
class FleetAsset(models.Model):
    """Physical resources for pollution intervention"""
    ASSET_TYPE_CHOICES = [
        ('SMOG_GUN', 'Smog Gun'),
        ('SPRINKLER', 'Water Sprinkler'),
        ('DRONE', 'Monitoring Drone'),
    ]
    
    STATUS_CHOICES = [
        ('IDLE', 'Idle'),
        ('DISPATCHED', 'Dispatched'),
        ('ACTIVE', 'Active'),
        ('RETURNING', 'Returning'),
        ('MAINTENANCE', 'Maintenance'),
    ]
    
    asset_id = models.CharField(max_length=20, unique=True, primary_key=True)
    asset_type = models.CharField(max_length=20, choices=ASSET_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='IDLE')
    
    # Location tracking
    current_lat = models.FloatField()
    current_lon = models.FloatField()
    home_station = models.CharField(max_length=100)
    
    # Operational metrics
    water_level_pct = models.IntegerField(default=100)
    fuel_level_pct = models.IntegerField(default=100)
    operational_hours = models.FloatField(default=0.0)
    
    # Metadata
    last_maintenance = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'fleet_assets'
        
    def __str__(self):
        return f"{self.asset_id} - {self.asset_type} ({self.status})"

class DispatchTicket(models.Model):
    """Mission assignments for pollution intervention"""
    URGENCY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('CRITICAL', 'Critical'),
    ]
    
    ticket_id = models.CharField(max_length=30, unique=True, primary_key=True)
    asset = models.ForeignKey(FleetAsset, on_delete=models.CASCADE, related_name='missions')
    
    # Target location
    target_station = models.CharField(max_length=100)
    target_lat = models.FloatField()
    target_lon = models.FloatField()
    
    # Pollution context
    predicted_pm25 = models.FloatField()
    predicted_aqi = models.IntegerField()
    forecast_time = models.DateTimeField()
    
    # Mission details
    urgency_level = models.CharField(max_length=20, choices=URGENCY_CHOICES)
    mission_brief = models.TextField()
    dispatch_time = models.DateTimeField(auto_now_add=True)
    estimated_arrival = models.DateTimeField()
    actual_arrival = models.DateTimeField(null=True, blank=True)
    
    # Status tracking
    is_completed = models.BooleanField(default=False)
    completion_time = models.DateTimeField(null=True, blank=True)
    effectiveness_score = models.FloatField(null=True, blank=True)
    
    class Meta:
        db_table = 'dispatch_tickets'
        ordering = ['-dispatch_time']
        
    def __str__(self):
        return f"{self.ticket_id} - {self.target_station}"

class InterventionLog(models.Model):
    """Track actual pollution reduction after intervention"""
    ticket = models.OneToOneField(DispatchTicket, on_delete=models.CASCADE, related_name='outcome')
    
    # Before intervention
    pre_intervention_pm25 = models.FloatField()
    pre_intervention_aqi = models.IntegerField()
    
    # After intervention
    post_intervention_pm25 = models.FloatField()
    post_intervention_aqi = models.IntegerField()
    
    # Metrics
    reduction_percentage = models.FloatField()
    intervention_duration_hours = models.FloatField()
    water_used_liters = models.IntegerField(null=True, blank=True)
    
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'intervention_logs'
        
    def save(self, *args, **kwargs):
        # Auto-calculate reduction percentage
        if self.pre_intervention_pm25 and self.post_intervention_pm25:
            self.reduction_percentage = (
                (self.pre_intervention_pm25 - self.post_intervention_pm25) / 
                self.pre_intervention_pm25 * 100
            )
        super().save(*args, **kwargs)


# Ward-based pollution tracking models
class Ward(models.Model):
    """Administrative ward information with boundary data"""
    ward_id = models.IntegerField(unique=True, primary_key=True)
    ward_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100, default='Delhi')
    state = models.CharField(max_length=100, default='Delhi')
    
    # Geographic data (from GitHub Municipal_Spatial_Data)
    boundary_geojson = models.JSONField(help_text='GeoJSON polygon of ward boundary')
    center_lat = models.FloatField()
    center_lon = models.FloatField()
    area_sq_km = models.FloatField(null=True, blank=True)
    
    # Demographics (optional)
    population = models.IntegerField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'wards'
        ordering = ['ward_id']
    
    def __str__(self):
        return f"Ward {self.ward_id} - {self.ward_name}"


class WardStationMapping(models.Model):
    """Maps monitoring stations to wards using geospatial coordinates"""
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE, related_name='stations')
    station_name = models.CharField(max_length=200)
    
    # Station coordinates
    latitude = models.FloatField()
    longitude = models.FloatField()
    
    # Verification
    is_primary_station = models.BooleanField(default=False, help_text='Main station for this ward')
    distance_from_center_km = models.FloatField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'ward_station_mapping'
        unique_together = ['ward', 'station_name']
    
    def __str__(self):
        return f"{self.station_name} -> Ward {self.ward.ward_id}"