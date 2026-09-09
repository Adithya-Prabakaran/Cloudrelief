"""
LocalStorageService — stands in for S3. Writes files under
LOCAL_STORAGE_DIR and serves them back via the /files/{key} route
(see app/routers/files.py).

To swap in real S3 later: implement S3StorageService(StorageService) using
boto3 (upload_fileobj + generate_presigned_url), then flip
STORAGE_PROVIDER=s3 in .env. No other file in the app needs to change.
"""
import os
from pathlib import Path

from app.core.config import settings
from app.services.storage.base import StorageService


class LocalStorageService(StorageService):
    def __init__(self, base_dir: str | None = None):
        self.base_dir = Path(base_dir or settings.LOCAL_STORAGE_DIR)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def upload_file(self, key: str, content: bytes, content_type: str | None = None) -> str:
        # content_type is accepted for interface parity with a future S3
        # implementation (which would set it as object metadata); the local
        # filesystem doesn't need it.
        dest = self.base_dir / key
        dest.parent.mkdir(parents=True, exist_ok=True)
        with open(dest, "wb") as f:
            f.write(content)
        return key

    def get_file_url(self, key: str) -> str:
        return f"{settings.FILES_BASE_URL}/{key}"

    def delete_file(self, key: str) -> None:
        path = self.base_dir / key
        if path.exists():
            os.remove(path)

    def read_file(self, key: str) -> bytes:
        """Local-only helper used by the /files/{key} route to stream bytes back."""
        path = self.base_dir / key
        with open(path, "rb") as f:
            return f.read()
