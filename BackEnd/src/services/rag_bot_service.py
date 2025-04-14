import os
import shutil
import logging
import asyncio
from pathlib import Path
import uuid
from typing import List, Dict, Any
import tempfile

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_community.embeddings import HuggingFaceEmbeddings

from BackEnd.src.core.config import settings

logger = logging.getLogger("rag_bot")


class RAGBotService:
    """Service to handle RAG (Retrieval-Augmented Generation) operations"""

    def __init__(self):
        try:
            # Initialize LLM
            self.llm = ChatGoogleGenerativeAI(
                api_key=settings.GEMINI_API_KEY, model="models/gemini-2.0-flash"
            )

            # Initialize embeddings
            self.embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )

            # Initialize memory
            self.memory = ConversationBufferMemory(
                memory_key="chat_history", return_messages=True
            )

            # Initialize text splitter
            self.text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000, chunk_overlap=200
            )

            # Vector store
            self.vector_store = None

            # File tracking
            self.processed_files = {}

            # System prompt
            self.system_prompt = """You are a helpful AI assistant specializing in information retrieval.
            Answer the user's question based on the provided context. If the information isn't in the context,
            say you don't know rather than making up an answer. Provide clear and concise responses."""

            logger.info("RAGBotService initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize RAGBotService: {str(e)}")
            raise

    async def process_files(self, files: List[Any]) -> Dict[str, Any]:
        """Process uploaded files and create embeddings"""
        try:
            file_ids = []
            all_docs = []

            for file in files:
                # Create a unique ID for the file
                file_id = str(uuid.uuid4())

                # Create temp file
                suffix = self._get_file_extension(file.filename)
                with tempfile.NamedTemporaryFile(
                    delete=False, suffix=suffix
                ) as temp_file:
                    temp_file.write(await file.read())
                    temp_path = temp_file.name

                # Process file based on type
                docs = await asyncio.to_thread(self._load_documents, temp_path, suffix)

                # Store file information
                self.processed_files[file_id] = {
                    "filename": file.filename,
                    "path": temp_path,
                }

                file_ids.append(file_id)
                all_docs.extend(docs)

            # Split documents
            splits = self.text_splitter.split_documents(all_docs)

            # Create or update vector store
            if self.vector_store is None:
                self.vector_store = await asyncio.to_thread(
                    FAISS.from_documents, splits, self.embeddings
                )
            else:
                await asyncio.to_thread(self.vector_store.add_documents, splits)

            return {
                "status": "success",
                "file_ids": file_ids,
                "message": f"Successfully processed {len(files)} files",
            }

        except Exception as e:
            logger.error(f"Error processing files: {str(e)}")
            return {
                "status": "error",
                "file_ids": [],
                "message": f"Error processing files: {str(e)}",
            }

    def _get_file_extension(self, filename: str) -> str:
        """Get file extension from filename"""
        return os.path.splitext(filename)[1].lower()

    def _load_documents(self, file_path: str, suffix: str) -> List[Any]:
        """Load documents based on file type"""
        try:
            if suffix == ".pdf":
                loader = PyPDFLoader(file_path)
            elif suffix in [".docx", ".doc"]:
                loader = Docx2txtLoader(file_path)
            elif suffix == ".txt":
                loader = TextLoader(file_path)
            else:
                raise ValueError(f"Unsupported file type: {suffix}")

            return loader.load()
        except Exception as e:
            logger.error(f"Error loading document {file_path}: {str(e)}")
            raise

    async def get_response(self, query: str) -> Dict[str, Any]:
        """Generate response using RAG"""
        try:
            if not self.vector_store:
                return {
                    "response": "No documents have been uploaded yet. Please upload documents first using the /rag/upload endpoint.",
                    "source_documents": [],
                    "status": "error",
                }

            # Use a simpler approach with direct retrieval
            retriever = self.vector_store.as_retriever(search_kwargs={"k": 3})
            docs = await asyncio.to_thread(retriever.get_relevant_documents, query)

            # Format documents for context
            context = "\n\n".join([doc.page_content for doc in docs])

            # Build prompt
            prompt = f"""
            System: {self.system_prompt}
            
            Context: {context}
            
            User: {query}
            """

            # Get response directly from LLM
            response = await asyncio.to_thread(self.llm.invoke, prompt)

            # Extract content from response
            answer = response.content if hasattr(response, "content") else str(response)

            # Update memory manually
            self.memory.chat_memory.add_user_message(query)
            self.memory.chat_memory.add_ai_message(answer)

            # Prepare source documents for response
            source_docs = []
            for doc in docs:
                source_docs.append(
                    {"content": doc.page_content, "metadata": doc.metadata}
                )

            return {
                "response": answer,
                "source_documents": source_docs,
                "status": "success",
            }

        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return {
                "response": f"I encountered an error while processing your query: {str(e)}. Please try again.",
                "source_documents": [],
                "status": "error",
            }

    def clear_memory(self) -> Dict[str, str]:
        """Clear conversation memory"""
        try:
            self.memory.clear()
            return {
                "status": "success",
                "message": "Conversation memory cleared successfully",
            }
        except Exception as e:
            logger.error(f"Error clearing memory: {str(e)}")
            return {"status": "error", "message": f"Error clearing memory: {str(e)}"}

    def delete_documents(self) -> dict:
        """
        Deletes all data from the vector database directory
        """
        vector_db_path = Path("/app/BackEnd/vectordbs")

        try:
            if vector_db_path.exists() and vector_db_path.is_dir():
                for item in vector_db_path.iterdir():
                    if item.is_file():
                        item.unlink()
                    elif item.is_dir():
                        shutil.rmtree(item)
                return {
                    "status": "success",
                    "message": "All documents and embeddings deleted.",
                }
            else:
                return {"status": "error", "message": "Vector DB directory not found."}
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to delete documents: {str(e)}",
            }
