# Health check API
from fastapi import APIRouter
from sqlalchemy import text
from src.database.database import engine

router = APIRouter()

@router.get("/", tags=["Health"])
def health_check():
    """
    Health check endpoint to verify if the API and database are running.
    """
    # Check API status
    api_status = "OK"
    
    # Check database status
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))  # Simple query to test DB
            database_status = "OK"
    except Exception as e:
        database_status = f"Error: {str(e)}"

    return {
        "api_status": api_status,
        "database_status": database_status
    }
