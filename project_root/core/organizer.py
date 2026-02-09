from __future__ import annotations
from pathlib import PurePosixPath
from typing import Optional
from metadata import FileMetadata
from classifier import ClassificationResult
from decision import DecisionResult, AUTO_ROUTE, MANUAL_REVIEW


# Constants

ROOT_FOLDER = "6th Sem College"
GLOBAL_MANUAL_REVIEW = "Manual Intervention Review"
LABS_FOLDER = "Labs"

CONTENT_TYPE_FOLDER_MAP = {
    "Text Book": "Text Book",
    "Notes": "Notes",
    "QPs": "QPs",
    "Assignments": "Assignments",
    "Important Questions": "Important Questions",
}

# Public accessible API

def resolve_destination(
    metadata: FileMetadata,
    classification: ClassificationResult,
    decision: DecisionResult,
) -> PurePosixPath:

    root = PurePosixPath(ROOT_FOLDER)

    # Rule 1: Global manual review
    if decision.action == MANUAL_REVIEW:
        return root / GLOBAL_MANUAL_REVIEW

    # Rule 2: Lab / Project Phase
    if classification.content_type == "Manual":
        return _resolve_lab_path(root, classification)

    # Rule 3: Theory subjects
    return _resolve_theory_path(root, classification)


# Helpers

def _resolve_lab_path(
    root: PurePosixPath,
    classification: ClassificationResult,
) -> PurePosixPath:
    labs_root = root / LABS_FOLDER

    if classification.subject:
        return labs_root / f"{classification.subject} Lab"

    # Fallback to Project Phase
    return labs_root / "Project Phase 1"


def _resolve_theory_path(
    root: PurePosixPath,
    classification: ClassificationResult,
) -> PurePosixPath:
    subject = classification.subject or GLOBAL_MANUAL_REVIEW
    subject_root = root / subject

    content_type = classification.content_type
    if content_type not in CONTENT_TYPE_FOLDER_MAP:
        return subject_root / GLOBAL_MANUAL_REVIEW

    base = subject_root / CONTENT_TYPE_FOLDER_MAP[content_type]

    # Notes -> Module folders
    if content_type == "Notes" and classification.module:
        return base / classification.module

    # Assignments -> Questions / Answers (future extension)
    return base
