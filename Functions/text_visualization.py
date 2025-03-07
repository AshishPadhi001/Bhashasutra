import os
import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
from Functions.advanced import Advanced
from Functions.basic import Basic

class TextVisualization:
    """
    Class for text visualization functions including word clouds and frequency plots.
    """
    
    def __init__(self, input_data, document_name="default"):
        """
        Initialize with input data (file path or raw text) and document name.
        """
        self.advanced = Advanced(input_data)
        self.basic = Basic(input_data)
        
        # Preprocessing
        self.text = self.advanced.convert_to_lowercase()
        self.text = self.basic.remove_punctuation(self.text)
        self.tokens = self.advanced.word_tokenizer()
        self.filtered_tokens = self.advanced.remove_stopwords()
        
        self.document_name = document_name
        
        # Define output directories
        self.wordcloud_folder = "wordclouds"
        self.freqplot_folder = "frequency_plots"
        
        os.makedirs(os.path.join(self.wordcloud_folder, self.document_name), exist_ok=True)
        os.makedirs(os.path.join(self.freqplot_folder, self.document_name), exist_ok=True)
    
    def generate_word_cloud(self, width=800, height=400, background_color='white',
                            max_words=100, colormap='viridis'):
        """Generate and save a word cloud as a JPEG file."""
        if not self.filtered_tokens:
            raise ValueError("No valid text available for visualization")
        
        text = ' '.join(self.filtered_tokens)
        wordcloud = WordCloud(
            width=width,
            height=height,
            background_color=background_color,
            max_words=max_words,
            colormap=colormap,
            contour_width=1,
            contour_color='steelblue'
        ).generate(text)
        
        output_path = os.path.join(self.wordcloud_folder, self.document_name, "wc.jpeg")
        wordcloud.to_file(output_path)
        print(f"Word cloud saved to {output_path}")
        
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.show()
    
    def generate_word_frequency_plot(self, top_n=20):
        """Generate and save a word frequency plot as a JPEG file."""
        if not self.filtered_tokens:
            raise ValueError("No valid text available for visualization")
        
        word_counts = Counter(self.filtered_tokens)
        top_words = word_counts.most_common(top_n)
        words, frequencies = zip(*top_words)
        
        plt.figure(figsize=(12, 6))
        plt.bar(words, frequencies, color='skyblue')
        plt.xticks(rotation=45, ha='right')
        plt.xlabel('Words')
        plt.ylabel('Frequency')
        plt.title(f'Top {top_n} Word Frequencies')
        plt.tight_layout()
        
        output_path = os.path.join(self.freqplot_folder, self.document_name, "freq_plot.jpeg")
        plt.savefig(output_path, bbox_inches='tight')
        print(f"Frequency plot saved to {output_path}")
        
        plt.show()
