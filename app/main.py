"""
main.py — FastAPI Application Entry Point
==========================================
Run locally with:
    uvicorn app.main:app --reload

Swagger UI :  http://127.0.0.1:8000/docs
ReDoc       :  http://127.0.0.1:8000/redoc
"""

from contextlib import asynccontextmanager
import logging
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import create_db_and_tables
from app.api.routes import router as api_router


# ---------------------------------------------------------------------------
# Lifespan — runs on startup / shutdown
# ---------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create database tables on startup."""
    create_db_and_tables()
    logging.getLogger("chicken_freshness_checker").info("Database tables ensured")
    yield  # App runs here
    # Shutdown logic (if any) goes after yield


# ---------------------------------------------------------------------------
# FastAPI Application
# ---------------------------------------------------------------------------
app = FastAPI(
    title="Chicken Freshness Checker API",
    description=(
        "Backend for an IoT-based Chicken Meat Spoilage Detection Device. "
        "Receives sensor data, processes it through an ML pipeline, and "
        "serves live results to an Android companion app."
    ),
    version="0.1.0",
    lifespan=lifespan,
)


# ---------------------------------------------------------------------------
# CORS — allow the Android app and local dev tools to call the API
# ---------------------------------------------------------------------------
# Configure logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger("chicken_freshness_checker")

# CORS — allow configured origins (set CORS_ORIGINS env var as comma-separated list)
cors_env = os.getenv("CORS_ORIGINS")
if cors_env:
    allow_origins = [o.strip() for o in cors_env.split(",") if o.strip()]
else:
    # Default to allow all for backward compatibility; set CORS_ORIGINS in production
    allow_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info("CORS origins: %s", allow_origins)


# ---------------------------------------------------------------------------
# Register Routes
# ---------------------------------------------------------------------------
app.include_router(api_router)


# ---------------------------------------------------------------------------
# Root health-check
# ---------------------------------------------------------------------------
@app.get("/", tags=["Health"])
def root():
    return {"status": "running", "service": "Chicken Freshness Checker API"}
