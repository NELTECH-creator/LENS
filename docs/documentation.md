---

📘 LENS – Technical Documentation (v1)

1. Project Overview

Project Name: LENS – Live Emergency Navigation System
Type: Web-based Multimodal AI Agent
Purpose: Provide real-time emergency guidance using live vision + audio + AI reasoning.

LENS turns a browser into a temporary AI first responder.


---

2. Core Features (MVP Scope)

Supported Emergency Types

🩸 Injury (bleeding)

⚕️ Unconscious person

🔥 Fire / smoke hazard


Multimodal Inputs

Live camera feed (video stream)

Live microphone input (speech + tone)


Outputs

Text instructions (on screen)

Spoken instructions (Text-to-Speech)

Emergency classification badge



---

3. System Architecture

High-Level Flow

User Camera + Mic
        ↓
Frame Capture + Speech Transcript
        ↓
Gemini Multimodal API
        ↓
Emergency Classification
        ↓
Instruction Formatting (Calm Mode)
        ↓
Text Display + TTS Playback


---

4. Technical Stack

Frontend

Next.js (React)

WebRTC / MediaDevices API

TailwindCSS

Browser SpeechRecognition (or Google STT)


Backend

Node.js API routes

Gemini Multimodal API

Google Cloud Text-to-Speech

Optional: Firebase (session state)



---

5. Key Components

5.1 Emergency Classifier

Gemini must output:

{
  "emergencyType": "Injury | Medical | Fire",
  "confidence": "low | medium | high",
  "instructions": ["Step 1", "Step 2", "Step 3"]
}


---

5.2 Calm Mode Filter

Before TTS:

Rules:

Max 12–15 words per sentence

No medical jargon

No exclamation marks

No alarming language


Purpose: Maintain reassurance under stress.


---

6. Performance Requirements

Response time ≤ 3 seconds

Frame capture interval: 2–3 seconds

Fail-safe fallback if AI fails (basic generic safety guidance)



---

7. Security & Responsibility

No storage of video streams

No persistent recording

Clear disclaimer: “Contact emergency services immediately.”

Avoid medical diagnosis claims



---
