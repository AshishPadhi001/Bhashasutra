import os

# Base Backend Directory
BASE_DIR = r"E:\Bhashasutra\BackEnd"

# Directory Structure
directories = [
    "src/api/endpoints",
    "src/core",
    "src/models",
    "src/schemas",
    "src/services",
    "src/utils",
    "src/database/migrations",
]

# Files to be created
files = {
    # API Endpoints
    "src/api/__init__.py": "",
    "src/api/endpoints/__init__.py": "",
    "src/api/endpoints/basic.py": "# Basic NLP API\n",
    "src/api/endpoints/advanced.py": "# Advanced NLP API\n",
    "src/api/endpoints/sentiment.py": "# Sentiment Analysis API\n",
    "src/api/endpoints/visualization.py": "# Text Visualization API\n",
    "src/api/endpoints/auth.py": "# Login & Signup API\n",
    "src/api/endpoints/users.py": "# User-related API\n",
    "src/api/endpoints/health.py": "# Health check API\n",
    # Core
    "src/core/__init__.py": "",
    "src/core/config.py": "# Configuration settings\n",
    "src/core/security.py": "# Security functions like JWT & password hashing\n",
    # Models (Separate for Each Feature)
    "src/models/__init__.py": "",
    "src/models/user.py": "# User model\n",
    "src/models/basic.py": "# Basic NLP model\n",
    "src/models/advanced.py": "# Advanced NLP model\n",
    "src/models/sentiment.py": "# Sentiment Analysis model\n",
    "src/models/visualization.py": "# Text Visualization model\n",
    # Schemas (Separate for Each Feature)
    "src/schemas/__init__.py": "",
    "src/schemas/user.py": "# User schemas\n",
    "src/schemas/basic.py": "# Basic NLP schemas\n",
    "src/schemas/advanced.py": "# Advanced NLP schemas\n",
    "src/schemas/sentiment.py": "# Sentiment Analysis schemas\n",
    "src/schemas/visualization.py": "# Text Visualization schemas\n",
    # Services (Separate for Each Feature)
    "src/services/__init__.py": "",
    "src/services/basic_service.py": "# Business logic for Basic NLP\n",
    "src/services/advanced_service.py": "# Business logic for Advanced NLP\n",
    "src/services/sentiment_service.py": "# Sentiment Analysis logic\n",
    "src/services/visualization_service.py": "# Text Visualization logic\n",
    "src/services/auth_service.py": "# Authentication logic (Login, Signup)\n",
    # Utils
    "src/utils/__init__.py": "",
    "src/utils/logger.py": "# Logging setup\n",
    "src/utils/helper.py": "# Helper functions\n",
    # Database
    "src/database/__init__.py": "",
    "src/database/database.py": "# Database connection setup\n",
    # Main FastAPI Entry
    "src/main.py": (
        "from fastapi import FastAPI\n"
        "from BackEnd.src.api.endpoints import basic, advanced, sentiment, visualization, auth, users, health\n\n"
        "app = FastAPI()\n\n"
        "# Include Routers\n"
        "app.include_router(basic.router, prefix='/basic', tags=['Basic NLP'])\n"
        "app.include_router(advanced.router, prefix='/advanced', tags=['Advanced NLP'])\n"
        "app.include_router(sentiment.router, prefix='/sentiment', tags=['Sentiment Analysis'])\n"
        "app.include_router(visualization.router, prefix='/visualization', tags=['Text Visualization'])\n"
        "app.include_router(auth.router, prefix='/auth', tags=['Authentication'])\n"
        "app.include_router(users.router, prefix='/users', tags=['Users'])\n"
        "app.include_router(health.router, prefix='/health', tags=['Health'])\n\n"
        "@app.get('/')\n"
        "def home():\n"
        "    return {'message': 'Welcome to Bhashasutra API'}\n"
    ),
    # Other Files
    "src/requirements.txt": "fastapi\nuvicorn\npydantic\nsqlalchemy\nbcrypt\npyjwt\n",
    "src/.env": "# Environment variables\n",
    "src/.gitignore": "*.pyc\n__pycache__/\n.env\n",
    "README.md": "# Bhashasutra API Backend\n",
}

# Create directories and files
for directory in directories:
    os.makedirs(os.path.join(BASE_DIR, directory), exist_ok=True)

for file_path, content in files.items():
    full_path = os.path.join(BASE_DIR, file_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

print("✅ Backend directory structure created successfully!")
