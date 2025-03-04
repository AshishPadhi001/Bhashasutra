import re
import string
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from textblob import TextBlob
from Functions.basic import Basic  # Import the Basic class

# Download NLTK resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

class Advanced:
    def __init__(self, file_path):
        # Create an instance of Basic class
        self.basic = Basic(file_path)
        
        # Add all Basic methods as attributes of Advanced class
        self.count_words = self.basic.count_words
        self.count_punctuation = self.basic.count_punctuation
        self.show_most_repeated_word = self.basic.show_most_repeated_word
        self.show_least_repeated_word = self.basic.show_least_repeated_word
        self.convert_to_lowercase = self.basic.convert_to_lowercase
        self.convert_to_uppercase = self.basic.convert_to_uppercase
        
        # Text 
        self.text = self.basic.text

    def word_tokenizer(self):
        """
        Tokenize text into words.
        Steps:
        1. Get the text
        2. Convert to lowercase
        3. Tokenize words
        """
        # Get the text
        text = self.text
        
        # Convert to lowercase
        text = self.convert_to_lowercase(text)
        
        # Tokenize words
        return word_tokenize(text)

    def sentence_tokenizer(self):
        """
        Tokenize text into sentences.
        Steps:
        1. Get the text
        2. Tokenize sentences
        """
        # Get the text
        text = self.text
        
        # Tokenize sentences
        return sent_tokenize(text)

    def remove_stopwords(self):
        """
        Remove stopwords from tokenized text.
        """
        #GEt the text
        #cnvert into lower
        #convert into tokens
        #remove the stopwords
        # Get the text
        text = self.text
        
        # Convert to lower
        text = self.convert_to_lowercase(text)
        
        # Convert into tokens
        tokens = word_tokenize(text)
        
        # Remove stopwords
        stop_words = set(stopwords.words('english'))
        return [word for word in tokens if word.lower() not in stop_words]

    def perform_stemming(self):
        """
        Apply Porter stemming to filtered tokens.
        """
        #GEt the text
        #cnvert into lower
        #convert into tokens
        #Remove the stopwords
        #then perform stemmatization
        # Get the text
        text = self.text
        
        # Convert to lower
        text = self.convert_to_lowercase(text)
        
        # Convert into tokens
        tokens = word_tokenize(text)
        
        # Remove stopwords
        stop_words = set(stopwords.words('english'))
        filtered_tokens = [word for word in tokens if word.lower() not in stop_words]
        
        # Perform stemming
        stemmer = PorterStemmer()
        return [stemmer.stem(word) for word in filtered_tokens]

    def perform_lemmatization(self):
        """
        Apply lemmatization to filtered tokens.
        """
        #GEt the text
        #cnvert into lower
        #convert into tokens
        #Remove the stopwords
        #then perform lemmatization
        # Get the text
        text = self.text
        
        # Convert to lower
        text = self.convert_to_lowercase(text)
        
        # Convert into tokens
        tokens = word_tokenize(text)
        
        # Remove stopwords
        stop_words = set(stopwords.words('english'))
        filtered_tokens = [word for word in tokens if word.lower() not in stop_words]
        
        # Perform lemmatization
        lemmatizer = WordNetLemmatizer()
        return [lemmatizer.lemmatize(word) for word in filtered_tokens]

    def pos_tagging(self):
        """
        Perform Part-of-Speech tagging on filtered tokens.
        """
        #GEt the text
        #cnvert into lower
        #convert into tokens
        #Remove the stopwords
        #perform lemmatization
        #perform pos tagging
        # Get the text
        text = self.text
        
        # Convert to lower
        text = self.convert_to_lowercase(text)
        
        # Convert into tokens
        tokens = word_tokenize(text)
        
        # Remove stopwords
        stop_words = set(stopwords.words('english'))
        filtered_tokens = [word for word in tokens if word.lower() not in stop_words]
        
        # Perform POS tagging
        try:
            return nltk.pos_tag(filtered_tokens) if filtered_tokens else ["No tokens available for POS tagging."]
        except Exception as e:
            return [f"POS tagging failed: {str(e)}"]

    def sentiment_analysis(self):
        """
        Perform sentiment analysis on preprocessed text.
        """
        #get the text
        #cnvert into lower
        #convert into tokens
        #Remove the stopwords
        #Analyze the sentiment
        # Get the text
        text = self.text
        
        # Convert to lower
        text = self.convert_to_lowercase(text)
        
        # Convert into tokens
        tokens = word_tokenize(text)
        
        # Remove stopwords
        stop_words = set(stopwords.words('english'))
        filtered_tokens = [word for word in tokens if word.lower() not in stop_words]
        
        # Analyze sentiment
        sentiment = TextBlob(' '.join(filtered_tokens)).sentiment
        return {"polarity": sentiment.polarity, "subjectivity": sentiment.subjectivity} if filtered_tokens else "No text available."

    def tfidf_vectorization(self):
        """
        Compute TF-IDF vectorization.
        """
        #GEt the text
        #cnvert into lower
        #convert into tokens
        #Remove the stopwords
        #perform lemmatization
        # Get the text
        text = self.text
        
        # Convert to lower
        text = self.convert_to_lowercase(text)
        
        # Convert into tokens
        tokens = word_tokenize(text)
        
        # Remove stopwords
        stop_words = set(stopwords.words('english'))
        filtered_tokens = [word for word in tokens if word.lower() not in stop_words]
        
        # Check if tokens exist
        if not filtered_tokens:
            return "No valid words available for TF-IDF vectorization."

        # Perform TF-IDF vectorization
        preprocessed_text = ' '.join(filtered_tokens)
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([preprocessed_text])
        return {
            "matrix": tfidf_matrix.toarray().tolist(), 
            "features": vectorizer.get_feature_names_out().tolist()
        }

    def process(self, choice):
        """
        Process the user's choice and return the corresponding function result.
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