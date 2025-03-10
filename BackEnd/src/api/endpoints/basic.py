# Basic NLP API
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from src.schemas.basic import BasicTextRequest, BasicFileResponse, BasicTextResponse
from src.services.basic_service import process_text_function, process_file_function
import logging

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter()

#Welcome Endpoint
@router.get("/welcome")
async def welcome():
    """Welcome endpoint to check if API is running."""
    return {"message": "Welcome to the Bhashasutra API! 🎉"}

### 📌 TEXT PROCESSING ENDPOINTS ###
@router.post("/text/count-words", response_model=BasicTextResponse)
async def count_words_text(request: BasicTextRequest):
    """ Count words from raw text """
    try:
        logger.info("Processing count_words request for text input")
        if not request.text or not request.text.strip():
            logger.warning("Empty text received for count_words")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Text cannot be empty"
            )
        result = process_text_function(request.text, "count_words")
        logger.info("Successfully processed count_words request")
        return {"result": result}
    except Exception as e:
        logger.error(f"Error processing count_words: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process text: {str(e)}"
        )

@router.post("/text/count-punctuation", response_model=BasicTextResponse)
async def count_punctuation_text(request: BasicTextRequest):
    """ Count punctuation marks from raw text """
    try:
        logger.info("Processing count_punctuation request for text input")
        if not request.text or not request.text.strip():
            logger.warning("Empty text received for count_punctuation")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Text cannot be empty"
            )
        result = process_text_function(request.text, "count_punctuation")
        logger.info("Successfully processed count_punctuation request")
        return {"result": result}
    except Exception as e:
        logger.error(f"Error processing count_punctuation: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process text: {str(e)}"
        )

@router.post("/text/most-repeated-word", response_model=BasicTextResponse)
async def most_repeated_word_text(request: BasicTextRequest):
    """ Find the most repeated word from raw text """
    try:
        logger.info("Processing most_repeated_word request for text input")
        if not request.text or not request.text.strip():
            logger.warning("Empty text received for most_repeated_word")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Text cannot be empty"
            )
        result = process_text_function(request.text, "most_repeated_word")
        logger.info("Successfully processed most_repeated_word request")
        return {"result": result}
    except Exception as e:
        logger.error(f"Error processing most_repeated_word: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process text: {str(e)}"
        )

@router.post("/text/least-repeated-word", response_model=BasicTextResponse)
async def least_repeated_word_text(request: BasicTextRequest):
    """ Find the least repeated word from raw text """
    try:
        logger.info("Processing least_repeated_word request for text input")
        if not request.text or not request.text.strip():
            logger.warning("Empty text received for least_repeated_word")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Text cannot be empty"
            )
        result = process_text_function(request.text, "least_repeated_word")
        logger.info("Successfully processed least_repeated_word request")
        return {"result": result}
    except Exception as e:
        logger.error(f"Error processing least_repeated_word: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process text: {str(e)}"
        )

@router.post("/text/to-lowercase", response_model=BasicTextResponse)
async def to_lowercase_text(request: BasicTextRequest):
    """ Convert text to lowercase """
    try:
        logger.info("Processing to_lowercase request for text input")
        if not request.text:
            logger.warning("Empty text received for to_lowercase")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Text cannot be empty"
            )
        result = process_text_function(request.text, "to_lower")
        logger.info("Successfully processed to_lowercase request")
        return {"result": result}
    except Exception as e:
        logger.error(f"Error processing to_lowercase: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process text: {str(e)}"
        )

@router.post("/text/to-uppercase", response_model=BasicTextResponse)
async def to_uppercase_text(request: BasicTextRequest):
    """ Convert text to uppercase """
    try:
        logger.info("Processing to_uppercase request for text input")
        if not request.text:
            logger.warning("Empty text received for to_uppercase")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Text cannot be empty"
            )
        result = process_text_function(request.text, "to_upper")
        logger.info("Successfully processed to_uppercase request")
        return {"result": result}
    except Exception as e:
        logger.error(f"Error processing to_uppercase: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process text: {str(e)}"
        )

