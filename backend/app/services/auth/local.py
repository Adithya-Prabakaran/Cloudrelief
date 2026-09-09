"""
LocalAuthService — JWT + bcrypt, stands in for Cognito.

To swap in real Cognito later: implement CognitoAuthService(AuthService)
using boto3's cognito-idp client (SignUp/InitiateAuth/GetUser), then flip
AUTH_PROVIDER=cognito in .env. Route handlers already only call the
AuthService interface, so nothing else changes.
"""
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import create_access_token, decode_access_token, hash_password, verify_password
from app.models.db import User, UserRole
from app.services.auth.base import AuthService


class LocalAuthService(AuthService):
    def register(self, db: Session, email: str, password: str, full_name: str | None, role: str) -> User:
        existing = db.query(User).filter(User.email == email).first()
        if existing:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Email already registered")

        user = User(
            email=email,
            password_hash=hash_password(password),
            full_name=full_name,
            role=UserRole(role),
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def login(self, db: Session, email: str, password: str) -> tuple[str, User]:
        user = db.query(User).filter(User.email == email).first()
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid email or password")

        token = create_access_token(subject=user.user_id, role=user.role.value)
        return token, user

    def verify_token(self, token: str) -> dict | None:
        return decode_access_token(token)
