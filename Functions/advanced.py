import sys
import os
import re
import string
import pandas as pd
from textblob import TextBlob
from langdetect import detect  # Language detection
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
import nltk
import spacy

# Download necessary NLTK data if not already downloaded
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords")

try:
    nltk.data.find("corpora/wordnet")
except LookupError:
    nltk.download("wordnet")

# 🔹 Dynamically add 'Functions/' to Python's path (Same as basic_service.py)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

# ✅ Now import `Basic` AFTER modifying sys.path (Same as Basic in basic_service.py)
from basic import Basic  # Import Basic from Functions/basic.py


class Advanced:
    """
    Advanced text processing class that builds upon Basic functionality.
    Provides NLP capabilities like tokenization, stemming, lemmatization,
    TF-IDF analysis, and text summarization.

    This class works with both file paths and raw text inputs.
    """

    def __init__(self, input_data):
        """
        Initialize the Advanced class with either a file path or raw text.

        Args:
            input_data (str): A file path (PDF, DOCX, TXT) or raw text.
        """
        # Initialize basic spaCy model for NER
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            # Download the model if not already downloaded
            import subprocess

            subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
            self.nlp = spacy.load("en_core_web_sm")

        # Initialize the Basic class which handles text extraction
        self.basic = Basic(input_data)  # Supports both file and raw text

        # Import basic functions to maintain interface compatibility
        self.count_words = self.basic.count_words
        self.count_punctuation = self.basic.count_punctuation
        self.show_most_repeated_word = self.basic.show_most_repeated_word
        self.show_least_repeated_word = self.basic.show_least_repeated_word
        self.convert_to_lowercase = self.basic.convert_to_lowercase
        self.convert_to_uppercase = self.basic.convert_to_uppercase
        self.remove_punctuation = self.basic.remove_punctuation

        # Pre-process the text for advanced operations (lowercase and no punctuation)
        self.text = self.basic.text
        self.processed_text = self.remove_punctuation(
            self.convert_to_lowercase(self.text)
        )

    def word_tokenizer(self):
        """
        Split text into individual words using NLTK word tokenizer.

        Returns:
            list: List of individual word tokens
        """
        return word_tokenize(self.processed_text)

    def sentence_tokenizer(self):
        """
        Split text into sentences using NLTK sentence tokenizer.

        Returns:
            list: List of sentences
        """
        # Use original text to maintain sentence structure with punctuation
        return sent_tokenize(self.text)

    def remove_stopwords(self):
        """
        Remove common stopwords (like 'the', 'a', 'an') from the tokenized text.

        Returns:
            list: List of tokens with stopwords removed
        """
        tokens = word_tokenize(self.processed_text)
        stop_words = set(stopwords.words("english"))
        return [word for word in tokens if word not in stop_words]

    def perform_stemming(self):
        """
        Reduce words to their word stem using Porter Stemmer.
        Example: 'running' -> 'run'

        Returns:
            list: List of stemmed words
        """
        tokens = self.remove_stopwords()
        stemmer = PorterStemmer()
        return [stemmer.stem(word) for word in tokens]

    def perform_lemmatization(self):
        """
        Reduce words to their base form using WordNet Lemmatizer.
        More linguistically accurate than stemming.
        Example: 'better' -> 'good'

        Returns:
            list: List of lemmatized words
        """
        tokens = self.remove_stopwords()
        lemmatizer = WordNetLemmatizer()
        return [lemmatizer.lemmatize(word) for word in tokens]

    def pos_tagging(self):
        """
        Perform part-of-speech tagging on tokens.
        Tags words as nouns, verbs, adjectives, etc.

        Returns:
            list: List of (word, tag) tuples
        """
        tokens = word_tokenize(self.processed_text)
        if not tokens:
            return ["No tokens available for POS tagging."]

        # Rule-based POS tagging
        pos_rules = {
            r".*ing$": "VBG",  # Gerunds (e.g., running)
            r".*ed$": "VBD",  # Past tense (e.g., played)
            r".*es$": "VBZ",  # 3rd person singular present (e.g., goes)
            r".*ly$": "RB",  # Adverbs (e.g., quickly)
            r".*able$|.*ible$": "JJ",  # Adjectives (e.g., flexible)
            r".*ion$": "NN",  # Nouns (e.g., revolution)
        }

        tagged_words = []
        for word in tokens:
            tag = "NN"  # Default to noun
            for pattern, pos in pos_rules.items():
                if re.match(pattern, word):
                    tag = pos
                    break
            tagged_words.append((word, tag))
        return tagged_words

    def tfidf_vectorization(self):
        """
        Calculate TF-IDF (Term Frequency-Inverse Document Frequency) scores.
        Identifies most important words in the text based on their frequency
        and uniqueness.

        Returns:
            dict: Dictionary containing top words and their TF-IDF scores
        """
        tokens = self.remove_stopwords()
        if not tokens:
            return "No valid words available for TF-IDF vectorization."

        preprocessed_text = " ".join(tokens)
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([preprocessed_text])
        df = pd.DataFrame(
            tfidf_matrix.toarray(), columns=vectorizer.get_feature_names_out()
        )
        top_words = df.T.sort_values(by=0, ascending=False).head(10)

        return {
            "Top TF-IDF Words": top_words.index.tolist(),
            "TF-IDF Scores": top_words[0].tolist(),
        }

    def text_summarization(self):
        """
        Generate an extractive summary of the text using TextRank (alternative to gensim).

        Returns:
            str: Summarized text.
        """
        try:
            parser = PlaintextParser.from_string(self.text, Tokenizer("english"))
            summarizer = TextRankSummarizer()
            summary = summarizer(
                parser.document, sentences_count=3
            )  # Adjust sentence count
            return " ".join(str(sentence) for sentence in summary)
        except Exception as e:
            return f"Error generating summary: {e}"

    def language_detection(self):
        """
        Detect the language of the text.

        Returns:
            str: Full language name (e.g., 'English' instead of 'en') or error message
        """
        try:
            # Get the ISO language code
            lang_code = detect(self.text)

            # Map of ISO codes to full language names
            # Expanded map of ISO codes to full language names (includes all languages detected by langdetect)
            language_map = {
                "af": "Afrikaans",
                "ar": "Arabic",
                "bg": "Bulgarian",
                "bn": "Bengali",
                "ca": "Catalan",
                "cs": "Czech",
                "cy": "Welsh",
                "da": "Danish",
                "de": "German",
                "el": "Greek",
                "en": "English",
                "es": "Spanish",
                "et": "Estonian",
                "fa": "Persian",
                "fi": "Finnish",
                "fr": "French",
                "gu": "Gujarati",
                "he": "Hebrew",
                "hi": "Hindi",
                "hr": "Croatian",
                "hu": "Hungarian",
                "id": "Indonesian",
                "it": "Italian",
                "ja": "Japanese",
                "kn": "Kannada",
                "ko": "Korean",
                "lt": "Lithuanian",
                "lv": "Latvian",
                "mk": "Macedonian",
                "ml": "Malayalam",
                "mr": "Marathi",
                "ne": "Nepali",
                "nl": "Dutch",
                "no": "Norwegian",
                "pa": "Punjabi",
                "pl": "Polish",
                "pt": "Portuguese",
                "ro": "Romanian",
                "ru": "Russian",
                "sk": "Slovak",
                "sl": "Slovenian",
                "so": "Somali",
                "sq": "Albanian",
                "sv": "Swedish",
                "sw": "Swahili",
                "ta": "Tamil",
                "te": "Telugu",
                "th": "Thai",
                "tl": "Tagalog",
                "tr": "Turkish",
                "uk": "Ukrainian",
                "ur": "Urdu",
                "vi": "Vietnamese",
                "zh-cn": "Chinese (Simplified)",
                "zh-tw": "Chinese (Traditional)",
                # Additional languages detected by langdetect
                "az": "Azerbaijani",
                "be": "Belarusian",
                "bs": "Bosnian",
                "eo": "Esperanto",
                "gl": "Galician",
                "ka": "Georgian",
                "kk": "Kazakh",
                "mg": "Malagasy",
                "mn": "Mongolian",
                "mt": "Maltese",
                "si": "Sinhala",
                "sr": "Serbian",
                "xh": "Xhosa",
                "yi": "Yiddish",
                "zu": "Zulu",
            }

            # Return full language name or code if not in map
            return language_map.get(lang_code, f"Unknown language code: {lang_code}")
        except:
            return "Could not detect language."

    def spell_check_and_grammar(self):
        """
        Check and correct spelling and grammar using TextBlob.

        Returns:
            str: Corrected text
        """
        return str(TextBlob(self.text).correct())

    def named_entity_recognition(self):
        """
        Extract named entities from text using spaCy.
        Identifies people, organizations, locations, dates, etc.

        Returns:
            list: List of (entity_text, entity_type) tuples
        """
        try:
            # Use original text for better entity recognition
            doc = self.nlp(self.text)

            # Extract entities with their types
            entities = [(ent.text, ent.label_) for ent in doc.ents]

            if not entities:
                return [("No entities found", "N/A")]

            return entities
        except Exception as e:
            return [(f"Error in NER: {str(e)}", "ERROR")]

    def topic_modeling(self, num_topics=5, num_words=10):
        """
        Perform LDA topic modeling to identify main topics in text.

        Args:
            num_topics (int): Number of topics to extract
            num_words (int): Number of words per topic to display

        Returns:
            dict: Dictionary with topics as keys and lists of words as values
        """
        try:
            # Create cleaned text without stopwords for better topic modeling
            tokens = self.remove_stopwords()
            cleaned_text = " ".join(tokens)

            # Check if there's enough text for topic modeling
            if len(tokens) < 50:
                return {
                    "Error": [
                        "Text too short for meaningful topic modeling. Need at least 50 words."
                    ]
                }

            # Create bag of words representation
            vectorizer = CountVectorizer(max_df=0.95, min_df=2, max_features=1000)
            X = vectorizer.fit_transform([cleaned_text])

            # Apply LDA
            lda = LatentDirichletAllocation(
                n_components=num_topics,
                max_iter=10,
                learning_method="online",
                random_state=42,
            )
            lda.fit(X)

            # Get feature names (words)
            feature_names = vectorizer.get_feature_names_out()

            # Format topics
            topics = {}
            for topic_idx, topic in enumerate(lda.components_):
                topic_words = [
                    feature_names[i] for i in topic.argsort()[: -num_words - 1 : -1]
                ]
                topics[f"Topic {topic_idx+1}"] = topic_words

            return topics
        except Exception as e:
            return {"Error": [f"Error in topic modeling: {str(e)}"]}

    def process(self, choice):
        """
        Process the user's choice and return the corresponding text analysis result.

        Args:
            choice (str): The option number as a string.

        Returns:
            Various: Result of the selected function or "Invalid choice" if the choice is not recognized.
        """
        options = {
            "1": self.word_tokenizer,
            "2": self.sentence_tokenizer,
            "3": self.remove_stopwords,
            "4": self.perform_stemming,
            "5": self.perform_lemmatization,
            "6": self.pos_tagging,
            "7": self.tfidf_vectorization,
            "8": self.language_detection,
            "9": self.spell_check_and_grammar,
            "10": self.named_entity_recognition,
            "11": self.topic_modeling,
        }
        return options.get(choice, lambda: "Invalid choice")()
