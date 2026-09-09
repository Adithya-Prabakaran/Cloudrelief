import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.session import engine
from app.models.db import Base
from app.routers import auth, files, incidents

logging.basicConfig(level=logging.INFO)
logging.info("CORS_ORIGINS=%s", settings.CORS_ORIGINS)

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    # Simple create_all instead of migrations, in keeping with the
    # "keep it simple / key-based" schema approach for this local stand-in.
    Base.metadata.create_all(bind=engine)


app.include_router(auth.router)
app.include_router(incidents.router)
app.include_router(files.router)


@app.get("/health")
def health():
    return {"status": "ok", "app": settings.APP_NAME}
