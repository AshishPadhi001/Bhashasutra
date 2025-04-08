import os
import sys

# Ensure the Functions directory is in the module search path
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/Functions")

from Functions.basic import Basic
from Functions.advanced import Advanced


# Safe import for dependencies with proper error handling
def safe_import(module_name, package=None):
    try:
        if package:
            module = __import__(module_name, fromlist=[package])
            return getattr(module, package) if package else module
        else:
            return __import__(module_name)
    except ImportError as e:
        print(f"⚠ Warning: Could not import {module_name}: {e}")
        return None
    except AttributeError as e:
        print(f"⚠ Warning: Module {module_name} does not contain {package}: {e}")
        return None


# Check for transformers library
transformers = safe_import("transformers")
if not transformers:
    print(
        "⚠ Warning: Hugging Face Transformers library not found. Please install with:"
    )
    print("   pip install transformers torch")
    print("   Using fallback extractive summarization for text summarization.")

# Safe import for modules with proper error handling
text_summarizer_module = safe_import("Functions.text_summarizer")
TextSummarizer = safe_import("Functions.text_summarizer", "TextSummarizer")

sentiment_module = safe_import("Functions.Sentiment_analysis")
Sentiment = safe_import("Functions.Sentiment_analysis", "Sentiment")

visualization_module = safe_import("Functions.text_visualization")
TextVisualization = safe_import("Functions.text_visualization", "TextVisualization")


def main_menu():
    """
    Displays the main menu for selecting input methods.

    Returns:
        tuple: (user_input, is_file) where:
               - user_input: The raw text or file path.
               - is_file: Boolean indicating if input is a file.
    """
    while True:
        print("\n📌 Select Input Method:")
        print("1. Enter Raw Text (for Sentiment Analysis, NLP functions)")
        print("2. Upload a File (TXT, DOCX, PDF for Text Processing & Visualization)")
        print("3. Exit")
        choice = input("Select an option (1-3): ").strip()

        if choice == "1":
            return input("\n📝 Enter your text: "), False  # Raw text
        elif choice == "2":
            return file_menu(), True  # File-based input
        elif choice == "3":
            print("👋 Exiting the program. Goodbye!")
            exit()
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")


def file_menu():
    """
    Prompts the user to enter a file path and validates it.

    Returns:
        str: Validated file path.
    """
    while True:
        file_path = input("\n📂 Enter the full file path (TXT, DOCX, PDF): ").strip()

        if os.path.exists(file_path) and file_path.lower().endswith(
            (".txt", ".docx", ".pdf")
        ):
            return file_path
        else:
            print("❌ Invalid file. Please enter a valid TXT, DOCX, or PDF file.")


def menu_handler(menu_dict, process_func):
    """
    Displays a menu based on a dictionary and processes user selection.

    Args:
        menu_dict (dict): Dictionary mapping menu options to descriptions.
        process_func (function): Function that processes user choice.
    """
    while True:
        print("\n📌 Menu:")
        for key, value in menu_dict.items():
            print(f"{key}. {value}")

        choice = input("Select an option: ").strip()

        if choice in menu_dict:
            if menu_dict[choice].lower().startswith("back"):
                break  # Exit loop if "Back to Main Menu" is selected

            result = process_func(choice)
            if result is not None:  # Check if result is not None before printing
                print("\n🔍 Result:", result)
        else:
            print("❌ Invalid choice. Please try again.")


def check_file_word_count(file_path, min_words=250):
    """
    Check if a file has enough words for processing.

    Args:
        file_path (str): Path to the file
        min_words (int): Minimum word count required

    Returns:
        tuple: (has_enough_words, word_count)
    """
    try:
        # Create Basic instance to process the file
        basic = Basic(file_path)
        word_count = basic.count_words()
        return word_count >= min_words, word_count
    except Exception as e:
        print(f"Error checking word count: {e}")
        return False, 0


