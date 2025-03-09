from textblob import TextBlob
import sys
import os

# 🔹 Add `Functions/` to Python’s path manually
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from basic import Basic  # Import from Functions/basic.py


class Sentiment:
    """
    Sentiment analysis class that analyzes the emotional tone of text.
    Now works with both file-based input and raw text.
    """
    def __init__(self, input_data):
        """
        Initialize the Sentiment class with either a file path or raw text.
        
        Args:
            input_data (str): A file path (PDF, DOCX, TXT) or raw text.
        """
        # Initialize Basic class for text extraction and preprocessing
        self.basic = Basic(input_data)
        
        # Get the processed text - works for both file and raw text
        self.text = self.basic.text
        
        # Preprocess text for better sentiment analysis
        # Remove punctuation and convert to lowercase
        self.processed_text = self.basic.remove_punctuation(
            self.basic.convert_to_lowercase(self.text)
        )

    def analyze(self):
        """
        Perform sentiment analysis on the processed text.
        
        Returns:
            dict: Dictionary containing sentiment category, polarity, and subjectivity scores.
                - sentiment: 'Positive', 'Negative', or 'Neutral'
                - polarity: Score from -1 (negative) to 1 (positive)
                - subjectivity: Score from 0 (objective) to 1 (subjective)
        """
        if not self.text:
            return {
                "sentiment": "Unknown",
                "polarity": 0.0,
                "subjectivity": 0.0,
                "error": "No text available for sentiment analysis."
            }

        # Analyze sentiment using TextBlob
        analysis = TextBlob(self.text).sentiment
        polarity = analysis.polarity
        
        # Categorize sentiment based on polarity score
        sentiment_category = (
            "Positive" if polarity > 0 else
            "Negative" if polarity < 0 else
            "Neutral"
        )
        
        # Return comprehensive results
        return {
            "sentiment": sentiment_category,
            "polarity": polarity,
            "subjectivity": analysis.subjectivity,
            "text_sample": self.text[:100] + "..." if len(self.text) > 100 else self.text
        }
        
    def get_detailed_analysis(self):
        """
        Provide a more detailed analysis with sentence-level breakdown.
        
        Returns:
            dict: Detailed sentiment analysis including overall and sentence-level.
        """
        if not self.text:
            return {"error": "No text available for detailed sentiment analysis."}
            
        # Get overall sentiment
        overall = self.analyze()
        
        # Analyze individual sentences
        blob = TextBlob(self.text)
        sentences = []
        
        for sentence in blob.sentences:
            if len(sentence.string.strip()) > 0:
                polarity = sentence.sentiment.polarity
                sentiment_category = (
                    "Positive" if polarity > 0 else
                    "Negative" if polarity < 0 else
                    "Neutral"
                )
                
                sentences.append({
                    "text": sentence.string,
                    "sentiment": sentiment_category,
                    "polarity": polarity,
                    "subjectivity": sentence.sentiment.subjectivity
                })
        
        # Return comprehensive analysis
        return {
            "overall": overall,
            "sentences": sentences,
            "sentence_count": len(sentences),
            "positive_sentences": sum(1 for s in sentences if s["sentiment"] == "Positive"),
            "negative_sentences": sum(1 for s in sentences if s["sentiment"] == "Negative"),
            "neutral_sentences": sum(1 for s in sentences if s["sentiment"] == "Neutral")
        }