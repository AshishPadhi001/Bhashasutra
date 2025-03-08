from textblob import TextBlob
from Functions.basic import Basic
from Functions.advanced import Advanced

class Sentiment:
    def __init__(self, input_data):
        """
        Initialize the Sentiment class with either raw text or a file.
        
        Args:
        - input_data (str): Raw text or file path.
        """
        self.basic = Basic(input_data)
        self.advanced = Advanced(input_data)
        self.text = self.advanced.text if isinstance(input_data, str) and input_data.endswith((".txt", ".docx", ".pdf")) else input_data

    def analyze(self):
        """
        Perform sentiment analysis on the processed text.
        """
        if not self.text:
            return "No text available for sentiment analysis."

        analysis = TextBlob(self.text).sentiment
        polarity = analysis.polarity
        sentiment_category = (
            "Positive" if polarity > 0 else
            "Negative" if polarity < 0 else
            "Neutral"
        )
        return {
            "sentiment": sentiment_category,
            "polarity": polarity,
            "subjectivity": analysis.subjectivity
        }
