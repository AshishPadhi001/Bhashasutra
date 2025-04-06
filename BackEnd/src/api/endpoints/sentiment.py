import logging
from fastapi import APIRouter, HTTPException
from src.schemas.sentiment import SentimentTextRequest, SentimentTextResponse
from src.services.sentiment_service import analyze_text_sentiment

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/sentiment", tags=["Sentiment Analysis"])


### TEXT SENTIMENT ANALYSIS ###
@router.post(
    "/analyze/text", response_model=SentimentTextResponse, tags=["Sentiment Analysis"]
)
async def analyze_text(request: SentimentTextRequest):
    """
    Perform sentiment analysis on raw text.
    """
    logger.info("Received sentiment analysis request")

    try:
        logger.debug(f"Processing text of length {len(request.text)} characters")
        result = analyze_text_sentiment(request.text)
        logger.info("Successfully analyzed sentiment")
        return {"result": result}
    except Exception as e:
        logger.error(f"Error in sentiment analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/detailed-analysis/text",
    response_model=SentimentTextResponse,
    tags=["Sentiment Analysis"],
)
async def detailed_analysis_text(request: SentimentTextRequest):
    """
    Perform a detailed sentiment analysis on raw text.
    """
    logger.info("Received detailed sentiment analysis request")

    try:
        logger.debug(
            f"Processing detailed analysis for text of length {len(request.text)} characters"
        )
        result = analyze_text_sentiment(request.text, detailed=True)
        logger.info("Successfully completed detailed sentiment analysis")
        return {"result": result}
    except Exception as e:
        logger.error(f"Error in detailed sentiment analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
