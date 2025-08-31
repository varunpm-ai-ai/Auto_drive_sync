# Utility functions (hashing, slugify, etc.)

import hashlib
import re

def sha256_file(path, chunk_size=1024*1024):
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        for chunk in iter(lambda: fh.read(chunk_size), b''):
            h.update(chunk)
    return h.hexdigest()


def normalize_text(text: str) -> str:
    """
    Lowercase, remove extra spaces and non-alphanumeric characters.
    Useful for keyword matching in PDF/classifier.
    """
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)          
    text = re.sub(r'[^a-z0-9 ]', '', text)    
    return text.strip()