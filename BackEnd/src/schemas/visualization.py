# src/schemas/visualization.py

from pydantic import BaseModel
from typing import Optional


class VisualizationResponse(BaseModel):
    success: bool
    message: str
    image_url: Optional[str] = None
