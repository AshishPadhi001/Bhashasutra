# Sentiment Analysis API
from fastapi import APIRouter, HTTPException
from src.schemas.sentiment import SentimentTextRequest, SentimentTextResponse
from src.services.sentiment_service import analyze_text_sentiment

router = APIRouter()

### 📌 TEXT SENTIMENT ANALYSIS ###
@router.post("/analyze", response_model=SentimentTextResponse, tags=["Sentiment Analysis"])
async def analyze_text(request: SentimentTextRequest):
    """
    Perform sentiment analysis on raw text.
    """
    try:
        result = analyze_text_sentiment(request.text)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/detailed-analysis", response_model=SentimentTextResponse, tags=["Sentiment Analysis"])
async def detailed_analysis_text(request: SentimentTextRequest):
    """
    Perform a detailed sentiment analysis on raw text.
    """
    try:
        result = analyze_text_sentiment(request.text, detailed=True)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
