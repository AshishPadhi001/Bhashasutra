import sys
import os

# 🔹 Add `Functions/` to Python’s import path manually
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../Functions")))

from Sentiment_analysis import Sentiment  # Import Sentiment class

### 📌 FUNCTION TO PROCESS TEXT SENTIMENT ANALYSIS ###
def analyze_text_sentiment(text: str, detailed: bool = False) -> dict:
    """
    Perform sentiment analysis on text.
    """
    sentiment_instance = Sentiment(text)
    return sentiment_instance.get_detailed_analysis() if detailed else sentiment_instance.analyze()
