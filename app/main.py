from fastapi import FastAPI

from .database import engine, Base
from .routers import flight_router
from .utils.logger import get_logger

# Initialize logger
logger = get_logger(__name__)

# Create tables
Base.metadata.create_all(bind=engine)
logger.info("Database tables created successfully")

app = FastAPI(
    title="Bhindi's Flight Booking API",
    version="1.0.0"
)

# Include routers
app.include_router(flight_router.router)
logger.info("API routers initialized")

@app.get("/")
def read_root():
    return {
        "message": "Welcome to Bhindi's Flight Booking API",
        "docs_url": "/docs"
    }
