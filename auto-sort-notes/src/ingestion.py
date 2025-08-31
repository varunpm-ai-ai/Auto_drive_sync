# Read WhatsApp media files

from pathlib import Path
from typing import Iterator, List, Optional, Union
import mimetypes
import os
from datetime import datetime

ALLOWED_EXT = {'.pdf', '.docx', '.doc', '.pptx', '.txt', '.jpg', '.jpeg', '.png'}

def iter_files(root: Union[str, Path],
               allowed_ext: Optional[set]=None,
               ignore_hidden: bool=True) -> Iterator[Path]:
    root = Path(root)
    allowed_ext = allowed_ext or ALLOWED_EXT
    if not root.exists():
        return
    for p in root.rglob('*'):
        if not p.is_file():
            continue
        if ignore_hidden and p.name.startswith('.'):
            continue
        if p.suffix.lower() in allowed_ext:
            yield p
        

def file_metadata(path):
    st = path.stat()
    mime, _ = mimetypes.guess_type(str(path))
    return {
        "path": str(path),
        "name": path.name,
        "ext": path.suffix.lower(),
        "size": st.st_size,
        "mtime": datetime.fromtimestamp(st.st_mtime).isoformat(),
        "ctime": datetime.fromtimestamp(st.st_ctime).isoformat(),
        "mime": mime or "application/octet-stream"
    }