# Google Classroom integration

from googleapiclient.discovery import build
from src.auth import get_credentials

creds = get_credentials()
classroom_service = build("classroom", "v1", credentials=creds)

def post_material(course_id: str, drive_file_id: str, title: str = None):
    """
    Posts a Drive file as Course Material to the given Classroom course.
    """
    title = title or "New uploaded note"

    material = {
        "driveFile": {
            "driveFile": {
                "id": drive_file_id
            }
        }
    }

    coursework = {
        "title": title,
        "materials": [material]
    }

    # Create course material
    created = classroom_service.courses().courseWorkMaterials().create(
        courseId=course_id,
        body=coursework
    ).execute()

    print(f"✅ Posted to Classroom: {created.get('title')} (ID: {created.get('id')})")
    return created.get("id")
