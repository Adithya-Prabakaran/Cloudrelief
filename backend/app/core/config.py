"""
Central app configuration, loaded from environment variables (see .env.example).

Every *_PROVIDER flag here selects a concrete service implementation in
app/services/factory.py. This file has no cloud-specific logic — it only
reads env vars. When AWS/Oracle providers are added, only .env changes,
never this file.
"""
import os
from pathlib import Path


def _bool(val: str, default: bool = False) -> bool:
    if val is None:
        return default
    return val.strip().lower() in ("1", "true", "yes", "on")


class Settings:
    # --- General ---
    APP_NAME: str = "CloudRelief"
    ENV: str = os.getenv("ENV", "development")

    # --- Database (Postgres locally, stands in for DynamoDB later) ---
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://cloudrelief:cloudrelief@localhost:5432/cloudrelief",
    )

    # --- Auth / JWT ---
    JWT_SECRET: str = os.getenv("JWT_SECRET", "dev-secret-change-me")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRE_MINUTES: int = int(os.getenv("JWT_EXPIRE_MINUTES", "1440"))

    # --- Service provider switches ---
    STORAGE_PROVIDER: str = os.getenv("STORAGE_PROVIDER", "local")  # local | cloudinary | s3
    AUTH_PROVIDER: str = os.getenv("AUTH_PROVIDER", "local")  # local | cognito
    NOTIFY_PROVIDER: str = os.getenv("NOTIFY_PROVIDER", "console")  # console | sns
    CLASSIFIER_PROVIDER: str = os.getenv("CLASSIFIER_PROVIDER", "mock")  # mock | rekognition

    # --- Local storage (stands in for S3) ---
    LOCAL_STORAGE_DIR: str = os.getenv(
        "LOCAL_STORAGE_DIR", str(Path(__file__).resolve().parents[2] / "storage" / "uploads")
    )
    FILES_BASE_URL: str = os.getenv("FILES_BASE_URL", "http://localhost:8000/files")

    # --- Cloudinary (used when STORAGE_PROVIDER=cloudinary) ---
    CLOUDINARY_URL: str = os.getenv("CLOUDINARY_URL", "")

    # --- CORS ---
    CORS_ORIGINS: list[str] = [
        origin.strip()
        for origin in os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:5174").split(",")
        if origin.strip()
    ]

    # --- Severity scoring constants (see app/core/severity.py) ---
    URGENCY_WEIGHT: float = float(os.getenv("URGENCY_WEIGHT", "0.2"))
    DENSITY_CAP: float = float(os.getenv("DENSITY_CAP", "5"))
    DENSITY_WEIGHT: float = float(os.getenv("DENSITY_WEIGHT", "1.0"))
    ALERT_THRESHOLD: float = float(os.getenv("ALERT_THRESHOLD", "0.6"))
    DENSITY_RADIUS_KM: float = float(os.getenv("DENSITY_RADIUS_KM", "5"))
    DENSITY_WINDOW_HOURS: float = float(os.getenv("DENSITY_WINDOW_HOURS", "24"))


settings = Settings()
