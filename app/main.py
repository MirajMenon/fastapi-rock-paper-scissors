import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routers import game_router
from sqlalchemy import text
from app.database.database import engine, Base, get_db, SessionLocal

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        db: SessionLocal = next(get_db())
        db.execute(text("SELECT 1"))
        logger.info("Database connected successfully")
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
    
    yield
    
    # Shutdown (cleanup if needed)
    logger.info("Application shutting down...")


app = FastAPI(title="Rock Paper Scissors API", lifespan=lifespan)

app.include_router(game_router.router)


@app.get("/")
def health_check():
    return {"status": "OK"}
