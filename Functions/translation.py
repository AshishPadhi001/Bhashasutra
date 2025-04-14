from deep_translator import GoogleTranslator
import sys
import os

# 🔹 Dynamically add parent directory to Python's path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from basic import Basic  # Import Basic from parent directory


class Translation:
    """
    Language translation class that translates text between different languages.
    Works with raw text input using deep-translator library.
    """

    def __init__(self, input_data):
        """
        Initialize the Translation class with raw text.

        Args:
            input_data (str): Raw text to be translated.
        """
        # Initialize Basic class for text extraction and preprocessing
        self.basic = Basic(input_data)

        # Get the processed text - works for raw text
        self.text = self.basic.text

        # Common language codes dictionary for user-friendly display
        self.language_codes = {
            "afrikaans": "af",
            "albanian": "sq",
            "amharic": "am",
            "arabic": "ar",
            "armenian": "hy",
            "assamese": "as",
            "aymara": "ay",
            "azerbaijani": "az",
            "bambara": "bm",
            "basque": "eu",
            "belarusian": "be",
            "bengali": "bn",
            "bhojpuri": "bho",
            "bosnian": "bs",
            "bulgarian": "bg",
            "catalan": "ca",
            "cebuano": "ceb",
            "chichewa": "ny",
            "chinese": "zh-CN",
            "chinese (simplified)": "zh-CN",
            "chinese (traditional)": "zh-TW",
            "corsican": "co",
            "croatian": "hr",
            "czech": "cs",
            "danish": "da",
            "divehi": "dv",
            "dogri": "doi",
            "dutch": "nl",
            "english": "en",
            "esperanto": "eo",
            "estonian": "et",
            "ewe": "ee",
            "filipino": "fil",
            "finnish": "fi",
            "french": "fr",
            "frisian": "fy",
            "galician": "gl",
            "georgian": "ka",
            "german": "de",
            "greek": "el",
            "guarani": "gn",
            "gujarati": "gu",
            "haitian creole": "ht",
            "hausa": "ha",
            "hawaiian": "haw",
            "hebrew": "iw",
            "hindi": "hi",
            "hmong": "hmn",
            "hungarian": "hu",
            "icelandic": "is",
            "igbo": "ig",
            "ilocano": "ilo",
            "indonesian": "id",
            "irish": "ga",
            "italian": "it",
            "japanese": "ja",
            "javanese": "jv",
            "kannada": "kn",
            "kazakh": "kk",
            "khmer": "km",
            "kinyarwanda": "rw",
            "konkani": "gom",
            "korean": "ko",
            "krio": "kri",
            "kurdish": "ku",
            "kurdish (sorani)": "ckb",
            "kyrgyz": "ky",
            "lao": "lo",
            "latin": "la",
            "latvian": "lv",
            "lingala": "ln",
            "lithuanian": "lt",
            "luganda": "lg",
            "luxembourgish": "lb",
            "macedonian": "mk",
            "maithili": "mai",
            "malagasy": "mg",
            "malay": "ms",
            "malayalam": "ml",
            "maltese": "mt",
            "maori": "mi",
            "marathi": "mr",
            "meiteilon (manipuri)": "mni-Mtei",
            "mizo": "lus",
            "mongolian": "mn",
            "myanmar (burmese)": "my",
            "nepali": "ne",
            "norwegian": "no",
            "odia (oriya)": "or",
            "oromo": "om",
            "pashto": "ps",
            "persian": "fa",
            "polish": "pl",
            "portuguese": "pt",
            "punjabi": "pa",
            "quechua": "qu",
            "romanian": "ro",
            "russian": "ru",
            "samoan": "sm",
            "sanskrit": "sa",
            "scots gaelic": "gd",
            "sepedi": "nso",
            "serbian": "sr",
            "sesotho": "st",
            "shona": "sn",
            "sindhi": "sd",
            "sinhala": "si",
            "slovak": "sk",
            "slovenian": "sl",
            "somali": "so",
            "spanish": "es",
            "sundanese": "su",
            "swahili": "sw",
            "swedish": "sv",
            "tajik": "tg",
            "tamil": "ta",
            "tatar": "tt",
            "telugu": "te",
            "thai": "th",
            "tigrinya": "ti",
            "tsonga": "ts",
            "turkish": "tr",
            "turkmen": "tk",
            "twi": "ak",
            "ukrainian": "uk",
            "urdu": "ur",
            "uyghur": "ug",
            "uzbek": "uz",
            "vietnamese": "vi",
            "welsh": "cy",
            "xhosa": "xh",
            "yiddish": "yi",
            "yoruba": "yo",
            "zulu": "zu",
        }

        # Store supported languages - retrieved on first use
        self._supported_languages = None

    def _get_supported_languages(self):
        """
        Get list of supported languages from the GoogleTranslator.

        Returns:
            dict: Dictionary of supported languages and their codes
        """
        if self._supported_languages is None:
            # Get all supported languages
            try:
                self._supported_languages = GoogleTranslator().get_supported_languages(
                    as_dict=True
                )
            except Exception:
                # If fetching fails, use our predefined dictionary
                self._supported_languages = {
                    v: k for k, v in self.language_codes.items()
                }

        return self._supported_languages

    def translate(self, target_language="en", source_language="auto"):
        """
        Translate the text to the target language.

        Args:
            target_language (str): Language code or name to translate to (default: "en" for English).
            source_language (str): Language code to translate from (default: "auto" for auto-detection).

        Returns:
            dict: Dictionary containing original text, translated text, source and target languages.
        """
        if not self.text:
            return {"error": "No text available for translation."}

        # Convert language name to code if provided
        target_lang_code = self._get_language_code(target_language)
        source_lang_code = source_language if source_language != "auto" else "auto"

        # deep_translator has a character limit for each translation request
        # We'll split long texts into chunks and translate each chunk
        max_chunk_size = 4999  # deep_translator limit is 5000 chars

        try:
            if len(self.text) > max_chunk_size:
                chunks = [
                    self.text[i : i + max_chunk_size]
                    for i in range(0, len(self.text), max_chunk_size)
                ]
                translated_chunks = []

                # For the first chunk, we can auto-detect the language if needed
                translator = GoogleTranslator(
                    source=source_lang_code, target=target_lang_code
                )
                first_translation = translator.translate(chunks[0])
                translated_chunks.append(first_translation)

                # If source was auto, use the detected language for subsequent chunks for consistency
                if source_lang_code == "auto":
                    detected_source = translator.source
                    source_lang_code = detected_source

                    # Use detected source for remaining chunks
                    for chunk in chunks[1:]:
                        translator = GoogleTranslator(
                            source=source_lang_code, target=target_lang_code
                        )
                        translated_chunks.append(translator.translate(chunk))
                else:
                    # Source was specified, use it for all chunks
                    for chunk in chunks[1:]:
                        translated_chunks.append(translator.translate(chunk))

                translated_text = " ".join(translated_chunks)
            else:
                # For short texts, just translate directly
                translator = GoogleTranslator(
                    source=source_lang_code, target=target_lang_code
                )
                translated_text = translator.translate(self.text)

                if source_lang_code == "auto":
                    source_lang_code = translator.source

            # Get readable language names
            source_name = self._get_language_name(source_lang_code)
            target_name = self._get_language_name(target_lang_code)

            # Return results
            return {"original_text": self.text, "translated_text": translated_text}

        except Exception as e:
            return {"error": f"Translation failed: {str(e)}"}

    def detect_language(self):
        """
        Detect the language of the input text.

        Returns:
            dict: Dictionary containing detected language information.
        """
        if not self.text:
            return {"error": "No text available for language detection."}

        # Take a sample for detection if the text is very long
        sample_text = self.text[:1000] if len(self.text) > 1000 else self.text

        try:
            # deep-translator detects language during translation
            # We'll translate a short sample to English and get the detected source
            translator = GoogleTranslator(source="auto", target="en")
            translator.translate(sample_text)
            detected_lang_code = translator.source

            # Get readable language name
            language_name = self._get_language_name(detected_lang_code)

            # Return detected language info
            return {
                "language_code": detected_lang_code,
                "language_name": language_name,
                "confidence": None,  # deep-translator doesn't provide confidence scores
                "text_sample": (
                    self.text[:100] + "..." if len(self.text) > 100 else self.text
                ),
            }

        except Exception as e:
            return {"error": f"Language detection failed: {str(e)}"}

    def _get_language_code(self, language):
        """
        Convert language name to language code.

        Args:
            language (str): Language name or code.

        Returns:
            str: Language code.
        """
        # If already a code and already in proper format, return it
        if isinstance(language, str) and len(language) <= 5:
            # Check if it's a valid code directly
            supported_langs = self._get_supported_languages()
            for code in supported_langs.keys():
                if code.lower() == language.lower():
                    return code

        # Check if the language name is in our dictionary
        if isinstance(language, str) and language.lower() in self.language_codes:
            return self.language_codes[language.lower()]

        # If not found, return the input (might be a valid code)
        return language

    def _get_language_name(self, code):
        """
        Convert language code to language name.

        Args:
            code (str): Language code.

        Returns:
            str: Language name or original code if not found.
        """
        # Try to get the language name from supported languages
        supported_langs = self._get_supported_languages()
        if code in supported_langs:
            return supported_langs[code].title()

        # Fallback to our custom dictionary
        for name, lang_code in self.language_codes.items():
            if lang_code.lower() == code.lower():
                return name.title()

        # If not found, return the code
        return code

    def process(self):
        """
        Process translation request directly with user input for target language.

        Returns:
            dict: Translation result.
        """
        try:
            # First detect the source language
            detection_result = self.detect_language()

            # Ask for target language
            print(
                "\n🌐 Current text is in:",
                detection_result.get("language_name", "Unknown language"),
            )
            target_language = input("Enter target language for translation: ").strip()

            # Translate the text
            result = self.translate(target_language=target_language)

            if "error" in result:
                return result

            # Format a nice output for the user
            return {
                "From": f"{result['source_language_name']} ({result['source_language_code']})",
                "To": f"{result['target_language_name']} ({result['target_language_code']})",
                "Original": result["original_text"],
                "Translation": result["translated_text"],
            }

        except Exception as e:
            return {"error": f"Translation process failed: {str(e)}"}
