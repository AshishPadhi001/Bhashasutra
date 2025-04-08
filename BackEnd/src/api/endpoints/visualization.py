from fastapi import APIRouter, UploadFile, File, HTTPException
from BackEnd.src.schemas.visualization import VisualizationResponse
from BackEnd.src.services.visualization_service import VisualizationService
from BackEnd.src.utils.logger import get_logger

# Set up router
router = APIRouter(prefix="/visualization", tags=["visualization"])

# Set up logger
logger = get_logger(__name__)


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
    try:
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
    except HTTPException as http_exc:
        if http_exc.status_code == 429:
            logger.warning("Rate limit exceeded")
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded. Please try again after some time.",
            )
        raise
    except Exception as e:
        logger.error(f"Error in create_word_cloud endpoint: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Word cloud generation failed: {str(e)}"
        )


@router.post("/frequency-plot/file", response_model=VisualizationResponse)
async def create_frequency_plot(file: UploadFile = File(...)):
    """
    Upload a file and generate a word frequency plot
    """
    try:
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
    except HTTPException as http_exc:
        if http_exc.status_code == 429:
            logger.warning("Rate limit exceeded")
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded. Please try again after some time.",
            )
        raise
    except Exception as e:
        logger.error(f"Error in create_frequency_plot endpoint: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Frequency plot generation failed: {str(e)}"
        )


@router.post("/sentiment-graphs/file", response_model=VisualizationResponse)
async def create_sentiment_distribution(file: UploadFile = File(...)):
    """
    Upload a file and generate a sentiment graphs visualization
    """
    try:
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
    except HTTPException as http_exc:
        if http_exc.status_code == 429:
            logger.warning("Rate limit exceeded")
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded. Please try again after some time.",
            )
        raise
    except Exception as e:
        logger.error(f"Error in create_sentiment_distribution endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Sentiment distribution generation failed: {str(e)}",
        )


@router.post("/tfidf-heatmap/file", response_model=VisualizationResponse)
async def create_tfidf_heatmap(file: UploadFile = File(...)):
    """
    Upload a file and generate a TF-IDF heatmap visualization
    """
    try:
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
    except HTTPException as http_exc:
        if http_exc.status_code == 429:
            logger.warning("Rate limit exceeded")
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded. Please try again after some time.",
            )
        raise
    except Exception as e:
        logger.error(f"Error in create_tfidf_heatmap endpoint: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"TF-IDF heatmap generation failed: {str(e)}"
        )
