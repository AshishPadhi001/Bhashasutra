from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from src.schemas.advanced import TextRequest, FileRequest, ProcessResponse
from src.services.advanced_service import process_text_function, process_file_function
import logging
from typing import Dict, Any

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/advanced", tags=["Advanced NLP"])


### 📌 TEXT PROCESSING ENDPOINTS ###
@router.post("/word_tokenizer/text", response_model=ProcessResponse)
async def word_tokenizer_text(request: TextRequest):
    try:
        logger.info(
            f"Processing text with word_tokenizer, text length: {len(request.text)}"
        )
        result = process_text_function(request.text, "word_tokenizer")
        logger.debug("Word tokenization completed successfully")
        return {"result": result}
    except Exception as e:
        logger.error(f"Error in word_tokenizer_text: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing text: {str(e)}")


@router.post("/sentence_tokenizer/text", response_model=ProcessResponse)
async def sentence_tokenizer_text(request: TextRequest):
    try:
        logger.info(
            f"Processing text with sentence_tokenizer, text length: {len(request.text)}"
        )
        result = process_text_function(request.text, "sentence_tokenizer")
        logger.debug("Sentence tokenization completed successfully")
        return {"result": result}
    except Exception as e:
        logger.error(f"Error in sentence_tokenizer_text: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing text: {str(e)}")


@router.post("/remove_stopwords/text", response_model=ProcessResponse)
async def remove_stopwords_text(request: TextRequest):
    try:
        logger.info(
            f"Processing text with remove_stopwords, text length: {len(request.text)}"
        )
        result = process_text_function(request.text, "remove_stopwords")
        logger.debug("Stopwords removal completed successfully")
        return {"result": result}
    except Exception as e:
        logger.error(f"Error in remove_stopwords_text: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing text: {str(e)}")


@router.post("/perform_stemming/text", response_model=ProcessResponse)
async def perform_stemming_text(request: TextRequest):
    try:
        logger.info(
            f"Processing text with perform_stemming, text length: {len(request.text)}"
        )
        result = process_text_function(request.text, "perform_stemming")
        logger.debug("Stemming completed successfully")
        return {"result": result}
    except Exception as e:
        logger.error(f"Error in perform_stemming_text: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing text: {str(e)}")


@router.post("/perform_lemmatization/text", response_model=ProcessResponse)
async def perform_lemmatization_text(request: TextRequest):
    try:
        logger.info(
            f"Processing text with perform_lemmatization, text length: {len(request.text)}"
        )
        result = process_text_function(request.text, "perform_lemmatization")
        logger.debug("Lemmatization completed successfully")
        return {"result": result}
    except Exception as e:
        logger.error(f"Error in perform_lemmatization_text: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing text: {str(e)}")


@router.post("/pos_tagging/text", response_model=ProcessResponse)
async def pos_tagging_text(request: TextRequest):
    try:
        logger.info(
            f"Processing text with pos_tagging, text length: {len(request.text)}"
        )
        result = process_text_function(request.text, "pos_tagging")

        # Convert (word, tag) tuples into "word/TAG" strings
        formatted_result = [f"{word}/{tag}" for word, tag in result]

        logger.debug("POS tagging completed successfully")
        return {"result": formatted_result}
    except Exception as e:
        logger.error(f"Error in pos_tagging_text: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing text: {str(e)}")


@router.post("/tfidf_vectorization/text", response_model=ProcessResponse)
async def tfidf_vectorization_text(request: TextRequest):
    try:
        logger.info(
            f"Processing text with tfidf_vectorization, text length: {len(request.text)}"
        )
        result = process_text_function(request.text, "tfidf_vectorization")

        # Convert dictionary to a list of "word: score" formatted strings
        formatted_result = [
            f"{word}: {score}"
            for word, score in zip(result["Top TF-IDF Words"], result["TF-IDF Scores"])
        ]

        logger.debug("TF-IDF vectorization completed successfully")
        return {"result": formatted_result}  # Ensure this returns a list
    except Exception as e:
        logger.error(f"Error in tfidf_vectorization_text: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing text: {str(e)}")


@router.post("/text_summarization/text", response_model=ProcessResponse)
async def text_summarization_text(request: TextRequest):
    try:
        logger.info(
            f"Processing text with text_summarization, text length: {len(request.text)}"
        )
        result = process_text_function(request.text, "text_summarization")

        # Convert result to a list (FastAPI expects a list in ProcessResponse)
        formatted_result = [result]  # ✅ Wrap string in a list

        logger.debug("Text summarization completed successfully")
        return {"result": formatted_result}  # ✅ Ensure it returns a list
    except Exception as e:
        logger.error(f"Error in text_summarization_text: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing text: {str(e)}")


@router.post("/language_detection/text", response_model=ProcessResponse)
async def language_detection_text(request: TextRequest):
    try:
        logger.info(
            f"Processing text with language_detection, text length: {len(request.text)}"
        )
        result = process_text_function(request.text, "language_detection")

        # ✅ Convert string response to a list
        formatted_result = [result]  # Wrap string in a list

        logger.debug("Language detection completed successfully")
        return {"result": formatted_result}  # ✅ Ensure it returns a list
    except Exception as e:
        logger.error(f"Error in language_detection_text: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing text: {str(e)}")


@router.post("/spell_check_and_grammar/text", response_model=ProcessResponse)
async def spell_check_and_grammar_text(request: TextRequest):
    try:
        logger.info(
            f"Processing text with spell_check_and_grammar, text length: {len(request.text)}"
        )
        result = process_text_function(request.text, "spell_check_and_grammar")

        # ✅ Convert string response to list
        formatted_result = [result]  # Wrap the string inside a list

        logger.debug("Spell check and grammar completed successfully")
        return {"result": formatted_result}  # ✅ Ensure it returns a list
    except Exception as e:
        logger.error(f"Error in spell_check_and_grammar_text: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing text: {str(e)}")


