# Development Guide

## Project Architecture

```
ai_meetinghost/
├── backend/                 # Python FastAPI server
│   ├── main.py             # Main API endpoints
│   ├── services/           # Core services
│   │   ├── speech_service.py    # Whisper STT
│   │   ├── tts_service.py       # Text-to-Speech
│   │   └── llm_service.py       # GPT-4 integration
│   └── config/
│       └── meeting_agenda.json  # Meeting structure
│
├── frontend/               # React application
│   ├── public/
│   └── src/
│       ├── App.js         # Main component
│       ├── App.css        # Styling
│       └── index.js       # Entry point
│
├── requirements.txt       # Python dependencies
├── .env.example          # Environment template
└── README.md             # Project overview
```

## API Endpoints

### Meeting Management

**GET `/api/agenda`**
- Returns meeting agenda configuration
- Response: JSON with title, duration, topics

**POST `/api/meeting/start`**
- Starts a new meeting session
- Initializes meeting state

**POST `/api/meeting/stop`**
- Stops current meeting
- Clears meeting state

**GET `/api/meeting/status`**
- Returns current meeting status
- Includes current topic and transcription count

### Speech & Audio

**POST `/api/transcribe`**
- Transcribes audio file to text
- Body: FormData with audio file
- Returns: `{ transcription: string }`

**POST `/api/speak/opening`**
- Generates opening speech
- Returns: `{ text: string, audio: base64 }`

**POST `/api/speak/next-topic`**
- Introduces next topic
- Returns: `{ text: string, audio: base64 }`

**POST `/api/speak/transition`**
- Transitions between topics
- Returns: `{ text: string, audio: base64 }`

**POST `/api/speak/smart`**
- AI-generated contextual response
- Body: `{ message: string }`
- Returns: `{ text: string, audio: base64 }`

**WebSocket `/ws/transcription`**
- Real-time transcription stream
- Send: audio bytes
- Receive: `{ type: "transcription", text: string }`

## Frontend State Management

```javascript
// Meeting State
{
  meetingActive: boolean,     // Is meeting running?
  agenda: object,             // Meeting agenda config
  currentTopic: object,       // Current topic info
  transcription: array,       // Transcription history
  isListening: boolean,       // Mic active?
  isSpeaking: boolean,        // Bot speaking?
  botMessage: string          // Last bot message
}
```

## Adding New Features

### Add a New API Endpoint

1. Edit `backend/main.py`
2. Define new endpoint:

```python
@app.post("/api/custom-action")
async def custom_action(data: dict):
    # Your logic here
    return {"status": "success"}
```

3. Call from frontend:

```javascript
const response = await axios.post(`${API_BASE}/api/custom-action`, {
  // your data
});
```

### Modify Meeting Agenda Structure

1. Edit `backend/config/meeting_agenda.json`
2. Add new fields to topics
3. Update `backend/main.py` endpoints to use new fields
4. Update frontend to display new information

### Change Bot Personality

Edit `backend/services/llm_service.py`:

```python
self.system_prompt = """Your custom personality here..."""
```

### Add Custom Voice

For OpenAI TTS, modify the voice parameter in API calls:

```python
response = await client.audio.speech.create(
    model="tts-1",
    voice="nova",  # Change this: alloy, echo, fable, onyx, nova, shimmer
    input=text
)
```

## Testing

### Test Backend Directly

```bash
# Start backend
cd backend
python main.py

# In another terminal, test with curl
curl http://localhost:8000/api/agenda
```

### Test Speech Recognition

```python
# Test script
from services.speech_service import SpeechService

service = SpeechService()
with open("test.wav", "rb") as f:
    result = await service.transcribe(f.read())
    print(result)
```

### Test TTS

```python
from services.tts_service import TTSService

service = TTSService()
audio = await service.synthesize("Hello, this is a test")
print(f"Generated audio: {len(audio)} bytes")
```

## Performance Optimization

### Reduce API Latency

1. **Use streaming APIs** (not yet implemented)
2. **Cache common responses**
3. **Pre-generate static transitions**

### Reduce Costs

1. Use `tts-1` instead of `tts-1-hd`
2. Use `gpt-3.5-turbo` for simple responses
3. Limit transcription frequency (currently 5-second chunks)

## Deployment

### Deploy Backend (Heroku Example)

```bash
# Add Procfile
echo "web: cd backend && uvicorn main:app --host 0.0.0.0 --port \$PORT" > Procfile

# Deploy
heroku create your-app-name
heroku config:set OPENAI_API_KEY=your_key
git push heroku main
```

### Deploy Frontend (Vercel Example)

```bash
cd frontend
npm run build
npx vercel --prod
```

Update frontend `API_BASE` to your backend URL.

## Common Issues

### CORS Errors
- Check `allow_origins` in `backend/main.py`
- Make sure both servers are running

### Audio Format Issues
- Ensure browser records in supported format
- Check `MediaRecorder` options

### WebSocket Connection Fails
- Check firewall settings
- Verify WebSocket URL is correct
- Try polling as fallback

## Contributing

1. Create feature branch
2. Make changes
3. Test thoroughly
4. Submit pull request

## License

MIT
