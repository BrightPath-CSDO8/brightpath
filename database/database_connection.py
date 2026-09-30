import os
import time
import pyodbc

from dotenv import load_dotenv

pyodbc.pooling = False


load_dotenv()


SERVER = os.getenv("AZURE_SQL_SERVER")
DATABASE = os.getenv("AZURE_SQL_DATABASE")
USERNAME = os.getenv("AZURE_SQL_USERNAME")
PASSWORD = os.getenv("AZURE_SQL_PASSWORD")


def get_connection():
    connection_string = (
        "Driver={ODBC Driver 18 for SQL Server};"
        f"Server=tcp:{SERVER},1433;"
        f"Database={DATABASE};"
        f"Uid={USERNAME};"
        f"Pwd={PASSWORD};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=60;"
    )

    max_attempts = 5

    for attempt in range(1, max_attempts + 1):
        try:
            print(f"Connecting to Azure SQL (attempt {attempt})...")

            connection = pyodbc.connect(connection_string)

            print("Azure SQL connection established.")
            return connection

        except pyodbc.Error as error:
            print(f"Connection attempt {attempt} failed.")

            if attempt < max_attempts:
                print("Waiting 10 seconds before retrying...")
                time.sleep(10)
            else:
                print("Unable to connect to Azure SQL.")
                raise error
