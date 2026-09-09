"""
Serves uploaded files back to the frontend. Only meaningful for
STORAGE_PROVIDER=local — once S3 is wired in, StorageService.get_file_url()
returns a presigned S3 URL directly and this route is unused (but harmless
to leave in place).
"""
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import Response

from app.services.factory import get_storage_service
from app.services.storage.local import LocalStorageService

router = APIRouter(prefix="/files", tags=["files"])


@router.get("/{key:path}")
def get_file(key: str):
    storage = get_storage_service()
    if not isinstance(storage, LocalStorageService):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Local file serving disabled")

    try:
        content = storage.read_file(key)
    except FileNotFoundError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "File not found")

    return Response(content=content, media_type="application/octet-stream")
