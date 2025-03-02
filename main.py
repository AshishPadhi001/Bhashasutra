from Functions.basic import Basic
from Functions.advanced import Advanced

def basic_menu(basic):
    menu = {
        "1": "Count Words",
        "2": "Count Punctuation",
        "3": "Show Most Repeated Word",
        "4": "Show Least Repeated Word",
        "5": "Convert to Lowercase",
        "6": "Convert to Uppercase",
        "7": "Back to Main Menu"
    }
    
    while True:
        print("\nBasic NLP Menu:")
        for key, value in menu.items():
            print(f"{key}. {value}")
        
        choice = input("Select an option (1-7): ")
        if choice == "7":
            break  # Return to the main menu
        
        result = basic.process(choice)
        print("\nResult:", result)

def advanced_menu(advanced):
    menu = {
        "1": "Tokenization",
        "2": "Remove Stopwords",
        "3": "Stemming",
        "4": "Lemmatization",
        "5": "POS Tagging",
        "6": "Sentiment Analysis",
        "7": "TF-IDF Vectorization",
        "8": "Back to Main Menu"
    }
    
    while True:
        print("\nAdvanced NLP Menu:")
        for key, value in menu.items():
            print(f"{key}. {value}")
        
        choice = input("Select an option (1-8): ")
        if choice == "8":
            break  # Return to the main menu
        
        result = advanced.process(choice)
        print("\nResult:", result)

def main():
    file_path = input("Enter the file path: ")
    basic = Basic(file_path)
    advanced = Advanced(file_path)
    
    while True:
        print("\nMain Menu:")
        print("1. Basic NLP Functions")
        print("2. Advanced NLP Functions")
        print("3. Exit")
        
        choice = input("Select an option (1-3): ")
        if choice == "1":
            basic_menu(basic)
        elif choice == "2":
            advanced_menu(advanced)
        elif choice == "3":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()