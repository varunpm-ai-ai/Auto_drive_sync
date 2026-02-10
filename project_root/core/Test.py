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


# from pathlib import Path
# from decision import (
#     make_decision,
#     AUTO_ROUTE,
#     NEEDS_CONTENT_PEEK,
#     MANUAL_REVIEW,
# )
# from metadata import FileMetadata
# from classifier import ClassificationResult


# def fake_metadata(ext=".pdf"):
#     return FileMetadata(
#         path=Path(f"test{ext}"),
#         name=f"test{ext}",
#         stem="test",
#         extension=ext,
#         size_bytes=1000,
#         created_at=None,
#         modified_at=None,
#         accessed_at=None,
#         guessed_category="document",
#     )


# def print_result(label, decision):
#     print(f"{label}")
#     print(f"  action     : {decision.action}")
#     print(f"  reason     : {decision.reason}")
#     print(f"  confidence : {decision.confidence}")
#     print("-" * 50)


# def test_confident_classification():
#     print("TEST 1: Confident classification → AUTO_ROUTE")

#     metadata = fake_metadata(".pdf")

#     classification = ClassificationResult(
#         subject="Machine Learning",
#         content_type="Notes",
#         module="Module 1",
#         confidence=0.9,
#         reason="strong signals",
#     )

#     decision = make_decision(
#         metadata=metadata,
#         classification=classification,
#         content_peek_attempted=False,
#     )

#     print_result("Expected AUTO_ROUTE", decision)


# def test_needs_content_peek():
#     print("TEST 2: Low confidence → NEEDS_CONTENT_PEEK")

#     metadata = fake_metadata(".pdf")

#     classification = ClassificationResult(
#         subject=None,
#         content_type=None,
#         module=None,
#         confidence=0.3,
#         reason="weak signals",
#     )

#     decision = make_decision(
#         metadata=metadata,
#         classification=classification,
#         content_peek_attempted=False,
#     )

#     print_result("Expected NEEDS_CONTENT_PEEK", decision)


# def test_manual_review_after_peek():
#     print("TEST 3: Still low confidence → MANUAL_REVIEW")

#     metadata = fake_metadata(".jpg")

#     classification = ClassificationResult(
#         subject=None,
#         content_type=None,
#         module=None,
#         confidence=0.2,
#         reason="handwritten or unclear",
#     )

#     decision = make_decision(
#         metadata=metadata,
#         classification=classification,
#         content_peek_attempted=True,
#     )

#     print_result("Expected MANUAL_REVIEW", decision)


# if __name__ == "__main__":
#     test_confident_classification()
#     test_needs_content_peek()
#     test_manual_review_after_peek()

# from pathlib import Path

# from content_peek import peek_content


# def print_result(label, result):
#     print(label)
#     print(f"  is_digital_text       : {result.is_digital_text}")
#     print(f"  is_scanned            : {result.is_scanned}")
#     print(f"  is_handwritten_likely : {result.is_handwritten_likely}")
#     print(f"  keywords              : {result.keywords}")
#     print(f"  reason                : {result.reason}")
#     print("-" * 60)


# def test_digital_pdf():
#     print("TEST 1: Digital PDF (should detect text)")
#     path = Path("../tests/sample_digital.pdf")
#     result = peek_content(path)
#     print_result("Expected: digital text", result)


# def test_scanned_pdf():
#     print("TEST 2: Scanned PDF (no text)")
#     path = Path("../tests/sample_scanned.pdf")
#     result = peek_content(path)
#     print_result("Expected: scanned pdf", result)


# def test_image():
#     print("TEST 3: Image (handwritten heuristic)")
#     path = Path("../tests/sample_image.jpg")
#     result = peek_content(path)
#     print_result("Expected: image heuristic", result)


# def test_unsupported_file():
#     print("TEST 4: Unsupported file type")
#     path = Path("../tests/sample.txt")
#     result = peek_content(path)
#     print_result("Expected: unsupported fallback", result)


# if __name__ == "__main__":
#     test_digital_pdf()
#     test_scanned_pdf()
#     test_image()
#     test_unsupported_file()

# from pathlib import PurePosixPath, Path

# from organizer import resolve_destination
# from metadata import FileMetadata
# from classifier import ClassificationResult
# from decision import DecisionResult, AUTO_ROUTE, MANUAL_REVIEW


# def fake_metadata():
#     return FileMetadata(
#         path=Path("dummy.pdf"),
#         name="dummy.pdf",
#         stem="dummy",
#         extension=".pdf",
#         size_bytes=1234,
#         created_at=None,
#         modified_at=None,
#         accessed_at=None,
#         guessed_category="document",
#     )


# def print_result(label, path):
#     print(label)
#     print(f"  resolved path: {path}")
#     print("-" * 60)


# def test_theory_notes_module():
#     print("TEST 1: Theory subject → Notes → Module")

#     classification = ClassificationResult(
#         subject="Machine Learning",
#         content_type="Notes",
#         module="Module 1",
#         confidence=0.9,
#         reason="strong signals",
#     )

