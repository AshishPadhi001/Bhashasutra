import logging
from fastapi import APIRouter, HTTPException
from BackEnd.src.schemas.translation import TranslationRequest, TranslationResponse
from BackEnd.src.services.translation_service import translate_text

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/translation", tags=["Translation"])


@router.post("/translate", response_model=TranslationResponse)
async def translate_text_endpoint(request: TranslationRequest):
    """
    Translate text to the specified target language.

    This endpoint takes raw text and a target language and returns the translated text.
    Both text and target language are required.
    """
    logger.info("Received translation request")

    try:
        # Validate that both inputs are provided
        if not request.text or not request.text.strip():
            raise ValueError("Text for translation cannot be empty")

        if not request.target_language or not request.target_language.strip():
            raise ValueError("Target language must be specified")

        logger.debug(
            f"Processing translation of text (length: {len(request.text)} characters) to {request.target_language}"
        )
        result = translate_text(request.text, target_language=request.target_language)

        if "error" in result:
            logger.error(f"Translation error: {result['error']}")
            raise HTTPException(status_code=400, detail=result["error"])

        logger.info("Successfully translated text")
        return {"result": result}
    except ValueError as ve:
        logger.error(f"Validation error: {str(ve)}")
        raise HTTPException(status_code=400, detail=str(ve))
    except HTTPException as http_exc:
        if http_exc.status_code == 429:
            logger.warning("Rate limit exceeded")
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded. Please try again after some time.",
            )
        raise
    except Exception as e:
        logger.error(f"Error in translation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
