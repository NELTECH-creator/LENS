# LENS — Project Context for AI Assistants

## What Is LENS?

LENS (Live Emergency Navigation System) is a **real-time AI-powered emergency guidance agent** that runs entirely in a web browser.

The core idea: when someone encounters an emergency (someone is bleeding, unconscious, or there's a fire), they open LENS, point their phone camera at the scene, and the AI watches the video feed, identifies the emergency, and speaks calm step-by-step first-aid instructions back to the user in real time — like having a first responder in their pocket.

**Target users:** General public, students, families — especially in low-resource or delayed-response settings.

**Hackathon:** Gemini Live Agent Challenge — **Live Agents** category (mandatory: must use Gemini Live API or ADK, hosted on Google Cloud).

**This is NOT:**
- A medical diagnostic tool
- A replacement for calling emergency services
- A recording or surveillance tool

---

## Problem Being Solved

Emergency response has a critical gap:
- People panic and don't know what to do in the first minutes
- Emergency services can take 5–15+ minutes to arrive
- Most people have no first aid training
- Searching the internet during an emergency is slow and chaotic

LENS fills that gap with an AI agent that guides you through the emergency *while* you wait for help.

---

## How It Works (Full Flow)

```
┌──────────────────────────────────────────────────────────────────┐
│  BROWSER (Next.js Frontend)                                      │
│                                                                  │
│  1. User opens LENS → taps "Start Emergency Session"             │
│  2. Camera + microphone activate (MediaDevices API)              │
│  3. Audio: captured as PCM 16-bit, 16kHz mono                    │
│  4. Video: JPEG frames captured from camera stream               │
│  5. Media streamed to backend via WebSocket (wss://)             │
│                                                                  │
│  ← Receives audio response (PCM 16-bit, 24kHz mono)             │
│  ← Receives text transcription events (JSON)                    │
│  ← Plays audio through device speakers                           │
│  ← Displays emergency status + text overlay                      │
└───────────────────────┬──────────────────────────────────────────┘
                        │ WebSocket
                        ▼
┌──────────────────────────────────────────────────────────────────┐
│  BACKEND (FastAPI Python Server — Cloud Run)                     │
│                                                                  │
│  • WebSocket proxy between browser and Gemini Live API           │
│  • Manages session lifecycle (connect, disconnect, timeout)      │
│  • Injects emergency system prompt on session setup              │
│  • Relays audio/video from browser → Gemini                      │
│  • Relays audio responses from Gemini → browser                  │
│  • Handles fail-safe: sends fallback if Gemini disconnects       │
│  • API keys and credentials stay server-side                     │
└───────────────────────┬──────────────────────────────────────────┘
                        │ WebSocket
                        ▼
┌──────────────────────────────────────────────────────────────────┐
│  GEMINI LIVE API (Google Cloud)                                  │
│                                                                  │
│  Model: gemini-2.5-flash-native-audio-preview-12-2025            │
│                                                                  │
│  • Receives continuous audio + video stream                      │
│  • Processes video at 1 FPS                                      │
│  • Built-in Voice Activity Detection (VAD)                       │
│  • Classifies emergency from visual + audio input                │
│  • Generates calm spoken instructions (native audio output)      │
│  • Supports barge-in (user can interrupt)                        │
│  • Session memory within active session                          │
│  • Proactive audio — speaks when it sees something concerning    │
└──────────────────────────────────────────────────────────────────┘
```

---

## Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Frontend** | Next.js 15 (React 18) + TypeScript | UI framework |
| **Styling** | Tailwind CSS 3 + Sass | Utility-first styling |
| **Backend** | **FastAPI (Python 3.12)** | WebSocket proxy server |
| **AI** | **Gemini Live API** (`gemini-2.5-flash-native-audio-preview-12-2025`) | Real-time multimodal AI with native audio I/O |
| **SDK** | **Google Gen AI SDK for Python** (`google-genai`) | Live API client |
| **Communication** | **WebSocket** (bidirectional) | Browser ↔ Backend ↔ Gemini |
| **Frontend Hosting** | Firebase App Hosting | Serverless deployment |
| **Backend Hosting** | **Google Cloud Run** | Container deployment for FastAPI |

### What Does NOT Exist (Eliminated by Architecture Pivot)
- ~~Google Cloud Text-to-Speech~~ — Gemini speaks natively via Live API
- ~~Genkit flows / `.prompt` files~~ — replaced by system prompt in Live API config
- ~~REST API endpoints (`/api/analyze`, `/api/tts`)~~ — replaced by WebSocket
- ~~Separate Calm Mode filter~~ — baked into the system prompt
- ~~Structured JSON responses~~ — Gemini speaks directly; text transcription is secondary
- ~~Frame capture every 2–3s~~ — Live API processes video at 1 FPS automatically

---

## Audio Specifications

| Direction | Format | Sample Rate | Channels |
|---|---|---|---|
| Browser → Backend → Gemini (mic) | PCM 16-bit signed | 16,000 Hz | Mono |
| Gemini → Backend → Browser (response) | PCM 16-bit signed | 24,000 Hz | Mono |

---

## Project Structure

```
LENS/
├── context.md                             ← This file (AI assistant context)
├── README.md                              ← Project overview
│
├── docs/
│   ├── LENS-Basic PRD.md                  ← Product requirements document
│   ├── LENS-Architecture-Pivot.md         ← Architecture pivot details
│   └── documentation.md                   ← Technical architecture doc
│
├── frontend/                              ← Next.js app (frontend team)
│   ├── package.json
│   ├── next.config.mjs
│   ├── tailwind.config.ts
│   ├── tsconfig.json
│   ├── firebase.json                      ← Firebase App Hosting config
│   ├── apphosting.yaml                    ← Cloud Run config for frontend
│   └── src/
│       ├── app/
│       │   ├── page.tsx                   ← Landing page
│       │   ├── layout.tsx                 ← Root layout
│       │   └── session/                   ← Emergency session page (planned)
│       ├── components/                    ← React UI components
│       ├── data/                          ← Static data
│       └── lib/
│           ├── hooks/                     ← React hooks
│           └── ...                        ← Utilities
│
└── backend/                               ← FastAPI Python server (backend team)
    ├── main.py                            ← FastAPI app — /ws WebSocket + /health
    ├── gemini_live.py                     ← Gemini Live API session wrapper
    ├── emergency_prompt.py                ← System prompt (calm emergency agent)
    ├── fallback.py                        ← Fail-safe generic instructions
    ├── requirements.txt                   ← Python deps
    ├── Dockerfile                         ← Cloud Run container
    ├── deploy.sh                          ← Automated Cloud Run deployment
    ├── .gitignore                         ← Python gitignore
    └── venv/                              ← Local Python virtual environment (gitignored)
```

---

## Backend Files Explained

| File | What It Does |
|---|---|
| **`main.py`** | FastAPI server. `/ws` WebSocket endpoint accepts browser connections, creates a Gemini Live session, relays audio/video/text bidirectionally. `/health` for Cloud Run. On error → sends fallback instructions. |
| **`gemini_live.py`** | `GeminiLiveSession` class. Wraps `google-genai` SDK. Connects to Gemini Live API with system prompt, voice config (Aoede), proactive audio, and transcription. Manages async I/O queues for audio, video, and text. Yields events (transcripts, turn_complete, interrupted, errors). |
| **`emergency_prompt.py`** | `EMERGENCY_SYSTEM_PROMPT` constant. Instructs Gemini to act as a calm emergency agent. Contains all behavioral rules: classify emergencies, speak step-by-step, max 12-15 words/sentence, no jargon, always remind to call services, never go silent. |
| **`fallback.py`** | `get_fallback_response()` returns pre-built generic safety instructions when Gemini is unreachable. 8 instructions + disclaimer. |
| **`Dockerfile`** | Python 3.12 slim. Installs deps, copies source, runs `python main.py` on port 8080. |
| **`deploy.sh`** | Builds container via Cloud Build, deploys to Cloud Run, prints service URL. |

---

## WebSocket Protocol (Browser ↔ Backend)

| From | Format | Meaning |
|---|---|---|
| Client → Server | **Binary** | PCM audio from microphone |
| Client → Server | **JSON text** `{"type": "image", "data": "<base64>"}` | JPEG camera frame |
| Client → Server | **Plain text** | Text message to Gemini |
| Server → Client | **Binary** | PCM audio response from Gemini |
| Server → Client | **JSON text** `{"type": "user_transcript", "text": "..."}` | User's speech transcription |
| Server → Client | **JSON text** `{"type": "gemini_transcript", "text": "..."}` | Gemini's speech transcription |
| Server → Client | **JSON text** `{"type": "turn_complete"}` | Gemini finished speaking |
| Server → Client | **JSON text** `{"type": "interrupted"}` | User interrupted (barge-in) |
| Server → Client | **JSON text** `{"type": "fallback", ...}` | Fail-safe instructions |
| Server → Client | **JSON text** `{"type": "error", "error": "..."}` | Error event |

---

## Session Lifecycle

1. User clicks "Start Emergency Session"
2. Frontend opens WebSocket to `wss://backend-url/ws`
3. Backend creates Gemini Live API session with emergency system prompt
4. Frontend streams camera video + mic audio → backend → Gemini
5. Gemini analyzes scene, speaks calm instructions → backend → frontend
6. Frontend plays audio + shows text overlay
7. Continuous loop until:
   - User clicks "End Session" → graceful disconnect
   - 10-minute session limit → reconnect or end
   - Connection error → serve fail-safe fallback

---

## Team & Responsibilities

| Role | Area |
|---|---|
| **Backend Engineer** | FastAPI server, Gemini Live API integration, system prompt, fallback, deployment |
| **Frontend Engineer** | Emergency session UI, camera/mic capture, PCM audio handling, WebSocket client, status overlay |
| **Maps & Routing** (future) | Location awareness, nearby hospital lookup |
| **Product / Docs Lead** | PRD, documentation, demo coordination |

---

## Supported Emergency Types (MVP)

1. 🩸 **Injury** — Bleeding, cuts, lacerations, visible wounds
2. ⚕️ **Medical** — Unconscious person, cardiac/respiratory event, seizure
3. 🔥 **Fire** — Active fire, smoke, burn injuries

---

## Key Design Principles

1. **Calm over accuracy** — Instructions must be reassuring, not alarming
2. **Speed** — Optimize for < 3s response time
3. **No storage** — Video frames / audio never persisted; privacy first
4. **Fail-safe** — If AI fails, serve generic safety guidance (never go silent)
5. **Accessible** — Works on mobile browser, no app install required
6. **Proactive** — Gemini speaks when it sees something, without being asked

---

## MVP Success Criteria

- Demo runs without failure
- AI response latency ≤ 3 seconds
- Emergency correctly classified (Injury / Medical / Fire)
- Calm, spoken instructions delivered via Gemini's native audio
- Judges understand the value in under 60 seconds

---

## Deadline

- **Project deadline: March 16, 2026**
- **Dev start: February 17, 2026**
- **Testing phase: ~March 9–15**

---

## Running the Backend Locally

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create .env with your GCP project
echo "PROJECT_ID=your-gcp-project-id" > .env

# Authenticate with Google Cloud
gcloud auth application-default login

# Start the server
python main.py
# → Runs on http://localhost:8080
# → Health check: http://localhost:8080/health
# → WebSocket: ws://localhost:8080/ws
```

---

## What Still Needs to Be Built

### Backend (your domain)
- [x] FastAPI server with WebSocket endpoint
- [x] Gemini Live API session wrapper
- [x] Emergency system prompt
- [x] Fail-safe fallback
- [x] Dockerfile + deploy script
- [ ] `.env` configuration with real GCP project ID
- [ ] End-to-end test with live Gemini connection
- [ ] Cloud Run deployment

### Frontend (frontend team's domain)
- [ ] Emergency session page (`/session`)
- [ ] WebSocket client (`websocket-client.ts`)
- [ ] Camera/mic capture + PCM encoding (`media-handler.ts`)
- [ ] AudioWorklet for PCM playback (`pcm-processor.ts`)
- [ ] Emergency session controller component
- [ ] Status overlay (emergency badge + text)
- [ ] Disclaimer banner
- [ ] Landing page with "Start Emergency Session" button
