from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from metadata import FileMetadata
from classifier import ClassificationResult

# Decision actions

AUTO_ROUTE = "AUTO_ROUTE"
NEEDS_CONTENT_PEEK = "NEEDS_CONTENT_PEEK"
MANUAL_REVIEW = "MANUAL_REVIEW"

# Decision schema

@dataclass
class DecisionResult:
    action: str
    reason: str
    subject: Optional[str] 
    content_type: Optional[str]
    confidence: float
    
# Core decision logic

CONFIDENCE_THRESHOLD = 0.7

def make_decision(
    metadata: FileMetadata,
    classification: ClassificationResult,
    content_peek_attempted: bool = False,
) -> DecisionResult:
    
    # First decision -> Auto rout
    if (
        classification.subject
        and classification.content_type
        and classification.confidence >= CONFIDENCE_THRESHOLD
    ):
        return DecisionResult(
            action=AUTO_ROUTE,
            reason="confident classification",
            subject=classification.subject,
            content_type=classification.content_type,
            confidence=classification.confidence,
        )
        
    # Second decition -> Content Peek
    if not content_peek_attempted and _supports_content_peek(metadata):
        return DecisionResult(
            action=NEEDS_CONTENT_PEEK,
            reason="low confidence, attempting content peek",
            subject=classification.subject,
            content_type=classification.content_type,
            confidence=classification.confidence,
        )

    # Third decision -> manual review
    return DecisionResult(
        action=MANUAL_REVIEW,
        reason="unable to classify confidently",
        subject=classification.subject,
        content_type=classification.content_type,
        confidence=classification.confidence,
    )
    

# Public accesable API

def _supports_content_peek(metadata: FileMetadata) -> bool:

    return metadata.extension in {".pdf", ".jpg", ".jpeg", ".png"}