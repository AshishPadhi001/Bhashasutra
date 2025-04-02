# File: BackEnd/src/schemas/visualization.py

from pydantic import BaseModel
from typing import List, Optional

class VisualizationRequest(BaseModel):
    text: Optional[str] = None

class VisualizationResponse(BaseModel):
    message: str
    image_paths: List[str] = []
    image_urls: List[str] = []  # Add this field for ngrok URLs