@router.post("/text/remove-punctuation", response_model=BasicTextResponse)
async def remove_punctuation_text(request: BasicTextRequest):
    """ Remove punctuation from raw text """
    try:
        logger.info("Processing remove_punctuation request for text input")
        if not request.text:
            logger.warning("Empty text received for remove_punctuation")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Text cannot be empty"
            )
        result = process_text_function(request.text, "remove_punctuation")
        logger.info("Successfully processed remove_punctuation request")
        return {"result": result}
    except Exception as e:
        logger.error(f"Error processing remove_punctuation: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process text: {str(e)}"
        )

@router.post("/text/remove-numbers", response_model=BasicTextResponse)
async def remove_numbers_text(request: BasicTextRequest):
    """ Remove numbers from raw text """
    try:
        logger.info("Processing remove_numbers request for text input")
        if not request.text:
            logger.warning("Empty text received for remove_numbers")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Text cannot be empty"
            )
        result = process_text_function(request.text, "remove_numbers")
        logger.info("Successfully processed remove_numbers request")
        return {"result": result}
    except Exception as e:
        logger.error(f"Error processing remove_numbers: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process text: {str(e)}"
        )

@router.post("/text/remove-extra-whitespace", response_model=BasicTextResponse)
async def remove_extra_whitespace_text(request: BasicTextRequest):
    """ Remove extra whitespace from raw text """
    try:
        logger.info("Processing remove_extra_whitespace request for text input")
        if not request.text:
            logger.warning("Empty text received for remove_extra_whitespace")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Text cannot be empty"
            )
        result = process_text_function(request.text, "remove_extra_whitespace")
        logger.info("Successfully processed remove_extra_whitespace request")
        return {"result": result}
    except Exception as e:
        logger.error(f"Error processing remove_extra_whitespace: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process text: {str(e)}"
        )

@router.post("/text/average-word-length", response_model=BasicTextResponse)
async def average_word_length_text(request: BasicTextRequest):
    """ Find the average word length from raw text """
    try:
        logger.info("Processing average_word_length request for text input")
        if not request.text or not request.text.strip():
            logger.warning("Empty text received for average_word_length")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Text cannot be empty"
            )
        result = process_text_function(request.text, "find_average_word_length")
        logger.info("Successfully processed average_word_length request")
        return {"result": result}
    except Exception as e:
        logger.error(f"Error processing average_word_length: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process text: {str(e)}"
        )

@router.post("/text/average-sentence-length", response_model=BasicTextResponse)
async def average_sentence_length_text(request: BasicTextRequest):
    """ Find the average sentence length from raw text """
    try:
        logger.info("Processing average_sentence_length request for text input")
        if not request.text or not request.text.strip():
            logger.warning("Empty text received for average_sentence_length")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Text cannot be empty"
            )
        result = process_text_function(request.text, "find_average_sentence_length")
        logger.info("Successfully processed average_sentence_length request")
        return {"result": result}
    except Exception as e:
        logger.error(f"Error processing average_sentence_length: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process text: {str(e)}"
        )

@router.post("/text/reverse-text", response_model=BasicTextResponse)
async def reverse_text_text(request: BasicTextRequest):
    """ Reverse the text """
    try:
        logger.info("Processing reverse_text request for text input")
        if not request.text:
            logger.warning("Empty text received for reverse_text")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Text cannot be empty"
            )
        result = process_text_function(request.text, "reverse_text")
        logger.info("Successfully processed reverse_text request")
        return {"result": result}
    except Exception as e:
        logger.error(f"Error processing reverse_text: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process text: {str(e)}"
        )

@router.post("/text/count-unique-words", response_model=BasicTextResponse)
async def count_unique_words_text(request: BasicTextRequest):
    """ Count unique words in text """
    try:
        logger.info("Processing count_unique_words request for text input")
        if not request.text or not request.text.strip():
            logger.warning("Empty text received for count_unique_words")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Text cannot be empty"
            )
        result = process_text_function(request.text, "count_unique_words")
        logger.info("Successfully processed count_unique_words request")
        return {"result": result}
    except Exception as e:
        logger.error(f"Error processing count_unique_words: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process text: {str(e)}"
        )

