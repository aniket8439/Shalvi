# 🤖 SHALVI — Personal AI Voice Assistant

> *Inspired by Tony Stark's FRIDAY — built for Aniket.*

## Features
- 🎙️ Voice input (browser mic / push-to-talk)
- 🔊 Natural female voice output (Edge TTS — free)
- 🧠 LLM-powered conversation (Groq free tier — Llama 3)
- 💬 Web-based UI with chat history
- 🧬 Personality system prompt — gentle, loyal, FRIDAY-style

## Quick Start

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up environment
cp .env.example .env
# Edit .env and add your GROQ_API_KEY (free at https://console.groq.com)

# 4. Run
python app.py
```

Then open **http://localhost:5000** in your browser.

## Architecture
```
┌──────────────────────────────────┐
│         Browser (Web UI)         │
│  Mic → STT (Web Speech API)     │
│  Chat UI + Audio Playback        │
└────────────┬─────────────────────┘
             │ REST / WebSocket
┌────────────▼─────────────────────┐
│        Flask Backend (app.py)    │
│  ┌─────────────────────────┐     │
│  │   Shalvi Core Engine    │     │
│  │  - Personality Layer    │     │
│  │  - Conversation Memory  │     │
│  │  - Response Generation  │     │
│  └────────┬────────────────┘     │
│           │                      │
│  ┌────────▼────────────────┐     │
│  │  Groq API (Llama 3)    │     │
│  │  (Free LLM Backend)    │     │
│  └─────────────────────────┘     │
│  ┌─────────────────────────┐     │
│  │  Edge TTS (Free Voice)  │     │
│  └─────────────────────────┘     │
└──────────────────────────────────┘
```

## Phase 2 (Future)
- Fine-tune personality on your speech patterns
- Local Whisper STT for privacy
- Wake-word detection ("Hey Shalvi")
- Smart home integration
- Persistent memory with vector DB
