import os
from sqlmodel import SQLModel, create_engine, Session
from app import models  # noqa: F401  # Import to ensure models are registered

# Database URL from environment or default to SQLite file
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data.db")
engine = create_engine(DATABASE_URL, echo=False)

def init_db():
    """Create database tables."""
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session