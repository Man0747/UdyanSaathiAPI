from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import pollutionModel
from .serializer import *
from .DBOPS import PollutionDAO

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
