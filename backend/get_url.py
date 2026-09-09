import msal
import os
from dotenv import load_dotenv

load_dotenv()


# Use your exact settings
ENTRA_AZURE_CLIENT_ID = os.getenv("ENTRA_AZURE_CLIENT_ID")
ENTRA_AZURE_CLIENT_SECRET = os.getenv("ENTRA_AZURE_CLIENT_SECRET")
AUTHORITY = os.getenv("AUTHORITY")
ENTRA_AZURE_REDIRECT_URI = os.getenv("ENTRA_AZURE_REDIRECT_URI")

app = msal.ConfidentialClientApplication(
    client_id=ENTRA_AZURE_CLIENT_ID,
    authority=AUTHORITY,
    client_credential=ENTRA_AZURE_CLIENT_SECRET,
)

# Print the URL directly to your terminal
flow = app.initiate_auth_code_flow(
    scopes=["User.Read"], redirect_uri=ENTRA_AZURE_REDIRECT_URI
)
print("\n--- COPY AND PASTE THIS URL INTO YOUR BROWSER ---")
print(flow["auth_uri"])
print("------------------------------------------------\n")
