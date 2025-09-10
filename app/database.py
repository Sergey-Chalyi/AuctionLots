from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import DATABASE_URL
from .models import Base

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_tables():
    """Create all database tables."""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Dependency to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
