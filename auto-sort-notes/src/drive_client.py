# Google Drive helper functions

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from src.auth import get_credentials

creds = get_credentials()
drive_service = build("drive", "v3", credentials=creds)

def upload_file(file_path: str, folder_id: str):
    """
    Uploads a file to Google Drive inside the specified folder.
    If a file with same name exists, it creates a new version (optional: dedupe logic can be added later).
    """
    file_metadata = {
        "name": file_path.split("/")[-1],
        "parents": [folder_id]
    }

    media = MediaFileUpload(file_path, resumable=True)
    file = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id, name"
    ).execute()

    print(f"✅ Uploaded: {file['name']} (ID: {file['id']})")
    return file['id']