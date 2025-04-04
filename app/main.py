from fastapi import FastAPI
import uvicorn

from .database import engine, Base
from .routers import flight_router
from .utils.logger import get_logger
from mcp_server import mcp

# Initialize logger
logger = get_logger(__name__)

# Create tables
Base.metadata.create_all(bind=engine)
logger.info("Database tables created successfully")

app = FastAPI(
    title="Bhindi's Flight Booking API",
    version="0.1.0"
)

# Include routers
app.include_router(flight_router.router)
logger.info("API routers initialized")

# Mount the MCP SSE server
app.mount("/mcp", app=mcp.sse_app())
logger.info("MCP SSE server mounted at /mcp")

@app.get("/")
def read_root():
    return {
        "message": "Welcome to Bhindi's Flight Booking API",
        "docs_url": "/docs",
        "mcp_url": "/mcp"
    }

@app.get("/health")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
