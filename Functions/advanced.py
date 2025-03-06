import re
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from textblob import TextBlob
import pandas as pd
from Functions.basic import Basic  # Import the Basic class

class Advanced:
    def __init__(self, input_data):
        """
        Initialize the Advanced class with either a file path or raw text.

        Args:
        - input_data (str): A file path (PDF, DOCX, TXT) or raw text.
        """
        self.basic = Basic(input_data)  # Supports both file and raw text
        self.count_words = self.basic.count_words
        self.count_punctuation = self.basic.count_punctuation
        self.show_most_repeated_word = self.basic.show_most_repeated_word
        self.show_least_repeated_word = self.basic.show_least_repeated_word
        self.convert_to_lowercase = self.basic.convert_to_lowercase
        self.convert_to_uppercase = self.basic.convert_to_uppercase
        self.text = self.basic.text  # Extracted from file or direct raw text

    def word_tokenizer(self):
        return word_tokenize(self.text.lower())

    def sentence_tokenizer(self):
        return sent_tokenize(self.text)

    def remove_stopwords(self):
        tokens = word_tokenize(self.text.lower())
        stop_words = set(stopwords.words('english'))
        return [word for word in tokens if word not in stop_words]

    def perform_stemming(self):
        tokens = word_tokenize(self.convert_to_lowercase(self.text))
        stop_words = set(stopwords.words('english'))
        filtered_tokens = [word for word in tokens if word not in stop_words]
        stemmer = PorterStemmer()
        return [stemmer.stem(word) for word in filtered_tokens]

    def perform_lemmatization(self):
        tokens = word_tokenize(self.convert_to_lowercase(self.text))
        stop_words = set(stopwords.words('english'))
        filtered_tokens = [word for word in tokens if word not in stop_words]
        lemmatizer = WordNetLemmatizer()
        return [lemmatizer.lemmatize(word) for word in filtered_tokens]

    def pos_tagging(self):
        tokens = word_tokenize(self.convert_to_lowercase(self.text))

        if not tokens:
            return ["No tokens available for POS tagging."]

        # Simple rule-based POS tagging (fallback method)
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

    def sentiment_analysis(self):
        tokens = word_tokenize(self.convert_to_lowercase(self.text))
        stop_words = set(stopwords.words('english'))
        filtered_tokens = [word for word in tokens if word not in stop_words]

        if not filtered_tokens:
            return "No text available."

        sentiment = TextBlob(' '.join(filtered_tokens)).sentiment
        polarity = sentiment.polarity

        sentiment_category = (
            "Positive" if polarity > 0 else
            "Negative" if polarity < 0 else
            "Neutral"
        )

        return {"sentiment": sentiment_category, "polarity": polarity, "subjectivity": sentiment.subjectivity}

    def tfidf_vectorization(self):
        tokens = word_tokenize(self.convert_to_lowercase(self.text))
        stop_words = set(stopwords.words('english'))
        filtered_tokens = [word for word in tokens if word not in stop_words]

        if not filtered_tokens:
            return "No valid words available for TF-IDF vectorization."

        preprocessed_text = ' '.join(filtered_tokens)
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([preprocessed_text])
        df = pd.DataFrame(tfidf_matrix.toarray(), columns=vectorizer.get_feature_names_out())
        top_words = df.T.sort_values(by=0, ascending=False).head(10)

        return {"Top TF-IDF Words": top_words.index.tolist(), "TF-IDF Scores": top_words[0].tolist()}

    def process(self, choice):
        """
        Process the user's choice and return the corresponding text analysis result.

        Args:
        - choice (str): The option number as a string.

        Returns:
        - Result of the selected function or "Invalid choice" if the choice is not recognized.
        """
        options = {
            "1": self.word_tokenizer,
            "2": self.sentence_tokenizer,
            "3": self.remove_stopwords,
            "4": self.perform_stemming,
            "5": self.perform_lemmatization,
            "6": self.pos_tagging,
            "7": self.sentiment_analysis,
            "8": self.tfidf_vectorization
        }
        return options.get(choice, lambda: "Invalid choice")()
