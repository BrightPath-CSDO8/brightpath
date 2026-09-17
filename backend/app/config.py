import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///edulearn.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
