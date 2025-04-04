# Main.py

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from src.api.endpoints import bot
from src.core.config import get_settings
from src.database.database import engine, Base
from src.api.endpoints import (
    users,
    health,
    basic,
    advanced,
    sentiment,
    visualization,
    auth,
)

from src.utils.logger import logger
from src.middleware.cors import setup_cors  # Import CORS middleware
from src.middleware.throttling import ThrottleMiddleware  # Import Throttling middleware
from src.middleware.rate_limiting import (
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
visualizations_dir = os.path.join(root_dir, "visualizations")
os.makedirs(visualizations_dir, exist_ok=True)
app.mount(
    "/visualizations", StaticFiles(directory=visualizations_dir), name="visualizations"
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(basic.router, tags=["Basic NLP"])
app.include_router(advanced.router, prefix="/advanced", tags=["Advanced NLP"])
app.include_router(sentiment.router, prefix="/sentiment", tags=["Sentiment Analysis"])
app.include_router(
    visualization.router, prefix="/visualization", tags=["visualization"]
)
app.include_router(bot.router, tags=["Bot"])


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
