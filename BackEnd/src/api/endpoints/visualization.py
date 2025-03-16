import os
import logging
from fastapi import APIRouter, UploadFile, File, HTTPException, Response
from fastapi.responses import FileResponse
from src.services.visualization_service import process_visualization
from src.schemas.visualization import VisualizationResponse

# Set up logger
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/wordcloud", response_model=VisualizationResponse)
async def generate_wordcloud(file: UploadFile = File(...)):
    """Generate a Word Cloud visualization from a text file."""
    try:
        logger.info(f"Processing wordcloud visualization for file: {file.filename}")
        result = await process_visualization(file, "wordcloud")
        logger.info(f"Successfully generated wordcloud visualization")
        return result
    except Exception as e:
        logger.error(f"Error generating wordcloud visualization: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate wordcloud: {str(e)}")

@router.post("/frequency", response_model=VisualizationResponse)
async def generate_word_frequency(file: UploadFile = File(...)):
    """Generate a Word Frequency Plot visualization from a text file."""
    try:
        logger.info(f"Processing word frequency visualization for file: {file.filename}")
        result = await process_visualization(file, "frequency")
        logger.info(f"Successfully generated word frequency visualization")
        return result
    except Exception as e:
        logger.error(f"Error generating word frequency visualization: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate word frequency plot: {str(e)}")

@router.post("/sentiment", response_model=VisualizationResponse)
async def generate_sentiment_distribution(file: UploadFile = File(...)):
    """Generate a Sentiment Distribution visualization from a text file."""
    try:
        logger.info(f"Processing sentiment distribution visualization for file: {file.filename}")
        result = await process_visualization(file, "sentiment")
        logger.info(f"Successfully generated sentiment distribution visualization")
        return result
    except Exception as e:
        logger.error(f"Error generating sentiment distribution visualization: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate sentiment analysis: {str(e)}")

@router.post("/tfidf", response_model=VisualizationResponse)
async def generate_tfidf_heatmap(file: UploadFile = File(...)):
    """Generate a TF-IDF Heatmap visualization from a text file."""
    try:
        logger.info(f"Processing TF-IDF heatmap visualization for file: {file.filename}")
        result = await process_visualization(file, "tfidf")
        logger.info(f"Successfully generated TF-IDF heatmap visualization")
        return result
    except Exception as e:
        logger.error(f"Error generating TF-IDF heatmap visualization: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate TF-IDF heatmap: {str(e)}")
