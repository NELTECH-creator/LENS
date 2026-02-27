"""
LENS — Gemini Live API Session Wrapper

Manages the real-time bidirectional connection between the LENS backend
and the Gemini Live API. Handles audio/video/text input streams and
receives audio output + transcription events.

Based on Google's reference demo:
https://github.com/GoogleCloudPlatform/generative-ai/tree/main/gemini/multimodal-live-api
"""

import asyncio
import inspect
import logging

from google import genai
from google.genai import types

from emergency_prompt import EMERGENCY_SYSTEM_PROMPT

logger = logging.getLogger(__name__)


class GeminiLiveSession:
    """
    Wraps the Gemini Live API session for LENS emergency guidance.

    Connects to Gemini using the Google Gen AI SDK and manages three
    async input streams (audio, video, text) plus audio output with
    transcription events.
    """

    def __init__(
        self,
        project_id: str,
        location: str,
        model: str,
        input_sample_rate: int = 16000,
        voice_name: str = "Aoede",
    ):
        """
        Initialize the Gemini Live API client.

        Args:
            project_id: Google Cloud project ID
            location: Google Cloud region (e.g., "us-central1")
            model: Gemini model name for Live API
            input_sample_rate: Audio input sample rate in Hz (default 16000)
            voice_name: Gemini voice preset (default "Aoede" — calm, neutral)
        """
        self.project_id = project_id
        self.location = location
        self.model = model
        self.input_sample_rate = input_sample_rate
        self.voice_name = voice_name
        self.client = genai.Client(
            vertexai=True,
            project=project_id,
            location=location,
        )

    async def start_session(
        self,
        audio_input_queue: asyncio.Queue,
        video_input_queue: asyncio.Queue,
        text_input_queue: asyncio.Queue,
        audio_output_callback,
        audio_interrupt_callback=None,
    ):
        """
        Start a Gemini Live API session and manage I/O streams.

        This is an async generator that yields events (transcriptions,
        turn completions, interruptions, errors) to the caller.

        Args:
            audio_input_queue: Queue of raw PCM audio bytes from the mic
            video_input_queue: Queue of JPEG image bytes from the camera
            text_input_queue: Queue of text strings from the user
            audio_output_callback: Called with PCM audio bytes from Gemini
            audio_interrupt_callback: Called when Gemini is interrupted
        """
        config = types.LiveConnectConfig(
            response_modalities=[types.Modality.AUDIO],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(
                        voice_name=self.voice_name,
                    )
                )
            ),
            system_instruction=types.Content(
                parts=[types.Part(text=EMERGENCY_SYSTEM_PROMPT)]
            ),
            input_audio_transcription=types.AudioTranscriptionConfig(),
            output_audio_transcription=types.AudioTranscriptionConfig(),
            proactivity=types.ProactivityConfig(proactive_audio=True),
        )

        async with self.client.aio.live.connect(
            model=self.model, config=config
        ) as session:

            async def send_audio():
                """Relay mic audio from frontend to Gemini."""
                try:
                    while True:
                        chunk = await audio_input_queue.get()
                        await session.send_realtime_input(
                            audio=types.Blob(
                                data=chunk,
                                mime_type=f"audio/pcm;rate={self.input_sample_rate}",
                            )
                        )
                except asyncio.CancelledError:
                    pass

            async def send_video():
                """Relay camera frames from frontend to Gemini."""
                try:
                    while True:
                        chunk = await video_input_queue.get()
                        await session.send_realtime_input(
                            video=types.Blob(
                                data=chunk,
                                mime_type="image/jpeg",
                            )
                        )
                except asyncio.CancelledError:
                    pass

            async def send_text():
                """Relay text input from frontend to Gemini."""
                try:
                    while True:
                        text = await text_input_queue.get()
                        await session.send(input=text, end_of_turn=True)
                except asyncio.CancelledError:
                    pass

            event_queue = asyncio.Queue()

            async def receive_loop():
                """Receive responses from Gemini and dispatch to queues."""
                try:
                    while True:
                        async for response in session.receive():
                            server_content = response.server_content
                            tool_call = response.tool_call

                            if server_content:
                                # Audio output from Gemini
                                if server_content.model_turn:
                                    for part in server_content.model_turn.parts:
                                        if part.inline_data:
                                            if inspect.iscoroutinefunction(
                                                audio_output_callback
                                            ):
                                                await audio_output_callback(
                                                    part.inline_data.data
                                                )
                                            else:
                                                audio_output_callback(
                                                    part.inline_data.data
                                                )

                                # User speech transcription
                                if (
                                    server_content.input_transcription
                                    and server_content.input_transcription.text
                                ):
                                    await event_queue.put(
                                        {
                                            "type": "user_transcript",
                                            "text": server_content.input_transcription.text,
                                        }
                                    )

                                # Gemini speech transcription
                                if (
                                    server_content.output_transcription
                                    and server_content.output_transcription.text
                                ):
                                    await event_queue.put(
                                        {
                                            "type": "gemini_transcript",
                                            "text": server_content.output_transcription.text,
                                        }
                                    )

                                # Turn complete
                                if server_content.turn_complete:
                                    await event_queue.put({"type": "turn_complete"})

                                # Interrupted (barge-in)
                                if server_content.interrupted:
                                    if audio_interrupt_callback:
                                        if inspect.iscoroutinefunction(
                                            audio_interrupt_callback
                                        ):
                                            await audio_interrupt_callback()
                                        else:
                                            audio_interrupt_callback()
                                    await event_queue.put({"type": "interrupted"})

                            if tool_call:
                                # LENS doesn't use tools currently, but log it
                                logger.warning(
                                    f"Unexpected tool call received: {tool_call}"
                                )

                except Exception as e:
                    await event_queue.put({"type": "error", "error": str(e)})
                finally:
                    await event_queue.put(None)

            # Launch all async tasks
            send_audio_task = asyncio.create_task(send_audio())
            send_video_task = asyncio.create_task(send_video())
            send_text_task = asyncio.create_task(send_text())
            receive_task = asyncio.create_task(receive_loop())

            try:
                while True:
                    event = await event_queue.get()
                    if event is None:
                        break
                    if isinstance(event, dict) and event.get("type") == "error":
                        yield event
                        break
                    yield event
            finally:
                send_audio_task.cancel()
                send_video_task.cancel()
                send_text_task.cancel()
                receive_task.cancel()
