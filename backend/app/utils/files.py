import hashlib
from pathlib import Path

from fastapi import UploadFile


def compute_sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def save_upload(upload_dir: Path, upload: UploadFile, raw: bytes) -> Path:
    upload_dir.mkdir(parents=True, exist_ok=True)
    file_path = upload_dir / upload.filename
    counter = 1
    while file_path.exists():
        stem = Path(upload.filename).stem
        suffix = Path(upload.filename).suffix
        file_path = upload_dir / f"{stem}_{counter}{suffix}"
        counter += 1
    file_path.write_bytes(raw)
    return file_path
