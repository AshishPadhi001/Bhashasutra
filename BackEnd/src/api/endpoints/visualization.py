# src/api/endpoints/visualization.py

from fastapi import APIRouter, UploadFile, File, HTTPException
from src.schemas.visualization import VisualizationResponse
from src.services.visualization_service import VisualizationService

router = APIRouter()


async def validate_file(file: UploadFile):
    """Validate the uploaded file"""
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")

    # Check file extension
    allowed_extensions = [".txt", ".docx", ".pdf"]
    file_ext = "." + file.filename.split(".")[-1].lower()

    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file format. Please upload a file with one of these extensions: {', '.join(allowed_extensions)}",
        )


@router.post("/wordcloud/file", response_model=VisualizationResponse)
async def create_word_cloud(file: UploadFile = File(...)):
    """
    Upload a file and generate a word cloud visualization
    """
    await validate_file(file)

    # Process the visualization
    result = await VisualizationService.generate_word_cloud(file=file)

    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])

    return VisualizationResponse(
        success=result["success"],
        message=result["message"],
        image_url=result["image_url"],
    )


@router.post("/frequency-plot/file", response_model=VisualizationResponse)
async def create_frequency_plot(file: UploadFile = File(...)):
    """
    Upload a file and generate a word frequency plot
    """
    await validate_file(file)

    # Process the visualization
    result = await VisualizationService.generate_frequency_plot(file=file)

    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])

    return VisualizationResponse(
        success=result["success"],
        message=result["message"],
        image_url=result["image_url"],
    )


@router.post("/sentiment-distribution/file", response_model=VisualizationResponse)
async def create_sentiment_distribution(file: UploadFile = File(...)):
    """
    Upload a file and generate a sentiment distribution visualization
    """
    await validate_file(file)

    # Process the visualization
    result = await VisualizationService.generate_sentiment_distribution(file=file)

    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])

    return VisualizationResponse(
        success=result["success"],
        message=result["message"],
        image_url=result["image_url"],
    )


@router.post("/tfidf-heatmap/file", response_model=VisualizationResponse)
async def create_tfidf_heatmap(file: UploadFile = File(...)):
    """
    Upload a file and generate a TF-IDF heatmap visualization
    """
    await validate_file(file)

    # Process the visualization
    result = await VisualizationService.generate_tfidf_heatmap(file=file)

    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])

    return VisualizationResponse(
        success=result["success"],
        message=result["message"],
        image_url=result["image_url"],
    )
