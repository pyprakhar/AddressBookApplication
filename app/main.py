from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database.db import Base, engine, SessionLocal
from fastapi.responses import JSONResponse
from fastapi import status
import logging
from sqlalchemy import text
from app.api.address import address_router

# Set up logging
logger = logging.getLogger("uvicorn.error")
logging.basicConfig(level=logging.INFO)

# Lifespan context manager for startup and shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application startup")
    yield
    logger.info("Application shutdown")

# Initialize FastAPI application with lifespan for startup and shutdown events
app = FastAPI(lifespan=lifespan, title="Address Book API", description="API for managing addresses with geolocation data", version="1.0.0")

# Create the database tables if they don't exist
try:
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully")
    logger.info("Database tables created successfully")
except Exception as exc:
    print(f"Failed to create database tables: {exc}")
    logger.exception("Failed to create database tables")
    raise exc

# Root endpoint to verify that the application is running
@app.get("/")
def root():
    return {"message": "App is running"}

# Health check endpoint to verify database connectivity
@app.get(
        "/health_check/db",
          tags=["Health"],
          summary="Check database connectivity",
          description="Endpoint to verify if the application can connect to the database."
          )
def health_check():
    db = None
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        logger.info("Database connection healthy")
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "status": "ok",
                "database": "connected"
            }
        )
    except Exception as exc:
        logger.exception("Database health check failed:", exc)
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "error",
                "database": "disconnected"
            }
        )
    finally:
        if db:
            db.close()


# Include the address router using advance python practices for better modularity and maintainability and logging
logger.info("Including address router")
app.include_router(address_router)
