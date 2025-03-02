

import re
import string
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from textblob import TextBlob
from Functions.basic import Basic

# Directly download the necessary resources
# This ensures they're available before attempting to use them
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger_eng ')  # This is the correct resource name


class Advanced:
    """
    Advanced NLP class providing functionalities such as stemming, lemmatization, POS tagging,
    sentiment analysis, and TF-IDF vectorization.
    """

    def __init__(self, file_path):
        self.basic = Basic(file_path)
        self.text = self.preprocess_text()
        self.tokens = word_tokenize(self.text) if self.text else []
        self.filtered_tokens = self.remove_stopwords()

    def preprocess_text(self):
        """Convert text to lowercase and remove punctuation."""
        text = self.basic.convert_to_lowercase()
        return text.translate(str.maketrans('', '', string.punctuation))

    def remove_stopwords(self):
        """Remove stopwords from tokenized text."""
        stop_words = set(stopwords.words('english'))
        return [word for word in self.tokens if word.lower() not in stop_words]

    def perform_stemming(self):
        """Apply Porter stemming to filtered tokens."""
        stemmer = PorterStemmer()
        return [stemmer.stem(word) for word in self.filtered_tokens]

    def perform_lemmatization(self):
        """Apply lemmatization to filtered tokens."""
        lemmatizer = WordNetLemmatizer()
        return [lemmatizer.lemmatize(word) for word in self.filtered_tokens]

    def pos_tagging(self):
        """Perform Part-of-Speech tagging on filtered tokens."""
        try:
            # First try the standard pos_tag function
            return nltk.pos_tag(self.filtered_tokens) if self.filtered_tokens else ["No tokens available for POS tagging."]
        except LookupError:
            # If it fails, implement a fallback solution
            try:
                # Explicitly download the resource again if needed
                nltk.download('averaged_perceptron_tagger')
                # Try again after downloading
                return nltk.pos_tag(self.filtered_tokens) if self.filtered_tokens else ["No tokens available for POS tagging."]
            except Exception as e:
                # If all else fails, return information about the error
                return [f"POS tagging failed: {str(e)}. Try running 'nltk.download('averaged_perceptron_tagger')' manually."]

    def sentiment_analysis(self):
        """Perform sentiment analysis on preprocessed text."""
        sentiment = TextBlob(self.text).sentiment
        return {"polarity": sentiment.polarity, "subjectivity": sentiment.subjectivity} if self.text else "No text available."

    def tfidf_vectorization(self):
        """Compute TF-IDF vectorization."""
        if not self.filtered_tokens:
            return "No valid words available for TF-IDF vectorization."

        preprocessed_text = ' '.join(self.filtered_tokens)
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([preprocessed_text])
        return {"matrix": tfidf_matrix.toarray().tolist(), "features": vectorizer.get_feature_names_out().tolist()}

    def process(self, choice):
        """
        Process the user's choice and return the corresponding NLP function result.
        """
        options = {
            "1": lambda: self.tokens,
            "2": lambda: self.filtered_tokens,
            "3": lambda: self.perform_stemming(),
            "4": lambda: self.perform_lemmatization(),
            "5": lambda: self.pos_tagging(),
            "6": lambda: self.sentiment_analysis(),
            "7": lambda: self.tfidf_vectorization()
        }

        return options.get(choice, lambda: "Invalid choice")()