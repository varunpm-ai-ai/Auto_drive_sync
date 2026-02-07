from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any
import os
from pypdf import PdfReader
from docx import Document
from pptx import Presentation
from PIL import Image, ExifTags


# File meta data schema
@dataclass
class FileMetadata:
    path: Path
    name: str
    stem: str
    extension: str
    
    size_bytes: int
    created_at: datetime
    modified_at: datetime
    accessed_at: datetime
    
    guessed_category: str
    source: str = "unknown"
    ingested_at: datetime = field(default_factory=datetime.utcnow)
    
    format_metadata: Dict[str, Any] = field(default_factory=dict)
    

# Get Universal Meta data of documents
def _extract_universal_metadata(path: Path) -> FileMetadata:
    # Status information
    stat = path.stat()
    # .Extention data 
    extension = path.suffix.lower()
        
    if extension in {".pdf", ".docx", ".pptx"}:
       guessed_category = "document"
    elif extension in {".jpg", ".jpeg", ".png"}:
       guessed_category = "image"
    else:
       guessed_category = "unknown"
           
    return FileMetadata(
        path=path,
        name=path.name,
        stem=path.stem,
        extension=extension,
        size_bytes=stat.st_size,
        created_at=datetime.fromtimestamp(stat.st_ctime),
        modified_at=datetime.fromtimestamp(stat.st_mtime),
        accessed_at=datetime.fromtimestamp(stat.st_atime),
        guessed_category=guessed_category,
)


# .pdf extention meta data    
def _extract_pdf_metadata(path: Path) -> Dict[str, Any]:
    try:
        reader = PdfReader(str(path))
        info = reader.metadata or {}

        return {
            "pages": len(reader.pages),
            "title": info.get("/Title"),
            "author": info.get("/Author"),
            "encrypted": reader.is_encrypted,
        }
    except Exception as e:
        return {"error": str(e)}
    

# .doc extention meta data 
def _extract_docx_metadata(path: Path) -> Dict[str, Any]:
    try:
        doc = Document(str(path))
        props = doc.core_properties

        return {
            "author": props.author,
            "title": props.title,
            "created": props.created,
            "modified": props.modified,
        }
    except Exception as e:
        return {"error": str(e)}


# .pptx extention meta data
def _extract_pptx_metadata(path: Path) -> Dict[str, Any]:
    try:
        prs = Presentation(str(path))

        return {
            "slides": len(prs.slides),
            "title": prs.core_properties.title,
            "author": prs.core_properties.author,
            "created": prs.core_properties.created,
        }
    except Exception as e:
        return {"error": str(e)}


# imgae extention meta data 
def _extract_image_metadata(path: Path) -> Dict[str, Any]:
    try:
        with Image.open(path) as img:
            data = {
                "format": img.format,
                "width": img.width,
                "height": img.height,
                "mode": img.mode,
            }

            exif = img._getexif()
            if exif:
                readable_exif = {
                    ExifTags.TAGS.get(k, k): v
                    for k, v in exif.items()
                }
                data["exif"] = readable_exif

            return data
    except Exception as e:
        return {"error": str(e)}
    

# Public accesable API 
def extract_metadata(path: Path, source: str = "unknown") -> FileMetadata:
    if not path.exists() or not path.is_file():
        raise FileNotFoundError(f"Invalid file: {path}")

    metadata = _extract_universal_metadata(path)
    metadata.source = source

    ext = metadata.extension

    if ext == ".pdf":
        metadata.format_metadata = _extract_pdf_metadata(path)
    elif ext == ".docx":
        metadata.format_metadata = _extract_docx_metadata(path)
    elif ext == ".pptx":
        metadata.format_metadata = _extract_pptx_metadata(path)
    elif ext in {".jpg", ".jpeg", ".png"}:
        metadata.format_metadata = _extract_image_metadata(path)

    return metadata


        
        