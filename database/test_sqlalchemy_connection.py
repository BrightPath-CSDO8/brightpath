from sqlalchemy import create_engine, text
from database_connection import get_connection


engine = create_engine(
    "mssql+pyodbc://",
    creator=get_connection,
    pool_pre_ping=True,
    pool_recycle=300
)


with engine.connect() as connection:
    result = connection.execute(
        text("SELECT 1 AS TestConnection")
    )

    row = result.fetchone()

    print("SQLAlchemy Azure SQL connection successful.")
    print("TestConnection:", row[0])