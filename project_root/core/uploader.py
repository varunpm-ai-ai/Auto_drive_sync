from __future__ import annotations
from pathlib import Path,PurePosixPath
from typing import Dict, Optional
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from config.settings import DRIVE_ROOT_ID

SCOPES = ["https://www.googleapis.com/auth/drive.file"]

# Start drive service via token 
def _get_drive_service():
    creds = Credentials.from_authorized_user_file(
        "token.json", SCOPES
    )
    return build("drive", "v3", credentials=creds)

# Create folder if does not exhists 
def _get_or_create_folder(
    service,
    parent_id: str,
    folder_name: str,
) -> str:
    query = (
        f"mimeType='application/vnd.google-apps.folder' "
        f"and name='{folder_name}' "
        f"and '{parent_id}' in parents "
        f"and trashed=false"
    )

    response = service.files().list(
        q=query,
        spaces="drive",
        fields="files(id, name)",
    ).execute()

    files = response.get("files", [])

    if files:
        return files[0]["id"]
    
    folder_metadata = {
        "name": folder_name,
        "mimeType": "application/vnd.google-apps.folder",
        "parents": [parent_id],
    }

    folder = service.files().create(
        body=folder_metadata,
        fields="id",
    ).execute()

    return folder["id"]

# Check the file paths 
def ensure_folder_path(
    service,
    logical_path: PurePosixPath,
) -> str:
    
    current_parent = DRIVE_ROOT_ID

    # Skip root name if included
    parts = list(logical_path.parts)
    if parts and parts[0] == logical_path.root:
        parts = parts[1:]

    for folder_name in parts:
        current_parent = _get_or_create_folder(
            service,
            parent_id=current_parent,
            folder_name=folder_name,
        )

    return current_parent

# Check if file exhists 
def _file_exists(
    service,
    parent_id: str,
    filename: str,
) -> Optional[str]:
    query = (
        f"name='{filename}' "
        f"and '{parent_id}' in parents "
        f"and trashed=false"
    )

    response = service.files().list(
        q=query,
        spaces="drive",
        fields="files(id, name)",
    ).execute()

    files = response.get("files", [])
    return files[0]["id"] if files else None

# Upload the file 
def upload_file(
    local_path: Path,
    logical_drive_path: PurePosixPath,
) -> str:

    service = _get_drive_service()

    # Ensure folders
    folder_id = ensure_folder_path(service, logical_drive_path)

    # Check if file already exists
    existing_file_id = _file_exists(
        service,
        parent_id=folder_id,
        filename=local_path.name,
    )

    if existing_file_id:
        return existing_file_id

    media = MediaFileUpload(
        local_path,
        resumable=True,
    )

    file_metadata = {
        "name": local_path.name,
        "parents": [folder_id],
    }

    uploaded = service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id",
    ).execute()

    return uploaded["id"]







