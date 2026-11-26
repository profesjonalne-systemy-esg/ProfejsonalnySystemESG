import os
import uuid
from pathlib import Path
from typing import BinaryIO

MAX_BYTES = 25 * 1024 * 1024
MIME_TYPES = {
    ".pdf": "application/pdf",
    ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".txt": "text/plain",
}


class UnsupportedType(ValueError):
    pass


class TooLarge(ValueError):
    pass


def upload_dir() -> Path:
    path = Path(os.getenv("UPLOAD_DIR", "data/uploads"))
    path.mkdir(parents=True, exist_ok=True)
    return path


def clean_name(filename: str | None) -> str:
    """Sama nazwa pliku, bez katalogów podanych przez przeglądarkę."""
    return (filename or "plik").replace("\\", "/").split("/")[-1][:255] or "plik"


def extension(filename: str) -> str:
    ext = Path(filename).suffix.lower()
    if ext not in MIME_TYPES:
        raise UnsupportedType(f"Nieobsługiwany format: {filename}. Dozwolone: PDF, XLSX, DOCX, TXT")
    return ext


def read_limited(stream: BinaryIO, filename: str) -> bytes:
    data = stream.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise TooLarge(f"Plik {filename} przekracza 25 MB")
    return data


def save(data: bytes, ext: str) -> str:
    """Zapisuje pod losową nazwą, więc pliki o tej samej nazwie się nie nadpisują."""
    path = upload_dir() / f"{uuid.uuid4().hex}{ext}"
    path.write_bytes(data)
    return str(path)
