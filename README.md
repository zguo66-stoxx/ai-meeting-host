# AI Meeting Host Chatbot MVP

A meeting host chatbot that can listen to meetings, understand the agenda, and speak when prompted via a button click.

## Features

- 🎤 **Real-time Speech Recognition** - Listens to meeting audio continuously
- 🗣️ **Text-to-Speech** - Speaks with natural AI voice
- ⏯️ **Push-to-Talk Control** - Only speaks when button is clicked
- 📋 **Agenda-Aware** - Knows meeting structure and topics
- 👥 **Role Tracking** - Knows who leads which topic
- ⚡ **Fast Response** - Pre-scripted transitions for instant playback

## Architecture

```
├── backend/          # FastAPI server
│   ├── main.py      # Main API server
│   ├── services/    # Speech, TTS, LLM services
│   └── config/      # Meeting agenda configuration
├── frontend/        # React UI
│   └── src/         # Components and logic
└── requirements.txt # Python dependencies
```

## Quick Start

### 1. Backend Setup

```bash
cd backend
pip install -r ../requirements.txt
python main.py
```

Backend runs on `http://localhost:8000`

### 2. Frontend Setup

```bash
cd frontend
npm install
npm start
```

Frontend runs on `http://localhost:3000`

### 3. Configure Meeting

Edit `backend/config/meeting_agenda.json` with your meeting structure:

```json
{
  "title": "Weekly Team Sync",
  "duration": 60,
  "topics": [
    {
      "title": "Project Updates",
      "lead": "Sarah",
      "duration": 20
    }
  ]
}
```

## Usage

1. Open the web interface
2. Click **"Start Meeting"** - Bot begins listening
3. Bot shows live transcription
4. Click **"SPEAK"** button when you want the bot to talk
5. Bot will provide context-aware responses

## Environment Variables

Create `.env` file:

```
OPENAI_API_KEY=your_key_here
ELEVENLABS_API_KEY=your_key_here  # Optional
```

## Tech Stack

- **Backend**: Python, FastAPI, WebSockets
- **Frontend**: React, Web Audio API
- **Speech-to-Text**: OpenAI Whisper API
- **Text-to-Speech**: System TTS (free) or ElevenLabs
- **LLM**: OpenAI GPT-4 Turbo

## Roadmap

- [x] Basic UI with speak button
- [x] Real-time transcription
- [x] Pre-scripted agenda transitions
- [ ] Streaming TTS for lower latency
- [ ] Speaker diarization
- [ ] Meeting summary generation
- [ ] Teams/Zoom integration

## License

MIT
