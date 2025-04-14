import logging
from typing import List
from fastapi import (
    APIRouter,
    UploadFile,
    File,
    WebSocket,
    WebSocketDisconnect,
    HTTPException,
    Depends,
)

from BackEnd.src.services.rag_bot_service import RAGBotService
from BackEnd.src.schemas.rag_bot import (
    FileUploadResponse,
    QueryResponse,
    DeleteMemoryResponse,
)

logger = logging.getLogger("rag_bot")
router = APIRouter(prefix="/rag", tags=["RAG Bot"])

# Singleton service
rag_service = RAGBotService()


@router.post("/upload", response_model=FileUploadResponse)
async def upload_files(files: List[UploadFile] = File(...)):
    """
    Upload documents (PDF, DOCX, or TXT) for RAG processing
    """
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")

    # Check file types
    for file in files:
        if not file.filename.lower().endswith((".pdf", ".docx", ".doc", ".txt")):
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type for {file.filename}. Please upload PDF, DOCX, or TXT files only.",
            )

    # Process files
    result = await rag_service.process_files(files)

    return FileUploadResponse(
        status=result["status"], file_ids=result["file_ids"], message=result["message"]
    )


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for RAG queries
    """
    await websocket.accept()

    try:
        while True:
            # Receive query from client
            query = await websocket.receive_text()

            # Check if any documents have been uploaded
            if not rag_service.vector_store:
                await websocket.send_json(
                    {
                        "response": "No documents have been uploaded yet. Please upload PDF, DOCX, or TXT files first using the /rag/upload endpoint.",
                        "source_documents": [],
                        "status": "error",
                    }
                )
                continue

            # Get response from RAG service
            response = await rag_service.get_response(query)

            # Send response back to client
            await websocket.send_json(response)

    except WebSocketDisconnect:
        logger.info("WebSocket client disconnected")

        # Clear memory and delete documents
        rag_service.clear_memory()
        rag_service.delete_documents()

    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
        try:
            await websocket.send_json(
                {
                    "response": f"An error occurred: {str(e)}",
                    "source_documents": [],
                    "status": "error",
                }
            )
        except:
            pass


@router.delete("/memory", response_model=DeleteMemoryResponse)
async def clear_memory():
    """
    Clear conversation memory
    """
    result = rag_service.clear_memory()
    return DeleteMemoryResponse(status=result["status"], message=result["message"])


@router.delete("/documents", response_model=DeleteMemoryResponse)
async def delete_documents():
    """
    Delete all processed documents and reset vector store
    """
    result = rag_service.delete_documents()
    return DeleteMemoryResponse(status=result["status"], message=result["message"])
