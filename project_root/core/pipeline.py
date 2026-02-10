from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from core.metadata import extract_metadata, FileMetadata
from core.classifier import classify, ClassificationResult
from core.decision import (
    make_decision,
    DecisionResult,
    AUTO_ROUTE,
    NEEDS_CONTENT_PEEK,
    MANUAL_REVIEW,
)
from core.content_peek import peek_content, ContentPeekResult

# Pipeline Scema

@dataclass
class PipelineResult:
    metadata: FileMetadata
    classification: ClassificationResult
    decision: DecisionResult
    content_peek: Optional[ContentPeekResult] = None
    
# Core pipeline

def run_pipeline(path, source: str = "unknown") -> PipelineResult:
    # Step 1: metadata
    metadata = extract_metadata(path, source=source)

    # Step 2: initial classification
    classification = classify(metadata)

    # Step 3: decision
    decision = make_decision(
        metadata=metadata,
        classification=classification,
        content_peek_attempted=False,
    )
    
    content_peek_result = None

    # Step 4: optional content peek escalation
    if decision.action == NEEDS_CONTENT_PEEK:
        
        content_peek_result = peek_content(path)

        # Step 5: re-classify with content hints
        classification = classify(
            metadata,
            content_hints=content_peek_result,
        )
        
        # Step 6: final decision (peek attempted)
        decision = make_decision(
            metadata=metadata,
            classification=classification,
            content_peek_attempted=True,
        )

    # Step 5: final outcome
    return PipelineResult(
        metadata=metadata,
        classification=classification,
        decision=decision,
    )