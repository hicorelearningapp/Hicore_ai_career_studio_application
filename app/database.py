from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from contextlib import contextmanager

# ---------------- Database URL ----------------
DATABASE_URL = "sqlite:///./app.db"

# ---------------- Engine & Session ----------------
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # Required for SQLite
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ---------------- Base for Models ----------------
Base = declarative_base()

# ---------------- Dependency for FastAPI ----------------
def get_db():
    """
    Yields a database session for FastAPI endpoints.
    Ensures session is closed after each request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------- Context manager for standalone DB operations ----------------
@contextmanager
def get_session():
    """
    Use this context manager for database operations outside FastAPI,
    like scripts or CLI tasks.
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
