# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import APIRouter, Depends

# Define your database URL (e.g., PostgreSQL, SQLite, etc.)
DATABASE_URL = "postgresql://user:password@db:5432/yourdbname"

# Create an engine that will communicate with the database
engine = create_engine(DATABASE_URL, echo=True)

# Create a sessionmaker to handle database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


router = APIRouter()

# Dependency function to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
