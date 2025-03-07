import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import nltk
from Functions.advanced import Advanced  # Importing Advanced class for text processing

# Ensure necessary NLTK resources are downloaded
nltk.download('punkt')
nltk.download('stopwords')


class TextVisualization:
    """
    Class for text visualization functions including word clouds and frequency plots.
    """

    def __init__(self, input_data, document_name="default"):
        """
        Initialize with input data (file path or raw text) and document name.

        Parameters:
        - input_data (str): A file path or raw text.
        - document_name (str): Name for organizing output files (default: "default").
        """
        self.advanced = Advanced(input_data)  # Initialize using Advanced class
        self.text = self.advanced.text
        self.tokens = self.advanced.word_tokenizer()  # Tokenization
        self.filtered_tokens = self.advanced.remove_stopwords()  # Remove stopwords
        self.document_name = document_name

        # Define folders for output
        self.wordcloud_folder = "wordclouds"
        self.freqplot_folder = "frequency_plots"

        # Ensure output directories exist
        os.makedirs(os.path.join(self.wordcloud_folder, self.document_name), exist_ok=True)
        os.makedirs(os.path.join(self.freqplot_folder, self.document_name), exist_ok=True)

    def generate_word_cloud(self, width=800, height=400, background_color='white',
                            max_words=100, colormap='viridis'):
        """
        Generate and save a word cloud using the raw (non-lemmatized) words.

        Parameters:
        - width (int): Width of the word cloud image.
        - height (int): Height of the word cloud image.
        - background_color (str): Background color of the word cloud.
        - max_words (int): Maximum number of words to include.
        - colormap (str): Matplotlib colormap for word cloud.

        Returns:
        - WordCloud object.
        """
        if not self.tokens:
            raise ValueError("No valid text available for visualization")

        # Join tokens back into a single string for WordCloud
        text = ' '.join(self.tokens)

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

        # Save image
        output_path = os.path.join(self.wordcloud_folder, self.document_name, "wc.png")
        wordcloud.to_file(output_path)
        print(f"Word cloud saved to {output_path}")

        # Display word cloud
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.show()

        return wordcloud

    def word_frequency_plot(self, top_n=20):
        """
        Generate and save a bar plot of word frequencies using raw words.

        Parameters:
        - top_n (int): Number of top words to include.

        Returns:
        - Tuple (words, frequencies) lists of the plotted data.
        """
        if not self.tokens:
            raise ValueError("No valid text available for visualization")

        # Count word frequencies
        word_counts = Counter(self.tokens)
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

        # Save plot
        output_path = os.path.join(self.freqplot_folder, self.document_name, "freq_plot.png")
        plt.savefig(output_path, bbox_inches='tight')
        print(f"Frequency plot saved to {output_path}")

        plt.show()

        return words, frequencies

    def process(self, choice, **kwargs):
        """
        Process the user's visualization choice with optional parameters.

        Parameters:
        - choice (str): Visualization choice ('1' for WordCloud, '2' for Frequency Plot).
        - **kwargs: Additional parameters for specific visualizations.

        Returns:
        - Object: Result of the chosen visualization.
        """
        options = {
            "1": lambda: self.generate_word_cloud(**kwargs),
            "2": lambda: self.word_frequency_plot(**kwargs)
        }

        return options.get(choice, lambda: "Invalid choice")()
