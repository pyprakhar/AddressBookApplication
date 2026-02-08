from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database.db import engine, SessionLocal
from fastapi.responses import JSONResponse
from fastapi import status
import logging
from sqlalchemy import text

logger = logging.getLogger("uvicorn.error")
logging.basicConfig(level=logging.INFO)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application startup")
    yield
    logger.info("Application shutdown")

app = FastAPI(lifespan=lifespan)

@app.get("/")
def root():
    return {"message": "App is running"}

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


