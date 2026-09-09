"""
StorageService interface. Route handlers must depend on this ABC only —
never import LocalStorageService (or a future S3StorageService) directly.
Get an instance via app.services.factory.get_storage_service().
"""
from abc import ABC, abstractmethod


class StorageService(ABC):
    @abstractmethod
    def upload_file(self, key: str, content: bytes, content_type: str | None = None) -> str:
        """Store `content` under `key`. Returns the storage key (not a URL)."""
        raise NotImplementedError

    @abstractmethod
    def get_file_url(self, key: str) -> str:
        """Return a URL the frontend can load the file from.

        Local impl returns a static /files/:key path. A future
        S3StorageService would return a presigned URL here instead —
        callers never need to know the difference.
        """
        raise NotImplementedError

    @abstractmethod
    def delete_file(self, key: str) -> None:
        raise NotImplementedError
