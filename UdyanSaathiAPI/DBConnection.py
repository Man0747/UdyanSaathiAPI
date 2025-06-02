import mysql.connector
import os
import environ

class DBConnection:
    

    # keyword = "Azure"

    keyword = "Azure"
    # keyword = "Azure"

    # CONDITION TO CHECK THE DATABASE KEYWORD TO USE
    if(keyword == "Azure"):
        #CONFIGURATION FOR DATABASE CONNECTION 
        @classmethod
        def database_connection(self):
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            env = environ.Env()
            # Read environment variables from .env file if present
            environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
            # Azure_Host = env('AZURE_DATABASE_HOST')
            db_config = {
                'host': env('AZURE_DATABASE_HOST'),
                'user': env('AZURE_DATABASE_USER'),
                'password': env('AZURE_DATABASE_PASSWORD'),
                'database': env('DATABASE_NAME'),
                'client_flags': [mysql.connector.ClientFlag.SSL],
                'ssl_ca': os.path.join(BASE_DIR, 'certificates', 'DigiCertGlobalRootG2.crt.pem')

            }
            # CONNECTING TO DATABASE
            try:
                connection = mysql.connector.connect(**db_config)
                return connection
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                return None
    else:
        #CONFIGURATION FOR DATABASE CONNECTION 
        @classmethod
        def database_connection(self):
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            env = environ.Env()
            # Read environment variables from .env file if present
            environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
            db_config = {
                'host': env('LOCAL_DATABASE_HOST'),
                'user': env('LOCAL_DATABASE_USER'),
                'password': env('LOCAL_DATABASE_PASSWORD'),
                'database': env('DATABASE_NAME')
            }
            # CONNECTING TO DATABASE
            try:
                connection = mysql.connector.connect(**db_config)
                return connection
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                return None
     
    # CLOSING THE DATABASE CONNECTION