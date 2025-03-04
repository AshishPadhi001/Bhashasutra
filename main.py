from Functions.basic import Basic
from Functions.advanced import Advanced
from Functions.text_visualization import TextVisualization

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
        "1": "Word Tokenization",
        "2": "Sentence Tokenization",
        "3": "Remove Stopwords",
        "4": "Stemming",
        "5": "Lemmatization",
        "6": "POS Tagging",
        "7": "Sentiment Analysis",
        "8": "TF-IDF Vectorization",
        "9": "Back to Main Menu"
    }
    
    while True:
        print("\nAdvanced NLP Menu:")
        for key, value in menu.items():
            print(f"{key}. {value}")
        
        choice = input("Select an option (1-9): ")
        if choice == "9":
            break  # Return to the main menu
        
        result = advanced.process(choice)
        print("\nResult:", result)

def visualization_menu(text):
    visualization = TextVisualization(text)
    menu = {
        "1": "Generate Word Cloud",
        "2": "Word Frequency Plot",
        "3": "Back to Main Menu"
    }
    
    while True:
        print("\nText Visualization Menu:")
        for key, value in menu.items():
            print(f"{key}. {value}")
        
        choice = input("Select an option (1-3): ")
        if choice == "3":
            break  # Return to the main menu
        
        result = visualization.process(choice)
        print("\nResult:", result)

def main():
    file_path = input("Enter the file path: ")
    basic = Basic(file_path)
    advanced = Advanced(file_path)
    text = basic.text  # Extract text for visualization
    
    while True:
        print("\nMain Menu:")
        print("1. Basic NLP Functions")
        print("2. Advanced NLP Functions")
        print("3. Text Visualization")
        print("4. Exit")
        
        choice = input("Select an option (1-4): ")
        if choice == "1":
            basic_menu(basic)
        elif choice == "2":
            advanced_menu(advanced)
        elif choice == "3":
            visualization_menu(text)
        elif choice == "4":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
