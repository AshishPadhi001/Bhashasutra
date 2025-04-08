from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException,
)
from fastapi.responses import JSONResponse
import os
from BackEnd.src.schemas.summarizer import TextSummarizerRequest, SummarizerResponse
from BackEnd.src.services.summarizer_service import SummarizerService
from BackEnd.src.utils.logger import get_logger
from typing import Dict

# Set up router
router = APIRouter(prefix="/summarizer", tags=["Summarizer"])

# Set up logger
logger = get_logger(__name__)


# Helper function to format the response
def format_summary_response(result: Dict) -> Dict:
    """Format the summarizer response to only include summary and word count"""
    if not result["success"]:
        # Return error response as is
        return result

    # Return only the summary and word count for successful responses
    return {
        "success": True,
        "summary": result["summary"],
        "word_count": result["word_count"],
    }


@router.post("/text/brief", response_model=SummarizerResponse)
async def summarize_text_brief(request: TextSummarizerRequest):
    """Generate a brief summary from raw text input."""
    try:
        result = await SummarizerService.summarize_text(
            input_text=request.input_text, level="brief"
        )

        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["error"])

        # Return simplified response
        return format_summary_response(result)
    except HTTPException as http_exc:
        if http_exc.status_code == 429:
            logger.warning("Rate limit exceeded")
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded. Please try again after some time.",
            )
        raise
    except Exception as e:
        logger.error(f"Error in summarize_text_brief endpoint: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Brief summarization failed: {str(e)}"
        )


@router.post("/text/medium", response_model=SummarizerResponse)
async def summarize_text_medium(request: TextSummarizerRequest):
    """Generate a medium summary from raw text input."""
    try:
        result = await SummarizerService.summarize_text(
            input_text=request.input_text, level="medium"
        )

        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["error"])

        # Return simplified response
        return format_summary_response(result)
    except HTTPException as http_exc:
        if http_exc.status_code == 429:
            logger.warning("Rate limit exceeded")
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded. Please try again after some time.",
            )
        raise
    except Exception as e:
        logger.error(f"Error in summarize_text_medium endpoint: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Medium summarization failed: {str(e)}"
        )


@router.post("/text/detailed", response_model=SummarizerResponse)
async def summarize_text_detailed(request: TextSummarizerRequest):
    """Generate a detailed summary from raw text input."""
    try:
        result = await SummarizerService.summarize_text(
            input_text=request.input_text, level="detailed"
        )

        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["error"])

        # Return simplified response
        return format_summary_response(result)
    except HTTPException as http_exc:
        if http_exc.status_code == 429:
            logger.warning("Rate limit exceeded")
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded. Please try again after some time.",
            )
        raise
    except Exception as e:
        logger.error(f"Error in summarize_text_detailed endpoint: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Detailed summarization failed: {str(e)}"
        )


@router.post("/file/brief", response_model=SummarizerResponse)
async def summarize_file_brief(file: UploadFile = File(...)):
    """Generate a brief summary from an uploaded file (PDF, DOCX, TXT)."""
    try:
        # Validate file extension
        file_extension = os.path.splitext(file.filename)[1].lower()
        if file_extension not in [".pdf", ".docx", ".txt"]:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file format. Only PDF, DOCX, and TXT files are supported.",
            )

        result = await SummarizerService.summarize_file(
            file_content=file.file, filename=file.filename, level="brief"
        )

        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["error"])

        # Return simplified response
        return format_summary_response(result)
    except HTTPException as http_exc:
        if http_exc.status_code == 429:
            logger.warning("Rate limit exceeded")
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded. Please try again after some time.",
            )
        raise
    except Exception as e:
        logger.error(f"Error in summarize_file_brief endpoint: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Brief file summarization failed: {str(e)}"
        )


@router.post("/file/medium", response_model=SummarizerResponse)
async def summarize_file_medium(file: UploadFile = File(...)):
    """Generate a medium summary from an uploaded file (PDF, DOCX, TXT)."""
    try:
        # Validate file extension
        file_extension = os.path.splitext(file.filename)[1].lower()
        if file_extension not in [".pdf", ".docx", ".txt"]:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file format. Only PDF, DOCX, and TXT files are supported.",
            )

        result = await SummarizerService.summarize_file(
            file_content=file.file, filename=file.filename, level="medium"
        )

        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["error"])

        # Return simplified response
        return format_summary_response(result)
    except HTTPException as http_exc:
        if http_exc.status_code == 429:
            logger.warning("Rate limit exceeded")
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded. Please try again after some time.",
            )
        raise
    except Exception as e:
        logger.error(f"Error in summarize_file_medium endpoint: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Medium file summarization failed: {str(e)}"
        )


@router.post("/file/detailed", response_model=SummarizerResponse)
async def summarize_file_detailed(file: UploadFile = File(...)):
    """Generate a detailed summary from an uploaded file (PDF, DOCX, TXT)."""
    try:
        # Validate file extension
        file_extension = os.path.splitext(file.filename)[1].lower()
        if file_extension not in [".pdf", ".docx", ".txt"]:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file format. Only PDF, DOCX, and TXT files are supported.",
            )

        result = await SummarizerService.summarize_file(
            file_content=file.file, filename=file.filename, level="detailed"
        )

        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["error"])

        # Return simplified response
        return format_summary_response(result)
    except HTTPException as http_exc:
        if http_exc.status_code == 429:
            logger.warning("Rate limit exceeded")
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded. Please try again after some time.",
            )
        raise
    except Exception as e:
        logger.error(f"Error in summarize_file_detailed endpoint: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Detailed file summarization failed: {str(e)}"
        )
