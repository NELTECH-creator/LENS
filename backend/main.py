"""
LENS — FastAPI Backend Server

WebSocket proxy server that sits between the Next.js frontend and the
Gemini Live API. Handles session lifecycle, relays audio/video/text
bidirectionally, and serves fail-safe fallback when Gemini is unavailable.

Usage:
    python main.py

Environment variables:
    PROJECT_ID  — Google Cloud project ID (required)
    LOCATION    — Google Cloud region (default: us-central1)
    MODEL       — Gemini model name (default: gemini-2.5-flash-native-audio-preview-12-2025)
    PORT        — Server port (default: 8080)
"""

import asyncio
import base64
import json
import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from fallback import get_fallback_response
from gemini_live import GeminiLiveSession

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────
# Configuration
# ──────────────────────────────────────────────

PROJECT_ID = os.getenv("PROJECT_ID", "your-gcp-project-id")
LOCATION = os.getenv("LOCATION", "us-central1")
MODEL = os.getenv("MODEL", "gemini-2.5-flash-native-audio-preview-12-2025")

# ──────────────────────────────────────────────
# FastAPI Application
# ──────────────────────────────────────────────

app = FastAPI(
    title="LENS Backend",
    description="Live Emergency Navigation System — Gemini Live API proxy",
    version="1.0.0",
)

# CORS — allow the Next.js frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Tighten in production to frontend URL only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ──────────────────────────────────────────────
# Health Check
# ──────────────────────────────────────────────


@app.get("/health")
async def health_check():
    """Health check endpoint for Cloud Run."""
    return {"status": "ok", "service": "lens-backend"}


# ──────────────────────────────────────────────
# WebSocket Endpoint
# ──────────────────────────────────────────────


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    Main WebSocket endpoint for LENS emergency sessions.

    Protocol:
        - Client sends binary data → audio (PCM 16-bit, 16kHz mono)
        - Client sends JSON text with type "image" → video frame (JPEG)
        - Client sends plain text → text message
        - Server sends binary data → audio response (PCM 16-bit, 24kHz mono)
        - Server sends JSON text → events (transcripts, turn_complete, etc.)
    """
    await websocket.accept()
    logger.info("Emergency session WebSocket connected")

    # Input queues for the Gemini session
    audio_input_queue: asyncio.Queue = asyncio.Queue()
    video_input_queue: asyncio.Queue = asyncio.Queue()
    text_input_queue: asyncio.Queue = asyncio.Queue()

    async def audio_output_callback(data: bytes):
        """Send Gemini's audio response back to the browser."""
        await websocket.send_bytes(data)

    async def audio_interrupt_callback():
        """Handle barge-in (user interrupted Gemini mid-speech)."""
        logger.info("User interrupted Gemini (barge-in)")

    # Create the Gemini Live session
    gemini_session = GeminiLiveSession(
        project_id=PROJECT_ID,
        location=LOCATION,
        model=MODEL,
        input_sample_rate=16000,
        voice_name="Aoede",
    )

    async def receive_from_client():
        """
        Receive messages from the browser WebSocket and route
        them to the appropriate input queue.
        """
        try:
            while True:
                message = await websocket.receive()

                # Binary data → audio from microphone
                if message.get("bytes"):
                    await audio_input_queue.put(message["bytes"])

                # Text data → could be JSON (image) or plain text
                elif message.get("text"):
                    text = message["text"]
                    try:
                        payload = json.loads(text)
                        if isinstance(payload, dict) and payload.get("type") == "image":
                            # Video frame: base64 JPEG → raw bytes
                            image_data = base64.b64decode(payload["data"])
                            await video_input_queue.put(image_data)
                            continue
                    except json.JSONDecodeError:
                        pass

                    # Plain text message
                    await text_input_queue.put(text)

        except WebSocketDisconnect:
            logger.info("Client disconnected from emergency session")
        except Exception as e:
            logger.error(f"Error receiving from client: {e}")

    # Start receiving from client in background
    receive_task = asyncio.create_task(receive_from_client())

    async def run_gemini_session():
        """Run the Gemini Live session and forward events to the client."""
        async for event in gemini_session.start_session(
            audio_input_queue=audio_input_queue,
            video_input_queue=video_input_queue,
            text_input_queue=text_input_queue,
            audio_output_callback=audio_output_callback,
            audio_interrupt_callback=audio_interrupt_callback,
        ):
            if event:
                await websocket.send_json(event)

    try:
        await run_gemini_session()
    except Exception as e:
        logger.error(f"Gemini session error: {e}")
        # Send fallback instructions to the client
        try:
            fallback = get_fallback_response()
            await websocket.send_json(fallback)
            logger.info("Sent fallback instructions to client")
        except Exception:
            logger.error("Failed to send fallback — client may be disconnected")
    finally:
        receive_task.cancel()
        try:
            await websocket.close()
        except Exception:
            pass
        logger.info("Emergency session ended")


# ──────────────────────────────────────────────
# Entry Point
# ──────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8080))
    logger.info(f"Starting LENS backend on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
