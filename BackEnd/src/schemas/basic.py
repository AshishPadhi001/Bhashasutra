# Basic NLP schemas
from pydantic import BaseModel

class BasicTextRequest(BaseModel):
    text: str

class BasicTextResponse(BaseModel):
    result: str

class BasicFileResponse(BaseModel):
    result: str
