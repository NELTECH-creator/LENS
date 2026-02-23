<div align="center">

# 🚑 LENS — Live Emergency Navigation System

### _Real-time AI emergency guidance, right from your browser._

[![Next.js](https://img.shields.io/badge/Next.js-15-black?logo=next.js)](https://nextjs.org/)
[![Gemini](https://img.shields.io/badge/Gemini_2.5-Flash-4285F4?logo=google)](https://ai.google.dev/)
[![Genkit](https://img.shields.io/badge/Google-Genkit-FF6F00?logo=firebase)](https://firebase.google.com/docs/genkit)
[![Firebase](https://img.shields.io/badge/Firebase-App_Hosting-FFCA28?logo=firebase)](https://firebase.google.com/)
[![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-3-06B6D4?logo=tailwindcss)](https://tailwindcss.com/)
[![License](https://img.shields.io/badge/License-Apache_2.0-green.svg)](LICENSE)

<br />

> **When someone collapses in front of you and you don't know what to do — LENS does.**
>
> Point your camera. The AI sees the emergency. It tells you what to do, step by step, in a calm voice.

<br />

[Getting Started](#-getting-started) · [How It Works](#-how-it-works) · [Architecture](#-system-architecture) · [API Reference](#-api-reference) · [Contributing](#-contributing)

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
- [API Reference](#-api-reference)
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
3. **Speaks** calm, clear first-aid instructions through the phone's speakers
4. **Loops** continuously, adapting instructions as the scene changes

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
| 🗣️ **Spoken instructions** | Calm Text-to-Speech guides the user step by step |
| 🧠 **Multimodal AI reasoning** | Gemini 2.5 Flash processes image + audio + context simultaneously |
| 😌 **Calm Mode** | All instructions are rewritten to be short, reassuring, and jargon-free |
| 📱 **Zero install** | Runs in any modern mobile browser — no app download needed |
| 🔄 **Continuous loop** | Captures new frames every 2–3 seconds and adapts instructions |

---

## 🔄 How It Works

```
┌─────────────────────────────────────────────────────────────────────┐
│  1. USER opens LENS in their browser                                │
│  2. Taps "Start Emergency Session"                                  │
│  3. Camera + microphone activate                                    │
└────────────────────────┬────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│  4. Every 2–3 seconds:                                              │
│     • Capture a video frame → base64 image                          │
│     • Capture speech transcript (optional, via SpeechRecognition)   │
│  5. Send frame + context to backend API                             │
└────────────────────────┬────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│  BACKEND                                                            │
│                                                                     │
│  6. Gemini Multimodal API analyzes image + context                  │
│  7. Returns structured response:                                    │
│     {                                                               │
│       "emergencyType": "Injury | Medical | Fire",                   │
│       "confidence": "low | medium | high",                          │
│       "instructions": ["Step 1...", "Step 2...", "Step 3..."]       │
│     }                                                               │
│  8. Calm Mode Filter rewrites instructions:                         │
│     • Max 12–15 words per sentence                                  │
│     • No medical jargon · No exclamation marks                      │
│     • Reassuring, steady language                                   │
│  9. Google Cloud TTS converts instructions → audio                  │
└────────────────────────┬────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│  10. Frontend receives:                                             │
│      • Emergency classification badge                               │
│      • Text instructions (on-screen)                                │
│      • Audio instructions (played through speakers)                 │
│  11. Loop → capture next frame → repeat from step 4                 │
└─────────────────────────────────────────────────────────────────────┘
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

### High-Level Architecture

```
┌──────────────────────────────────────────────────────┐
│                    CLIENT (Browser)                   │
│                                                      │
│  ┌──────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │  Camera   │  │    Speech    │  │   Audio      │   │
│  │  Capture  │  │  Recognition │  │   Playback   │   │
│  └─────┬─────┘  └──────┬───────┘  └──────▲───────┘   │
│        │               │                 │           │
│        └───────┬───────┘                 │           │
│                ▼                         │           │
│  ┌─────────────────────────┐             │           │
│  │    Emergency Session    │             │           │
│  │      UI Controller      │─────────────┘           │
│  └────────────┬────────────┘                         │
└───────────────┼──────────────────────────────────────┘
                │  HTTPS (POST)
                ▼
┌──────────────────────────────────────────────────────┐
│              SERVER (Next.js API Routes)              │
│                                                      │
│  ┌──────────────┐                                    │
│  │ POST /api/   │                                    │
│  │   analyze    │                                    │
│  └──────┬───────┘                                    │
│         ▼                                            │
│  ┌──────────────────────────────┐                    │
│  │      Genkit Flow Engine      │                    │
│  │                              │                    │
│  │  ┌────────────────────────┐  │                    │
│  │  │  Emergency Classifier  │──┼──→ Gemini 2.5     │
│  │  │   (Multimodal Prompt)  │  │    Flash API      │
│  │  └───────────┬────────────┘  │                    │
│  │              ▼               │                    │
│  │  ┌────────────────────────┐  │                    │
│  │  │   Calm Mode Filter     │  │                    │
│  │  └───────────┬────────────┘  │                    │
│  │              ▼               │                    │
│  │  ┌────────────────────────┐  │                    │
│  │  │   Google Cloud TTS     │  │                    │
│  │  └───────────┬────────────┘  │                    │
│  └──────────────┼───────────────┘                    │
│                 ▼                                    │
│  ┌──────────────────────────────┐                    │
│  │   Response: JSON + Audio     │                    │
│  └──────────────────────────────┘                    │
│                                                      │
│  ┌──────────────────────────────┐                    │
│  │  Firebase (Firestore)        │  ← Session state   │
│  │  Firebase App Hosting        │  ← Deployment      │
│  └──────────────────────────────┘                    │
└──────────────────────────────────────────────────────┘
```

### Core Backend Components

| Component | Purpose |
|---|---|
| **Emergency Classifier** | Genkit flow that sends camera frame + context to Gemini multimodal API and returns structured emergency classification |
| **Calm Mode Filter** | Post-processor that rewrites AI-generated instructions into short, reassuring, jargon-free sentences |
| **TTS Engine** | Google Cloud Text-to-Speech wrapper that converts calm instructions into natural-sounding audio |
| **API Route** | Next.js `POST /api/analyze` endpoint that orchestrates the full pipeline |

### Core Frontend Components

| Component | Purpose |
|---|---|
| **Emergency Session Controller** | Manages camera/mic access, frame capture loop, and session lifecycle |
| **Camera Capture** | Uses `MediaDevices.getUserMedia()` to access camera; captures frames as base64 every 2–3s |
| **Speech Recognition** | Browser `SpeechRecognition` API for optional voice input from user |
| **Audio Playback** | Plays TTS audio response through device speakers |
| **Status Overlay** | Displays emergency type badge, confidence level, and text instructions |

---

## ⚙️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Framework** | [Next.js 15](https://nextjs.org/) (React 18) | Full-stack web framework with API routes |
| **Language** | TypeScript | Type-safe development |
| **Styling** | [Tailwind CSS 3](https://tailwindcss.com/) + Sass | Utility-first CSS + preprocessor |
| **AI Orchestration** | [Google Genkit](https://firebase.google.com/docs/genkit) | AI flow management, prompt templates, structured output |
| **AI Model** | [Gemini 2.5 Flash](https://ai.google.dev/) (via Vertex AI) | Multimodal analysis (image + text input) |
| **TTS** | [Google Cloud Text-to-Speech](https://cloud.google.com/text-to-speech) | Natural-sounding audio generation |
| **Database** | [Cloud Firestore](https://firebase.google.com/docs/firestore) | Real-time session state (optional) |
| **Hosting** | [Firebase App Hosting](https://firebase.google.com/docs/app-hosting) | Serverless deployment on Cloud Run |
| **Camera/Audio** | WebRTC / MediaDevices API | Browser-native camera and mic access |
| **Speech Input** | Web SpeechRecognition API | Browser-native speech-to-text |

---

## 📁 Project Structure

```
LENS/
├── CLAUDE.md                              # AI assistant context file
├── README.md                              # This file
├── LICENSE                                # Apache 2.0
│
├── docs/
│   ├── LENS-Basic PRD.md                  # Product requirements document
│   ├── documentation.md                   # Technical architecture doc
│   ├── contributing.md                    # Contribution guidelines
│   └── code-of-conduct.md                # Code of conduct
│
├── prompts/
│   └── emergencyClassify.prompt           # Gemini prompt for emergency analysis (planned)
│
├── src/
│   ├── index.ts                           # Genkit entry point
│   │
│   ├── app/
│   │   ├── layout.tsx                     # Root layout
│   │   ├── page.tsx                       # Home / landing page
│   │   ├── globals.scss                   # Global styles
│   │   ├── not-found.tsx                  # 404 page
│   │   └── api/                           # API routes (backend endpoints)
│   │       ├── analyze/
│   │       │   └── route.ts               # POST /api/analyze (planned)
│   │       └── tts/
│   │           └── route.ts               # POST /api/tts (planned)
│   │
│   ├── components/                        # React UI components
│   │   └── svg/                           # SVG icon components
│   │
│   ├── data/                              # Static data files
│   │
│   └── lib/
│       ├── genkit/
│       │   ├── genkit.config.ts           # Genkit + Vertex AI configuration
│       │   ├── emergencyFlow.ts           # Emergency classification flow (planned)
│       │   ├── calmFilter.ts              # Calm Mode post-processor (planned)
│       │   └── types.ts                   # TypeScript type definitions
│       │
│       ├── tts/
│       │   └── googleTTS.ts              # Google Cloud TTS wrapper (planned)
│       │
│       └── hooks/                         # Custom React hooks
│
├── load-firestore-data/                   # Firestore seed data scripts
│
├── firebase.json                          # Firebase project config
├── firestore.rules                        # Firestore security rules
├── firestore.indexes.json                 # Firestore indexes
├── apphosting.yaml                        # Firebase App Hosting (Cloud Run) config
│
├── next.config.mjs                        # Next.js configuration
├── tailwind.config.ts                     # Tailwind CSS configuration
├── tsconfig.json                          # TypeScript configuration
├── postcss.config.js                      # PostCSS configuration
├── package.json                           # Dependencies and scripts
└── package-lock.json                      # Dependency lock file
```

---

## 🚀 Getting Started

### Prerequisites

- **Node.js** 20, 22, or 24
- **npm** (comes with Node.js)
- **Google Cloud project** with the following APIs enabled:
  - Vertex AI API
  - Cloud Text-to-Speech API
- **Firebase project** linked to your GCP project
- **Genkit CLI** (installed as dev dependency)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/NELTECH-creator/LENS.git
cd LENS

# 2. Install dependencies
npm install

# 3. Set up environment variables (see below)
cp .env.example .env.local  # or create manually

# 4. Configure your Firebase project ID
# Edit src/lib/genkit/genkit.config.ts and replace REPLACE_WITH_YOUR_PROJECT_ID

# 5. Start the development server
npm run dev
```

### Available Scripts

| Script | Command | Description |
|---|---|---|
| **Dev** | `npm run dev` | Start Genkit + Next.js dev server with hot reload |
| **Dev (Next only)** | `npm run dev:next` | Start only Next.js (no Genkit) |
| **Dev (Genkit only)** | `npm run dev:genkit` | Start only Genkit dev server |
| **Build** | `npm run build` | Production build |
| **Lint** | `npm run lint` | Run ESLint |

---

## 🔐 Environment Variables

Create a `.env.local` file in the project root:

```env
# Google Cloud / Firebase
GOOGLE_CLOUD_PROJECT=your-gcp-project-id
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json

# Vertex AI
VERTEX_AI_LOCATION=us-central1

# Google Cloud Text-to-Speech (uses same service account)
# No additional env vars needed if GOOGLE_APPLICATION_CREDENTIALS is set

# Optional: Firebase
FIREBASE_PROJECT_ID=your-firebase-project-id
```

---

## 📡 API Reference

### `POST /api/analyze`

Analyzes a camera frame and returns emergency classification with spoken instructions.

**Request:**

```json
{
  "frame": "data:image/jpeg;base64,/9j/4AAQSkZJRg...",
  "transcript": "someone fell down and is not moving",
  "sessionId": "optional-session-id"
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `frame` | `string` | ✅ | Base64-encoded JPEG image from camera |
| `transcript` | `string` | ❌ | User's speech transcript for additional context |
| `sessionId` | `string` | ❌ | Session identifier for continuity |

**Response:**

```json
{
  "emergencyType": "Medical",
  "confidence": "high",
  "instructions": [
    "Check if the person is breathing.",
    "Gently tilt their head back to open the airway.",
    "Place them on their side in a recovery position.",
    "Stay with them and keep them warm."
  ],
  "audio": "data:audio/mp3;base64,SUQzBAAAAAAAI1RTU...",
  "disclaimer": "This is AI guidance only. Call emergency services immediately."
}
```

| Field | Type | Description |
|---|---|---|
| `emergencyType` | `"Injury" \| "Medical" \| "Fire"` | Classified emergency type |
| `confidence` | `"low" \| "medium" \| "high"` | AI confidence level |
| `instructions` | `string[]` | Calm, filtered step-by-step instructions |
| `audio` | `string` | Base64-encoded TTS audio of the instructions |
| `disclaimer` | `string` | Legal/safety disclaimer (always included) |

**Error Response:**

```json
{
  "error": "analysis_failed",
  "fallback": true,
  "instructions": [
    "Stay calm and assess the situation.",
    "Call emergency services right away.",
    "Move to a safe location if needed.",
    "Wait for help to arrive."
  ],
  "audio": "data:audio/mp3;base64,..."
}
```

> ⚠️ **Fail-safe:** If AI analysis fails for any reason, the API returns generic safety guidance instead of an error. The user must never see a blank screen during an emergency.

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

---

## ✅ MVP Success Criteria

| Metric | Target |
|---|---|
| **Demo stability** | Runs start-to-finish without crash or failure |
| **Response latency** | ≤ 3 seconds from frame capture to audio playback |
| **Classification accuracy** | Correctly identifies Injury / Medical / Fire scenarios |
| **Instruction delivery** | Calm, spoken instructions play within 3 seconds |
| **Judge comprehension** | Value proposition understood in under 60 seconds |

---

## 👥 Team

| Role | Responsibility |
|---|---|
| 🧠 **Backend Engineer** | API routes, Genkit AI flows, Calm Mode filter, TTS integration |
| 🎨 **Frontend Engineer** | Emergency session UI, camera/mic integration, audio playback, status overlay |
| 🗺 **Maps & Routing Engineer** | Location awareness, nearby hospital lookup (future) |
| 📊 **Product & Docs Lead** | PRD, documentation, demo coordination, testing |

**Project Lead:** Nwakanma Nelson  
**Location:** Nigeria 🇳🇬

---

## 🗺 Roadmap

### MVP (Current — Due March 16, 2026)

- [x] Project scaffolding and tech stack setup
- [x] Genkit + Vertex AI configuration
- [x] Firebase infrastructure
- [ ] Emergency classification Genkit flow
- [ ] Calm Mode instruction filter
- [ ] Google Cloud TTS integration
- [ ] `POST /api/analyze` endpoint
- [ ] Emergency session UI (camera + mic)
- [ ] Audio playback + text display
- [ ] Emergency type badge component
- [ ] Fail-safe fallback responses
- [ ] End-to-end demo

### Post-MVP

| Feature | Description |
|---|---|
| 🌐 Multi-language TTS | Support for multiple languages and regional dialects |
| 📍 Location awareness | Auto-detect nearest hospital and emergency services |
| 📴 Offline fallback | Text-based guidance when network is unavailable |
| 📱 SMS integration | Auto-send emergency alerts to contacts or services |
| 🤖 Predictive dispatch | AI-powered prediction of emergency type before full analysis |
| 🚑 Ambulance routing | Traffic-aware navigation for emergency vehicles |
| 🏛️ Government APIs | Integration with national emergency response systems |
| 🫁 More emergency types | Choking, drowning, seizures, allergic reactions, etc. |

---

## 📅 Timeline

| Milestone | Date |
|---|---|
| 🚀 Development kickoff | February 17, 2026 |
| 🔨 Backend core (AI + TTS) | ~March 3, 2026 |
| 🎨 Frontend integration | ~March 7, 2026 |
| 🧪 Testing phase begins | March 9, 2026 |
| 📌 **Project deadline** | **March 16, 2026** |

---

## 🔒 Security & Privacy

| Concern | Approach |
|---|---|
| **Video data** | Frames are processed in memory and immediately discarded. No storage, ever. |
| **Audio data** | Speech transcripts are not persisted beyond the active session. |
| **No recordings** | LENS does not record, save, or transmit video/audio to any storage. |
| **Authentication** | No user accounts required for MVP. Zero PII collected. |
| **Communication** | All API calls over HTTPS. |
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

- Follow existing code style (ESLint + Prettier configs included)
- Write TypeScript — no plain JS
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
