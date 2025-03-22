from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.endpoints import basic, sentiment, advanced, visualization, auth, users
from src.utils.logger import logger
from src.database.database import engine, Base

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="BhashaSutra API",
    description="API for BhashaSutra NLP Services",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include Routers
app.include_router(auth.router, prefix='/auth', tags=['Authentication'])
app.include_router(users.router, prefix='/users', tags=['Users'])
app.include_router(basic.router, prefix='/basic', tags=['Basic NLP'])
app.include_router(advanced.router, prefix='/advanced', tags=['Advanced NLP'])
app.include_router(sentiment.router, prefix='/sentiment', tags=['Sentiment Analysis'])
app.include_router(visualization.router, prefix='/visualization', tags=['Text Visualization'])
# app.include_router(health.router, prefix='/health', tags=['Health'])

# ✅ Root Endpoint
@app.get("/", tags=["Root"])
def home():
    logger.info("Root endpoint accessed")
    return {
        "message": "Welcome to Bhashasutra API",
        "status": "Running",
        "version": "1.0"
    }
    
# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info("Starting Bhashasutra API")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down Bhashasutra API")