# from pathlib import Path
# from watcher import setup_logger, start_watcher, run_forever

# logger = setup_logger(log_file=Path("watcher.log"))

# path = Path(
#     r"C:\Users\DELL\AppData\Local\Packages\5319275A.WhatsAppDesktop_cv1g1gvanyjgm"
#     r"\LocalState\sessions\B7AF7A014325C70D65D45E4162CE8581436F7572"
#     r"\transfers\2026-06"
# )

# observer = start_watcher(path, recursive=False, logger=logger)
# run_forever(observer, logger)

# from pathlib import Path

# from classifier import classify
# from metadata import FileMetadata


# TEST_FILES = [
#     "Machine Learning Module 1 Notes.pdf",
#     "ML Assignment 2 Answers.pdf",
#     "Cloud Computing QP Jan 2024.pdf",
#     "BCT Textbook Blockchain.pdf",
#     "DevOps Lab Manual.pdf",
#     "Project Phase 1 Manual.pdf",
#     "WhatsApp Image 2026-02-05 at 1.15.46 PM.jpeg",
#     "document.pdf",
#     "scan123.pdf",
# ]


# def fake_metadata(filename: str) -> FileMetadata:
#     path = Path(filename)

#     return FileMetadata(
#         path=path,
#         name=path.name,
#         stem=path.stem,
#         extension=path.suffix.lower(),
#         size_bytes=0,
#         created_at=None,
#         modified_at=None,
#         accessed_at=None,
#         guessed_category="document",
#     )


# def run_tests():
#     print("\n=== CLASSIFIER TEST RESULTS ===\n")

#     for file in TEST_FILES:
#         metadata = fake_metadata(file)
#         result = classify(metadata)

#         print(f"File: {file}")
#         print(f"  Subject      : {result.subject}")
#         print(f"  Content Type : {result.content_type}")
#         print(f"  Module       : {result.module}")
#         print(f"  Confidence   : {result.confidence}")
#         print(f"  Reason       : {result.reason}")
#         print("-" * 60)


# if __name__ == "__main__":
#     run_tests()


