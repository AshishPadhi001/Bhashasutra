import sys
import os
import shutil
from fastapi import UploadFile

# 🔹 Dynamically add 'Functions/' to Python's path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../Functions"))
)

# ✅ Now import `Advanced` AFTER modifying sys.path
from advanced import Advanced  # Import Advanced class from Functions/advanced.py


### 📌 FUNCTION TO PROCESS TEXT ###
def process_text_function(text: str, function: str) -> str:
    """
    Process text based on the requested function.
    """
    advanced_instance = Advanced(text)

    function_mapping = {
        "word_tokenizer": advanced_instance.word_tokenizer,
        "sentence_tokenizer": advanced_instance.sentence_tokenizer,
        "remove_stopwords": advanced_instance.remove_stopwords,
        "perform_stemming": advanced_instance.perform_stemming,
        "perform_lemmatization": advanced_instance.perform_lemmatization,
        "pos_tagging": advanced_instance.pos_tagging,
        "tfidf_vectorization": advanced_instance.tfidf_vectorization,
        "language_detection": advanced_instance.language_detection,
        "spell_check_and_grammar": advanced_instance.spell_check_and_grammar,
        "named_entity_recognition": advanced_instance.named_entity_recognition,
        "topic_modeling": advanced_instance.topic_modeling,
    }

    return function_mapping.get(function, lambda: "Invalid function")()


### 📌 FUNCTION TO PROCESS FILE ###
async def process_file_function(file: UploadFile, function: str) -> str:
    """
    Process a file, extract its text, and apply the function.
    """
    file_path = f"temp/{file.filename}"

    # 🔹 Ensure temp directory exists
    os.makedirs("temp", exist_ok=True)

    # 🔹 Save file temporarily
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        advanced_instance = Advanced(file_path)  # Extract text
        extracted_text = advanced_instance.text
        return process_text_function(extracted_text, function)
    except Exception as e:
        return f"Error processing file: {str(e)}"
    finally:
        # 🔹 Cleanup temp file
        if os.path.exists(file_path):
            os.remove(file_path)
