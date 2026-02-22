
📘 Functional Requirements Document (FRD)

Project Name

LENS – Live Emergency Navigation System

Version

v1.0 (Hackathon MVP)

Document Owner

LENS Core Team


---

1️⃣ Introduction

1.1 Purpose

This document defines the functional requirements for LENS, a multimodal AI-powered web application that provides real-time emergency guidance using vision, audio, and speech output via Gemini and Google Cloud.

1.2 Scope

LENS will:

Capture live camera and microphone input.

Analyze emergency scenarios using Gemini multimodal APIs.

Classify the emergency type.

Provide calm, structured, step-by-step voice and text guidance.

Encourage contacting emergency services.


LENS will NOT:

Provide medical diagnosis.

Replace emergency services.

Store video or personal data.



---

2️⃣ System Overview

LENS is a web-based AI agent that:

1. Sees (camera input)


2. Hears (voice input)


3. Understands (Gemini reasoning)


4. Speaks (TTS guidance)



Core equation:

Emergency\ Guidance = f(Vision + Audio + Context)


---

3️⃣ Functional Requirements


---

FR-1: Emergency Session Initiation

Description

User must be able to start an emergency session from the web interface.

Requirements

User clicks “Start Emergency Session.”

Browser requests:

Camera permission

Microphone permission


Session state is activated.


Acceptance Criteria

Permissions requested successfully.

UI indicates session is active.

Live preview visible.



---

FR-2: Live Video Capture

Description

System must capture frames from live camera feed.

Requirements

Capture frame every 2–3 seconds.

Convert frame to format supported by Gemini.

Send frame securely to backend API.


Acceptance Criteria

Frame successfully processed.

No persistent storage.

Processing latency < 3 seconds.



---

FR-3: Audio Capture & Transcription

Description

System must capture user speech and convert to text.

Requirements

Activate microphone on session start.

Transcribe speech using:

Browser SpeechRecognition API OR

Google Cloud Speech-to-Text.


Combine transcript with visual frame for AI analysis.


Acceptance Criteria

Spoken input appears as text.

Transcription accuracy reasonable (>80% expected).



---

FR-4: Emergency Classification

Description

System must classify emergency type.

Supported Categories (MVP)

Injury (bleeding)

Fire/Smoke

Unconscious person


Requirements

Gemini must return structured JSON:

{
  "emergencyType": "Injury | Fire | Medical",
  "confidence": "low | medium | high",
  "instructions": ["Step 1", "Step 2", "Step 3"]
}

Acceptance Criteria

Correct classification for demo scenarios.

Confidence value displayed in UI.

Invalid output handled gracefully.



---

FR-5: Calm Mode Instruction Filter

Description

Instructions must be simplified before delivery.

Requirements

Maximum 15 words per instruction.

No medical jargon.

No alarming tone.

No exclamation marks.

Clear step numbering.


Acceptance Criteria

Output readable at Grade 6–8 level.

Instructions displayed cleanly.

Voice tone remains neutral and calm.



---

FR-6: Voice Output (Text-to-Speech)

Description

System must speak instructions aloud.

Requirements

Convert AI output to speech.

Use Google Cloud Text-to-Speech.

Voice should be calm and neutral.

Playback must begin automatically.


Acceptance Criteria

Audio plays within 1 second of text display.

No overlapping audio.

Clear pronunciation.



---

FR-7: Emergency Disclaimer

Description

System must inform user to contact emergency services.

Requirements

Display persistent banner: “Call emergency services immediately.”

Not replace professional care.


Acceptance Criteria

Disclaimer visible throughout session.

Cannot be removed by user.



---

FR-8: Fail-Safe Mode

Description

System must handle AI or API failure.

Requirements

If:

API timeout

Invalid JSON

Model error


Then:

Display generic emergency instructions.

Notify user calmly.


Acceptance Criteria

App does not crash.

Fallback content shown within 3 seconds.



---

FR-9: Session Termination

Description

User must be able to end emergency session.

Requirements

“End Session” button.

Stop camera stream.

Stop microphone.

Stop TTS.

Clear temporary state.


Acceptance Criteria

Camera light turns off.

Mic deactivates.

Session resets.



---

4️⃣ Non-Functional Requirements


---

Performance

AI response ≤ 3 seconds.

Frame capture ≤ 2–3 seconds interval.

TTS playback ≤ 1 second delay.



---

Security

No video storage.

No audio storage.

HTTPS only.

API keys secured in backend.



---

Usability

Large buttons.

High contrast UI.

Simple layout.

Accessible font size.



---

Reliability

Graceful fallback if AI fails.

No unhandled exceptions.

Clear error messaging.



---

5️⃣ Constraints

Internet required.

Browser must support MediaDevices API.

Gemini API quota limits.

Google Cloud usage costs.



---

6️⃣ Future Functional Enhancements (Post-MVP)

Multi-language support.

Location-based emergency routing.

Offline fallback mode.

Emergency contact auto-dial.

Hospital availability lookup.

Analytics dashboard.



---

7️⃣ Success Criteria

Live demo works.

Multimodal input visible.

Voice output functional.

Judges understand use case in < 60 seconds.

Clear differentiation from chatbot projects.



---
