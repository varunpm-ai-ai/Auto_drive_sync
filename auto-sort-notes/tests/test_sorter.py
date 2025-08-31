# Unit tests go here

import os
from pathlib import Path
from src.ingestion import iter_files

def test_iter_files(tmp_path):
    f1 = tmp_path / "note.pdf"
    f1.write_bytes(b"hello")
    f2 = tmp_path / "image.jpg"
    f2.write_bytes(b"\xff\xd8\xff")
    files = list(iter_files(tmp_path))
    assert len(files) == 2