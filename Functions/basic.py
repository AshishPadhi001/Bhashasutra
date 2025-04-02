import os
import PyPDF2
import docx
import string
import re
from collections import Counter

class Basic:
    """
    Basic text processing class that handles text extraction from files
    and provides fundamental text analysis functions.
    
    This class works with both file paths and raw text inputs.
    """
    def __init__(self, input_data):
        """
        Initialize the Basic class with either a file path or raw text.
        
        Args:
            input_data (str): A file path (PDF, DOCX, TXT) or raw text.
            
        Raises:
            ValueError: If input is not a string or a valid file path.
        """
        if isinstance(input_data, str) and os.path.exists(input_data):
            # Input is a file path
            self.file_path = input_data
            self.is_file = True
            self.text = self.extract_text()
        elif isinstance(input_data, str):
            # Input is raw text
            self.file_path = None
            self.is_file = False
            self.text = input_data.strip()
        else:
            raise ValueError("Input must be a file path or raw text string.")

    def extract_text(self):
        """
        Extract text from the file based on its extension.
        
        Returns:
            str: Extracted text from the file.
            
        Raises:
            ValueError: If file type is not supported.
        """
        if not self.file_path:
            return self.text
        
        # Determine file extension and use appropriate extraction method
        ext = os.path.splitext(self.file_path)[1].lower()
        if ext == ".pdf":
            return self.extract_text_from_pdf()
        elif ext == ".docx":
            return self.extract_text_from_docx()
        elif ext == ".txt":
            return self.extract_text_from_txt()
        else:
            raise ValueError("Invalid file type. Only PDF, DOCX, and TXT files are allowed.")

    def extract_text_from_pdf(self):
        """
        Extract text from a PDF file.
        
        Returns:
            str: Extracted text from the PDF.
        """
        text = ""
        try:
            with open(self.file_path, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    extracted = page.extract_text()
                    text += extracted if extracted else ""
            return text.strip()
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            return ""

    def extract_text_from_docx(self):
        """
        Extract text from a DOCX file.
        
        Returns:
            str: Extracted text from the DOCX.
        """
        try:
            doc = docx.Document(self.file_path)
            return " ".join([para.text for para in doc.paragraphs]).strip()
        except Exception as e:
            print(f"Error extracting text from DOCX: {e}")
            return ""

    def extract_text_from_txt(self):
        """
        Extract text from a TXT file.
        
        Returns:
            str: Extracted text from the TXT file.
        """
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                return file.read().strip()
        except Exception as e:
            print(f"Error extracting text from TXT: {e}")
            return ""

    def count_words(self):
        """
        Count the number of words in the text.
        
        Returns:
            int: Number of words.
        """
        words = re.findall(r'\b\w+\b', self.text)
        return len(words)

    def count_punctuation(self):
        """
        Count the number of punctuation marks in the text.
        
        Returns:
            int: Count of punctuation marks.
        """
        return sum(1 for char in self.text if char in string.punctuation)

    def show_most_repeated_word(self):
        """
        Find the most frequently occurring word in the text.
        
        Returns:
            tuple: (word, count) of the most repeated word.
        """
        words = re.findall(r'\b\w+\b', self.text)
        counter = Counter(words)
        if not counter:
            return ("None", 0)
        
        most_common = counter.most_common(1)[0]
        return most_common  # Return (word, count) tuple

    def show_least_repeated_word(self):
        """
        Find the least frequently occurring word in the text.
        
        Returns:
            tuple: (word, count) of the least repeated word.
        """
        words = re.findall(r'\b\w+\b', self.text)
        counter = Counter(words)
        return min(counter.items(), key=lambda x: x[1]) if counter else ("None", 0)

    def convert_to_lowercase(self, text=None):
        """
        Convert text to lowercase.
        
        Args:
            text (str, optional): Text to convert. If None, uses the stored text.
            
        Returns:
            str: Lowercase text.
        """
        return (text or self.text).lower()

    def convert_to_uppercase(self, text=None):
        """
        Convert text to uppercase.
        
        Args:
            text (str, optional): Text to convert. If None, uses the stored text.
            
        Returns:
            str: Uppercase text.
        """
        return (text or self.text).upper()
    
    def remove_punctuation(self, text=None):
        """
        Remove punctuation from text.
        
        Args:
            text (str, optional): Text to process. If None, uses the stored text.
            
        Returns:
            str: Text with punctuation removed.
        """
        return re.sub(f"[{string.punctuation}]", "", text or self.text)
    
    def remove_numbers(self):
        """
        Remove all numbers from the text.
        
        Returns:
            str: Text with numbers removed.
        """
        return re.sub(r'\d+', '', self.text)

    def remove_extra_whitespace(self):
        """
        Remove extra whitespace, including leading and trailing.
        
        Returns:
            str: Text with normalized whitespace.
        """
        return re.sub(r'\s+', ' ', self.text).strip()

    def find_average_word_length(self):
        """
        Calculate the average length of words in the given text.
        
        Args:
            text (str): Input text.

        Returns:
            float: Average word length or 0 if no words found.
        """
        words = re.findall(r'\w+', self.text)  # Extract words (ignoring punctuation)
        
        if not words:
            return 0.0  # Avoid division by zero
        
        total_length = sum(len(word) for word in words)
        avg_length = total_length / len(words)
        
        return round(avg_length, 2)  # Rounded for better readability



    def find_average_sentence_length(self):
        """
        Calculate the average number of words per sentence.
        
        Returns:
            float: Average sentence length in words or 0 if no sentences found.
        """
        sentences = re.split(r'[.!?]', self.text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if not sentences:
            return 0
            
        avg_length = sum(len(s.split()) for s in sentences) / len(sentences)
        return avg_length
    
    def replace_word(self, old_word, new_word):
        """
        Replace all occurrences of a word with another word.
        
        Args:
            old_word (str): Word to be replaced.
            new_word (str): Word to replace with.
            
        Returns:
            str: Text with replacements made.
        """
        return self.text.replace(old_word, new_word)
    
    def reverse_text(self):
        """
        Reverse the entire text.
        
        Returns:
            str: Reversed text.
        """
        return self.text[::-1]
    
    def count_unique_words(self):
        """
        Count the number of unique words in the text.
        
        Returns:
            int: Count of unique words.
        """
        words = re.findall(r'\b\w+\b', self.text)
        return len(set(words))
    
    def extract_proper_nouns(self):
        """
        Extract words that are likely proper nouns (capitalized).
        
        Returns:
            list: List of potential proper nouns.
        """
        words = re.findall(r'\b[A-Z][a-z]*\b', self.text)
        return list(set(words))
    
    def process(self, choice):
        """
        Process the user's choice and return the corresponding text analysis result.
        
        Args:
            choice (str): Option number as a string.
            
        Returns:
            Various: Result of the selected function or "Invalid choice" message.
        """
        functions = {
            "1": self.count_words,
            "2": self.count_punctuation,
            "3": self.show_most_repeated_word,
            "4": self.show_least_repeated_word,
            "5": self.convert_to_lowercase,
            "6": self.convert_to_uppercase,
            "7": self.remove_punctuation,
            "8": self.remove_numbers,
            "9": self.remove_extra_whitespace,
            "10": self.find_average_word_length,
            "11": self.find_average_sentence_length,
            "12": lambda: self.replace_word(input("Enter word to replace: "), input("Enter new word: ")),
            "13": self.reverse_text,
            "14": self.count_unique_words,
            "15": self.extract_proper_nouns
        }
        
        if choice in functions:
            return functions[choice]()
        else:
            return "Invalid choice"