@router.post("/text/extract-proper-nouns", response_model=BasicTextResponse)
async def extract_proper_nouns_text(request: BasicTextRequest):
    """ Extract proper nouns from text """
    try:
        logger.info("Processing extract_proper_nouns request for text input")
        if not request.text or not request.text.strip():
            logger.warning("Empty text received for extract_proper_nouns")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Text cannot be empty"
            )
        result = process_text_function(request.text, "extract_proper_nouns")
        logger.info("Successfully processed extract_proper_nouns request")
        return {"result": result}
    except Exception as e:
        logger.error(f"Error processing extract_proper_nouns: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process text: {str(e)}"
        )

### 📌 FILE PROCESSING ENDPOINTS ###
@router.post("/file/count-words", response_model=BasicFileResponse)
async def count_words_file(file: UploadFile = File(...)):
    try:
        logger.info(f"Processing count_words request for file: {file.filename}")
        if not file:
            logger.warning("No file received for count_words")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No file provided"
            )
        result = await process_file_function(file, "count_words")
        logger.info(f"Successfully processed count_words for file: {file.filename}")
        return {"result": result}
    except HTTPException as he:
        # Re-raise HTTP exceptions without modifying them
        raise he
    except Exception as e:
        logger.error(f"Error processing count_words for file {file.filename}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process file: {str(e)}"
        )

@router.post("/file/count-punctuation", response_model=BasicFileResponse)
async def count_punctuation_file(file: UploadFile = File(...)):
    try:
        logger.info(f"Processing count_punctuation request for file: {file.filename}")
        if not file:
            logger.warning("No file received for count_punctuation")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No file provided"
            )
        result = await process_file_function(file, "count_punctuation")
        logger.info(f"Successfully processed count_punctuation for file: {file.filename}")
        return {"result": result}
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error processing count_punctuation for file {file.filename}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process file: {str(e)}"
        )

@router.post("/file/most-repeated-word", response_model=BasicFileResponse)
async def most_repeated_word_file(file: UploadFile = File(...)):
    try:
        logger.info(f"Processing most_repeated_word request for file: {file.filename}")
        if not file:
            logger.warning("No file received for most_repeated_word")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No file provided"
            )
        result = await process_file_function(file, "most_repeated_word")
        logger.info(f"Successfully processed most_repeated_word for file: {file.filename}")
        return {"result": result}
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error processing most_repeated_word for file {file.filename}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process file: {str(e)}"
        )

@router.post("/file/least-repeated-word", response_model=BasicFileResponse)
async def least_repeated_word_file(file: UploadFile = File(...)):
    try:
        logger.info(f"Processing least_repeated_word request for file: {file.filename}")
        if not file:
            logger.warning("No file received for least_repeated_word")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No file provided"
            )
        result = await process_file_function(file, "least_repeated_word")
        logger.info(f"Successfully processed least_repeated_word for file: {file.filename}")
        return {"result": result}
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error processing least_repeated_word for file {file.filename}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process file: {str(e)}"
        )

@router.post("/file/to-lowercase", response_model=BasicFileResponse)
async def to_lowercase_file(file: UploadFile = File(...)):
    try:
        logger.info(f"Processing to_lowercase request for file: {file.filename}")
        if not file:
            logger.warning("No file received for to_lowercase")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No file provided"
            )
        result = await process_file_function(file, "to_lower")
        logger.info(f"Successfully processed to_lowercase for file: {file.filename}")
        return {"result": result}
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error processing to_lowercase for file {file.filename}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process file: {str(e)}"
        )

@router.post("/file/to-uppercase", response_model=BasicFileResponse)
async def to_uppercase_file(file: UploadFile = File(...)):
    try:
        logger.info(f"Processing to_uppercase request for file: {file.filename}")
        if not file:
            logger.warning("No file received for to_uppercase")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No file provided"
            )
        result = await process_file_function(file, "to_upper")
        logger.info(f"Successfully processed to_uppercase for file: {file.filename}")
        return {"result": result}
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error processing to_uppercase for file {file.filename}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process file: {str(e)}"
        )

