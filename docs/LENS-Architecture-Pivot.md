# LENS — Architecture Pivot: Gemini Live API

## Date: February 24, 2026

## Status: Active — Replaces previous backend architecture

---

## Why The Pivot

LENS is entered in the **Live Agents** category of the Gemini Live Agent Challenge hackathon. This category has a **mandatory technical requirement**:

> **Must use Gemini Live API or ADK (Agent Development Kit). Agents must be hosted on Google Cloud.**

The original architecture (Genkit + REST API + separate TTS) does not satisfy this requirement. The Gemini Live API is not only compliant — it's a significantly better fit for LENS's real-time emergency guidance use case.

---

## What Changed

### Architecture Comparison

| Area | Old Plan (FRD) | New Plan (Live API) |
|---|---|---|
| **AI Integration** | Genkit + Vertex AI (REST, frame-by-frame) | Gemini Live API via WebSocket (real-time streaming) |
| **Backend** | Next.js API routes (`/api/analyze`, `/api/tts`) | FastAPI (Python) WebSocket proxy server |
| **AI Model** | Gemini 2.5 Flash (standard multimodal) | `gemini-2.5-flash-native-audio-preview-12-2025` (Live API model with native audio) |
| **TTS** | Separate Google Cloud Text-to-Speech service | **Eliminated** — Gemini Live API speaks natively |
| **Communication** | HTTP POST per frame every 2–3 seconds | Persistent WebSocket, continuous bidirectional stream |
| **Calm Mode** | Separate post-processing filter module | Embedded in system prompt — Gemini responds calmly by instruction |
| **Audio Format** | MP3 base64 from Google Cloud TTS | Raw PCM 16-bit, 24kHz mono streamed from Gemini |
| **AI Orchestration** | Google Genkit flows + `.prompt` files | Google Gen AI SDK for Python (`google-genai`) |

### What Got Eliminated

These components from the original FRD are **no longer needed**:

- ~~`POST /api/analyze` REST endpoint~~ → replaced by persistent WebSocket session
- ~~`POST /api/tts` endpoint~~ → Gemini speaks directly via native audio
- ~~Google Cloud Text-to-Speech integration~~ → native audio output from Live API
- ~~Separate Calm Mode filter module~~ → system prompt instructs Gemini to respond calmly
- ~~Genkit flows (`emergencyFlow.ts`)~~ → replaced by Live API session with system instruction
- ~~Genkit `.prompt` files~~ → replaced by system instruction in Live API config
- ~~Frame capture every 2–3s logic~~ → Live API processes video at 1 FPS automatically
- ~~Structured JSON response parsing~~ → Gemini responds with voice directly; optional text transcription available

### What Stays The Same

| Area | Status |
|---|---|
| Frontend framework | Next.js 15 + React 18 + TypeScript + Tailwind CSS 3 |
| Frontend hosting | Firebase App Hosting |
| Camera/mic capture | Browser MediaDevices API |
| Emergency types (MVP) | Injury, Medical, Fire |
| Fail-safe fallback | Required — generic guidance if connection drops |
| No data storage | Privacy-first, no frames or audio persisted |
| Disclaimer banner | Always visible during session |
| Design principles | Calm over accuracy, speed, fail-safe, accessible |
| Deadline | March 16, 2026 |

---

## New System Architecture

### High-Level Flow

```
┌─────────────────────────────────────────────────────────────────┐
│  BROWSER (Next.js Frontend)                                     │
│                                                                 │
│  1. User opens LENS → taps "Start Emergency Session"            │
│  2. Camera + microphone activate (MediaDevices API)             │
│  3. Audio: captured as PCM 16-bit, 16kHz mono                   │
│  4. Video: frames captured from camera stream                   │
│  5. Media chunks sent to backend via WebSocket                  │
│                                                                 │
│  ← Receives audio response (PCM 16-bit, 24kHz mono)            │
│  ← Receives optional text transcription                         │
│  ← Plays audio through device speakers                          │
│  ← Displays emergency status + text overlay                     │
└───────────────────────┬─────────────────────────────────────────┘
                        │ WebSocket (wss://)
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│  BACKEND (FastAPI Python Server — Cloud Run)                    │
│                                                                 │
│  • WebSocket proxy between browser and Gemini Live API          │
│  • Manages session lifecycle (connect, disconnect, timeout)     │
│  • Injects emergency system prompt on session setup             │
│  • Relays audio/video chunks from browser → Gemini              │
│  • Relays audio responses from Gemini → browser                 │
│  • Handles fail-safe: serves fallback if Gemini disconnects     │
│  • API keys and credentials stay server-side                    │
│                                                                 │
└───────────────────────┬─────────────────────────────────────────┘
                        │ WebSocket (wss://)
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│  GEMINI LIVE API (Google Cloud)                                 │
│                                                                 │
│  Model: gemini-2.5-flash-native-audio-preview-12-2025           │
│                                                                 │
│  • Receives continuous audio + video stream                     │
│  • Processes video at 1 FPS                                     │
│  • Built-in Voice Activity Detection (VAD)                      │
│  • Classifies emergency from visual + audio input               │
│  • Generates calm spoken instructions (native audio output)     │
│  • Supports barge-in (user can interrupt)                       │
│  • Session memory within active session                         │
│  • Optional text transcription of responses                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Backend Core (FastAPI)

```python
# Simplified connection pattern using Google Gen AI SDK
from google import genai

