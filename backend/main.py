"""
AI Meeting Host Chatbot - Main API Server
"""
import os
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from typing import Optional
import asyncio

from services.speech_service import SpeechService
from services.tts_service import TTSService
from services.llm_service import LLMService

# Load environment variables
load_dotenv()

app = FastAPI(title="AI Meeting Host API")

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
speech_service = SpeechService()
tts_service = TTSService()
llm_service = LLMService()

# Load meeting agenda
with open("config/meeting_agenda.json", "r") as f:
    MEETING_AGENDA = json.load(f)

# Meeting state
meeting_state = {
    "is_active": False,
    "current_topic_index": -1,
    "transcription": [],
    "start_time": None
}


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "ok", "service": "AI Meeting Host API"}


@app.get("/api/agenda")
async def get_agenda():
    """Get the meeting agenda"""
    return MEETING_AGENDA


@app.post("/api/meeting/start")
async def start_meeting():
    """Start a new meeting"""
    meeting_state["is_active"] = True
    meeting_state["current_topic_index"] = -1
    meeting_state["transcription"] = []
    meeting_state["start_time"] = asyncio.get_event_loop().time()
    
    return {
        "status": "started",
        "message": "Meeting started successfully"
    }


@app.post("/api/meeting/stop")
async def stop_meeting():
    """Stop the current meeting"""
    meeting_state["is_active"] = False
    
    return {
        "status": "stopped",
        "message": "Meeting stopped successfully"
    }


@app.get("/api/meeting/status")
async def get_meeting_status():
    """Get current meeting status"""
    current_topic = None
    if 0 <= meeting_state["current_topic_index"] < len(MEETING_AGENDA["topics"]):
        current_topic = MEETING_AGENDA["topics"][meeting_state["current_topic_index"]]
    
    return {
        "is_active": meeting_state["is_active"],
        "current_topic_index": meeting_state["current_topic_index"],
        "current_topic": current_topic,
        "transcription_count": len(meeting_state["transcription"])
    }


@app.post("/api/transcribe")
async def transcribe_audio(audio: UploadFile = File(...)):
    """Transcribe uploaded audio chunk"""
    try:
        audio_data = await audio.read()
        transcription = await speech_service.transcribe(audio_data)
        
        # Store transcription
        meeting_state["transcription"].append(transcription)
        
        return {
            "status": "success",
            "transcription": transcription
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )


@app.post("/api/speak/opening")
async def speak_opening():
    """Generate speech for meeting opening"""
    try:
        opening_text = MEETING_AGENDA["opening"]
        meeting_state["current_topic_index"] = 0
        
        audio_data = await tts_service.synthesize(opening_text)
        
        return {
            "status": "success",
            "text": opening_text,
            "audio": audio_data,
            "action": "opening"
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )


@app.post("/api/speak/next-topic")
async def speak_next_topic():
    """Generate speech for next topic introduction"""
    try:
        current_index = meeting_state["current_topic_index"]
        
        if current_index < 0:
            return JSONResponse(
                status_code=400,
                content={"status": "error", "message": "Meeting not started"}
            )
        
        if current_index >= len(MEETING_AGENDA["topics"]):
            # Meeting is over, give closing
            closing_text = MEETING_AGENDA["closing"]
            audio_data = await tts_service.synthesize(closing_text)
            
            return {
                "status": "success",
                "text": closing_text,
                "audio": audio_data,
                "action": "closing"
            }
        
        # Get current topic intro
        topic = MEETING_AGENDA["topics"][current_index]
        intro_text = topic["intro"]
        
        audio_data = await tts_service.synthesize(intro_text)
        
        return {
            "status": "success",
            "text": intro_text,
            "audio": audio_data,
            "action": "topic_intro",
            "topic": topic
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )


@app.post("/api/speak/transition")
async def speak_transition():
    """Generate speech for topic transition"""
    try:
        current_index = meeting_state["current_topic_index"]
        
        if current_index < 0 or current_index >= len(MEETING_AGENDA["topics"]):
            return JSONResponse(
                status_code=400,
                content={"status": "error", "message": "Invalid topic index"}
            )
        
        topic = MEETING_AGENDA["topics"][current_index]
        transition_text = topic["transition"]
        
        # Move to next topic
        meeting_state["current_topic_index"] += 1
        
        audio_data = await tts_service.synthesize(transition_text)
        
        return {
            "status": "success",
            "text": transition_text,
            "audio": audio_data,
            "action": "transition"
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )


@app.post("/api/speak/smart")
async def speak_smart(context: dict):
    """Generate intelligent response based on context"""
    try:
        # Get recent transcription for context
        recent_transcripts = meeting_state["transcription"][-5:]
        current_topic = None
        
        if 0 <= meeting_state["current_topic_index"] < len(MEETING_AGENDA["topics"]):
            current_topic = MEETING_AGENDA["topics"][meeting_state["current_topic_index"]]
        
        # Generate response using LLM
        response_text = await llm_service.generate_response(
            transcripts=recent_transcripts,
            current_topic=current_topic,
            agenda=MEETING_AGENDA,
            custom_context=context.get("message", "")
        )
        
        audio_data = await tts_service.synthesize(response_text)
        
        return {
            "status": "success",
            "text": response_text,
            "audio": audio_data,
            "action": "smart_response"
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )


@app.websocket("/ws/transcription")
async def websocket_transcription(websocket: WebSocket):
    """WebSocket endpoint for real-time transcription"""
    await websocket.accept()
    
    try:
        while True:
            # Receive audio data
            audio_data = await websocket.receive_bytes()
            
            # Transcribe
            transcription = await speech_service.transcribe(audio_data)
            
            # Send back transcription
            await websocket.send_json({
                "type": "transcription",
                "text": transcription
            })
            
            # Store in meeting state
            meeting_state["transcription"].append(transcription)
            
    except WebSocketDisconnect:
        print("WebSocket disconnected")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
