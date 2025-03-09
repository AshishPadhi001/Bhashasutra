import os
import sys

# Ensure the Functions directory is in the module search path
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/Functions")

from Functions.basic import Basic
from Functions.advanced import Advanced

# Safe import for Sentiment module
try:
    from Functions.sentiment import Sentiment  # Import Sentiment class safely
except ModuleNotFoundError:
    print("Warning: Sentiment module not found. Sentiment analysis will be disabled.")
    Sentiment = None

def main_menu():
    while True:
        print("\nSelect Input Method:")
        print("1. Enter Raw Text")
        print("2. Upload a File")
        print("3. Exit")
        choice = input("Select an option (1-3): ").strip()
        
        if choice == "1":
            return input("Enter your text: "), False
        elif choice == "2":
            return file_menu(), True
        elif choice == "3":
            print("Exiting the program. Goodbye!")
            exit()
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

def file_menu():
    file_types = {"1": "txt", "2": "docx", "3": "pdf"}
    while True:
        print("\nSelect File Type:")
        for key, value in file_types.items():
            print(f"{key}. {value.upper()} File")
        
        choice = input("Select an option (1-3): ").strip()
        if choice in file_types:
            file_path = input(f"Enter the {file_types[choice].upper()} file path: ").strip()
            if file_path.endswith(f".{file_types[choice]}"):
                return file_path
            print(f"Invalid file type. Please enter a {file_types[choice].upper()} file.")
        else:
            print("Invalid choice. Please select 1, 2, or 3.")

def menu_handler(menu_dict, process_func):
    while True:
        print("\nMenu:")
        for key, value in menu_dict.items():
            print(f"{key}. {value}")
        choice = input("Select an option: ")
        
        if choice in menu_dict:
            if menu_dict[choice].lower().startswith("back"):
                break  # Exit the loop if "Back to Main Menu" is selected
            print("\nResult:", process_func(choice))
        else:
            print("Invalid choice. Please try again.")

def main():
    while True:
        user_input, is_file = main_menu()
        
        basic = Basic(user_input)
        advanced = Advanced(user_input)
        sentiment = Sentiment(user_input) if Sentiment else None
        text = advanced.text if is_file else user_input  # Use raw text for sentiment analysis
        
        while True:
            print("\nMain Menu:")
            print("1. Basic NLP Functions")
            print("2. Advanced NLP Functions")
            if Sentiment:
                print("3. Sentiment Analysis")
            print("4. Change Input Method")
            if is_file:
                print("5. Text Visualization")
                print("6. Exit")
            else:
                print("5. Exit")
            
            valid_choices = {str(i) for i in range(1, 7 if is_file else 6)}
            
            choice = input("Select an option: ")
            
            if choice not in valid_choices:
                print("Invalid choice. Please try again.")
                continue
            
            if choice == "1":
                menu_handler({
                    "1": "Count Words", "2": "Count Punctuation", "3": "Show Most Repeated Word",
                    "4": "Show Least Repeated Word", "5": "Convert to Lowercase", "6": "Convert to Uppercase",
                    "7": "Remove Punctuation", "8": "Remove Numbers", "9": "Remove Extra Whitespace",
                    "10": "Find Average Word Length", "11": "Find Average Sentence Length", "12": "Replace a Word/Phrase",
                    "13": "Reverse Text", "14": "Count Unique Words", "15": "Extract Proper Nouns", "16": "Back to Main Menu"
                }, basic.process)
            elif choice == "2":
                menu_handler({
                    "1": "Word Tokenization", "2": "Sentence Tokenization", "3": "Remove Stopwords",
                    "4": "Stemming", "5": "Lemmatization", "6": "POS Tagging",
                    "7": "TF-IDF Vectorization", "8": "Text Summarization", "9": "Language Detection",
                    "10": "Spell Checking & Grammar Correction", "11": "Back to Main Menu"
                }, advanced.process)
            elif choice == "3" and Sentiment:
                print("\nSentiment Analysis Result:", sentiment.analyze())
            elif choice == "4":
                break  # Restart input method selection
            elif choice == "5" and is_file:
                from Functions.text_visualization import TextVisualization  # Import inside function to prevent circular import
                menu_handler({
                    "1": "Generate Word Cloud", "2": "Word Frequency Plot", "3": "Sentiment Analysis Distribution Graph",
                    "4": "TF-IDF Heatmap", "5": "Back to Main Menu"
                }, lambda x: TextVisualization(text).process(x))
            elif choice == "5" or (choice == "6" and is_file):  # Always map exit to last number
                print("Exiting the program. Goodbye!")
                exit()

if __name__ == "__main__":
    main()
