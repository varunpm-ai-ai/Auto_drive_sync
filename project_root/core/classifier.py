from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
import re

from core.metadata import FileMetadata
from core.content_peek import ContentPeekResult


# Classification data schema

@dataclass
class ClassificationResult:
    subject: Optional[str]
    content_type: Optional[str]
    module: Optional[str]
    confidence: float
    reason: str

# Knowledge base

SUBJECT_KEYWORDS = {
    "Machine Learning": ["ml", "machine learning", "BCS602"],
    "Cloud Computing": ["cc", "cloud computing", "BCS601"],
    "Blockchain Technology": ["bct", "blockchain", "BCS613A"],
    "DevOps": ["devops", "BCSL657D"],
    "Indian Knowledge System": ["iks", "BIKS609"],
    "Yoga": ["yoga", "BYOK658"],
}

LAB_SUBJECT_KEYWORDS = {
    "Machine Learning": ["ml lab", "BCSL606"],
    "Cloud Computing": ["cc lab"],
    "DevOps": ["devops lab"],
}

CONTENT_TYPE_KEYWORDS = {
    "Text Book": ["textbook", "book"],
    "Notes": ["notes", "note", "module"],
    "QPs": ["qp", "question paper"],
    "Assignments": ["assignment", "asg"],
    "Important Questions": ["important", "imp", "quiz", "worksheet"],
    "Manual": ["manual", "lab", "program"],
}

GENERIC_NAMES = {
    "document",
    "scan",
    "image",
    "whatsappimage",
    "whatsappdocument",
}

# Normalising the strings
def _normalize(text: str) -> str:
    return re.sub(r"[\s\-_]", "", text.lower())

# Identifying generic names
def _is_generic_name(stem: str) -> bool:
    norm = _normalize(stem)
    return any(g in norm for g in GENERIC_NAMES)

# Detection logic
def _detect_subject(name: str) -> Optional[str]:
    norm_name = _normalize(name)

    # 1️ Detect LAB subjects 
    for subject, keywords in LAB_SUBJECT_KEYWORDS.items():
        for kw in keywords:
            if _normalize(kw) in norm_name:
                return subject

    # 2️ Detect THEORY subjects
    for subject, keywords in SUBJECT_KEYWORDS.items():
        for kw in keywords:
            if _normalize(kw) in norm_name:
                return subject

    return None

# Detect content type
def _detect_content_type(name: str) -> Optional[str]:
    norm_name = _normalize(name)

    for ctype, keywords in CONTENT_TYPE_KEYWORDS.items():
        for kw in keywords:
            if _normalize(kw) in norm_name:
                return ctype

    return None


def _detect_module(name: str) -> Optional[str]:
    match = re.search(r"(module|mod|m)\s*(\d)", name.lower())
    if match:
        return f"Module {match.group(2)}"
    return None


# Public accesable API

def classify(
    metadata: FileMetadata,
    content_hints: Optional[ContentPeekResult] = None
) -> ClassificationResult:

    name = metadata.stem
    confidence = 0.0
    reason = []

    subject = _detect_subject(name)
    if subject:
        confidence += 0.4
        reason.append("subject keyword match")

    content_type = _detect_content_type(name)
    if content_type:
        confidence += 0.3
        reason.append("content-type keyword match")

    module = None
    if content_type == "Notes":
        module = _detect_module(name)
        if module:
            confidence += 0.2
            reason.append("module detected")

    if not _is_generic_name(name):
        confidence += 0.1
        reason.append("non-generic filename")

    # Content peek if generic file name
    if content_hints:
        if content_hints.is_digital_text:
            confidence += 0.2
            reason.append("digital text detected via content peek")

        if content_hints.keywords:
            confidence += 0.1
            reason.append("keywords found in content peek")

        if content_hints.is_handwritten_likely:
            reason.append("handwritten content detected")

    confidence = round(min(confidence, 1.0), 2)

    if confidence < 0.7:
        reason.append("low confidence → manual review")

    return ClassificationResult(
        subject=subject,
        content_type=content_type,
        module=module,
        confidence=confidence,
        reason=", ".join(reason),
    )
