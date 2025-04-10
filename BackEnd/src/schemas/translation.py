from pydantic import BaseModel, Field
from typing import Dict, Any, Optional


class TranslationRequest(BaseModel):
    text: str = Field(..., description="Raw text to be translated")
    target_language: str = Field(..., description="Target language code or name")


class TranslationResponse(BaseModel):
    result: Dict[str, Any]
