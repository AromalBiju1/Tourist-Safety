"""
Alternative Database Configuration for SQLite
Use this if you don't have PostgreSQL installed
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# SQLite database file path
SQLITE_DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "tourist_safety.db")
DATABASE_URL = f"sqlite:///{SQLITE_DB_PATH}"

# Create database engine for SQLite
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # Required for SQLite
)

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


# Instructions to switch to SQLite:
# 1. Rename database.py to database_postgres.py
# 2. Rename this file (database_sqlite.py) to database.py
# 3. Remove PostGIS geometry column from city.py model
# 4. Run: python scripts/seed_database.py
