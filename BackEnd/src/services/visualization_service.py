# File: BackEnd/src/services/visualization_service.py

import os
import sys
import shutil
from fastapi import UploadFile
import logging

# Get logger
logger = logging.getLogger(__name__)

# Add Functions directory to sys.path to make it importable
functions_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../Functions"))
if functions_path not in sys.path:
    sys.path.append(functions_path)

# Import the TextVisualization class
from text_visualization import TextVisualization

async def process_visualization(file: UploadFile, visualization_type: str, base_url: str):
    """
    Process a file and generate a specific visualization.
    
    Args:
        file (UploadFile): The uploaded file (TXT, DOCX, PDF).
        visualization_type (str): The type of visualization to generate.
        base_url (str): The base URL to use for generating image URLs.
        
    Returns:
        dict: Dictionary with message and generated image paths and URLs.
    """
    temp_dir = "temp"
    file_path = os.path.join(temp_dir, file.filename)
    
    # Ensure temp directory exists
    os.makedirs(temp_dir, exist_ok=True)
    
    try:
        # Save file temporarily
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        
        # Initialize visualization processor
        visualizer = TextVisualization(file_path)
        
        visualization_mapping = {
            "wordcloud": visualizer.generate_word_cloud,
            "frequency": visualizer.generate_word_frequency_plot,
            "sentiment": visualizer.generate_sentiment_distribution,
            "tfidf": visualizer.generate_tfidf_heatmap,
        }
        
        if visualization_type not in visualization_mapping:
            return {"message": "Invalid visualization type", "image_paths": [], "image_urls": []}
        
        # Generate the selected visualization
        visualization_mapping[visualization_type]()
        
        # Get directory path based on visualization type
        output_dir = visualizer.output_dirs[visualization_type]
        
        # Get image paths and create URLs
        saved_images = [os.path.join(output_dir, img) for img in os.listdir(output_dir) if img.endswith(".jpg")]
        
        # Create URLs using the base_url
        url_type_mapping = {
            "wordcloud": "wordclouds",
            "frequency": "frequency_plots",
            "sentiment": "sentiment_graphs",
            "tfidf": "tfidf_heatmaps"
        }
        
        # Generate URLs for direct access to images
        image_urls = [
            f"{base_url}/visualizations/{url_type_mapping[visualization_type]}/{os.path.basename(img)}"
            for img in saved_images
        ]
        
        # Also provide alternative direct API endpoint URLs
        api_image_urls = [
            f"{base_url}/api/v1/visualization/images/{visualization_type}/{os.path.basename(img)}"
            for img in saved_images
        ]
        
        image_urls.extend(api_image_urls)
        
        return {
            "message": f"{visualization_type.capitalize()} visualization generated successfully!",
            "image_paths": saved_images,
            "image_urls": image_urls
        }
    
    except Exception as e:
        logger.error(f"Error processing visualization: {str(e)}")
        return {
            "message": f"Failed to generate {visualization_type}: {str(e)}",
            "image_paths": [],
            "image_urls": []
        }
    
    finally:
        # Cleanup: Delete the temporary file
        if os.path.exists(file_path):
            os.remove(file_path)