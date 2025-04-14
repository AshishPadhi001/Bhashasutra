import logging
import asyncio
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain.chains import LLMChain
from BackEnd.src.core.config import settings
from BackEnd.src.utils.prompt import prompt

logger = logging.getLogger("bhasha_bot")


class BhashaBotService:
    """
    Service to handle interactions with Google's Gemini 2.0 API using LangChain.
    Includes conversation memory for persistent interactions.
    """

    def __init__(self):
        # Initialize Gemini API with LangChain
        try:
            self.model = ChatGoogleGenerativeAI(
                api_key=settings.GEMINI_API_KEY, model="models/gemini-2.0-flash"
            )
            self.memory = ConversationBufferMemory(
                memory_key="messages", return_messages=True
            )

            # Create a system prompt to focus responses on ML, DL, and NLP with personality
            self.system_message = f"""{prompt}"""

            self.prompt = ChatPromptTemplate(
                input_variables=["content", "messages"],
                messages=[
                    SystemMessagePromptTemplate.from_template(self.system_message),
                    MessagesPlaceholder(variable_name="messages"),
                    HumanMessagePromptTemplate.from_template("{content}"),
                ],
            )

            self.chain = LLMChain(
                llm=self.model, prompt=self.prompt, memory=self.memory
            )
            logger.info(
                "BhashaBotService initialized with Gemini 2.0 and LangChain memory"
            )
        except Exception as e:
            logger.error(f"Failed to initialize Gemini with LangChain: {str(e)}")
            raise

    async def get_response(self, user_query: str) -> str:
        """
        Get a response from Gemini for the user query, with conversation history
        """
        try:
            # Run in a thread pool to avoid blocking the event loop
            response = await asyncio.to_thread(self._generate_response, user_query)
            return response
        except Exception as e:
            logger.error(f"Error getting response from Gemini: {str(e)}")
            return "I'm having trouble connecting to my knowledge base right now. Please try again in a moment."

    def _generate_response(self, user_query: str) -> str:
        """
        Internal method to call Gemini API via LangChain
        """
        try:
            result = self.chain({"content": user_query})
            return result["text"]
        except Exception as e:
            logger.error(f"Gemini API error: {str(e)}")
            raise

    def clear_memory(self):
        """
        Clear the conversation history
        """
        self.memory.clear()
