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
]