client = genai.Client(project="your-project-id", location="us-central1")

config = {
    "response_modalities": ["AUDIO"],
    "system_instruction": EMERGENCY_SYSTEM_PROMPT,
    "speech_config": {
        "voice_config": {
            "prebuilt_voice_config": {
                "voice_name": "Aoede"  # calm, neutral voice
            }
        }
    }
}

async with client.aio.live.connect(
    model="gemini-2.5-flash-native-audio-preview-12-2025",
    config=config
) as session:
    # Relay audio/video from frontend → Gemini
    # Relay audio responses from Gemini → frontend
    await asyncio.gather(
        send_audio(session),
        send_video(session),
        receive_responses(session)
    )
```

---

## Updated Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Frontend** | Next.js 15 (React 18) + TypeScript | UI framework |
| **Styling** | Tailwind CSS 3 + Sass | Utility-first styling |
| **Backend** | **FastAPI (Python)** | WebSocket proxy server |
| **AI** | **Gemini Live API** (`gemini-2.5-flash-native-audio`) | Real-time multimodal AI with native audio |
| **SDK** | **Google Gen AI SDK for Python** (`google-genai`) | Live API client |
| **Communication** | **WebSocket** (bidirectional) | Browser ↔ Backend ↔ Gemini |
| **Frontend Hosting** | Firebase App Hosting | Serverless deployment |
| **Backend Hosting** | **Google Cloud Run** | Container deployment for FastAPI |
| **Database** | Firebase Firestore (optional) | Session state if needed |

---

## Updated Project Structure (Planned)

```
LENS/
├── CLAUDE.md                              # AI assistant context
├── LENS-Architecture-Pivot.md             # This document
├── README.md                              # Project overview
│
├── frontend/                              # Next.js app (existing, restructured)
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx                   # Landing / start session
│   │   │   └── session/
│   │   │       └── page.tsx               # Emergency session UI
│   │   ├── components/
│   │   │   ├── EmergencySession.tsx        # Main session controller
│   │   │   ├── StatusOverlay.tsx           # Emergency type badge + text
│   │   │   ├── DisclaimerBanner.tsx        # Persistent safety disclaimer
│   │   │   └── AudioPlayback.tsx           # PCM audio player
│   │   ├── lib/
│   │   │   ├── websocket-client.ts         # WebSocket connection to backend
│   │   │   ├── media-handler.ts            # Camera/mic capture + PCM encoding
│   │   │   └── pcm-processor.ts            # AudioWorklet for PCM processing
│   │   └── hooks/
│   │       └── useEmergencySession.ts      # Session lifecycle hook
│   ├── firebase.json
│   ├── apphosting.yaml
│   └── package.json
│
├── backend/                               # FastAPI server (NEW)
│   ├── main.py                            # FastAPI app + WebSocket endpoint
│   ├── gemini_live.py                     # Gemini Live API wrapper
│   ├── emergency_prompt.py                # System prompt for emergency agent
│   ├── fallback.py                        # Fail-safe generic instructions
│   ├── requirements.txt                   # Python dependencies
│   ├── Dockerfile                         # Cloud Run container
│   └── deploy.sh                          # Automated deployment script
│
├── infrastructure/                        # IaC for bonus points
│   └── deploy-cloud-run.sh               # Cloud Run deployment automation
│
└── docs/
    ├── LENS-Basic PRD.md
    ├── LENS_FRD.md                        # Original FRD (reference only)
    └── architecture-diagram.png           # For submission
