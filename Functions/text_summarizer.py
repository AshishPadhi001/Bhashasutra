import nltk
import re
import sys
import os
from transformers import pipeline

# Add path for importing Basic class
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Download necessary NLTK resources (if not already downloaded)
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")


class TextSummarizer:
    """
    Text summarization class that provides summaries of text using Hugging Face transformers.
    Works with both file-based input and raw text.

    Usage example:
    summarizer = TextSummarizer(input_data)
    summary = summarizer.summarize(level='brief')
    """

    def __init__(self, input_data):
        """
        Initialize the TextSummarizer class with either a file path or raw text.

        Args:
            input_data (str): A file path (PDF, DOCX, TXT) or raw text.
        """
        # Import here to avoid circular imports
        from Functions.basic import Basic

        # Initialize Basic class for text extraction and preprocessing
        self.basic = Basic(input_data)

        # Get the processed text - works for both file and raw text
        self.text = self.basic.text

        # Store the word count for validation
        self.word_count = self.basic.count_words()

        # Minimum word count required for summarization
        self.min_word_count = 250

        # Check if the text meets minimum word count requirement
        self.has_enough_words = self.word_count >= self.min_word_count

        # Load the transformer model for summarization only if text is long enough
        self.transformer_available = False
        if self.has_enough_words:
            try:
                self.transformer_summarizer = pipeline(
                    "summarization", model="facebook/bart-large-cnn"
                )
                self.transformer_available = True
            except Exception as e:
                print(f"Warning: Could not load transformer model: {e}")
                print("Falling back to extractive summarization.")

    def _calculate_sentence_scores(self):
        """
        Calculate importance scores for each sentence in the text.
        Used as fallback if transformer model is not available.

        Returns:
            tuple: (sentences, sentence_scores)
                - sentences: List of sentences in the text
                - sentence_scores: Dictionary mapping sentences to their importance scores
        """
        from nltk.tokenize import sent_tokenize
        from nltk.corpus import stopwords
        from nltk.probability import FreqDist
        from heapq import nlargest

        # Ensure stopwords are downloaded
        try:
            nltk.data.find("corpora/stopwords")
        except LookupError:
            nltk.download("stopwords")

        # Tokenize the text into sentences
        sentences = sent_tokenize(self.text)

        # Remove stopwords for better word frequency analysis
        stop_words = set(stopwords.words("english"))

        # Tokenize and clean words
        words = [
            word.lower()
            for word in re.findall(r"\b\w+\b", self.text)
            if word.lower() not in stop_words
        ]

        # Calculate word frequencies
        freq = FreqDist(words)

        # Calculate scores for each sentence based on word frequencies
        sentence_scores = {}

        for sentence in sentences:
            for word in re.findall(r"\b\w+\b", sentence.lower()):
                if word in freq:
                    if sentence not in sentence_scores:
                        sentence_scores[sentence] = freq[word]
                    else:
                        sentence_scores[sentence] += freq[word]

        # Normalize scores by sentence length
        for sentence in sentence_scores:
            sentence_scores[sentence] = sentence_scores[sentence] / max(
                1, len(re.findall(r"\b\w+\b", sentence))
            )

        return sentences, sentence_scores

    def _extractive_summarize(self, level="medium"):
        """
        Generate a summary using extractive summarization (NLTK-based).

        Args:
            level (str): Level of summary detail ('brief', 'medium', or 'detailed')

        Returns:
            dict: Summary results with text and metadata
        """
        from heapq import nlargest
        from nltk.tokenize import sent_tokenize

        # Get sentences and their scores
        sentences, sentence_scores = self._calculate_sentence_scores()

        # Determine summary size based on level
        if level.lower() == "brief":
            # About 10% of original sentences or minimum 3 sentences
            summary_size = max(3, int(len(sentences) * 0.1))
            summary_description = "Brief summary (extractive)"
        elif level.lower() == "detailed":
            # About 30% of original sentences
            summary_size = max(5, int(len(sentences) * 0.3))
            summary_description = "Detailed summary (extractive)"
        else:  # medium (default)
            # About 20% of original sentences
            summary_size = max(4, int(len(sentences) * 0.2))
            summary_description = "Medium summary (extractive)"

        # Limit summary size to the number of available sentences
        summary_size = min(summary_size, len(sentences))

        # Extract top sentences for the summary
        summary_sentences = nlargest(
            summary_size, sentence_scores, key=sentence_scores.get
        )

        # Preserve original sentence order
        summary_sentences = [
            sentence for sentence in sentences if sentence in summary_sentences
        ]

        # Join sentences into a complete summary
        summary = " ".join(summary_sentences)

        # Calculate compression ratio
        compression_ratio = round(
            (1 - (len(summary_sentences) / len(sentences))) * 100, 1
        )

        return {
            "success": True,
            "summary": summary,
            "level": level,
            "description": summary_description,
            "original_sentences": len(sentences),
            "summary_sentences": len(summary_sentences),
            "compression_ratio": f"{compression_ratio}%",
            "word_count": {
                "original": self.word_count,
                "summary": len(re.findall(r"\b\w+\b", summary)),
            },
        }

    def _transformer_summarize(self, level="medium"):
        """
        Generate a summary using transformer-based models (Hugging Face).

        Args:
            level (str): Level of summary detail ('brief', 'medium', or 'detailed')

        Returns:
            dict: Summary results with text and metadata
        """
        from nltk.tokenize import sent_tokenize

        # Set max length and min length based on level
        if level.lower() == "brief":
            max_length = max(100, int(self.word_count * 0.15))
            min_length = max(30, int(self.word_count * 0.05))
            summary_description = "Brief summary (transformer)"
        elif level.lower() == "detailed":
            max_length = max(300, int(self.word_count * 0.40))
            min_length = max(100, int(self.word_count * 0.25))
            summary_description = "Detailed summary (transformer)"
        else:  # medium (default)
            max_length = max(200, int(self.word_count * 0.25))
            min_length = max(50, int(self.word_count * 0.15))
            summary_description = "Medium summary (transformer)"

        # Ensure max_length is within model limits (typically 1024 tokens for BART)
        max_length = min(1024, max_length)
        min_length = min(max_length - 1, min_length)

        # Some transformer models have input length limitations
        # If text is too long, we'll chunk it and summarize each chunk
        max_input_length = 1024  # Typical limit for BART models

        # Count original sentences
        original_sentences = len(sent_tokenize(self.text))

        if len(self.text.split()) > max_input_length:
            # Simple chunking by splitting into roughly equal parts
            chunks = self._chunk_text(self.text, max_input_length)
            summaries = []

            for chunk in chunks:
                chunk_summary = self.transformer_summarizer(
                    chunk,
                    max_length=max(30, max_length // len(chunks)),
                    min_length=max(10, min_length // len(chunks)),
                    do_sample=False,
                )[0]["summary_text"]
                summaries.append(chunk_summary)

            summary = " ".join(summaries)
        else:
            # Summarize the entire text at once
            summary = self.transformer_summarizer(
                self.text, max_length=max_length, min_length=min_length, do_sample=False
            )[0]["summary_text"]

        # Count summary sentences
        summary_sentences = len(sent_tokenize(summary))

        # Calculate compression ratio based on word count
        summary_word_count = len(re.findall(r"\b\w+\b", summary))
        compression_ratio = round((1 - (summary_word_count / self.word_count)) * 100, 1)

        return {
            "success": True,
            "summary": summary,
            "level": level,
            "description": summary_description,
            "original_sentences": original_sentences,
            "summary_sentences": summary_sentences,
            "compression_ratio": f"{compression_ratio}%",
            "word_count": {"original": self.word_count, "summary": summary_word_count},
        }

    def _chunk_text(self, text, max_chunk_size):
        """
        Split text into chunks that don't exceed max_chunk_size words.
        Try to split at sentence boundaries when possible.

        Args:
            text (str): Text to split
            max_chunk_size (int): Maximum words per chunk

        Returns:
            list: List of text chunks
        """
        from nltk.tokenize import sent_tokenize

        sentences = sent_tokenize(text)
        chunks = []
        current_chunk = []
        current_size = 0

        for sentence in sentences:
            sentence_size = len(sentence.split())

            if current_size + sentence_size <= max_chunk_size:
                current_chunk.append(sentence)
                current_size += sentence_size
            else:
                # If the current chunk has content, add it to chunks
                if current_chunk:
                    chunks.append(" ".join(current_chunk))

                # Start a new chunk with the current sentence
                current_chunk = [sentence]
                current_size = sentence_size

        # Add the last chunk if it has content
        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks

    def summarize(self, level="medium"):
        """
        Generate a summary of the text at the specified level.
        Uses transformer-based summarization if available, otherwise falls back to extractive.

        Args:
            level (str): Level of summary detail ('brief', 'medium', or 'detailed')

        Returns:
            dict: Summary results with text and metadata
        """
        # Check if text has enough words
        if not self.has_enough_words:
            words_needed = self.min_word_count - self.word_count
            return {
                "success": False,
                "summary": None,
                "error": f"Text is too short for summarization. Current word count is {self.word_count}. Need {words_needed} more words to reach minimum of {self.min_word_count}.",
            }

        # Use transformer-based summarization if available
        if self.transformer_available:
            try:
                return self._transformer_summarize(level)
            except Exception as e:
                print(f"Transformer summarization failed: {e}")
                print("Falling back to extractive summarization.")
                return self._extractive_summarize(level)
        else:
            # Fall back to extractive summarization
            return self._extractive_summarize(level)

    def process(self, choice):
        """
        Process different summarization options based on user choice.

        Args:
            choice (str): The summarization option.
                "1": Brief summary
                "2": Medium summary
                "3": Detailed summary
                "4": Back to main menu

        Returns:
            str: Formatted summary result with metadata.
        """
        if choice == "1":
            level = "brief"
        elif choice == "2":
            level = "medium"
        elif choice == "3":
            level = "detailed"
        elif choice == "4":  # Back to main menu
            return None
        else:
            return "Invalid choice for summarization level."

        # Check if the text meets minimum word count before processing
        if not self.has_enough_words:
            words_needed = self.min_word_count - self.word_count
            return f"Text is too short for summarization. Current word count is {self.word_count}. Need {words_needed} more words to reach minimum of {self.min_word_count}."

        result = self.summarize(level)

        if not result["success"]:
            return result["error"]

        # Format the response nicely
        response = (
            f"\n📝 {result['description']} ({result['compression_ratio']} compression):\n\n"
            f"{result['summary']}\n\n"
            f"📊 Statistics:\n"
            f"• Original: {result['word_count']['original']} words, {result['original_sentences']} sentences\n"
            f"• Summary: {result['word_count']['summary']} words, {result['summary_sentences']} sentences"
        )

        return response
