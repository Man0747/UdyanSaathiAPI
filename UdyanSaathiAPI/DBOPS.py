from .models import *  # Import the model class
import mysql.connector
from .DBConnection import DBConnection
from datetime import datetime, timedelta

# Get today's date


class PollutionDAO:
    @classmethod    
    def find_PollutionData_By_Station(cls, pol_station):
        dbconnection = DBConnection()
        connection = dbconnection.database_connection()
        cursor = connection.cursor()

        query = "SELECT distinct State,Station,City,AQI,PM25,PM10,NO2,OZONE,CO,AQI_Quality,Pol_Date FROM\
                 udyaansaathidata.hourlydata WHERE Station = %s and Pol_Date in\
                 (SELECT Max(Pol_Date) FROM udyaansaathidata.hourlydata WHERE Station = %s)\
        order by AQI desc\
                 limit 1;"
        cursor.execute(query, (pol_station,pol_station,))
        results = cursor.fetchall()

        pollution_list = []

        for row in results:
            pollution_instance = pollutionModel()
            pollution_instance.State = row[0]
            pollution_instance.Station = row[1]
            pollution_instance.City = row[2]
            pollution_instance.AQI = row[3]
            pollution_instance.PM25 = row[4]
            pollution_instance.PM10 = row[5]
            pollution_instance.NO2 = row[6]
            pollution_instance.OZONE = row[7]
            pollution_instance.CO = row[8]
            pollution_instance.AQI_Quality = row[9]

            # Assume that the Pol_Date is in the 10th position of the row
            pollution_instance.Pol_Date = row[10].strftime('%Y-%m-%d %H:%M:%S')
            
            # Call the clean method to format the Date field
            pollution_instance.clean()

            pollution_list.append(pollution_instance)

        cursor.close()
        connection.close()

        return pollution_list

    @classmethod    
    def find_Stations_By_City(cls, stationName):
       
        dbconnection = DBConnection()
        connection = dbconnection.database_connection()
        cursor = connection.cursor()
        stationName = '%' + stationName + '%'
        query = "SELECT DISTINCT Station FROM udyaansaathidata.stations WHERE City LIKE %s OR Station LIKE %s;"
        
        cursor.execute(query, (stationName,stationName,))
        results = cursor.fetchall()

        station_list = []

        for row in results:
            pollution_instance = stationModel()
            pollution_instance.Station = row[0]

            station_list.append(pollution_instance)

        cursor.close()
        connection.close()

        return station_list

    @classmethod    
    def find_All_Stations(cls):
       
        dbconnection = DBConnection()
        connection = dbconnection.database_connection()
        cursor = connection.cursor()
       
        query = "SELECT Distinct City FROM udyaansaathidata.stations "
       
        # cursor.execute(query, (stationName,stationName,))
        cursor.execute(query, ())
        results = cursor.fetchall()

        all_station_list = []

        for row in results:
            pollution_instance = stationModel()
            pollution_instance.Station = row[0]

            all_station_list.append(pollution_instance)

        cursor.close()
        connection.close()

        return all_station_list
    @classmethod


    def find_Top6_Most_Polluted_Cities(cls,todate):
       
        dbconnection = DBConnection()
        connection = dbconnection.database_connection()
        cursor = connection.cursor()   

        # stationName = '%' + stationName + '%'
        
        query = "SELECT City, MAX(AQI) AS AQI, MAX(PM25) AS PM25, MAX(PM10) AS PM10, MAX(CO) AS CO, MAX(OZONE) AS OZONE, MAX(SO2) AS SO2, MAX(NO2) AS NO2, MAX(NH3) AS NH3\
                FROM udyaansaathidata.pollutiondata\
                WHERE Pol_Date BETWEEN (\
                        SELECT MAX(Pol_Date) - INTERVAL %s DAY FROM udyaansaathidata.pollutiondata\
                    ) AND (\
                        SELECT MAX(Pol_Date) FROM udyaansaathidata.pollutiondata\
                    )\
                GROUP BY City\
                HAVING \
                AQI > 0\
                AND PM25 > 0\
                AND PM10 > 0\
                AND CO > 0\
                AND OZONE > 0\
                AND SO2 > 0\
                AND NO2 > 0\
                AND NH3 > 0\
                ORDER BY AQI DESC\
                LIMIT 6;"
        
       
        cursor.execute(query,(todate,))
        results = cursor.fetchall()

        Top10Cities_List = []

        for row in results:
            pollution_instance = Top10CitiesModel()
            pollution_instance.City = row[0]
            pollution_instance.AQI = row[1]
            pollution_instance.PM25 = row[2]
            pollution_instance.PM10 = row[3]
            pollution_instance.CO = row[4]
            pollution_instance.OZONE = row[5]
            pollution_instance.SO2 = row[6]
            pollution_instance.NO2 = row[7]
            pollution_instance.NH3 = row[8]

            Top10Cities_List.append(pollution_instance)

        cursor.close()
        connection.close()

        return Top10Cities_List
    
    @classmethod
    def find_Top6_Least_Polluted_Cities(cls,todate):
       
        dbconnection = DBConnection()
        connection = dbconnection.database_connection()
        cursor = connection.cursor()   

        # stationName = '%' + stationName + '%'
        
        query = "SELECT City, Min(AQI) AS AQI, Min(PM25) AS PM25, Min(PM10) AS PM10, Min(CO) AS CO, Min(OZONE) AS OZONE, Min(SO2) AS SO2, Min(NO2) AS NO2, Min(NH3) AS NH3\
                FROM udyaansaathidata.pollutiondata\
                WHERE Pol_Date BETWEEN (\
                        SELECT MAX(Pol_Date) - INTERVAL %s DAY FROM udyaansaathidata.pollutiondata\
                    ) AND (\
                        SELECT MAX(Pol_Date) FROM udyaansaathidata.pollutiondata\
                    )\
                GROUP BY City\
                HAVING \
                AQI > 0\
                AND PM25 > 0\
                AND PM10 > 0\
                AND CO > 0\
                AND OZONE > 0\
                AND SO2 > 0\
                AND NO2 > 0\
                AND NH3 > 0\
                ORDER BY AQI asc\
                LIMIT 6;"
        
       
        cursor.execute(query,(todate,))
        results = cursor.fetchall()

        Top10LeastCities_List = []

        for row in results:
            pollution_instance = Top10LeastCitiesModel()
            pollution_instance.City = row[0]
            pollution_instance.AQI = row[1]
            pollution_instance.PM25 = row[2]
            pollution_instance.PM10 = row[3]
            pollution_instance.CO = row[4]
            pollution_instance.OZONE = row[5]
            pollution_instance.SO2 = row[6]
            pollution_instance.NO2 = row[7]
            pollution_instance.NH3 = row[8]

            Top10LeastCities_List.append(pollution_instance)

        cursor.close()
        connection.close()

        return Top10LeastCities_List
    
    @classmethod
    def find_GraphData(cls,pol_City,todate):
       
        dbconnection = DBConnection()
        connection = dbconnection.database_connection()
        cursor = connection.cursor()   

        # stationName = '%' + stationName + '%'
        
        query = "SELECT\
                    City,\
                    Pol_Date,\
                    ROUND(AVG(AQI), 2) AS AQI,\
                    ROUND(AVG(NH3), 2) AS NH3,\
                    ROUND(AVG(PM10), 2) AS PM10,\
                    ROUND(AVG(PM25), 2) AS PM25,\
                    ROUND(AVG(NO2), 2) AS NO2,\
                    ROUND(AVG(SO2), 2) AS SO2,\
                    ROUND(AVG(CO), 2) AS CO,\
                    ROUND(AVG(OZONE), 2) AS OZONE\
                FROM\
                    udyaansaathidata.pollutiondata\
                WHERE\
                    City = %s\
                    AND Pol_Date BETWEEN (\
                        SELECT MAX(Pol_Date) - INTERVAL %s DAY FROM udyaansaathidata.pollutiondata\
                    ) AND (\
                        SELECT MAX(Pol_Date) FROM udyaansaathidata.pollutiondata\
                    )\
                GROUP BY\
                    City, Pol_Date\
                ORDER BY\
                    Pol_Date;"
                        
        cursor.execute(query,(pol_City,todate,))
        results = cursor.fetchall()

        GraphData_List = []

        for row in results:
            pollution_instance = graphDataModel()
            pollution_instance.City = row[0]
            pollution_instance.Pol_Date = row[1].strftime('%Y-%m-%d')
            pollution_instance.AQI = row[2]
            pollution_instance.NH3 = row[3]
            pollution_instance.PM10 = row[4]
            pollution_instance.PM25 = row[5]
            pollution_instance.NO2 = row[6]
            pollution_instance.SO2 = row[7]
            pollution_instance.CO = row[8]
            pollution_instance.OZONE = row[9]
            GraphData_List.append(pollution_instance)

        cursor.close()
        connection.close()

        return GraphData_List
    @classmethod
    def find_MetroCities_Data(cls,todate):
        dbconnection = DBConnection()
        connection = dbconnection.database_connection()
        cursor = connection.cursor()   

        # stationName = '%' + stationName + '%'
        
        query = "SELECT\
                City,\
                ROUND(AVG(AQI), 2) AS AQI,\
                ROUND(AVG(NH3), 2) AS NH3,\
                ROUND(AVG(PM10), 2) AS PM10,\
                ROUND(AVG(PM25), 2) AS PM25,\
                ROUND(AVG(NO2), 2) AS NO2,\
                ROUND(AVG(SO2), 2) AS SO2,\
                ROUND(AVG(CO), 2) AS CO,\
                ROUND(AVG(OZONE), 2) AS OZONE\
                FROM\
                udyaansaathidata.pollutiondata\
                WHERE\
                Pol_Date BETWEEN (\
                        SELECT MAX(Pol_Date) - INTERVAL %s DAY FROM udyaansaathidata.pollutiondata\
                    ) AND (\
                        SELECT MAX(Pol_Date) FROM udyaansaathidata.pollutiondata\
                    )\
                AND City IN ('Bengaluru', 'Hyderabad', 'Chennai', 'Kolkata', 'Mumbai', 'Delhi')\
                GROUP BY\
                City\
                ORDER BY\
                AQI DESC;"
        
       
        cursor.execute(query,(todate,))
        results = cursor.fetchall()

        TopMetroCitiesModel_List = []

        for row in results:
            pollution_instance = TopMetroCitiesModel()
            pollution_instance.City = row[0]
            pollution_instance.AQI = row[1]
            pollution_instance.PM25 = row[2]
            pollution_instance.PM10 = row[3]
            pollution_instance.CO = row[4]
            pollution_instance.OZONE = row[5]
            pollution_instance.SO2 = row[6]
            pollution_instance.NO2 = row[7]
            pollution_instance.NH3 = row[8]

            TopMetroCitiesModel_List.append(pollution_instance)

        cursor.close()
        connection.close()

        return TopMetroCitiesModel_List
    @classmethod
    def find_Aqi_Calendar_Data(cls,pol_Station):
        
        dbconnection = DBConnection()
        connection = dbconnection.database_connection()
        cursor = connection.cursor()   

        # stationName = '%' + stationName + '%'
        
        query = "SELECT distinct Station,AQI,Pol_Date\
                FROM udyaansaathidata.pollutiondata\
                WHERE Station = %s\
                order by pol_date"
        
        cursor.execute(query,(pol_Station,))
        results = cursor.fetchall()

        AqiCalendarModel_List = []

        for row in results:
            pollution_instance = AqiCalendarModel()
            pollution_instance.Station = row[0]
            pollution_instance.AQI = row[1]
            pollution_instance.Pol_Date = row[2].strftime('%Y-%m-%d')
            AqiCalendarModel_List.append(pollution_instance)

        cursor.close()
        connection.close()

        return AqiCalendarModel_List
    
    def find_ML_Data(pol_Station):
       
        dbconnection = DBConnection()
        connection = dbconnection.database_connection()
        cursor = connection.cursor()   

        # stationName = '%' + stationName + '%'
        
        query = "SELECT * FROM udyaansaathidata.mldata\
                 where Station = %s;"
        
        cursor.execute(query,(pol_Station,))
        results = cursor.fetchall()

        MLmodel_List = []

        for row in results:
            pollution_instance = MlModel()
            pollution_instance.Station = row[0]
            pollution_instance.Day1 = row[1]
            pollution_instance.Day2 = row[2]
            pollution_instance.Day3 = row[3]
            pollution_instance.Day4 = row[4]
            pollution_instance.Day5 = row[5]

            MLmodel_List.append(pollution_instance)

        cursor.close()
        connection.close()

        return MLmodel_List
    

    @classmethod    
    def find_Map_Data(cls):
        dbconnection = DBConnection()
        connection = dbconnection.database_connection()
        cursor = connection.cursor()

        query = "SELECT \
                hd.State,\
                hd.Station,\
                hd.City,\
                hd.AQI,\
                hd.AQI_Quality,\
                hd.Longitude,\
                hd.Latitude,\
                hd.Pol_Date \
            FROM \
                udyaansaathidata.hourlydata AS hd\
            INNER JOIN (\
                SELECT \
                    Station,\
                    MAX(Pol_Date) AS MaxPolDate \
                FROM \
                    udyaansaathidata.hourlydata \
                GROUP BY \
                    Station\
            ) AS sub\
            ON \
                hd.Station = sub.Station AND hd.Pol_Date = sub.MaxPolDate;"
        cursor.execute(query, ())
        results = cursor.fetchall()

        mapData_list = []

        for row in results:
            mapData_instance = mapDataModel()
            mapData_instance.State = row[0]
            mapData_instance.Station = row[1]
            mapData_instance.City = row[2]
            mapData_instance.AQI = row[3]
            # mapData_instance.PM25 = row[4]
            # mapData_instance.PM10 = row[5]
            # mapData_instance.NO2 = row[6]
            # mapData_instance.OZONE = row[7]
            # mapData_instance.CO = row[8]
            mapData_instance.AQI_Quality = row[4]
            mapData_instance.Longitude = row[5]
            mapData_instance.Latitude = row[6]

            # Assume that the Pol_Date is in the 10th position of the row
            mapData_instance.Pol_Date = row[7].strftime('%Y-%m-%d %H:%M:%S')
            
            # Call the clean method to format the Date field
            mapData_instance.clean()

            mapData_list.append(mapData_instance)

        cursor.close()
        connection.close()

        return mapData_list
    @classmethod
    def find_StationsCoordinates(cls,pol_station):
        dbconnection = DBConnection()
        connection = dbconnection.database_connection()
        cursor = connection.cursor()

        query = "SELECT Station,Longitude,Latitude FROM udyaansaathidata.stations where Station = %s Limit 1"
        cursor.execute(query, (pol_station,))
        results = cursor.fetchall()
        
        StationsCoordinatesList=[]

        for row in results:
            StationsCoordinates = StationsCoordinatesModel()
            StationsCoordinates.Station = row[0]
            StationsCoordinates.Longitude = row[1]
            StationsCoordinates.Latitude = row[2]

            StationsCoordinatesList.append(StationsCoordinates)

        cursor.close()
        connection.close()

        return StationsCoordinatesList
