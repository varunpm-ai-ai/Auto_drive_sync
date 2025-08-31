import os
from pathlib import Path

# Root project name
PROJECT_NAME = "auto-sort-notes"

# Folder structure
folders = [
    f"{PROJECT_NAME}/src",
    f"{PROJECT_NAME}/tests",
    f"{PROJECT_NAME}/data/samples",
    f"{PROJECT_NAME}/output/logs",
    f"{PROJECT_NAME}/docs",
    f"{PROJECT_NAME}/scripts",
]

# Files with initial content
files = {
    f"{PROJECT_NAME}/.gitignore": """__pycache__/
*.py[cod]
*.log
.venv/
env/
venv/
.vscode/
.idea/
.DS_Store
Thumbs.db
token.json
client_secret.json
config.json
""",

    f"{PROJECT_NAME}/README.md": "# Auto Sort Notes\n\nA Python project that automatically classifies and uploads notes from WhatsApp to Google Drive and Classroom.\n",

    f"{PROJECT_NAME}/requirements.txt": """google-auth
google-auth-oauthlib
google-api-python-client
python-dotenv
pydantic
tqdm
python-magic; platform_system != "Windows"
python-magic-bin; platform_system == "Windows"
""",

    f"{PROJECT_NAME}/config.example.json": """{
  "whatsapp_root": "/path/to/WhatsApp/Media",
  "include_dirs": ["WhatsApp Documents", "WhatsApp Images"],
  "exclude_patterns": ["Status", ".thumbs", ".tmp"],
  "subjects": {
    "DSA": ["dsa", "data structure"],
    "OS": ["os", "operating system"]
  },
  "module_patterns": {
    "Module1": ["unit 1", "module 1"],
    "Module2": ["unit 2", "module 2"]
  },
  "textbook_keywords": ["textbook", "chapter"],
  "drive": {
    "root_folder_name": "CollegeNotes",
    "create_subject_folders": true
  },
  "classroom": {
    "enabled": false,
    "course_map": {}
  }
}
""",

    f"{PROJECT_NAME}/main.py": "from src import auth, ingestion, classifier, drive_client, classroom_client, file_mapper, utils\n\nif __name__ == '__main__':\n    print('🚀 Auto Sort Notes project initialized!')\n",

    f"{PROJECT_NAME}/src/__init__.py": "",
    f"{PROJECT_NAME}/src/auth.py": "# Google OAuth helpers\n",
    f"{PROJECT_NAME}/src/ingestion.py": "# Read WhatsApp media files\n",
    f"{PROJECT_NAME}/src/classifier.py": "# Classify files by subject/module/textbook\n",
    f"{PROJECT_NAME}/src/drive_client.py": "# Google Drive helper functions\n",
    f"{PROJECT_NAME}/src/classroom_client.py": "# Google Classroom integration\n",
    f"{PROJECT_NAME}/src/file_mapper.py": "# Map files to correct Drive folders\n",
    f"{PROJECT_NAME}/src/utils.py": "# Utility functions (hashing, slugify, etc.)\n",

    f"{PROJECT_NAME}/tests/__init__.py": "",
    f"{PROJECT_NAME}/tests/test_sorter.py": "# Unit tests go here\n",

    f"{PROJECT_NAME}/docs/project_report.md": "# Project Report\n\n## Abstract\n\n## Features\n\n## Future Scope\n",

    f"{PROJECT_NAME}/scripts/init_project.py": "# (This script itself!)\n"
}

def create_structure():
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
    for path, content in files.items():
        file_path = Path(path)
        if not file_path.exists():   # ✅ only create missing files
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"🆕 Created {file_path}")
        else:
            print(f"✔️ Skipped existing {file_path}")

if __name__ == "__main__":
    create_structure()
    print(f"\n✅ Project scaffold '{PROJECT_NAME}' is ready!")
