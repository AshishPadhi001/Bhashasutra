from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from src.api.endpoints import bot
from src.core.config import get_settings
from src.database.database import engine, Base
from src.api.endpoints import users, health, basic, advanced, sentiment, visualization, auth,bot
from src.utils.logger import logger
import os

# Create the database tables
Base.metadata.create_all(bind=engine)

# Get settings from config
settings = get_settings()

# Initialize FastAPI app
app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (for production, specify frontend domains)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Ensure visualization directories exist
viz_dirs = [
    "visualizations/wordclouds",
    "visualizations/frequency_plots",
    "visualizations/sentiment_graphs",
    "visualizations/tfidf_heatmaps"
]
for directory in viz_dirs:
    os.makedirs(directory, exist_ok=True)

# Mount the visualizations directory to serve static files
app.mount("/visualizations", StaticFiles(directory="visualizations"), name="visualizations")

# Include routers
app.include_router(auth.router, prefix='/auth', tags=['Authentication'])
app.include_router(users.router, prefix='/users', tags=['Users'])
app.include_router(basic.router, tags=['Basic NLP'])
app.include_router(advanced.router, prefix='/advanced', tags=['Advanced NLP'])
app.include_router(sentiment.router, prefix='/sentiment', tags=['Sentiment Analysis'])
app.include_router(visualization.router, prefix='/visualization', tags=['Text Visualization'])
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

# Add middleware to track the ngrok URL
@app.middleware("http")
async def add_base_url(request: Request, call_next):
    # Check if we're running behind ngrok
    host = request.headers.get("X-Forwarded-Host")
    proto = request.headers.get("X-Forwarded-Proto")
    
    if host and proto:
        # This is likely running behind ngrok
        request.state.base_url = f"{proto}://{host}"
    else:
        # Fallback to the direct URL
        server_host = request.headers.get("host", "localhost:8000")
        request.state.base_url = f"http://{server_host}"
    
    response = await call_next(request)
    return response
