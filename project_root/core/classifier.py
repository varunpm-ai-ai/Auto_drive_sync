from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
import re
from metadata import FileMetadata


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
    "Machine Learning": ["ml", "machine learning"],
    "Cloud Computing": ["cc", "cloud"],
    "Blockchain Technology": ["bct", "blockchain"],
    "DevOps": ["devops"],
    "Indian Knowledge System": ["iks"],
    "Yoga": ["yoga"],
}

CONTENT_TYPE_KEYWORDS = {
    "Text Book": ["textbook", "book"],
    "Notes": ["notes", "note", "module"],
    "QPs": ["qp", "question paper"],
    "Assignments": ["assignment", "asg"],
    "Important Questions": ["important", "imp"],
    "Manual": ["manual", "lab"],
}

GENERIC_NAMES = {
    "document",
    "scan",
    "image",
    "whatsapp image",
    "whatsapp document",
}

# Helper functions

# Normalise all the text fields 
def _normalize(text: str) -> str:
    return text.lower().strip()

# Generic Names handler
def _is_generic_name(stem: str) -> bool:
    stem = _normalize(stem)
    return any(g in stem for g in GENERIC_NAMES)

# Subject detection handler
def _detect_subject(name: str) -> Optional[str]:
    name = _normalize(name)
    for subject, keywords in SUBJECT_KEYWORDS.items():
        if any(k in name for k in keywords):
            return subject
    return None

# Keyword detection handler
def _detect_content_type(name: str) -> Optional[str]:
    name = _normalize(name)
    for ctype, keywords in CONTENT_TYPE_KEYWORDS.items():
        if any(k in name for k in keywords):
            return ctype
    return None

# Module detection handler
def _detect_module(name: str) -> Optional[str]:
    match = re.search(r"(module|mod|m)\s*(\d)", name.lower())
    if match:
        return f"Module {match.group(2)}"
    return None

# Public accesable api 
def classify(metadata: FileMetadata) -> ClassificationResult:
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