### 📌 FILE PROCESSING ENDPOINTS ###
@router.post("/word_tokenizer/file", response_model=ProcessResponse)
async def word_tokenizer_file(file: UploadFile = File(...)):
    try:
        logger.info(f"Processing file with word_tokenizer, filename: {file.filename}")
        result = await process_file_function(file, "word_tokenizer")
        logger.debug("Word tokenization of file completed successfully")
        return {"result": result}
    except Exception as e:
        logger.error(f"Error in word_tokenizer_file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")


@router.post("/sentence_tokenizer/file", response_model=ProcessResponse)
async def sentence_tokenizer_file(file: UploadFile = File(...)):
    try:
        logger.info(
            f"Processing file with sentence_tokenizer, filename: {file.filename}"
        )
        result = await process_file_function(file, "sentence_tokenizer")
        logger.debug("Sentence tokenization of file completed successfully")
        return {"result": result}
    except Exception as e:
        logger.error(f"Error in sentence_tokenizer_file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")


@router.post("/remove_stopwords/file", response_model=ProcessResponse)
async def remove_stopwords_file(file: UploadFile = File(...)):
    try:
        logger.info(f"Processing file with remove_stopwords, filename: {file.filename}")
        result = await process_file_function(file, "remove_stopwords")
        logger.debug("Stopwords removal from file completed successfully")
        return {"result": result}
    except Exception as e:
        logger.error(f"Error in remove_stopwords_file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")


@router.post("/perform_stemming/file", response_model=ProcessResponse)
async def perform_stemming_file(file: UploadFile = File(...)):
    try:
        logger.info(f"Processing file with perform_stemming, filename: {file.filename}")
        result = await process_file_function(file, "perform_stemming")
        logger.debug("Stemming of file completed successfully")
        return {"result": result}
    except Exception as e:
        logger.error(f"Error in perform_stemming_file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")


@router.post("/perform_lemmatization/file", response_model=ProcessResponse)
async def perform_lemmatization_file(file: UploadFile = File(...)):
    try:
        logger.info(
            f"Processing file with perform_lemmatization, filename: {file.filename}"
        )
        result = await process_file_function(file, "perform_lemmatization")
        logger.debug("Lemmatization of file completed successfully")
        return {"result": result}
    except Exception as e:
        logger.error(f"Error in perform_lemmatization_file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")


@router.post("/pos_tagging/file", response_model=ProcessResponse)
async def pos_tagging_file(file: UploadFile = File(...)):
    try:
        logger.info(f"Processing file with pos_tagging, filename: {file.filename}")
        result = await process_file_function(file, "pos_tagging")

        # Convert (word, tag) tuples into "word/TAG" strings
        formatted_result = [f"{word}/{tag}" for word, tag in result]

        logger.debug("POS tagging of file completed successfully")
        return {"result": formatted_result}
    except Exception as e:
        logger.error(f"Error in pos_tagging_file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")


@router.post("/tfidf_vectorization/file", response_model=ProcessResponse)
async def tfidf_vectorization_file(file: UploadFile = File(...)):
    try:
        logger.info(
            f"Processing file with tfidf_vectorization, filename: {file.filename}"
        )
        result = await process_file_function(file, "tfidf_vectorization")

        # Convert dictionary to a list of "word: score" formatted strings
        formatted_result = [
            f"{word}: {score}"
            for word, score in zip(result["Top TF-IDF Words"], result["TF-IDF Scores"])
        ]

        logger.debug("TF-IDF vectorization of file completed successfully")
        return {"result": formatted_result}  # Ensure this returns a list
    except Exception as e:
        logger.error(f"Error in tfidf_vectorization_file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")


@router.post("/text_summarization/file", response_model=ProcessResponse)
async def text_summarization_file(file: UploadFile = File(...)):
    try:
        logger.info(
            f"Processing file with text_summarization, filename: {file.filename}"
        )
        result = await process_file_function(file, "text_summarization")

        # ✅ Convert string response to a list
        formatted_result = [result]  # Wrap string in a list

        logger.debug("Text summarization of file completed successfully")
        return {"result": formatted_result}  # ✅ Ensure it returns a list
    except Exception as e:
        logger.error(f"Error in text_summarization_file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")


@router.post("/language_detection/file", response_model=ProcessResponse)
async def language_detection_file(file: UploadFile = File(...)):
    try:
        logger.info(
            f"Processing file with language_detection, filename: {file.filename}"
        )
        result = await process_file_function(file, "language_detection")

        # ✅ Convert string response to a list
        formatted_result = [result]  # Wrap string in a list

        logger.debug("Language detection of file completed successfully")
        return {"result": formatted_result}  # ✅ Ensure it returns a list
    except Exception as e:
        logger.error(f"Error in language_detection_file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")


@router.post("/spell_check_and_grammar/file", response_model=ProcessResponse)
async def spell_check_and_grammar_file(file: UploadFile = File(...)):
    try:
        logger.info(
            f"Processing file with spell_check_and_grammar, filename: {file.filename}"
        )
        result = await process_file_function(file, "spell_check_and_grammar")

        # ✅ Convert string response to a list
        formatted_result = [result]  # Wrap string in a list

        logger.debug("Spell check and grammar of file completed successfully")
        return {"result": formatted_result}  # ✅ Ensure it returns a list
    except Exception as e:
        logger.error(f"Error in spell_check_and_grammar_file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
