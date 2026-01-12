import mysql.connector
import os
import environ
import time

class DBConnectionError(Exception):
    """Custom exception for database connection failures"""
    pass

class DBConnection:
    
    _max_retries = 3
    _retry_delay = 2  # seconds

    @classmethod
    def database_connection(cls):
        """
        Establishes database connection with retry logic.
        Reads DATABASE_KEYWORD from .env to determine Azure vs Local.
        Raises DBConnectionError if connection fails after all retries.
        """
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Force fresh read of .env file
        env = environ.Env()
        env_file = os.path.join(BASE_DIR, '.env')
        environ.Env.read_env(env_file, overwrite=True)
        
        # Read database keyword from .env file (defaults to "Local" if not set)
        keyword = env('DATABASE_KEYWORD', default='Local')
        print(f"[DB] Using {keyword} database configuration (from {env_file})")
        
        if keyword == "Azure":
            db_config = {
                'host': env('AZURE_DATABASE_HOST'),
                'user': env('AZURE_DATABASE_USER'),
                'password': env('AZURE_DATABASE_PASSWORD'),
                'database': env('DATABASE_NAME'),
                'client_flags': [mysql.connector.ClientFlag.SSL],
                'ssl_ca': os.path.join(BASE_DIR, 'certificates', 'DigiCertGlobalRootG2.crt.pem'),
                'connection_timeout': 30,
                'autocommit': True
            }
        else:
            db_config = {
                'host': env('LOCAL_DATABASE_HOST'),
                'user': env('LOCAL_DATABASE_USER'),
                'password': env('LOCAL_DATABASE_PASSWORD'),
                'database': env('DATABASE_NAME'),
                'connection_timeout': 30,
                'autocommit': True
            }
        
        last_error = None
        for attempt in range(cls._max_retries):
            try:
                connection = mysql.connector.connect(**db_config)
                if connection.is_connected():
                    return connection
            except mysql.connector.Error as err:
                last_error = err
                print(f"[Attempt {attempt + 1}/{cls._max_retries}] Database connection error: {err}")
                if attempt < cls._max_retries - 1:
                    time.sleep(cls._retry_delay)
        
        error_msg = f"Failed to connect to database after {cls._max_retries} attempts. Last error: {last_error}"
        print(f"CRITICAL: {error_msg}")
        raise DBConnectionError(error_msg)