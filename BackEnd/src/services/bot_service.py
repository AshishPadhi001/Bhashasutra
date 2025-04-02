import logging
from typing import Optional
import torch
from sqlalchemy.orm import Session
from transformers import AutoTokenizer, AutoModelForQuestionAnswering

from ..models.bot import BotResponse
from ..schemas.bot import BotResponseCreate

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class BotService:
    def __init__(self):
        logger.info("Initializing Bot Service with DistilBERT model")

        try:
            self.tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased-distilled-squad")
            self.model = AutoModelForQuestionAnswering.from_pretrained("distilbert-base-uncased-distilled-squad")
            logger.info("Transformer model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load Transformer model: {e}")

        # FAQ Context about Bhashasutra
        self.bhashasutra_context = """
        Bhashasutra is an NLP-based web application developed for text analysis and processing.
        It provides basic tools like text summarization, keyword extraction, and language detection.
        It also offers advanced features like sentiment analysis, text visualization including word clouds,
        frequency plots, TF-IDF heatmaps, and sentiment graphs. The application is built with a FastAPI
        backend and uses various NLP libraries. Bhashasutra was created as a project to showcase
        natural language processing capabilities in a user-friendly web interface.
        """
        
        self.nlp_context = """
        Natural Language Processing (NLP) is a field of artificial intelligence that focuses on the interaction
        between computers and human language. It involves tasks like text classification, named entity recognition,
        sentiment analysis, machine translation, and question answering. NLP uses techniques from machine learning,
        deep learning, and linguistics to process and analyze large amounts of natural language data.
        Machine Learning (ML) is a subset of AI where algorithms learn patterns from data without being explicitly
        programmed. Common ML algorithms include decision trees, random forests, support vector machines, and neural
        networks. Deep Learning is a subset of ML using neural networks with many layers to learn representations of data.
        """

        logger.info("Bot Service initialized successfully.")

    def answer_question(self, question: str, db: Session) -> str:
        """Try to answer a question using FAQ database or transformer model"""
        logger.info(f"Received question: {question}")

        db_response = self._get_faq_answer(question, db)
        if db_response:
            logger.info("Found answer in FAQ database")
            return db_response

        logger.info("No FAQ answer found, using Transformer model")
        context = self.bhashasutra_context if "bhashasutra" in question.lower() else self.nlp_context
        answer = self._get_model_answer(question, context)
        
        if not answer:
            logger.warning("Model could not generate a valid response.")
            return "I don't have enough information to answer that question."

        return answer

    def _get_faq_answer(self, question: str, db: Session) -> Optional[str]:
        """Check if we have a predefined answer in the database"""
        logger.info("Checking FAQ database for answer")
        
        question_lower = question.lower()
        faq_responses = db.query(BotResponse).filter(BotResponse.is_faq == True).all()

        for resp in faq_responses:
            if any(keyword in question_lower for keyword in resp.question.lower().split()):
                logger.info(f"Match found in FAQ: {resp.question}")
                return resp.response
        
        logger.info("No match found in FAQ database")
        return None

    def _get_model_answer(self, question: str, context: str) -> str:
        """Use the transformer model to answer the question"""
        try:
            logger.info("Processing question with Transformer model")
            inputs = self.tokenizer(question, context, return_tensors="pt")

            with torch.no_grad():
                outputs = self.model(**inputs)

            answer_start = torch.argmax(outputs.start_logits)
            answer_end = torch.argmax(outputs.end_logits) + 1

            if answer_end <= answer_start:
                answer_end = answer_start + 1

            answer = self.tokenizer.convert_tokens_to_string(
                self.tokenizer.convert_ids_to_tokens(inputs.input_ids[0][answer_start:answer_end])
            )

            if not answer.strip():
                logger.warning("Transformer model returned an empty response")
                return "I couldn't find a specific answer to that question."

            logger.info(f"Generated answer: {answer}")
            return answer
        except Exception as e:
            logger.error(f"Error during model inference: {e}")
            return "I encountered an error while processing your question."

    def add_faq(self, faq: BotResponseCreate, db: Session) -> BotResponse:
        """Add a new FAQ to the database"""
        logger.info(f"Adding new FAQ: {faq.question}")

        db_faq = BotResponse(
            question=faq.question,
            response=faq.response,
            category=faq.category,
            is_faq=True
        )
        db.add(db_faq)
        db.commit()
        db.refresh(db_faq)

        logger.info(f"FAQ added successfully: {faq.question}")
        return db_faq