@router.post("/file/remove-punctuation", response_model=BasicFileResponse)
async def remove_punctuation_file(file: UploadFile = File(...)):
    try:
        logger.info(f"Processing remove_punctuation request for file: {file.filename}")
        if not file:
            logger.warning("No file received for remove_punctuation")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No file provided"
            )
        result = await process_file_function(file, "remove_punctuation")
        logger.info(f"Successfully processed remove_punctuation for file: {file.filename}")
        return {"result": result}
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error processing remove_punctuation for file {file.filename}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process file: {str(e)}"
        )

@router.post("/file/remove-numbers", response_model=BasicFileResponse)
async def remove_numbers_file(file: UploadFile = File(...)):
    try:
        logger.info(f"Processing remove_numbers request for file: {file.filename}")
        if not file:
            logger.warning("No file received for remove_numbers")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No file provided"
            )
        result = await process_file_function(file, "remove_numbers")
        logger.info(f"Successfully processed remove_numbers for file: {file.filename}")
        return {"result": result}
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error processing remove_numbers for file {file.filename}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process file: {str(e)}"
        )

@router.post("/file/remove-extra-whitespace", response_model=BasicFileResponse)
async def remove_extra_whitespace_file(file: UploadFile = File(...)):
    try:
        logger.info(f"Processing remove_extra_whitespace request for file: {file.filename}")
        if not file:
            logger.warning("No file received for remove_extra_whitespace")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No file provided"
            )
        result = await process_file_function(file, "remove_extra_whitespace")
        logger.info(f"Successfully processed remove_extra_whitespace for file: {file.filename}")
        return {"result": result}
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error processing remove_extra_whitespace for file {file.filename}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process file: {str(e)}"
        )

@router.post("/file/average-word-length", response_model=BasicFileResponse)
async def average_word_length_file(file: UploadFile = File(...)):
    try:
        logger.info(f"Processing average_word_length request for file: {file.filename}")
        if not file:
            logger.warning("No file received for average_word_length")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No file provided"
            )
        result = await process_file_function(file, "find_average_word_length")
        logger.info(f"Successfully processed average_word_length for file: {file.filename}")
        return {"result": result}
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error processing average_word_length for file {file.filename}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process file: {str(e)}"
        )

@router.post("/file/average-sentence-length", response_model=BasicFileResponse)
async def average_sentence_length_file(file: UploadFile = File(...)):
    try:
        logger.info(f"Processing average_sentence_length request for file: {file.filename}")
        if not file:
            logger.warning("No file received for average_sentence_length")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No file provided"
            )
        result = await process_file_function(file, "find_average_sentence_length")
        logger.info(f"Successfully processed average_sentence_length for file: {file.filename}")
        return {"result": result}
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error processing average_sentence_length for file {file.filename}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process file: {str(e)}"
        )

@router.post("/file/reverse-text", response_model=BasicFileResponse)
async def reverse_text_file(file: UploadFile = File(...)):
    try:
        logger.info(f"Processing reverse_text request for file: {file.filename}")
        if not file:
            logger.warning("No file received for reverse_text")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No file provided"
            )
        result = await process_file_function(file, "reverse_text")
        logger.info(f"Successfully processed reverse_text for file: {file.filename}")
        return {"result": result}
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error processing reverse_text for file {file.filename}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process file: {str(e)}"
        )

@router.post("/file/count-unique-words", response_model=BasicFileResponse)
async def count_unique_words_file(file: UploadFile = File(...)):
    try:
        logger.info(f"Processing count_unique_words request for file: {file.filename}")
        if not file:
            logger.warning("No file received for count_unique_words")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No file provided"
            )
        result = await process_file_function(file, "count_unique_words")
        logger.info(f"Successfully processed count_unique_words for file: {file.filename}")
        return {"result": result}
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error processing count_unique_words for file {file.filename}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process file: {str(e)}"
        )

@router.post("/file/extract-proper-nouns", response_model=BasicFileResponse)
async def extract_proper_nouns_file(file: UploadFile = File(...)):
    try:
        logger.info(f"Processing extract_proper_nouns request for file: {file.filename}")
        if not file:
            logger.warning("No file received for extract_proper_nouns")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No file provided"
            )
        result = await process_file_function(file, "extract_proper_nouns")
        logger.info(f"Successfully processed extract_proper_nouns for file: {file.filename}")
        return {"result": result}
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error processing extract_proper_nouns for file {file.filename}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process file: {str(e)}"
        )