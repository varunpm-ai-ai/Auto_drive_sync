from pdfminer.high_level import extract_text

def extract_pdf_text(path, max_pages=3):
    """Extract text from first N pages of a PDF."""
    try:
        text = extract_text(path, maxpages=max_pages)
        return text or ""
    except Exception as e:
        print(f"Error extracting {path}: {e}")
        return ""
