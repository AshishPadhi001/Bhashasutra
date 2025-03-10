import os
import sys

# Ensure the Functions directory is in the module search path
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/Functions")

from Functions.basic import Basic
from Functions.advanced import Advanced

# Safe import for Sentiment module (only for raw text)
try:
    from Functions.Sentiment_analysis import Sentiment
except ModuleNotFoundError:
    print("⚠ Warning: Sentiment module not found. Sentiment analysis will be disabled.")
    Sentiment = None

# Safe import for Text Visualization (only for file input)
try:
    from Functions.text_visualization import TextVisualization
except ModuleNotFoundError:
    print("⚠ Warning: Text Visualization module not found. Visualization features will be disabled.")
    TextVisualization = None

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
        
        if os.path.exists(file_path) and file_path.lower().endswith((".txt", ".docx", ".pdf")):
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
            print("\n🔍 Result:", process_func(choice))
        else:
            print("❌ Invalid choice. Please try again.")

def main():
    """
    Main function that runs the interactive menu system.
    """
    while True:
        user_input, is_file = main_menu()
        
        # Initialize classes based on input type
        basic = Basic(user_input)
        advanced = Advanced(user_input)
        sentiment = Sentiment(user_input) if Sentiment and not is_file else None  # Only for raw text
        text = advanced.text  # Always use extracted text from Advanced class

        while True:
            print("\n📌 Main Menu:")
            print("1. Basic NLP Functions")
            print("2. Advanced NLP Functions")
            
            if not is_file and Sentiment:  # Only show Sentiment Analysis for raw text
                print("3. Sentiment Analysis")
                print("4. Change Input Method")
                print("5. Exit")
                valid_choices = {"1", "2", "3", "4", "5"}
            elif is_file and TextVisualization:  # Only show Text Visualization for file input
                print("3. Text Visualization")
                print("4. Change Input Method")
                print("5. Exit")
                valid_choices = {"1", "2", "3", "4", "5"}
            else:
                print("3. Change Input Method")
                print("4. Exit")
                valid_choices = {"1", "2", "3", "4"}

            choice = input("Select an option: ").strip()
            
            if choice not in valid_choices:
                print("❌ Invalid choice. Please try again.")
                continue
            
            if choice == "1":
                menu_handler({
                    "1": "Count Words", "2": "Count Punctuation", "3": "Show Most Repeated Word",
                    "4": "Show Least Repeated Word", "5": "Convert to Lowercase", "6": "Convert to Uppercase",
                    "7": "Remove Punctuation", "8": "Remove Numbers", "9": "Remove Extra Whitespace",
                    "10": "Find Average Word Length", "11": "Find Average Sentence Length", 
                    "12": "Replace a Word/Phrase", "13": "Reverse Text", "14": "Count Unique Words", 
                    "15": "Extract Proper Nouns", "16": "Back to Main Menu"
                }, basic.process)
            elif choice == "2":
                menu_handler({
                    "1": "Word Tokenization", "2": "Sentence Tokenization", "3": "Remove Stopwords",
                    "4": "Stemming", "5": "Lemmatization", "6": "POS Tagging",
                    "7": "TF-IDF Vectorization", "8": "Text Summarization", "9": "Language Detection",
                    "10": "Spell Checking & Grammar Correction", "11": "Back to Main Menu"
                }, advanced.process)
            elif choice == "3" and not is_file and Sentiment:
                print("\n📊 Sentiment Analysis Result:", sentiment.analyze())
            elif choice == "3" and is_file and TextVisualization:
                menu_handler({
                    "1": "Generate Word Cloud", 
                    "2": "Word Frequency Plot", 
                    "3": "Sentiment Analysis Distribution Graph",
                    "4": "TF-IDF Heatmap", 
                    "5": "Back to Main Menu"
                }, lambda x: TextVisualization(user_input).process(int(x)))
            elif choice == "4":  # Change Input Method
                break
            elif choice == "5":  # Exit condition
                print("👋 Exiting the program. Goodbye!")
                exit()

if __name__ == "__main__":
    main()
