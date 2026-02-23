# LENS — Project Context for AI Assistants

## What Is LENS?

LENS (Live Emergency Navigation System) is a **real-time AI-powered emergency guidance agent** that runs entirely in a web browser.

The core idea: when someone encounters an emergency (someone is bleeding, unconscious, or there's a fire), they open LENS, point their phone camera at the scene, and the AI watches the video feed, identifies the emergency, and speaks calm step-by-step first-aid instructions back to the user in real time — like having a first responder in their pocket.

**Target users:** General public, students, families — especially in low-resource or delayed-response settings.

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
User opens browser app
        ↓
Clicks "Start Emergency Session"
        ↓
Camera + microphone activate (browser MediaDevices API / WebRTC)
        ↓
Every 2–3 seconds: capture a video frame (base64 image)
+ optional live speech transcript (browser SpeechRecognition API or Google STT)
        ↓
Send frame + context to backend API route
        ↓
Gemini Multimodal API analyzes image + audio context
        ↓
Returns structured emergency response:
{
  "emergencyType": "Injury | Medical | Fire",
  "confidence": "low | medium | high",
  "instructions": ["Step 1...", "Step 2...", "Step 3..."]
}
        ↓
Calm Mode Filter rewrites instructions:
  - Max 12–15 words per sentence
  - No medical jargon
  - No exclamation marks
  - Reassuring, steady language
        ↓
Google Cloud Text-to-Speech converts instructions → audio
        ↓
Frontend plays audio + displays text + shows emergency badge
        ↓
Loop: next frame captured → repeat
```

---

## Tech Stack (Actual / In Use)

| Layer | Technology |
|---|---|
| Frontend | Next.js 15 (React 18) + TypeScript |
| Styling | Tailwind CSS 3 + Sass |
| AI Orchestration | Google Genkit (`genkit`, `@genkit-ai/vertexai`, `@genkit-ai/firebase`) |
| AI Model | Gemini 2.5 Flash (via Vertex AI) — multimodal: image + text |
| TTS | Google Cloud Text-to-Speech API (planned, not yet integrated) |
| Database / Infra | Firebase (Firestore, Firebase App Hosting) |
| Prompts | Genkit `.prompt` files in `/prompts` |

---

## Codebase Reality Check

The current codebase is a **Google Compass travel itinerary starter template** that is being repurposed for LENS. Most of the existing UI/components (trip planning, destination cards, itinerary generation) are **not part of LENS** — they are leftover from the template and will be replaced.

**What exists that IS relevant:**
- `src/index.ts` — Genkit entry point
- `src/lib/genkit/genkit.config.ts` — Genkit + Vertex AI config
- `src/lib/genkit/itineraryFlow.ts` — Example Genkit flow (reference for building emergency flow)
- `src/lib/genkit/types.ts` — Type definitions (reference)
- `prompts/` — Example Genkit `.prompt` files (reference for prompt authoring)
- `firebase.json`, `firestore.rules`, `apphosting.yaml` — Firebase infrastructure config
- `next.config.mjs`, `tailwind.config.ts` — Framework config

**What needs to be built:**
- Emergency session UI (camera + mic activation, live view, status overlay)
- Emergency classification Genkit flow (Gemini multimodal)
- Calm Mode filter (post-processing AI instructions)
- Google Cloud TTS integration
- API routes: `POST /api/analyze`, optionally `POST /api/tts`
- Emergency badge component
- Text + audio instruction display

---

## Team & Responsibilities

| Role | Area |
|---|---|
| Frontend Engineer | Emergency session UI, camera/mic integration, audio playback |
| Backend Engineer | API routes, Gemini AI flow, Calm Mode filter, TTS integration |
| Maps & Routing (future) | Location awareness, nearby hospital lookup |
| Product / Docs Lead | PRD, documentation, demo coordination |

**Note:** TTS and backend are being owned by one team member. The frontend team handles camera/mic capture and UI rendering.

---

## MVP Success Criteria

- Demo runs without failure
- AI response latency ≤ 3 seconds from frame capture
- Emergency correctly classified (Injury / Medical / Fire)
- Calm, spoken instructions delivered within 3 seconds
- Judges understand the value in under 60 seconds

---

## Deadline

- **Project deadline: March 16, 2026**
- **Dev start: February 17, 2026**
- **Testing phase: ~March 9–15**

---

## Supported Emergency Types (MVP)

1. 🩸 **Injury** — Bleeding, cuts, lacerations
2. ⚕️ **Medical** — Unconscious person, possible cardiac/respiratory event
3. 🔥 **Fire** — Fire or smoke hazard

---

## Key Design Principles

1. **Calm over accuracy** — Instructions must be reassuring, not alarming
2. **Speed** — Every decision optimizes for < 3s response time
3. **No storage** — Video frames are never persisted; privacy first
4. **Fail-safe** — If AI fails, serve generic safety guidance (don't go blank)
5. **Accessible** — Works on mobile browser, no app install required

---

## Future Roadmap (Post-MVP)

- Multi-language TTS support
- Location awareness (nearest hospital / emergency services)
- Offline fallback text mode
- SMS emergency service integration
- AI-powered predictive dispatch
- Traffic-aware ambulance routing (original LENS vision)
- Government API integrations

---

## Key Files to Know

```
/
├── CLAUDE.md                          ← This file
├── docs/
│   ├── LENS-Basic PRD.md              ← Product requirements
│   └── documentation.md               ← Technical architecture doc
├── prompts/
│   └── itineraryGen.prompt            ← Example Genkit prompt (reference)
├── src/
│   ├── index.ts                       ← Genkit entry point
│   ├── app/
│   │   ├── page.tsx                   ← Home page (to be replaced)
│   │   └── api/                       ← API routes go here
│   └── lib/
│       └── genkit/
│           ├── genkit.config.ts       ← AI config (Vertex AI + Firebase)
│           └── itineraryFlow.ts       ← Example flow (reference)
└── firebase.json                      ← Firebase config
```
