"""
LENS Fail-Safe Fallback

Pre-built fallback instructions for when the Gemini Live API is unavailable
(connection drops, API errors, session timeout). The user must NEVER see a
blank or silent screen during an emergency.
"""

FALLBACK_INSTRUCTIONS = [
    "Stay calm. Take a slow, deep breath.",
    "Call emergency services right away if you have not already.",
    "If someone is hurt, do not move them unless they are in immediate danger.",
    "If there is bleeding, apply gentle pressure with a clean cloth.",
    "If someone is unconscious, check if they are breathing.",
    "If there is a fire, move away to a safe area immediately.",
    "Stay with the person and keep them warm and comfortable.",
    "Help is on the way. You are doing the right thing.",
]

FALLBACK_DISCLAIMER = (
    "The AI connection was lost. These are general safety guidelines. "
    "Please call your local emergency number for professional help."
)


def get_fallback_response() -> dict:
    """
    Returns a fallback response object to send to the frontend
    when the Gemini session is unavailable.
    """
    return {
        "type": "fallback",
        "instructions": FALLBACK_INSTRUCTIONS,
        "disclaimer": FALLBACK_DISCLAIMER,
    }