#     decision = DecisionResult(
#         subject="Machine Learning",
#         content_type="Notes",
#         action=AUTO_ROUTE,
#         confidence=0.9,
#         reason="confident classification",
#     )

#     path = resolve_destination(fake_metadata(), classification, decision)
#     print_result("Expected: 6th Sem College/Machine Learning/Notes/Module 1", path)


# def test_assignments():
#     print("TEST 2: Theory subject → Assignments")

#     classification = ClassificationResult(
#         subject="Cloud Computing",
#         content_type="Assignments",
#         module=None,
#         confidence=0.8,
#         reason="assignment detected",
#     )

#     decision = DecisionResult(
#         subject="Cloud Computing",
#         content_type="Assignments",
#         action=AUTO_ROUTE,
#         confidence=0.8,
#         reason="confident classification",
#     )

#     path = resolve_destination(fake_metadata(), classification, decision)
#     print_result("Expected: 6th Sem College/Cloud Computing/Assignments", path)


# def test_lab_manual():
#     print("TEST 3: Lab manual")

#     classification = ClassificationResult(
#         subject="DevOps",
#         content_type="Manual",
#         module=None,
#         confidence=0.8,
#         reason="lab manual",
#     )

#     decision = DecisionResult(
#         subject="DevOps",
#         content_type="Manual",
#         action=AUTO_ROUTE,
#         confidence=0.8,
#         reason="confident classification",
#     )

#     path = resolve_destination(fake_metadata(), classification, decision)
#     print_result("Expected: 6th Sem College/Labs/DevOps Lab", path)


# def test_global_manual_review():
#     print("TEST 4: Global manual review")

#     classification = ClassificationResult(
#         subject=None,
#         content_type=None,
#         module=None,
#         confidence=0.2,
#         reason="low confidence",
#     )

#     decision = DecisionResult(
#         subject=None,
#         content_type=None,
#         action=MANUAL_REVIEW,
#         confidence=0.2,
#         reason="manual review required",
#     )

#     path = resolve_destination(fake_metadata(), classification, decision)
#     print_result("Expected: 6th Sem College/Manual Intervention Review", path)


# def test_subject_manual_fallback():
#     print("TEST 5: Subject present but unknown content type")

#     classification = ClassificationResult(
#         subject="Blockchain Technology",
#         content_type=None,
#         module=None,
#         confidence=0.6,
#         reason="partial classification",
#     )

#     decision = DecisionResult(
#         subject="Blockchain Technology",
#         content_type=None,
#         action=AUTO_ROUTE,
#         confidence=0.6,
#         reason="auto route with fallback",
#     )

#     path = resolve_destination(fake_metadata(), classification, decision)
#     print_result(
#         "Expected: 6th Sem College/Blockchain Technology/Manual Intervention Review",
#         path,
#     )


# if __name__ == "__main__":
#     test_theory_notes_module()
#     test_assignments()
#     test_lab_manual()
#     test_global_manual_review()
#     test_subject_manual_fallback()


# from pathlib import Path
# from pipeline import run_pipeline


# def print_result(label, result):
#     print(label)
#     print(f"  file           : {result.metadata.name}")
#     print(f"  subject        : {result.classification.subject}")
#     print(f"  content_type   : {result.classification.content_type}")
#     print(f"  module         : {result.classification.module}")
#     print(f"  confidence     : {result.classification.confidence}")
#     print(f"  decision       : {result.decision.action}")
#     print(f"  reason         : {result.decision.reason}")
#     if result.content_peek:
#         print(f"  content_peek   : {result.content_peek.reason}")
#     print("-" * 70)


# def test_auto_route_notes():
#     print("TEST 1: Confident notes → AUTO_ROUTE")

#     path = Path("../tests/sample_digital.pdf")
#     result = run_pipeline(path, source="test")

#     print_result("Expected: AUTO_ROUTE, Notes", result)


# def test_escalation_to_peek_then_auto():
#     print("TEST 2: Generic name → peek → AUTO_ROUTE")

#     path = Path("../tests/document.pdf")  # generic name but digital text
#     result = run_pipeline(path, source="test")

#     print_result("Expected: NEEDS_PEEK → AUTO_ROUTE", result)


# def test_escalation_to_manual_review():
#     print("TEST 3: Scanned / handwritten → MANUAL_REVIEW")

#     path = Path("../tests/sample_scanned.pdf")
#     result = run_pipeline(path, source="test")

#     print_result("Expected: MANUAL_REVIEW", result)


# def test_image_manual_review():
#     print("TEST 4: Image → MANUAL_REVIEW")

#     path = Path("../tests/sample_image.jpg")
#     result = run_pipeline(path, source="test")

#     print_result("Expected: MANUAL_REVIEW", result)


# if __name__ == "__main__":
#     test_auto_route_notes()
#     test_escalation_to_peek_then_auto()
#     test_escalation_to_manual_review()
#     test_image_manual_review()
