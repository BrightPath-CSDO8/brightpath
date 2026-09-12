import struct
import time
import pyodbc

from azure.identity import DeviceCodeCredential


SERVER = "brightpath-sql-server.database.windows.net"
DATABASE = "brightpath-db"

SQL_COPT_SS_ACCESS_TOKEN = 1256

credential = DeviceCodeCredential()


def get_connection():
    token = credential.get_token(
        "https://database.windows.net/.default"
    ).token

    token_bytes = token.encode("utf-16-le")

    token_struct = struct.pack(
        f"<I{len(token_bytes)}s",
        len(token_bytes),
        token_bytes
    )

    connection_string = (
        "Driver={ODBC Driver 18 for SQL Server};"
        f"Server=tcp:{SERVER},1433;"
        f"Database={DATABASE};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=60;"
    )

    max_attempts = 5

    for attempt in range(1, max_attempts + 1):
        try:
            print(f"Connecting to Azure SQL (attempt {attempt})...")

            connection = pyodbc.connect(
                connection_string,
                attrs_before={
                    SQL_COPT_SS_ACCESS_TOKEN: token_struct
                }
            )

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