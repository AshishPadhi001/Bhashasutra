import sys
import os
import shutil
from fastapi import UploadFile

# 🔹 Dynamically add 'Functions/' to Python's path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../Functions")))

from text_visualization import TextVisualization

async def process_visualization(file: UploadFile, visualization_type: str):
    """
    Process a file and generate a specific visualization.

    Args:
        file (UploadFile): The uploaded file (TXT, DOCX, PDF).
        visualization_type (str): The type of visualization to generate.

    Returns:
        dict: Dictionary with message and generated image paths.
    """
    temp_dir = "temp"
    file_path = os.path.join(temp_dir, file.filename)

    # ✅ Ensure `temp/` directory exists and set proper permissions
    os.makedirs(temp_dir, exist_ok=True)

    try:
        # 🔹 Save file temporarily
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        # ✅ Initialize visualization processor
        visualizer = TextVisualization(file_path)

        visualization_mapping = {
            "wordcloud": visualizer.generate_word_cloud,
            "frequency": visualizer.generate_word_frequency_plot,
            "sentiment": visualizer.generate_sentiment_distribution,
            "tfidf": visualizer.generate_tfidf_heatmap,
        }

        if visualization_type not in visualization_mapping:
            return {"message": "Invalid visualization type", "image_paths": []}

        # 🔹 Generate the selected visualization
        visualization_mapping[visualization_type]()

        # Retrieve saved image path
        output_dir = visualizer.output_dirs[visualization_type]
        saved_images = [os.path.join(output_dir, img) for img in os.listdir(output_dir) if img.endswith(".jpg")]

        return {"message": f"{visualization_type.capitalize()} visualization generated successfully!", "image_paths": saved_images}

    except Exception as e:
        return {"message": f"Failed to generate {visualization_type}: {str(e)}", "image_paths": []}

    finally:
        # 🔹 Cleanup: Delete the temporary file
        if os.path.exists(file_path):
            os.remove(file_path)
