from pydantic import BaseModel
from typing import Optional, Dict, List, Any, Union


class TextSummarizerRequest(BaseModel):
    input_text: str

    class Config:
        json_schema_extra = {
            "example": {
                "input_text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit..."
            }
        }


class SummarizerResponse(BaseModel):
    success: bool
    summary: Optional[str] = None
    word_count: Optional[Dict[str, int]] = None

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "summary": "This is a generated summary of the provided text...",
                "word_count": {"original": 500, "summary": 125},
            }
        }
