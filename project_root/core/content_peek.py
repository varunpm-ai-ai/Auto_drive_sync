from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import List
from pypdf import PdfReader
from PIL import Image
import numpy as np

# Content peek scema 

@dataclass
class ContentPeekResult:
    is_digital_text: bool
    is_scanned: bool
    is_handwritten_likely: bool
    keywords: List[str]
    reason: str
    

# Public API

# Generic meta data peek
def peek_content(path: Path) -> ContentPeekResult:
    ext = path.suffix.lower()

    if ext == ".pdf":
        return _peek_pdf(path)

    if ext in {".jpg", ".jpeg", ".png"}:
        return _peek_image(path)

    return ContentPeekResult(
        is_digital_text=False,
        is_scanned=False,
        is_handwritten_likely=False,
        keywords=[],
        reason="unsupported file type for content peek",
    )
    

# Pdf content peek
def _peek_pdf(path: Path) -> ContentPeekResult:
    try:
        reader = PdfReader(str(path))
        if not reader.pages:
            return _empty_result("empty pdf")

        page = reader.pages[0]
        text = page.extract_text()

        if text and len(text.strip()) > 50:
            keywords = _extract_keywords(text)
            return ContentPeekResult(
                is_digital_text=True,
                is_scanned=False,
                is_handwritten_likely=False,
                keywords=keywords,
                reason="extractable digital text found on first page",
            )

        # No text → likely scanned
        return ContentPeekResult(
            is_digital_text=False,
            is_scanned=True,
            is_handwritten_likely=False,
            keywords=[],
            reason="no extractable text, likely scanned pdf",
        )

    except Exception as e:
        return _empty_result(f"pdf peek failed: {e}")


def _peek_image(path: Path) -> ContentPeekResult:
    try:
        with Image.open(path) as img:
            img = img.convert("L")  # grayscale
            arr = np.array(img)
            variance = arr.var()

            # Low variance -> Mustbe scanned or handwritten
            is_handwritten_likely = variance < 500

            return ContentPeekResult(
                is_digital_text=False,
                is_scanned=True,
                is_handwritten_likely=is_handwritten_likely,
                keywords=[],
                reason="image variance heuristic applied",
            )

    except Exception as e:
        return _empty_result(f"image peek failed: {e}")


def _extract_keywords(text: str, limit: int = 5) -> List[str]:
    words = [
        w.lower()
        for w in text.split()
        if len(w) > 4 and w.isalpha()
    ]
    return list(dict.fromkeys(words))[:limit]


def _empty_result(reason: str) -> ContentPeekResult:
    return ContentPeekResult(
        is_digital_text=False,
        is_scanned=False,
        is_handwritten_likely=False,
        keywords=[],
        reason=reason,
    )
