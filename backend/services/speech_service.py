"""
Speech-to-Text Service using GitHub Models Whisper
"""
import os
import io
from openai import AsyncOpenAI

# Initialize GitHub Models client
client = AsyncOpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=os.getenv("GITHUB_TOKEN")
)


class SpeechService:
    def __init__(self):
        self.model = "whisper-1"
    
    async def transcribe(self, audio_data: bytes) -> str:
        """
        Transcribe audio to text using GitHub Models Whisper
        
        Args:
            audio_data: Audio file bytes (WAV, MP3, etc.)
        
        Returns:
            Transcribed text
        """
        try:
            # Create file-like object from bytes
            audio_file = io.BytesIO(audio_data)
            audio_file.name = "audio.wav"
            
            # Call GitHub Models Whisper API
            response = await client.audio.transcriptions.create(
                model=self.model,
                file=audio_file
            )
            
            return response.text
        
        except Exception as e:
            print(f"Transcription error: {e}")
            return ""
