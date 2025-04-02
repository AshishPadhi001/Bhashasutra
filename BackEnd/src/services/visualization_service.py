# src/services/visualization_service.py

import os
import tempfile
from fastapi import UploadFile
from Functions.text_visualization import TextVisualization


class VisualizationService:
    BASE_URL = "https://humorous-doe-teaching.ngrok-free.app"

    @staticmethod
    async def generate_word_cloud(file: UploadFile):
        """Generate a word cloud visualization for the uploaded file"""
        return await VisualizationService._process_visualization(file, "wordcloud")

    @staticmethod
    async def generate_frequency_plot(file: UploadFile):
        """Generate a word frequency plot for the uploaded file"""
        return await VisualizationService._process_visualization(file, "freqplot")

    @staticmethod
    async def generate_sentiment_distribution(file: UploadFile):
        """Generate a sentiment distribution visualization for the uploaded file"""
        return await VisualizationService._process_visualization(file, "sentiment")

    @staticmethod
    async def generate_tfidf_heatmap(file: UploadFile):
        """Generate a TF-IDF heatmap visualization for the uploaded file"""
        return await VisualizationService._process_visualization(file, "tfidf")

    @staticmethod
    async def _process_visualization(file: UploadFile, viz_type: str):
        """
        Process the uploaded file and generate the requested visualization.

        Args:
            file: The uploaded file
            viz_type: Type of visualization to generate

        Returns:
            Dictionary with success status, message, and image URL
        """
        temp_file_path = None
        try:
            # Save uploaded file to temp directory
            temp_file_path = await VisualizationService._save_upload_file(file)

            # Initialize text visualization with file path
            visualizer = TextVisualization(temp_file_path)

            # Map visualization type to corresponding method and output filename pattern
            visualization_methods = {
                "wordcloud": (visualizer.generate_word_cloud, "_wc.jpg"),
                "freqplot": (visualizer.generate_word_frequency_plot, "_freqplot.jpg"),
                "sentiment": (
                    visualizer.generate_sentiment_distribution,
                    "_sentiment.jpg",
                ),
                "tfidf": (visualizer.generate_tfidf_heatmap, "_tfidf.jpg"),
            }

            # Execute the visualization method
            method, file_suffix = visualization_methods[viz_type]
            method()  # Generate the visualization

            # Get filename without extension for constructing URL
            filename = os.path.splitext(file.filename)[0]

            # Construct the URL to the generated image
            image_url = f"{VisualizationService.BASE_URL}/visualizations/{viz_type}s/{filename}/{filename}{file_suffix}"

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
        # Create temp file with same extension as original
        file_extension = os.path.splitext(file.filename)[1]
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=file_extension
        ) as temp_file:
            temp_file_path = temp_file.name

        # Write file content to temp file
        with open(temp_file_path, "wb") as f:
            content = await file.read()
            f.write(content)
            await file.seek(0)  # Reset file pointer for future reads

        return temp_file_path
