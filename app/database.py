"""
database.py — Database Engine & Session Setup
==============================================
Uses SQLModel with SQLite for local development.
Switch the DATABASE_URL to a PostgreSQL connection string for production.
"""

import os
from sqlmodel import SQLModel, create_engine, Session

# ---------------------------------------------------------------------------
# Database URL Configuration
# ---------------------------------------------------------------------------
# LOCAL DEV  : sqlite:///database.db   (file created in project root)
# PRODUCTION : postgresql://user:password@host:port/dbname
#
# Set the environment variable DATABASE_URL to override the default.
# ---------------------------------------------------------------------------
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///database.db")

# For SQLite we need connect_args to allow multi-threaded access (FastAPI is async).
connect_args = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}

engine = create_engine(DATABASE_URL, echo=True, connect_args=connect_args)


def create_db_and_tables():
    """Create all tables defined by SQLModel metadata."""
    SQLModel.metadata.create_all(engine)


def get_session():
    """
    Dependency generator for FastAPI routes.
    Yields a SQLModel Session and ensures it is closed after use.
    """
    with Session(engine) as session:
        yield session
