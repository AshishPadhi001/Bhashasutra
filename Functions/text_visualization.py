import os
import matplotlib

matplotlib.use("Agg")  # Use a non-interactive backend
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns
from wordcloud import WordCloud
from collections import Counter
import numpy as np
import pandas as pd
import re
from Functions.basic import Basic
from Functions.advanced import Advanced
from Functions.Sentiment_analysis import Sentiment


class TextVisualization:
    """
    Class for text visualization functions including:
    - Word Clouds
    - Word Frequency Plots
    - Sentiment Distribution
    - TF-IDF Heatmaps

    **This class only supports file-based input (TXT, DOCX, PDF).**
    """

    def __init__(self, file_path):
        """
        Initialize with a file path and extract text from it.

        Args:
            file_path (str): Path to the input file (TXT, DOCX, PDF).

        Raises:
            ValueError: If the input is not a valid file.
        """
        if not isinstance(file_path, str) or not os.path.exists(file_path):
            raise ValueError(
                "Error: Text visualization only supports file-based input. Provide a valid file path."
            )

        # Initialize processing classes
        self.basic = Basic(file_path)
        self.advanced = Advanced(file_path)
        self.sentiment = Sentiment(
            self.basic.text
        )  # Sentiment analysis on extracted text

        # Extract filename without extension for naming output files
        self.filename = os.path.splitext(os.path.basename(file_path))[0]

        # Define output directories for different visualizations
        self.output_dirs = {
            "wordcloud": f"BackEnd/visualizations/wordclouds/{self.filename}",
            "freqplot": f"BackEnd/visualizations/frequency_plots/{self.filename}",
            "sentiment": f"BackEnd/visualizations/sentiment_graphs/{self.filename}",
            "tfidf": f"BackEnd/visualizations/tfidf_heatmaps/{self.filename}",
        }

        # Create necessary directories
        self._create_output_dirs()

    def _create_output_dirs(self):
        """Create required output directories for storing visualization files."""
        for directory in self.output_dirs.values():
            os.makedirs(directory, exist_ok=True)

    def _get_output_path(self, viz_type, filename):
        """Generate the output file path for a visualization."""
        return os.path.join(self.output_dirs[viz_type], filename)

    def generate_word_cloud(self):
        """Generate and save a word cloud visualization."""
        text = self.advanced.text
        if not text:
            raise ValueError(
                "Error: No text found in the file for word cloud generation."
            )

        wordcloud = WordCloud(width=800, height=400, background_color="white").generate(
            text
        )

        plt.figure(figsize=(10, 6))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.title(f"Word Cloud - {self.filename}")

        output_path = self._get_output_path("wordcloud", f"{self.filename}_wc.jpg")
        plt.savefig(output_path, bbox_inches="tight", dpi=300)
        plt.close()
        print(f"✅ Word cloud saved: {output_path}")

    def generate_word_frequency_plot(self):
        """Generate and save a bar chart of the most common words."""
        filtered_tokens = self.advanced.remove_stopwords()
        if not filtered_tokens:
            raise ValueError(
                "Error: No valid words found in the file for frequency plot."
            )

        word_freq = Counter(filtered_tokens).most_common(20)
        words, frequencies = zip(*word_freq)

        plt.figure(figsize=(12, 8))
        bars = plt.bar(words, frequencies, color="skyblue")

        for bar in bars:
            plt.text(
                bar.get_x() + bar.get_width() / 2.0,
                bar.get_height(),
                str(int(bar.get_height())),
                ha="center",
                fontsize=8,
            )

        plt.xlabel("Words")
        plt.ylabel("Frequency")
        plt.title(f"Top 20 Word Frequencies - {self.filename}")
        plt.xticks(rotation=45, ha="right")

        output_path = self._get_output_path("freqplot", f"{self.filename}_freqplot.jpg")
        plt.savefig(output_path, bbox_inches="tight", dpi=300)
        plt.close()
        print(f"✅ Word frequency plot saved: {output_path}")

    def generate_sentiment_distribution(self):
        """Generate and save a pie chart showing sentiment distribution."""
        sentiment_results = self.sentiment.analyze()

        labels = ["Positive", "Negative", "Neutral"]
        sizes = [
            (
                sentiment_results["polarity"] * 100
                if sentiment_results["polarity"] > 0
                else 0
            ),
            (
                abs(sentiment_results["polarity"]) * 100
                if sentiment_results["polarity"] < 0
                else 0
            ),
            (1 - abs(sentiment_results["polarity"])) * 100,
        ]
        colors = ["#66b3ff", "#ff9999", "#99ff99"]

        plt.figure(figsize=(10, 6))
        plt.pie(sizes, labels=labels, autopct="%1.1f%%", colors=colors, startangle=140)
        plt.title(f"Sentiment Distribution - {self.filename}")

        output_path = self._get_output_path(
            "sentiment", f"{self.filename}_sentiment.jpg"
        )
        plt.savefig(output_path, bbox_inches="tight", dpi=300)
        plt.close()
        print(f"✅ Sentiment distribution saved: {output_path}")

    def generate_tfidf_heatmap(self):
        """Generate and save a heatmap of TF-IDF scores for top terms."""
        tfidf_results = self.advanced.tfidf_vectorization()

        if isinstance(tfidf_results, str):
            raise ValueError(f"Error: {tfidf_results}")

        df = pd.DataFrame(
            {
                "Word": tfidf_results["Top TF-IDF Words"],
                "TF-IDF Score": tfidf_results["TF-IDF Scores"],
            }
        )
        df = df.set_index("Word")

        plt.figure(figsize=(12, 8))
        cmap = LinearSegmentedColormap.from_list(
            "blue_gradient", ["#EBF5FB", "#2471A3"]
        )
        sns.heatmap(df.T, cmap=cmap, annot=True, fmt=".2f", linewidths=0.5)
        plt.title(f"Top TF-IDF Words - {self.filename}")

        output_path = self._get_output_path("tfidf", f"{self.filename}_tfidf.jpg")
        plt.savefig(output_path, bbox_inches="tight", dpi=300)
        plt.close()
        print(f"✅ TF-IDF heatmap saved: {output_path}")

    def process(self, choice):
        """Process user selection for visualization."""
        actions = {
            1: self.generate_word_cloud,
            2: self.generate_word_frequency_plot,
            3: self.generate_sentiment_distribution,
            4: self.generate_tfidf_heatmap,
        }
        if choice in actions:
            actions[choice]()
        else:
            print("❌ Invalid selection. Please choose a valid option.")
