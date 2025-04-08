import os
import tempfile
from typing import Dict, Any, Optional, BinaryIO
from Functions.text_summarizer import TextSummarizer
from BackEnd.src.utils.logger import get_logger

# Set up logger
logger = get_logger(__name__)


class SummarizerService:
    """Service for text summarization operations"""

    @staticmethod
    async def summarize_text(input_text: str, level: str) -> Dict[str, Any]:
        """
        Summarize raw text input using TextSummarizer class

        Args:
            input_text: Text content to summarize
            level: Level of summary detail ('brief', 'medium', or 'detailed')

        Returns:
            Dict containing summarization results and metadata
        """
        try:
            # Create summarizer instance with raw text
            summarizer = TextSummarizer(input_text)

            # Check if text meets minimum word count requirement
            if not summarizer.has_enough_words:
                words_needed = summarizer.min_word_count - summarizer.word_count
                return {
                    "success": False,
                    "error": f"Text is too short for summarization. Current word count is {summarizer.word_count}. Need {words_needed} more words to reach minimum of {summarizer.min_word_count}.",
                }

            # Generate summary
            summary_result = summarizer.summarize(level)

            return summary_result

        except Exception as e:
            logger.error(f"Error in text summarizer service: {str(e)}")
            return {"success": False, "error": f"Text summarization failed: {str(e)}"}

    @staticmethod
    async def summarize_file(
        file_content: BinaryIO, filename: str, level: str
    ) -> Dict[str, Any]:
        """
        Summarize uploaded file content using TextSummarizer class

        Args:
            file_content: Binary content of the uploaded file
            filename: Name of the uploaded file
            level: Level of summary detail ('brief', 'medium', or 'detailed')

        Returns:
            Dict containing summarization results and metadata
        """
        temp_file = None
        temp_path = None
        try:
            # Create a temporary file to store the uploaded content
            temp_fd, temp_path = tempfile.mkstemp(suffix=os.path.splitext(filename)[1])
            temp_file = os.fdopen(temp_fd, "wb")

            # Save uploaded content to temporary file
            file_content.seek(0)
            content = file_content.read()
            temp_file.write(content)
            temp_file.close()

            # Create summarizer instance with file path
            summarizer = TextSummarizer(temp_path)

            # Check if text meets minimum word count requirement
            if not summarizer.has_enough_words:
                words_needed = summarizer.min_word_count - summarizer.word_count
                return {
                    "success": False,
                    "error": f"Text is too short for summarization. Current word count is {summarizer.word_count}. Need {words_needed} more words to reach minimum of {summarizer.min_word_count}.",
                }

            # Generate summary
            summary_result = summarizer.summarize(level)

            # Clean up the temporary file
            os.unlink(temp_path)

            return summary_result

        except Exception as e:
            logger.error(f"Error in file summarizer service: {str(e)}")
            # Clean up temporary file if it exists
            if temp_file:
                temp_file.close()
            if temp_path and os.path.exists(temp_path):
                os.unlink(temp_path)

            return {"success": False, "error": f"File summarization failed: {str(e)}"}
