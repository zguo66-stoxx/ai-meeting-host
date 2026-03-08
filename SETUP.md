# Setup Guide - AI Meeting Host Chatbot

## Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn
- OpenAI API key (required)
- Microphone and speaker/headphones

## Step-by-Step Setup

### 1. Clone or Download the Project

```bash
cd ai_meetinghost
```

### 2. Set Up Environment Variables

Create a `.env` file in the root directory:

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```
OPENAI_API_KEY=sk-your-actual-api-key-here
```

**Get API Key:**
- Go to https://platform.openai.com/api-keys
- Create a new secret key
- Copy and paste it into `.env`

### 3. Backend Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# Navigate to backend folder
cd backend

# Start the server
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 4. Frontend Setup (New Terminal)

Open a new terminal window:

```bash
# Navigate to frontend folder
cd frontend

# Install Node dependencies
npm install

# Start the development server
npm start
```

Browser should automatically open to `http://localhost:3000`

## Testing the Setup

1. **Check Backend**: Visit `http://localhost:8000` - you should see `{"status":"ok"}`

2. **Check Frontend**: Visit `http://localhost:3000` - you should see the AI Meeting Host interface

3. **Test Microphone**: Click "Start Meeting" and allow microphone access when prompted

4. **Test Speaking**: Click the large orange "SPEAK" button - the bot should introduce the meeting

## Customizing Your Meeting

Edit `backend/config/meeting_agenda.json` to customize:

```json
{
  "title": "Your Meeting Name",
  "duration_minutes": 60,
  "opening": "Custom opening message...",
  "topics": [
    {
      "id": 1,
      "title": "Your Topic",
      "lead": "Person Name",
      "duration_minutes": 15,
      "intro": "What bot says when introducing this topic",
      "transition": "What bot says when transitioning away"
    }
  ]
}
```

## Troubleshooting

### Microphone Not Working
- Check browser permissions (usually icon in address bar)
- Try a different browser (Chrome works best)
- Check system microphone settings

### Backend Won't Start
- Make sure Python 3.8+ is installed: `python --version`
- Make sure all dependencies installed: `pip install -r requirements.txt`
- Check if port 8000 is already in use

### Frontend Won't Connect
- Make sure backend is running first
- Check console for CORS errors
- Try clearing browser cache

### Audio Not Playing
- Check speaker/headphone volume
- Check browser console for errors
- Try refreshing the page

### API Errors
- Verify your OpenAI API key is correct in `.env`
- Check you have credits in your OpenAI account
- Check the backend logs for detailed error messages

## Cost Estimation

With OpenAI APIs:
- **Whisper (Speech-to-Text)**: ~$0.006 per minute
- **TTS (Text-to-Speech)**: ~$0.015 per 1K characters
- **GPT-4 Turbo**: ~$0.01 per 1K tokens

**Example 1-hour meeting:**
- Transcription: ~$0.36
- Bot speaking 20 times: ~$0.30
- Smart responses: ~$0.50
- **Total: ~$1-2 per meeting**

## Next Steps

1. ✅ Test with a mock meeting
2. ✅ Customize the agenda for your team
3. ✅ Adjust bot personality in `backend/services/llm_service.py`
4. ✅ Try different TTS voices in `backend/services/tts_service.py`

## Optional Enhancements

### Use ElevenLabs for Better Voice Quality

1. Sign up at https://elevenlabs.io
2. Get your API key
3. Add to `.env`:
   ```
   ELEVENLABS_API_KEY=your_key_here
   ```
4. Restart backend - it will automatically use ElevenLabs

### Change TTS Voice (OpenAI)

Edit in `frontend/src/App.js`, the API calls can specify different voices:
- `alloy` (default)
- `echo`
- `fable`
- `onyx`
- `nova`
- `shimmer`

## Support

If you encounter issues:
1. Check the browser console (F12)
2. Check backend terminal logs
3. Review the troubleshooting section above
