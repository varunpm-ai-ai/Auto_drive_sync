from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import json
import os

SCOPES = ["https://www.googleapis.com/auth/drive.file"]
TOKEN_FILE = "token.json"

flow = InstalledAppFlow.from_client_secrets_file(
    "credentials.json", SCOPES
)
creds = flow.run_local_server(port=0)

# SAVE TOKEN EXPLICITLY
with open(TOKEN_FILE, "w") as token:
    token.write(creds.to_json())

service = build("drive", "v3", credentials=creds)

print("Authentication successful! token.json created.")
