from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from src.services.bhasha_bot_service import BhashaBotService
import logging
import json

router = APIRouter()
logger = logging.getLogger("bhasha_bot")


@router.websocket("/ws/bhashagyan")
async def bhashagyan_bot_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for BhashaGyan - AI assistant for ML, DL, and NLP questions.
    No authentication required, no conversation history stored.
    """
    await websocket.accept()
    bhasha_bot_service = BhashaBotService()

    try:
        logger.info("New client connected to BhashaGyan bot")
        await websocket.send_text(
            json.dumps(
                {
                    "type": "greeting",
                    "message": "I'm BhashaGyan, your AI assistant for Natural Language Processing and Machine Learning questions. How can I help you today?",
                }
            )
        )

        while True:
            data = await websocket.receive_text()
            logger.info(f"Received message from user")

            try:
                user_message = json.loads(data)
                question = user_message.get("message", "")

                if not question.strip():
                    await websocket.send_text(
                        json.dumps(
                            {
                                "type": "error",
                                "message": "Please provide a question or message.",
                            }
                        )
                    )
                    continue

                # Get response from Gemini without storing any data
                response = await bhasha_bot_service.get_response(question)

                await websocket.send_text(
                    json.dumps({"type": "response", "message": response})
                )

            except json.JSONDecodeError:
                logger.error("Invalid JSON received")
                await websocket.send_text(
                    json.dumps(
                        {
                            "type": "error",
                            "message": "Invalid message format. Please send a JSON object with a 'message' field.",
                        }
                    )
                )
            except Exception as e:
                logger.error(f"Error processing message: {str(e)}")
                await websocket.send_text(
                    json.dumps(
                        {
                            "type": "error",
                            "message": "An error occurred while processing your request.",
                        }
                    )
                )

    except WebSocketDisconnect:
        logger.info("Client disconnected from BhashaGyan bot")
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
