# BackEnd/src/schemas/rag_bot.py

from pydantic import BaseModel
from typing import List, Optional


class FileUploadResponse(BaseModel):
    """Response model for file upload status"""

    status: str
    file_ids: List[str]
    message: str


class QueryRequest(BaseModel):
    """Request model for RAG queries"""

    query: str


class QueryResponse(BaseModel):
    """Response model for RAG query results"""

    response: str
    source_documents: Optional[List[dict]] = None
    status: str


class DeleteMemoryResponse(BaseModel):
    """Response model for memory deletion"""

    status: str
    message: str
