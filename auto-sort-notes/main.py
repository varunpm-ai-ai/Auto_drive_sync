from src import auth, ingestion, classifier, drive_client, classroom_client, file_mapper, utils
from src.ingestion import iter_files,file_metadata
from src.utils import sha256_file
from src.classifier import detect_subject
from src.file_mapper import get_drive_folder,get_classroom_course
from src.drive_client import upload_file
from src.classroom_client import post_material
from pathlib import Path
import json

if __name__ == '__main__':
    print('🚀 Auto Sort Notes project initialized!')

    root = Path("data/samples")  # replace with your WhatsApp folder
    index_path = Path("output/index.json")
    index = json.loads(index_path.read_text()) if index_path.exists() else {}

    for file_path in iter_files(root):
        file_hash = sha256_file(file_path)
        if file_hash in index:
            print("🔹 Skipping duplicate:", file_path.name)
            continue

        meta = file_metadata(file_path)
        meta["hash"] = file_hash

        # Step 1: classify
        subject = detect_subject(file_path)
        meta["subject"] = subject

        # Step 2: map
        try:
            folder_id = get_drive_folder(subject)
            course_id = get_classroom_course(subject)
        except ValueError:
            print(f"⚠️ No mapping for subject: {subject}")
            index[file_hash] = meta
            continue

        # Step 3: upload/post
        drive_file_id = upload_file(str(file_path), folder_id)
        post_material(course_id, drive_file_id, title=file_path.name)

        meta["processed"] = True
        index[file_hash] = meta

    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_text(json.dumps(index, indent=2))
    print("✅ Workflow complete!")
