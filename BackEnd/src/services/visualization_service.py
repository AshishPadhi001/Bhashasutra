# src/services/visualization_service.py

import os
import tempfile
from fastapi import UploadFile
from Functions.text_visualization import TextVisualization


class VisualizationService:
    # The base URL for the ngrok server
    BASE_URL = "https://humorous-doe-teaching.ngrok-free.app"

    @staticmethod
    async def generate_word_cloud(file: UploadFile):
        """Generate a word cloud visualization for the uploaded file"""
        return await VisualizationService._process_visualization(file, 1, "wordcloud")

    @staticmethod
    async def generate_frequency_plot(file: UploadFile):
        """Generate a word frequency plot for the uploaded file"""
        return await VisualizationService._process_visualization(file, 2, "freqplot")

    @staticmethod
    async def generate_sentiment_distribution(file: UploadFile):
        """Generate a sentiment distribution visualization for the uploaded file"""
        return await VisualizationService._process_visualization(file, 3, "sentiment")

    @staticmethod
    async def generate_tfidf_heatmap(file: UploadFile):
        """Generate a TF-IDF heatmap visualization for the uploaded file"""
        return await VisualizationService._process_visualization(file, 4, "tfidf")

    @staticmethod
    async def _process_visualization(file: UploadFile, choice: int, viz_type: str):
        """
        Process the uploaded file and generate the requested visualization.

        Args:
            file: The uploaded file
            choice: Numeric choice for the TextVisualization.process method
            viz_type: Visualization type id for URL construction

        Returns:
            Dictionary with success status, message, and image URL
        """
        temp_file_path = None
        try:
            # Save uploaded file to temp directory
            temp_file_path = await VisualizationService._save_upload_file(file)

            # Initialize text visualization with file path
            visualizer = TextVisualization(temp_file_path)

            # Use the process method with the appropriate choice number
            visualizer.process(choice)

            # Get filename without extension for URL path
            filename = os.path.splitext(file.filename)[0]

            # Map visualization type to file suffix
            file_suffixes = {
                "wordcloud": "_wc.jpg",
                "freqplot": "_freqplot.jpg",
                "sentiment": "_sentiment.jpg",
                "tfidf": "_tfidf.jpg",
            }

            # Map visualization type to correct folder names
            folder_names = {
                "wordcloud": "wordclouds",
                "freqplot": "frequency_plots",
                "sentiment": "sentiment_graphs",
                "tfidf": "tfidf_heatmaps",
            }

            # Construct the URL to the generated image based on actual folder structure
            encoded_filename = filename.replace(
                " ", "%20"
            )  # URL encode spaces in the filename
            image_url = f"{VisualizationService.BASE_URL}/visualizations/{folder_names[viz_type]}/{encoded_filename}/{encoded_filename}{file_suffixes[viz_type]}"

            # Prepare friendly name for display in message
            viz_names = {
                "wordcloud": "Word Cloud",
                "freqplot": "Word Frequency Plot",
                "sentiment": "Sentiment Distribution",
                "tfidf": "TF-IDF Heatmap",
            }

            return {
                "success": True,
                "message": f"{viz_names[viz_type]} generated successfully",
                "image_url": image_url,
            }

        except Exception as e:
            return {
                "success": False,
                "message": f"Error generating visualization: {str(e)}",
            }
        finally:
            # Clean up temp file
            if temp_file_path and os.path.exists(temp_file_path):
                os.remove(temp_file_path)

    @staticmethod
    async def _save_upload_file(file: UploadFile) -> str:
        """Save an upload file to a temporary file and return the path"""
        # Create temp directory if it doesn't exist
        temp_dir = os.path.join(
            os.path.dirname(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            ),
            "temp",
        )
        os.makedirs(temp_dir, exist_ok=True)

        # Create temp file with original filename to maintain filename consistency
        temp_file_path = os.path.join(temp_dir, file.filename)

        # Write file content to temp file
        with open(temp_file_path, "wb") as f:
            content = await file.read()
            f.write(content)
            await file.seek(0)  # Reset file pointer for future reads

        return temp_file_path
