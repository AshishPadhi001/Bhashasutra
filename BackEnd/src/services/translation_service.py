import sys
import os

# 🔹 Add `Functions/` to Python's import path manually
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../Functions"))
)

from translation import Translation  # Import Translation class


def translate_text(text: str, target_language: str) -> dict:
    """
    Translate text to the target language.

    Args:
        text (str): Raw text to be translated
        target_language (str): Language code or name to translate to

    Returns:
        dict: Dictionary containing original text, translated text, and language information

    Raises:
        ValueError: If text or target_language is missing or empty
    """
    # Validate inputs
    if not text or text.strip() == "":
        raise ValueError("Text for translation cannot be empty")

    if not target_language or target_language.strip() == "":
        raise ValueError("Target language must be specified")

    # Create Translation instance with the input text
    translation_instance = Translation(text)

    # Perform the translation with the specified target language
    result = translation_instance.translate(target_language=target_language)

    # Return the translation result
    return result
