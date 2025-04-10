from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from BackEnd.src.services.bhasha_bot_service import BhashaBotService
import logging
import json

router = APIRouter()
logger = logging.getLogger("bhasha_bot")

# Dictionary to store user connections and their associated BhashaBotService instances
active_connections = {}


@router.websocket("/ws/bhashagyan")
async def bhashagyan_bot_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for BhashaGyan - AI assistant for ML, DL, and NLP questions.
    Includes conversation memory per connection.
    """
    await websocket.accept()

    # Create a unique instance for this connection
    connection_id = id(websocket)
    active_connections[connection_id] = BhashaBotService()
    bhasha_bot_service = active_connections[connection_id]

    try:
        logger.info(f"New client connected to BhashaGyan bot (id: {connection_id})")
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
            logger.info(f"Received message from user (id: {connection_id})")

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

                # Get response from Gemini with memory
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
        logger.info(f"Client disconnected from BhashaGyan bot (id: {connection_id})")
        # Clean up the memory when the connection closes
        if connection_id in active_connections:
            active_connections[connection_id].clear_memory()
            del active_connections[connection_id]

    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
        # Make sure to clean up on any error
        if connection_id in active_connections:
            active_connections[connection_id].clear_memory()
            del active_connections[connection_id]
