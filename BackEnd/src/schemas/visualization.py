from pydantic import BaseModel
from typing import List

class VisualizationResponse(BaseModel):
    message: str
    image_paths: List[str]  # List of saved image file paths
