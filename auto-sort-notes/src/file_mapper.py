# Map files to correct Drive folders

import json
from pathlib import Path

CONFIG_PATH = Path("config.json")  # user copies from config.example.json

def load_config():
    if not CONFIG_PATH.exists():
        raise FileNotFoundError("config.json not found. Please copy from config.example.json")
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

config = load_config()
mappings = config.get("SUBJECT_MAPPINGS", {})

def get_drive_folder(subject: str) -> str:
    mapping = mappings.get(subject)
    if not mapping:
        raise ValueError(f"No Drive folder ID found for subject: {subject}")
    return mapping["drive_folder_id"]

def get_classroom_course(subject: str) -> str:
    mapping = mappings.get(subject)
    if not mapping:
        raise ValueError(f"No Classroom course ID found for subject: {subject}")
    return mapping["classroom_course_id"]
