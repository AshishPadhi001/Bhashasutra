import secrets
import string
from datetime import datetime
from typing import Any, Dict
from ..utils.logger import get_logger

logger = get_logger(__name__)

def generate_random_string(length: int = 20) -> str:
    """
    Generate a random string of specified length
    Useful for creating API keys, random tokens, etc.
    
    Args:
        length: Length of the string to generate
        
    Returns:
        Random string containing letters and digits
    """
    try:
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(length))
    except Exception as e:
        logger.error(f"Error generating random string: {str(e)}")
        # Fallback to a simpler method if secrets module fails
        import random
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

def format_response(data: Any, success: bool = True, message: str = None) -> Dict[str, Any]:
    """
    Format standard API response with consistent structure
    
    Args:
        data: The data to return
        success: Whether the operation was successful
        message: Optional message to include
        
    Returns:
        Formatted API response dictionary
    """
    response = {
        "success": success,
        "timestamp": datetime.utcnow().isoformat(),
        "data": data
    }
    
    if message:
        response["message"] = message
        
    return response