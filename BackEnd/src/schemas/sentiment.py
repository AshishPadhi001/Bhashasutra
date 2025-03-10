# Sentiment Analysis schemas
from pydantic import BaseModel
from typing import Dict, Any

class SentimentTextRequest(BaseModel):
    text: str

class SentimentTextResponse(BaseModel):
    result: Dict[str, Any]
