import sys
import os
import shutil
from fastapi import UploadFile
# 🔹 Dynamically add Functions/ to Python's path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../Functions")))

from basic import Basic  # Import Basic class from Functions/basic.py

### 📌 FUNCTION TO PROCESS TEXT INPUT ###
def process_text_function(text: str, function: str) -> str:
    """
    Process raw text based on the requested function.
    """
    basic_instance = Basic(text)

    function_mapping = {
        "count_words": lambda: f"The text contains {basic_instance.count_words()} words.",
        "count_punctuation": lambda: f"The text contains {basic_instance.count_punctuation()} punctuation marks.",
        "most_repeated_word": lambda: f"The most repeated word is '{basic_instance.show_most_repeated_word()[0]}' which appears {basic_instance.show_most_repeated_word()[1]} times.",
        "least_repeated_word": lambda: f"The least repeated word is '{basic_instance.show_least_repeated_word()[0]}' which appears {basic_instance.show_least_repeated_word()[1]} times.",
        "to_lower": lambda: f"Text converted to lowercase: \"{basic_instance.convert_to_lowercase()}\"",
        "to_upper": lambda: f"Text converted to uppercase: \"{basic_instance.convert_to_uppercase()}\"",
        "remove_punctuation": lambda: f"Text with punctuation removed: \"{basic_instance.remove_punctuation()}\"",
        "remove_numbers": lambda: f"Text with numbers removed: \"{basic_instance.remove_numbers()}\"",
        "remove_extra_whitespace": lambda: f"Text with extra whitespace removed: \"{basic_instance.remove_extra_whitespace()}\"",
        "find_average_word_length": lambda: f"The average word length is {basic_instance.find_average_word_length():.2f} characters.",
        "find_average_sentence_length": lambda: f"The average sentence length is {basic_instance.find_average_sentence_length():.2f} words.",
        "reverse_text": lambda: f"Reversed text: \"{basic_instance.reverse_text()}\"",
        "count_unique_words": lambda: f"The text contains {basic_instance.count_unique_words()} unique words.",
        "extract_proper_nouns": lambda: f"Found {len(basic_instance.extract_proper_nouns())} potential proper nouns: {', '.join(basic_instance.extract_proper_nouns())}" if basic_instance.extract_proper_nouns() else "No proper nouns found in the text.",
    }

    result = function_mapping.get(function, lambda: "Invalid function")()
    return result


### 📌 FUNCTION TO PROCESS FILE UPLOAD ###
async def process_file_function(file: UploadFile, function: str) -> str:
    """
    Process a file upload, extract its text, and apply a function.
    """
    file_path = f"temp/{file.filename}"
    
    # 🔹 Ensure temp directory exists
    os.makedirs("temp", exist_ok=True)

    # 🔹 Save file temporarily
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        basic_instance = Basic(file_path)  # Extract text from file
        extracted_text = basic_instance.text
        return process_text_function(extracted_text, function)
    except Exception as e:
        return f"Error processing file: {str(e)}"
    finally:
        # 🔹 Cleanup: Delete the temporary file
        if os.path.exists(file_path):
            os.remove(file_path)