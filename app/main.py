"""
main.py — FastAPI Application Entry Point
==========================================
Run locally with:
    uvicorn app.main:app --reload

Swagger UI :  http://127.0.0.1:8000/docs
ReDoc       :  http://127.0.0.1:8000/redoc
"""

from contextlib import asynccontextmanager
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
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Tighten this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
