from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings
import os

# Check if we should use SQLite (easier setup) or PostgreSQL
USE_SQLITE = os.environ.get("USE_SQLITE", "true").lower() == "true"

if USE_SQLITE:
    # SQLite - No installation required!
    SQLITE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "tourist_safety.db")
    DATABASE_URL = f"sqlite:///{SQLITE_PATH}"
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
    print(f"📦 Using SQLite database: {SQLITE_PATH}")
else:
    # PostgreSQL - Requires installation
    DATABASE_URL = settings.DATABASE_URL
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20
    )
    print(f"🐘 Using PostgreSQL database")

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)
