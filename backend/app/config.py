import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY")

    # ENTRA_AZURE_CLIENT_ID = os.getenv("ENTRA_AZURE_CLIENT_ID")
    # ENTRA_AZURE_TENANT_ID = os.getenv("ENTRA_AZURE_TENANT_ID")
    # ENTRA_AZURE_CLIENT_SECRET = os.getenv("ENTRA_AZURE_CLIENT_SECRET")
    # MOCK_AUTH = os.getenv("MOCK_AUTH")
    # AUTHORITY = os.getenv("AUTHORITY")
    # ENTRA_AZURE_REDIRECT_URI = os.getenv("ENTRA_AZURE_REDIRECT_URI")
    # SCOPES = os.getenv("SCOPES")

    # ENTRA_AZURE_AUTHORITY = f"https://login.microsoftonline.com/{ENTRA_AZURE_TENANT_ID}"
