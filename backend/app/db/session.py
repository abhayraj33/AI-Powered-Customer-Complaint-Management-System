"""
Ye file database se connection banati hai.
Jo bhi DATABASE_URL .env me daala hai, wahi yaha use hoga.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    Ye function har API request ke liye ek fresh database
    connection deta hai, aur request khatam hone pe close kar deta hai.
    FastAPI ke 'Depends' ke saath use hota hai.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Ye saari tables create kar deta hai (agar already nahi hain)."""
    from app.db import models  # import zaroori hai taaki tables register ho
    Base.metadata.create_all(bind=engine)