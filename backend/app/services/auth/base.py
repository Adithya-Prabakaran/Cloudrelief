"""
AuthService interface. Route handlers must depend on this ABC only —
never import LocalAuthService (or a future CognitoAuthService) directly.
Get an instance via app.services.factory.get_auth_service().
"""
from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy.orm import Session


class AuthService(ABC):
    @abstractmethod
    def register(self, db: Session, email: str, password: str, full_name: str | None, role: str) -> Any:
        """Create a user account and return the created user record."""
        raise NotImplementedError

    @abstractmethod
    def login(self, db: Session, email: str, password: str) -> tuple[str, Any]:
        """Verify credentials and return (access_token, user_record)."""
        raise NotImplementedError

    @abstractmethod
    def verify_token(self, token: str) -> dict | None:
        """Return decoded token claims (sub, role) or None if invalid/expired."""
        raise NotImplementedError
