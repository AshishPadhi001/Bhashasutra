import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import numpy as np
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
import string

# Ensure necessary NLTK resources are downloaded
nltk.download('punkt')
nltk.download('stopwords')

class TextVisualization:
    """
    Class for text visualization functions including word clouds and frequency plots.
    """
    
    def __init__(self, text):
        """
        Initialize with text to visualize.
        
        Parameters:
        text (str): The text to be visualized
        """
        self.text = text
        self.processed_text = self._preprocess_text()
        
    def _preprocess_text(self):
        """
        Preprocess text by removing punctuation, converting to lowercase,
        and removing stopwords.
        """
        # Convert to lowercase and remove punctuation
        text = self.text.lower()
        text = text.translate(str.maketrans('', '', string.punctuation))
        
        # Tokenize and remove stopwords
        tokens = word_tokenize(text)
        stop_words = set(stopwords.words('english'))
        filtered_tokens = [word for word in tokens if word.lower() not in stop_words and len(word) > 1]
        
        return filtered_tokens
    
    def generate_word_cloud(self, output_path=None, width=800, height=400, 
                           background_color='white', max_words=100, 
                           colormap='viridis'):
        """
        Generate a word cloud from the text.
        
        Parameters:
        output_path (str): Path to save the word cloud image (optional)
        width (int): Width of the word cloud image
        height (int): Height of the word cloud image
        background_color (str): Background color of the word cloud
        max_words (int): Maximum number of words to include
        colormap (str): Matplotlib colormap to use for the word cloud
        
        Returns:
        WordCloud: WordCloud object
        """
        if not self.processed_text:
            raise ValueError("No valid text available for visualization")
            
        # Join tokens back into a single string for WordCloud
        text = ' '.join(self.processed_text)
        
        # Generate word cloud
        wordcloud = WordCloud(
            width=width, 
            height=height, 
            background_color=background_color,
            max_words=max_words,
            colormap=colormap,
            contour_width=1,
            contour_color='steelblue'
        ).generate(text)
        
        # Display word cloud
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        
        # Save if output path provided
        if output_path:
            plt.savefig(output_path, bbox_inches='tight')
            print(f"Word cloud saved to {output_path}")
        
        return wordcloud
    
    def word_frequency_plot(self, top_n=20, output_path=None):
        """
        Generate a bar plot of word frequencies.
        
        Parameters:
        top_n (int): Number of top words to include
        output_path (str): Path to save the frequency plot (optional)
        
        Returns:
        tuple: (words, frequencies) lists of the plotted data
        """
        if not self.processed_text:
            raise ValueError("No valid text available for visualization")
            
        # Count word frequencies
        word_counts = Counter(self.processed_text)
        top_words = word_counts.most_common(top_n)
        
        # Extract words and frequencies
        words = [word for word, count in top_words]
        frequencies = [count for word, count in top_words]
        
        # Create plot
        plt.figure(figsize=(12, 6))
        plt.bar(range(len(words)), frequencies, color='skyblue')
        plt.xticks(range(len(words)), words, rotation=45, ha='right')
        plt.xlabel('Words')
        plt.ylabel('Frequency')
        plt.title(f'Top {top_n} Word Frequencies')
        plt.tight_layout()
        
        # Save if output path provided
        if output_path:
            plt.savefig(output_path, bbox_inches='tight')
            print(f"Frequency plot saved to {output_path}")
        
        return words, frequencies

    def process(self, choice, **kwargs):
        """
        Process the user's visualization choice with optional parameters.
        
        Parameters:
        choice (str): Visualization choice (1 for WordCloud, 2 for Frequency Plot)
        **kwargs: Additional parameters for specific visualizations
        
        Returns:
        object: Result of the chosen visualization
        """
        options = {
            "1": lambda: self.generate_word_cloud(**kwargs),
            "2": lambda: self.word_frequency_plot(**kwargs)
        }
        
        return options.get(choice, lambda: "Invalid choice")()