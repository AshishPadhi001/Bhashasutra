#Basic.py

import os
import PyPDF2
import docx
import string
import re
from collections import Counter

class Basic:
    def __init__(self, file_path):
        self.file_path = file_path
        self.text = self.extract_text()
    
    def extract_text(self):
        ext = os.path.splitext(self.file_path)[1].lower()  # Get file extension
        if ext == ".pdf":
            return self.extract_text_from_pdf()
        elif ext == ".docx":
            return self.extract_text_from_docx()
        elif ext == ".txt":
            return self.extract_text_from_txt()
        else:
            raise ValueError("Invalid file type. Only PDF, DOCX, and TXT files are allowed.")
    
    def extract_text_from_pdf(self):
        text = ""
        with open(self.file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                extracted = page.extract_text()
                text += extracted if extracted else ""  # Handle None case
        return text.strip()
    
    def extract_text_from_docx(self):
        doc = docx.Document(self.file_path)
        return " ".join([para.text for para in doc.paragraphs]).strip()
    
    def extract_text_from_txt(self):
        with open(self.file_path, "r", encoding="utf-8") as file:
            return file.read().strip()
    
    def count_words(self):
        words = re.findall(r'\b\w+\b', self.text)  # More accurate word counting
        return len(words)
    
    def count_punctuation(self):
        return sum(1 for char in self.text if char in string.punctuation)
    
    def show_most_repeated_word(self):
        words = re.findall(r'\b\w+\b', self.text)
        counter = Counter(words)
        return counter.most_common(1)[0] if counter else ("None", 0)
    
    def show_least_repeated_word(self):
        words = re.findall(r'\b\w+\b', self.text)
        counter = Counter(words)
        return min(counter.items(), key=lambda x: x[1]) if counter else ("None", 0)
    
    def convert_to_lowercase(self):
        return self.text.lower()
    
    def convert_to_uppercase(self):
        return self.text.upper()
    
    def process(self, choice):
        options = {
            "1": self.count_words,
            "2": self.count_punctuation,
            "3": self.show_most_repeated_word,
            "4": self.show_least_repeated_word,
            "5": self.convert_to_lowercase,
            "6": self.convert_to_uppercase
        }

        if choice in options:
            return options[choice]()
        else:
            return "Invalid choice"
