from requests import Session
from BackEnd.src.database.database import init_db
from BackEnd.src.utils.logger import get_logger

logger = get_logger(__name__)

# Import your bot model
from ..models.bot import BotResponse


# In your initialization function, add some predefined FAQs
def init_bot_responses(db: Session) -> None:
    faqs = [
        {
            "question": "What is Bhashasutra?",
            "response": "Bhashasutra is an NLP-based web application that provides various text analysis tools including summarization, sentiment analysis, and text visualization.",
            "category": "general",
            "is_faq": True,
        },
        {
            "question": "Who made Bhashasutra?",
            "response": "Bhashasutra was developed as a project to showcase NLP capabilities in a user-friendly web interface.",
            "category": "general",
            "is_faq": True,
        },
        {
            "question": "What tools does Bhashasutra have?",
            "response": "Bhashasutra offers basic tools like text summarization, keyword extraction, and language detection. It also has advanced features like sentiment analysis and various text visualizations including word clouds, frequency plots, TF-IDF heatmaps, and sentiment graphs.",
            "category": "features",
            "is_faq": True,
        },
        {
            "question": "How does Bhashasutra work?",
            "response": "Bhashasutra works by processing text inputs through various NLP algorithms. The backend is built with FastAPI and uses libraries like NLTK, spaCy, and Hugging Face Transformers for text analysis. The results are then visualized or returned as structured data.",
            "category": "technical",
            "is_faq": True,
        },
    ]

    for faq in faqs:
        db_faq = (
            db.query(BotResponse)
            .filter(BotResponse.question == faq["question"])
            .first()
        )
        if not db_faq:
            db_faq = BotResponse(**faq)
            db.add(db_faq)

    db.commit()


if __name__ == "__main__":
    try:
        logger.info("Starting database initialization")
        init_db()
        logger.info("Database initialization completed successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)}")
