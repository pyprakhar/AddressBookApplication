"""
Database initialization script.
Run this script to create the database and tables if they don't already exist.
This is useful when cloning the repository or setting up a new environment.
"""

from app.database.db import Base, engine
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db():
    """Initialize the database by creating all tables."""
    try:
        logger.info("Initializing database...")
        Base.metadata.create_all(bind=engine)
        logger.info("✓ Database initialized successfully")
        logger.info("✓ All tables created")
        return True
    except Exception as exc:
        logger.error(f"✗ Failed to initialize database: {exc}")
        raise exc

if __name__ == "__main__":
    init_db()
