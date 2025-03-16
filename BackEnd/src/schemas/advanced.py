from typing import List
from pydantic import BaseModel
from fastapi import UploadFile, File


# Schema for Text-based Input
class TextRequest(BaseModel):
    text: str


# Schema for File-based Input
class FileRequest(BaseModel):
    file: UploadFile = File(...)


# Generic response schema
class ProcessResponse(BaseModel):
    result: List[str]
