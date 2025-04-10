# Main.py

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from BackEnd.src.core.config import get_settings
from BackEnd.src.database.database import engine, Base
from BackEnd.src.api.endpoints import (
    users,
    basic,
    advanced,
    sentiment,
    visualization,
    auth,
    summarizer,
    bhasha_bot,
    translation,
)

from BackEnd.src.utils.logger import logger
from BackEnd.src.middleware.cors import setup_cors  # Import CORS middleware
from BackEnd.src.middleware.throttling import (
    ThrottleMiddleware,
)  # Import Throttling middleware
from BackEnd.src.middleware.rate_limiting import (
    RateLimitMiddleware,
)  # Import Rate limiting middleware
import os

# Create the database tables
Base.metadata.create_all(bind=engine)

# Get settings from config
settings = get_settings()

# Initialize FastAPI app
app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version,
)

# Apply CORS middleware
setup_cors(app)

# Apply Throttling middleware
app.add_middleware(ThrottleMiddleware)

# Apply Rate Limiting middleware
app.add_middleware(RateLimitMiddleware)

# Mount the visualizations directory for static file serving
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
visualizations_dir = "app/BackEnd/" + os.path.join(root_dir, "visualizations")
os.makedirs(visualizations_dir, exist_ok=True)
app.mount(
    "/BackEnd/visualizations",  # This should match the URL path used in visualization_service.py
    StaticFiles(
        directory="/app/BackEnd/visualizations"
    ),  # Use absolute path inside Docker container
    name="visualizations",
)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(basic.router)
app.include_router(advanced.router)
app.include_router(sentiment.router)
app.include_router(visualization.router)
app.include_router(summarizer.router)
app.include_router(bhasha_bot.router)
app.include_router(translation.router)


# Root endpoint
@app.get("/", tags=["Root"])
async def home():
    logger.info("Root endpoint accessed")
    return {
        "message": "Welcome to the Bhashasutra API",
        "status": "Running",
        "version": settings.api_version,
    }


# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info("Starting Bhashasutra API")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down Bhashasutra API")
