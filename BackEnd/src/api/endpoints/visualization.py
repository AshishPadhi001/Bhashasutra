# File: BackEnd/src/api/endpoints/visualization.py

import os
import logging
from fastapi import APIRouter, UploadFile, File, HTTPException, Request
from fastapi.responses import FileResponse

from src.schemas.visualization import VisualizationResponse
from src.services.visualization_service import process_visualization

# Set up logger
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/visualization")

@router.post("/wordcloud/file", response_model=VisualizationResponse)
async def generate_wordcloud(request: Request, file: UploadFile = File(...)):
    """Generate a Word Cloud visualization from a text file."""
    try:
        logger.info(f"Processing wordcloud visualization for file: {file.filename}")
        # Get the base URL from the request state (set by middleware)
        base_url = request.state.base_url
        result = await process_visualization(file, "wordcloud", base_url)
        logger.info(f"Successfully generated wordcloud visualization")
        return result
    except Exception as e:
        logger.error(f"Error generating wordcloud visualization: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate wordcloud: {str(e)}")

@router.post("/frequency/file", response_model=VisualizationResponse)
async def generate_word_frequency(request: Request, file: UploadFile = File(...)):
    """Generate a Word Frequency Plot visualization from a text file."""
    try:
        logger.info(f"Processing word frequency visualization for file: {file.filename}")
        base_url = request.state.base_url
        result = await process_visualization(file, "frequency", base_url)
        logger.info(f"Successfully generated word frequency visualization")
        return result
    except Exception as e:
        logger.error(f"Error generating word frequency visualization: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate word frequency plot: {str(e)}")

@router.post("/sentiment/file", response_model=VisualizationResponse)
async def generate_sentiment_distribution(request: Request, file: UploadFile = File(...)):
    """Generate a Sentiment Distribution visualization from a text file."""
    try:
        logger.info(f"Processing sentiment distribution visualization for file: {file.filename}")
        base_url = request.state.base_url
        result = await process_visualization(file, "sentiment", base_url)
        logger.info(f"Successfully generated sentiment distribution visualization")
        return result
    except Exception as e:
        logger.error(f"Error generating sentiment distribution visualization: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate sentiment analysis: {str(e)}")

@router.post("/tfidf/file", response_model=VisualizationResponse)
async def generate_tfidf_heatmap(request: Request, file: UploadFile = File(...)):
    """Generate a TF-IDF Heatmap visualization from a text file."""
    try:
        logger.info(f"Processing TF-IDF heatmap visualization for file: {file.filename}")
        base_url = request.state.base_url
        result = await process_visualization(file, "tfidf", base_url)
        logger.info(f"Successfully generated TF-IDF heatmap visualization")
        return result
    except Exception as e:
        logger.error(f"Error generating TF-IDF heatmap visualization: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate TF-IDF heatmap: {str(e)}")

@router.get("/images/{visualization_type}/{filename}")
async def get_image(visualization_type: str, filename: str):
    """
    Serve a generated visualization image file.
    """
    valid_types = {
        "wordcloud": "visualizations/wordclouds",
        "frequency": "visualizations/frequency_plots",
        "sentiment": "visualizations/sentiment_graphs",
        "tfidf": "visualizations/tfidf_heatmaps"
    }
    
    if visualization_type not in valid_types:
        raise HTTPException(status_code=404, detail="Invalid visualization type")
    
    # Extract filename without directory parts for security
    safe_filename = os.path.basename(filename)
    
    # Construct path
    file_path = os.path.join(valid_types[visualization_type], safe_filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Image not found")
    
    return FileResponse(file_path)