def main():
    """
    Main function that runs the interactive menu system.
    """
    # Display welcome message with info about transformer support
    print("\n🔍 NLP Text Processing Tool")

    if transformers:
        print(
            "✅ Transformer models detected: Using advanced transformer-based summarization"
        )
    else:
        print("ℹ️ Transformer models not available: Will use extractive summarization")

    while True:
        user_input, is_file = main_menu()

        # Initialize basic class for word count check
        basic = Basic(user_input)
        word_count = basic.count_words()

        # Check if the text has enough words for summarization
        min_word_count = 250
        has_enough_words = word_count >= min_word_count

        # Display word count information for files
        if is_file:
            if has_enough_words:
                print(
                    f"\n✅ File has {word_count} words (minimum {min_word_count} required for summarization)"
                )
            else:
                print(
                    f"\n⚠ File has only {word_count} words. Need {min_word_count - word_count} more words for summarization"
                )

        # Initialize advanced class
        advanced = Advanced(user_input)

        # Initialize optional modules if available
        text_summarizer = None
        if TextSummarizer and text_summarizer_module:
            try:
                text_summarizer = TextSummarizer(user_input)
            except Exception as e:
                print(f"⚠ Warning: Error initializing text summarizer: {e}")

        # Initialize sentiment analysis ONLY for raw text input
        sentiment = None
        if Sentiment and sentiment_module and not is_file:
            try:
                sentiment = Sentiment(user_input)
            except Exception as e:
                print(f"⚠ Warning: Error initializing sentiment analysis: {e}")

        # Initialize text visualization ONLY for file input
        text_viz = None
        if TextVisualization and visualization_module and is_file:
            try:
                text_viz = TextVisualization(user_input)
            except Exception as e:
                print(f"⚠ Warning: Error initializing text visualization: {e}")

        while True:
            print("\n📌 Main Menu:")
            print("1. Basic NLP Functions")
            print("2. Advanced NLP Functions")

            # Dynamic menu options based on available modules and input type
            option_num = 3
            menu_options = {}

            # Add Text Summarizer if available and text has enough words
            if text_summarizer:
                if has_enough_words:
                    summary_type = "Transformer-Based" if transformers else "Extractive"
                    print(f"{option_num}. Text Summarization ({summary_type})")
                    menu_options[str(option_num)] = "summarizer"
                else:
                    print(
                        f"{option_num}. Text Summarization (Need {min_word_count - word_count} more words)"
                    )
                    menu_options[str(option_num)] = "short_summarizer"
                option_num += 1

            # Add Sentiment Analysis if available (only for raw text input)
            if sentiment:
                print(f"{option_num}. Sentiment Analysis")
                menu_options[str(option_num)] = "sentiment"
                option_num += 1

            # Add Visualization if available (only for file input)
            if text_viz:
                print(f"{option_num}. Text Visualization")
                menu_options[str(option_num)] = "visualization"
                option_num += 1

            # Add standard options
            print(f"{option_num}. Change Input Method")
            menu_options[str(option_num)] = "change_input"
            option_num += 1

            print(f"{option_num}. Exit")
            menu_options[str(option_num)] = "exit"

            # Get user choice
            choice = input("Select an option: ").strip()

            # Process user choice
            if choice == "1":
                menu_handler(
                    {
                        "1": "Count Words",
                        "2": "Count Punctuation",
                        "3": "Show Most Repeated Word",
                        "4": "Show Least Repeated Word",
                        "5": "Convert to Lowercase",
                        "6": "Convert to Uppercase",
                        "7": "Remove Punctuation",
                        "8": "Remove Numbers",
                        "9": "Remove Extra Whitespace",
                        "10": "Find Average Word Length",
                        "11": "Find Average Sentence Length",
                        "12": "Replace a Word/Phrase",
                        "13": "Reverse Text",
                        "14": "Count Unique Words",
                        "15": "Extract Proper Nouns",
                        "16": "Redability Score",
                        "17": "Back to Main Menu",
                    },
                    basic.process,
                )
            elif choice == "2":
                menu_handler(
                    {
                        "1": "Word Tokenization",
                        "2": "Sentence Tokenization",
                        "3": "Remove Stopwords",
                        "4": "Stemming",
                        "5": "Lemmatization",
                        "6": "POS Tagging",
                        "7": "TF-IDF Vectorization",
                        "8": "Language Detection",
                        "9": "Spell Checking & Grammar Correction",
                        "10": "Named Entity Recognition",
                        "11": "Topic Modelling",
                        "12": "Back to Main Menu",
                    },
                    advanced.process,
                )
            elif choice in menu_options:
                option = menu_options[choice]

                if option == "summarizer":
                    summary_type = "Transformer-Based" if transformers else "Extractive"
                    menu_handler(
                        {
                            "1": f"Brief Summary (Most Concise) - {summary_type}",
                            "2": f"Medium Summary (Balanced) - {summary_type}",
                            "3": f"Detailed Summary (Comprehensive) - {summary_type}",
                            "4": "Back to Main Menu",
                        },
                        text_summarizer.process,
                    )
                elif option == "short_summarizer":
                    print(
                        f"\n❌ Text is too short for summarization. Current word count is {word_count}. Need {min_word_count - word_count} more words to reach minimum of {min_word_count}."
                    )
                elif option == "sentiment":
                    print("\n📊 Sentiment Analysis Result:", sentiment.analyze())
                elif option == "visualization":
                    menu_handler(
                        {
                            "1": "Generate Word Cloud",
                            "2": "Word Frequency Plot",
                            "3": "Sentiment Analysis Distribution Graph",
                            "4": "TF-IDF Heatmap",
                            "5": "Back to Main Menu",
                        },
                        lambda x: text_viz.process(int(x)),
                    )
                elif option == "change_input":
                    break
                elif option == "exit":
                    print("👋 Exiting the program. Goodbye!")
                    exit()
            else:
                print("❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
