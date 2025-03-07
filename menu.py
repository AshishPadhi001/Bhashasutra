import os
from Functions.basic import Basic
from Functions.text_visualization import TextVisualization
from Functions.advanced import Advanced

def main_menu():
    while True:
        print("\nSelect Input Method:")
        print("1. Enter Raw Text")
        print("2. Upload a File")
        choice = input("Select an option (1-2): ").strip()
        
        if choice == "1":
            return input("Enter your text: ")
        elif choice == "2":
            return file_menu()
        else:
            print("Invalid choice. Please enter 1 or 2.")

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
    user_input = main_menu()
    
    is_file = isinstance(user_input, str) and user_input.endswith((".txt", ".docx", ".pdf"))
    basic = Basic(user_input if is_file else user_input)
    advanced = Advanced(user_input if is_file else user_input)
    text = advanced.text
    
    while True:
        print("\nMain Menu:")
        print("1. Basic NLP Functions")
        print("2. Advanced NLP Functions")
        print("3. Text Visualization")
        print("4. Exit")
        
        choice = input("Select an option (1-4): ")
        
        if choice == "1":
            menu_handler({
                "1": "Count Words", "2": "Count Punctuation", "3": "Show Most Repeated Word",
                "4": "Show Least Repeated Word", "5": "Convert to Lowercase", "6": "Convert to Uppercase",
                "7": "Remove Punctuation", "8": "Back to Main Menu"
            }, basic.process)
        elif choice == "2":
            menu_handler({
                "1": "Word Tokenization", "2": "Sentence Tokenization", "3": "Remove Stopwords",
                "4": "Stemming", "5": "Lemmatization", "6": "POS Tagging",
                "7": "Sentiment Analysis", "8": "TF-IDF Vectorization", "9": "Back to Main Menu"
            }, advanced.process)
        elif choice == "3":
            menu_handler({
                "1": "Generate Word Cloud", "2": "Word Frequency Plot", "3": "Back to Main Menu"
            }, lambda x: TextVisualization(text).process(x))
        elif choice == "4":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
