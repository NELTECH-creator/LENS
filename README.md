<div align="center">

# 🚑 LENS — Live Emergency Navigation System

### _Real-time AI emergency guidance, right from your browser._

[![Next.js](https://img.shields.io/badge/Next.js-15-black?logo=next.js)](https://nextjs.org/)
[![Gemini](https://img.shields.io/badge/Gemini_2.5-Flash_Native_Audio-4285F4?logo=google)](https://ai.google.dev/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Python_3.12-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Firebase](https://img.shields.io/badge/Firebase-App_Hosting-FFCA28?logo=firebase)](https://firebase.google.com/)
[![Cloud Run](https://img.shields.io/badge/Cloud_Run-Backend-4285F4?logo=googlecloud)](https://cloud.google.com/run)
[![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-3-06B6D4?logo=tailwindcss)](https://tailwindcss.com/)
[![License](https://img.shields.io/badge/License-Apache_2.0-green.svg)](LICENSE)

<br />

> **When someone collapses in front of you and you don't know what to do — LENS does.**
>
> Point your camera. The AI sees the emergency. It tells you what to do, step by step, in a calm voice.

<br />

[Getting Started](#-getting-started) · [How It Works](#-how-it-works) · [Architecture](#-system-architecture) · [WebSocket Protocol](#-websocket-protocol) · [Contributing](#-contributing)

</div>

---

## 📖 Table of Contents

- [Overview](#-overview)
- [The Problem](#-the-problem)
- [The Solution](#-the-solution)
- [How It Works](#-how-it-works)
- [Supported Emergencies](#-supported-emergency-types)
- [System Architecture](#-system-architecture)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Environment Variables](#-environment-variables)
- [WebSocket Protocol](#-websocket-protocol)
- [Design Principles](#-design-principles)
- [MVP Success Criteria](#-mvp-success-criteria)
- [Team](#-team)
- [Roadmap](#-roadmap)
- [Timeline](#-timeline)
- [Security & Privacy](#-security--privacy)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact)

---

## 🌍 Overview

**LENS** (Live Emergency Navigation System) is a **real-time AI-powered emergency guidance agent** that runs entirely in a web browser. It turns any smartphone into a temporary AI first responder.

When someone encounters an emergency — a person bleeding, someone unconscious, a fire — they open LENS, point their phone camera at the scene, and the AI:

1. **Sees** the emergency through the live camera feed
2. **Classifies** the type and severity in real time
3. **Speaks** calm, clear first-aid instructions through the phone's speakers using Gemini's native audio
4. **Adapts** continuously as the scene changes — no manual prompting needed

No app to download. No account to create. Just open and point.

---

## 🎯 The Problem

When emergencies happen, there is a **critical response gap**:

| The Reality | The Impact |
|---|---|
| 🫠 People panic and freeze | Precious minutes wasted doing nothing |
| 🤷 Most people have no first-aid training | Wrong actions can worsen injuries |
| 🔍 Searching the internet is slow and chaotic | Information overload during crisis |
| 🚑 Emergency services take 5–15+ minutes | The victim is alone with an untrained bystander |
| 🌍 Low-resource areas have minimal coverage | Many regions have no reliable EMS at all |

> Even a **5-minute delay** in basic first response can be the difference between life and death.

---

## 💡 The Solution

LENS fills the gap between **"emergency happens"** and **"professional help arrives"** with:

| Feature | Description |
|---|---|
| 📡 **Real-time vision analysis** | AI watches the live camera feed and identifies the emergency |
| 🗣️ **Spoken instructions** | Gemini's native audio speaks calm guidance — no separate TTS needed |
| 🧠 **Multimodal reasoning** | Gemini 2.5 Flash processes video + audio + context simultaneously |
| 😌 **Calm Mode** | Built into the system prompt — short, reassuring, jargon-free instructions |
| 📱 **Zero install** | Runs in any modern mobile browser — no app download needed |
| 🔄 **Continuous streaming** | Real-time WebSocket connection — not polling, not request/response |
| 🎙️ **Proactive AI** | Gemini speaks when it sees something concerning, without being asked |

---

## 🔄 How It Works

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

## 🚨 Supported Emergency Types

| Type | Emoji | Examples |
|---|---|---|
| **Injury** | 🩸 | Bleeding, cuts, lacerations, visible wounds |
| **Medical** | ⚕️ | Unconscious person, cardiac event, respiratory distress |
| **Fire** | 🔥 | Active fire, smoke hazard, burn injuries |

> **MVP scope** — additional emergency types (choking, drowning, seizures, etc.) planned for post-launch.

---

## 🏗 System Architecture

```
┌──────────────────────────────────────────────────────┐
│                    CLIENT (Browser)                   │
│                                                      │
│  ┌──────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │  Camera   │  │  Microphone  │  │   Audio      │   │
│  │  Capture  │  │  PCM 16kHz   │  │   Playback   │   │
│  └─────┬─────┘  └──────┬───────┘  └──────▲───────┘   │
│        │               │                 │           │
│        └───────┬───────┘                 │           │
│                ▼                         │           │
│  ┌─────────────────────────┐             │           │
│  │    Emergency Session    │             │           │
│  │      UI Controller      │─────────────┘           │
│  └────────────┬────────────┘                         │
└───────────────┼──────────────────────────────────────┘
                │  WebSocket (wss://)
                ▼
┌──────────────────────────────────────────────────────┐
│         BACKEND (FastAPI — Cloud Run)                 │
│                                                      │
│  ┌──────────────────────────────────────┐            │
│  │     /ws  WebSocket Endpoint          │            │
│  │                                      │            │
│  │  ┌────────────────────────────────┐  │            │
│  │  │   GeminiLiveSession Wrapper    │──┼──→ Gemini  │
│  │  │                                │  │    Live    │
│  │  │  • Emergency system prompt     │  │    API     │
│  │  │  • Audio/video/text relay      │  │            │
│  │  │  • Transcription events        │  │            │
│  │  │  • Barge-in handling           │  │            │
│  │  └───────────┬────────────────────┘  │            │
│  │              ▼                       │            │
│  │  ┌────────────────────────────────┐  │            │
│  │  │   Fail-safe Fallback           │  │            │
│  │  │   (if Gemini disconnects)      │  │            │
│  │  └────────────────────────────────┘  │            │
│  └──────────────────────────────────────┘            │
│                                                      │
│  ┌──────────────┐                                    │
│  │ /health GET  │  ← Cloud Run health check          │
│  └──────────────┘                                    │
└──────────────────────────────────────────────────────┘
```

### Core Backend Components

| Component | Purpose |
|---|---|
| **WebSocket Proxy** (`main.py`) | Accepts browser connections, creates Gemini session, relays audio/video/text bidirectionally |
| **Gemini Live Session** (`gemini_live.py`) | Wraps the Google Gen AI SDK, manages async I/O queues and transcription events |
| **Emergency System Prompt** (`emergency_prompt.py`) | Single instruction that makes Gemini act as a calm emergency agent — replaces both old classifier and Calm Mode filter |
| **Fail-safe Fallback** (`fallback.py`) | Pre-built safety instructions served when Gemini is unreachable |

### Core Frontend Components

| Component | Purpose |
|---|---|
| **Emergency Session Controller** | Manages camera/mic access, WebSocket connection, and session lifecycle |
| **Camera Capture** | Uses `MediaDevices.getUserMedia()` to access camera; streams JPEG frames via WebSocket |
| **PCM Audio Capture** | Captures microphone audio as PCM 16-bit, 16kHz mono |
| **Audio Playback** | AudioWorklet decodes and plays PCM 24kHz audio responses from Gemini |
| **Status Overlay** | Displays transcripts, emergency type badge, and disclaimer |

---

## ⚙️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Frontend** | [Next.js 15](https://nextjs.org/) (React 18) + TypeScript | UI framework |
| **Styling** | [Tailwind CSS 3](https://tailwindcss.com/) + Sass | Utility-first styling |
| **Backend** | [FastAPI](https://fastapi.tiangolo.com/) (Python 3.12) | WebSocket proxy server |
| **AI** | [Gemini Live API](https://ai.google.dev/) (`gemini-2.5-flash-native-audio-preview-12-2025`) | Real-time multimodal AI with native audio I/O |
| **SDK** | [Google Gen AI SDK for Python](https://pypi.org/project/google-genai/) (`google-genai`) | Live API client |
| **Communication** | WebSocket (bidirectional) | Browser ↔ Backend ↔ Gemini |
| **Frontend Hosting** | [Firebase App Hosting](https://firebase.google.com/docs/app-hosting) | Serverless deployment |
| **Backend Hosting** | [Google Cloud Run](https://cloud.google.com/run) | Container deployment for FastAPI |
| **Camera/Audio** | WebRTC / MediaDevices API | Browser-native camera and mic access |

### What Is NOT in the Stack

| ~~Technology~~ | Why Not |
|---|---|
| ~~Google Cloud TTS~~ | Gemini speaks natively via the Live API — no separate TTS needed |
| ~~Genkit / .prompt files~~ | Replaced by system prompt in Live API config |
| ~~REST API endpoints~~ | Replaced by real-time WebSocket |
| ~~Firestore~~ | No persistent storage needed for MVP |
| ~~Separate Calm Mode filter~~ | Baked into the emergency system prompt |

---

## 📁 Project Structure

```
LENS/
├── context.md                             # AI assistant context file
├── README.md                              # This file
├── LICENSE                                # Apache 2.0
│
├── docs/
│   ├── LENS-Basic PRD.md                  # Product requirements document
│   ├── LENS FRD.md                        # Functional requirements document
│   ├── LENS-Architecture-Pivot.md         # Architecture pivot details
│   ├── documentation.md                   # Technical architecture doc
│   ├── contributing.md                    # Contribution guidelines
│   └── code-of-conduct.md                # Code of conduct
│
├── backend/                               # FastAPI Python server
│   ├── main.py                            # FastAPI app — /ws WebSocket + /health
│   ├── gemini_live.py                     # Gemini Live API session wrapper
│   ├── emergency_prompt.py                # System prompt (calm emergency agent)
│   ├── fallback.py                        # Fail-safe generic instructions
│   ├── requirements.txt                   # Python deps
│   ├── Dockerfile                         # Cloud Run container
│   ├── deploy.sh                          # Automated Cloud Run deployment
│   ├── .gitignore                         # Python gitignore
│   └── venv/                              # Local virtual environment (gitignored)
│
└── frontend/                              # Next.js app
    ├── package.json
    ├── next.config.mjs
    ├── tailwind.config.ts
    ├── tsconfig.json
    └── src/
        ├── app/                           # Next.js app router pages
        ├── components/                    # React UI components
        ├── data/                          # Static data
        └── lib/                           # Utilities and hooks
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.12+** (for the backend)
- **Node.js 20+** and **npm** (for the frontend)
- **Google Cloud project** with the Vertex AI API enabled
- **gcloud CLI** installed and authenticated

### Backend Setup

```bash
# 1. Navigate to the backend directory
cd backend

# 2. Create a Python virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
echo "PROJECT_ID=your-gcp-project-id" > .env

# 5. Authenticate with Google Cloud
gcloud auth application-default login

# 6. Start the backend server
python main.py
# → Runs on http://localhost:8080
# → Health check: http://localhost:8080/health
# → WebSocket: ws://localhost:8080/ws
```

### Frontend Setup

```bash
# 1. Navigate to the frontend directory
cd frontend

# 2. Install dependencies
npm install

# 3. Start the development server
npm run dev
```

---

## 🔐 Environment Variables

### Backend (`backend/.env`)

```env
# Required
PROJECT_ID=your-gcp-project-id

# Optional (defaults shown)
LOCATION=us-central1
MODEL=gemini-2.5-flash-native-audio-preview-12-2025
PORT=8080
```

> **Note:** The backend uses Application Default Credentials (ADC). Run `gcloud auth application-default login` to authenticate locally, or use a service account on Cloud Run.

---

## 📡 WebSocket Protocol

The backend communicates with the frontend over a single WebSocket connection at `/ws`.

### Client → Server

| Format | Content |
|---|---|
| **Binary** | PCM audio from microphone (16-bit, 16kHz, mono) |
| **JSON text** `{"type": "image", "data": "<base64>"}` | JPEG camera frame |
| **Plain text** | Text message to Gemini |

### Server → Client

| Format | Content |
|---|---|
| **Binary** | PCM audio response from Gemini (16-bit, 24kHz, mono) |
| **JSON text** `{"type": "user_transcript", "text": "..."}` | User's speech transcription |
| **JSON text** `{"type": "gemini_transcript", "text": "..."}` | Gemini's speech transcription |
| **JSON text** `{"type": "turn_complete"}` | Gemini finished speaking |
| **JSON text** `{"type": "interrupted"}` | User interrupted (barge-in) |
| **JSON text** `{"type": "fallback", ...}` | Fail-safe instructions |
| **JSON text** `{"type": "error", "error": "..."}` | Error event |

### Audio Specifications

| Direction | Format | Sample Rate | Channels |
|---|---|---|---|
| Browser → Backend → Gemini (mic) | PCM 16-bit signed | 16,000 Hz | Mono |
| Gemini → Backend → Browser (response) | PCM 16-bit signed | 24,000 Hz | Mono |

---

## 🧭 Design Principles

| # | Principle | Description |
|---|---|---|
| 1 | **Calm over accuracy** | Instructions must be reassuring, never alarming. Tone saves lives. |
| 2 | **Speed above all** | Every architectural decision optimizes for < 3 second response time. |
| 3 | **No data storage** | Video frames are never persisted. No recordings. Privacy is absolute. |
| 4 | **Fail-safe always** | If AI fails, serve generic safety guidance. Never show a blank screen. |
| 5 | **Zero friction** | Works on any mobile browser. No app download, no account, no setup. |
| 6 | **Accessible language** | No medical jargon. Max 12–15 words per instruction. A child should understand. |
| 7 | **Always disclaim** | Every response reminds the user to call professional emergency services. |
| 8 | **Proactive guidance** | AI speaks when it sees something — the user shouldn't need to ask. |

---

## ✅ MVP Success Criteria

| Metric | Target |
|---|---|
| **Demo stability** | Runs start-to-finish without crash or failure |
| **Response latency** | ≤ 3 seconds from frame capture to audio playback |
| **Classification accuracy** | Correctly identifies Injury / Medical / Fire scenarios |
| **Instruction delivery** | Calm, spoken instructions via Gemini's native audio |
| **Judge comprehension** | Value proposition understood in under 60 seconds |

---

## 👥 Team

| Role | Responsibility |
|---|---|
| 🧠 **Backend Engineer** | FastAPI server, Gemini Live API integration, system prompt, fallback, Cloud Run deployment |
| 🎨 **Frontend Engineer** | Emergency session UI, camera/mic capture, WebSocket client, PCM audio playback, status overlay |
| 🗺 **Maps & Routing Engineer** | Location awareness, nearby hospital lookup (future) |
| 📊 **Product & Docs Lead** | PRD, documentation, demo coordination, testing |

**Project Lead:** Nwakanma Nelson  
**Location:** Nigeria 🇳🇬  
**Hackathon:** Gemini Live Agent Challenge — **Live Agents** category

---

## 🗺 Roadmap

### MVP (Current — Due March 16, 2026)

#### Backend
- [x] FastAPI server with WebSocket endpoint (`/ws`)
- [x] Gemini Live API session wrapper (`GeminiLiveSession`)
- [x] Emergency system prompt (10-rule calm agent instruction)
- [x] Fail-safe fallback instructions
- [x] Dockerfile for Cloud Run
- [x] Automated deployment script (`deploy.sh`)
- [ ] `.env` configuration with real GCP project
- [ ] End-to-end test with live Gemini connection
- [ ] Cloud Run deployment

#### Frontend
- [ ] Emergency session page (`/session`)
- [ ] WebSocket client
- [ ] Camera/mic capture + PCM encoding
- [ ] AudioWorklet for PCM playback
- [ ] Emergency session controller component
- [ ] Status overlay (emergency badge + transcripts)
- [ ] Disclaimer banner
- [ ] Landing page with "Start Emergency Session" button

### Post-MVP

| Feature | Description |
|---|---|
| 🌐 Multi-language support | Gemini speaks in the user's language |
| 📍 Location awareness | Auto-detect nearest hospital and emergency services |
| 📴 Offline fallback | Text-based guidance when network is unavailable |
| 📱 SMS integration | Auto-send emergency alerts to contacts or services |
| 🫁 More emergency types | Choking, drowning, seizures, allergic reactions, etc. |

---

## 📅 Timeline

| Milestone | Date |
|---|---|
| 🚀 Development kickoff | February 17, 2026 |
| 🔨 Backend scaffolding complete | February 27, 2026 ✅ |
| 🔧 Backend live testing & deployment | ~March 3, 2026 |
| 🎨 Frontend integration | ~March 7, 2026 |
| 🧪 Testing phase begins | March 9, 2026 |
| 📌 **Project deadline** | **March 16, 2026** |

---

## 🔒 Security & Privacy

| Concern | Approach |
|---|---|
| **Video data** | Frames are streamed and immediately discarded. No storage, ever. |
| **Audio data** | Audio is streamed in real time and not recorded or persisted. |
| **No recordings** | LENS does not record, save, or transmit video/audio to any storage. |
| **Authentication** | No user accounts required for MVP. Zero PII collected. |
| **Credentials** | API keys and GCP credentials stay server-side — never exposed to the browser. |
| **Communication** | All connections over HTTPS/WSS. |
| **Disclaimer** | Every response includes a reminder to contact professional emergency services. |
| **Compliance direction** | Designed with HIPAA-like privacy principles in mind. |

---

## 🤝 Contributing

We welcome contributors passionate about **civic tech**, **healthcare innovation**, **real-time systems**, and **geospatial intelligence**.

### How to Contribute

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/your-feature`)
3. **Commit** your changes with clear messages
4. **Push** to your branch (`git push origin feature/your-feature`)
5. **Submit** a Pull Request

### Guidelines

- Follow existing code style
- Backend: Python (FastAPI) — follow PEP 8
- Frontend: TypeScript — follow ESLint + Prettier configs
- Keep components focused and reusable
- Test your changes before submitting

See [`docs/contributing.md`](docs/contributing.md) for detailed guidelines and [`docs/code-of-conduct.md`](docs/code-of-conduct.md) for our code of conduct.

---

## 📄 License

This project is licensed under the **Apache License 2.0** — see the [LICENSE](LICENSE) file for details.

---

## 📬 Contact

| | |
|---|---|
| **Project Lead** | Nwakanma Nelson |
| **Email** | nwakanmae8@gmail.com |
| **Location** | Nigeria 🇳🇬 |

---

<div align="center">

### ⭐ Support the Mission

If you believe in technology that saves lives:

**Star this repo** · **Share the vision** · **Join the mission**

---

_Speed saves lives. Technology should serve that speed._

_LENS is not about building features. It is about building presence._

</div>
