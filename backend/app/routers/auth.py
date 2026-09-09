from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.schemas import LoginRequest, RegisterRequest, TokenResponse
from app.services.factory import get_auth_service

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    auth_service = get_auth_service()
    user = auth_service.register(
        db, email=payload.email, password=payload.password, full_name=payload.full_name, role="citizen"
    )
    token, _ = auth_service.login(db, email=payload.email, password=payload.password)
    return TokenResponse(access_token=token, role=user.role.value, user_id=user.user_id, email=user.email)


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    auth_service = get_auth_service()
    token, user = auth_service.login(db, email=payload.email, password=payload.password)
    return TokenResponse(access_token=token, role=user.role.value, user_id=user.user_id, email=user.email)
