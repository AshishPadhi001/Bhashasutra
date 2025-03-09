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
        "count_words": lambda: str(basic_instance.count_words()),  # Convert to string
        "count_punctuation": lambda: str(basic_instance.count_punctuation()),
        "most_repeated_word": lambda: str(basic_instance.show_most_repeated_word()),
        "least_repeated_word": lambda: str(basic_instance.show_least_repeated_word()),
        "to_lower": lambda: str(basic_instance.convert_to_lowercase()),
        "to_upper": lambda: str(basic_instance.convert_to_uppercase()),
        "remove_punctuation": lambda: str(basic_instance.remove_punctuation()),
        "remove_numbers": lambda: str(basic_instance.remove_numbers()),
        "remove_extra_whitespace": lambda: str(basic_instance.remove_extra_whitespace()),
        "find_average_word_length": lambda: str(basic_instance.find_average_word_length()),
        "find_average_sentence_length": lambda: str(basic_instance.find_average_sentence_length()),
        "reverse_text": lambda: str(basic_instance.reverse_text()),
        "count_unique_words": lambda: str(basic_instance.count_unique_words()),
        "extract_proper_nouns": lambda: str(basic_instance.extract_proper_nouns()),
    }

    return function_mapping.get(function, lambda: "Invalid function")()


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
