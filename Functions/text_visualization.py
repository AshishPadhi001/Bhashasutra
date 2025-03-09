import os
import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns  # For heatmap
from wordcloud import WordCloud
from collections import Counter
import numpy as np
import pandas as pd
from Functions.advanced import Advanced
from Functions.basic import Basic
from Functions.Sentiment_analysis import Sentiment  # Import Sentiment class

class TextVisualization:
    """
    Class for text visualization functions including word clouds, frequency plots, sentiment distribution, and TF-IDF heatmaps.
    """
    
    def __init__(self, input_data, document_name="default"):
        """
        Initialize with input data (file path or raw text) and document name.
        """
        self.advanced = Advanced(input_data)
        self.basic = Basic(input_data)
        self.sentiment = Sentiment(input_data)  # Initialize Sentiment Analysis
        
        # Preprocessing
        self.text = self.advanced.convert_to_lowercase()
        self.text = self.basic.remove_punctuation(self.text)
        self.tokens = self.advanced.word_tokenizer()
        self.filtered_tokens = self.advanced.remove_stopwords()
        
        self.document_name = document_name
        
        # Define output directories
        self.wordcloud_folder = "wordclouds"
        self.freqplot_folder = "frequency_plots"
        self.sentiment_folder = "sentiment_graphs"
        self.tfidf_folder = "tfidf_heatmaps"
        
        os.makedirs(os.path.join(self.wordcloud_folder, self.document_name), exist_ok=True)
        os.makedirs(os.path.join(self.freqplot_folder, self.document_name), exist_ok=True)
        os.makedirs(os.path.join(self.sentiment_folder, self.document_name), exist_ok=True)
        os.makedirs(os.path.join(self.tfidf_folder, self.document_name), exist_ok=True)
    
    def generate_sentiment_analysis_graph(self):
        """Generate and save a sentiment analysis distribution graph."""
        sentiment_results = self.sentiment.analyze()
        
        plt.figure(figsize=(8, 5))
        plt.bar(sentiment_results.keys(), sentiment_results.values(), color=['green', 'red', 'gray'])
        plt.xlabel("Sentiment")
        plt.ylabel("Score")
        plt.title("Sentiment Analysis Distribution")
        
        output_path = os.path.join(self.sentiment_folder, self.document_name, "sentiment_analysis.jpeg")
        plt.savefig(output_path, bbox_inches='tight')
        print(f"Sentiment analysis graph saved to {output_path}")
        
        plt.show()
    
    def process(self, choice):
        """Process user selection."""
        print(f"Debug: Received choice -> {choice} (Type: {type(choice)})")  # Debug print
        
        try:
            choice = int(choice)  # Ensure it's an integer
        except ValueError:
            raise ValueError(f"Invalid selection: {choice} (not an integer)")
        
        if choice == 1:
            return self.generate_word_cloud()
        elif choice == 2:
            return self.generate_word_frequency_plot()
        elif choice == 3:
            return self.generate_sentiment_distribution()
        elif choice == 4:
            return self.generate_tfidf_heatmap()
        elif choice == 5:
            return self.generate_sentiment_analysis_graph()
        elif choice == 6:
            print("Returning to main menu...")
            return None
        else:
            raise ValueError(f"Invalid selection: {choice}")
