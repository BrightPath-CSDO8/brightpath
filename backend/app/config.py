import os

from dotenv import load_dotenv
from database.database_connection import get_connection

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///edulearn.db")
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://127.0.0.1:5000")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


if Config.SQLALCHEMY_DATABASE_URI.startswith("mssql"):
    Config.SQLALCHEMY_ENGINE_OPTIONS = {
        "creator": get_connection,
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }
