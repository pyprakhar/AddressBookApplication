from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os 
from sqlalchemy.orm import Session


load_dotenv()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL")

# Create the SQLAlchemy engine and session factory
engine = create_engine(
    DATABASE_URL,
    connect_args = {"check_same_thread": False}
)

# Create a configured "Session" class and a base class for declarative models
SessionLocal = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine
)

# Dependency function to get a database session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Base class for declarative models
Base = declarative_base()