```

---

## Backend Responsibilities (Updated)

| Component | Purpose |
|---|---|
| **`main.py`** | FastAPI server with WebSocket endpoint; accepts browser connections, creates Gemini Live sessions, relays data bidirectionally |
| **`gemini_live.py`** | Wraps `google-genai` SDK; manages session connect/disconnect, sends audio/video chunks, receives responses |
| **`emergency_prompt.py`** | Contains the system instruction that makes Gemini act as a calm emergency guidance agent |
| **`fallback.py`** | Pre-recorded or pre-generated fallback audio + text for when Gemini is unavailable |
| **`Dockerfile`** | Container config for Cloud Run deployment |
| **`deploy.sh`** | Automated deployment script (bonus points for hackathon) |

---

## Emergency System Prompt (Core Logic)

The system prompt replaces both the old Gemini classification flow AND the Calm Mode filter. It instructs Gemini to:

1. Act as a calm, steady emergency guidance agent
2. Analyze what it sees through the camera feed
3. Classify the emergency (Injury, Medical, Fire)
4. Speak step-by-step first aid instructions
5. Use short sentences (max 12–15 words each)
6. Use no medical jargon, no exclamation marks
7. Maintain a reassuring tone throughout
8. Remind the user to call emergency services
9. Adapt instructions as the scene changes
10. If unsure, provide general safety guidance rather than silence

---

## Audio Specifications

| Direction | Format | Sample Rate | Channels |
|---|---|---|---|
| Browser → Backend → Gemini (mic input) | PCM 16-bit signed | 16,000 Hz | Mono |
| Gemini → Backend → Browser (AI response) | PCM 16-bit signed | 24,000 Hz | Mono |

The frontend must handle:
- Downsampling mic audio from browser default (typically 44.1kHz/48kHz) to 16kHz
- Playing back 24kHz PCM audio through an AudioWorklet or Web Audio API

---

## Session Lifecycle

```
1. User clicks "Start Emergency Session"
2. Frontend opens WebSocket to backend
3. Backend opens Gemini Live API session with emergency system prompt
4. Frontend streams camera video + mic audio → backend → Gemini
5. Gemini analyzes scene and speaks instructions → backend → frontend
6. Frontend plays audio + shows text overlay
7. Continuous loop until:
   a. User clicks "End Session" → graceful disconnect
   b. 10-minute session limit reached → reconnect or end
   c. Connection error → serve fail-safe fallback
```

---

## Hackathon Compliance Checklist

| Requirement | How LENS Satisfies It |
|---|---|
| ✅ Leverage a Gemini model | `gemini-2.5-flash-native-audio-preview-12-2025` |
| ✅ Use Google GenAI SDK or ADK | Google Gen AI SDK for Python (`google-genai`) |
| ✅ At least one Google Cloud service | Cloud Run (backend), Vertex AI (Gemini), Firebase (frontend hosting) |
| ✅ Live Agents: Gemini Live API or ADK | Gemini Live API via WebSocket |
| ✅ Hosted on Google Cloud | Cloud Run + Firebase App Hosting |
| ✅ Public GitHub repo | Yes, with README spin-up instructions |
| ✅ Architecture diagram | Required — will be created |
| ✅ Demo video < 4 minutes | Required — real working features, no mockups |
| 🎁 Published content | Planned — blog/video with #GeminiLiveAgentChallenge |
| 🎁 Automated cloud deployment | `deploy.sh` in repo |
| 🎁 GDG profile link | Optional |

---

## Key Differences for Frontend Team

The frontend engineer should be aware of these changes:

1. **No more REST API calls** — instead, open a WebSocket to the backend and stream media continuously
2. **Audio input must be PCM 16kHz mono** — requires downsampling from browser default
3. **Audio output is PCM 24kHz mono** — requires an AudioWorklet or Web Audio API to play raw PCM
4. **No more structured JSON responses** — Gemini speaks directly; text transcription is available as a secondary output
5. **Barge-in supported** — user can interrupt Gemini mid-speech and it will listen
6. **Video is processed at 1 FPS** — no need for the 2–3 second frame capture interval; just stream the camera feed

---

## Risk & Mitigation

| Risk | Mitigation |
|---|---|
| Gemini Live API session drops | Fail-safe fallback with pre-built generic emergency instructions |
| 10-minute session limit | Auto-reconnect logic or prompt user to restart session |
| Audio format mismatch | Frontend AudioWorklet handles PCM conversion; tested early |
| Network latency in Nigeria | Gemini Live API is low-latency by design; Cloud Run in closest region |
| Hackathon deadline (March 16) | FastAPI backend is lightweight; Google reference demos provide scaffolding |

---

## References

- [Gemini Live API Overview (Vertex AI)](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/live-api)
- [Get Started with Live API using Gen AI SDK](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/live-api/get-started-sdk)
- [Get Started with Live API using WebSockets](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/live-api/get-started-websocket)
- [Google Reference Demo: FastAPI + JS Frontend](https://github.com/GoogleCloudPlatform/generative-ai/tree/main/gemini/multimodal-live-api)
- [Live API Web Console (React Starter)](https://github.com/google-gemini/live-api-web-console)
- [Gemini Live API Blog Post](https://cloud.google.com/blog/topics/developers-practitioners/how-to-use-gemini-live-api-native-audio-in-vertex-ai)
