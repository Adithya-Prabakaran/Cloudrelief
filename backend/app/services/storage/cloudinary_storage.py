"""
CloudinaryStorageService — real object storage swap-in for StorageService.

Needed because free compute hosts (Render's free web service, for one) have
an ephemeral filesystem: anything LocalStorageService wrote to disk is wiped
on every restart/redeploy, which silently destroys citizen-submitted photos.
Cloudinary's free tier gives persistent storage without needing AWS.

Configure with a single CLOUDINARY_URL env var (the "API Environment
variable" Cloudinary's dashboard shows you verbatim), then flip
STORAGE_PROVIDER=cloudinary.
"""
import cloudinary
import cloudinary.uploader

from app.core.config import settings
from app.services.storage.base import StorageService


def _public_id(key: str) -> str:
    # Cloudinary manages its own format suffix; keeping the file extension
    # out of the public_id avoids it being double-applied in delivery URLs.
    return key.rsplit(".", 1)[0] if "." in key else key


class CloudinaryStorageService(StorageService):
    def __init__(self):
        cloudinary.config(cloudinary_url=settings.CLOUDINARY_URL, secure=True)

    def upload_file(self, key: str, content: bytes, content_type: str | None = None) -> str:
        cloudinary.uploader.upload(
            content, public_id=_public_id(key), resource_type="image", overwrite=True
        )
        return key

    def get_file_url(self, key: str) -> str:
        # key already encodes "<public_id>.<ext>", which is exactly the
        # delivery path Cloudinary expects.
        cloud_name = cloudinary.config().cloud_name
        return f"https://res.cloudinary.com/{cloud_name}/image/upload/{key}"

    def delete_file(self, key: str) -> None:
        cloudinary.uploader.destroy(_public_id(key), resource_type="image")
