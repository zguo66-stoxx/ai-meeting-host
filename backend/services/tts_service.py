"""
Text-to-Speech Service
Supports both system TTS (free) and ElevenLabs (premium)
"""
import os
import base64
from typing import Optional


class TTSService:
    def __init__(self):
        self.elevenlabs_key = os.getenv("ELEVENLABS_API_KEY")
        self.use_elevenlabs = bool(self.elevenlabs_key)
    
    async def synthesize(self, text: str, voice: str = "alloy") -> str:
        """
        Convert text to speech
        
        Args:
            text: Text to convert to speech
            voice: Voice ID (for OpenAI: alloy, echo, fable, onyx, nova, shimmer)
        
        Returns:
            Base64 encoded audio data
        """
        if self.use_elevenlabs:
            return await self._synthesize_elevenlabs(text, voice)
        else:
            return await self._synthesize_openai(text, voice)
    
    async def _synthesize_openai(self, text: str, voice: str) -> str:
        """Use OpenAI TTS (fast and good quality)"""
        try:
            from openai import AsyncOpenAI
            
            client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            
            response = await client.audio.speech.create(
                model="tts-1",  # or tts-1-hd for higher quality
                voice=voice,
                input=text,
                response_format="mp3"
            )
            
            # Get audio bytes
            audio_bytes = response.content
            
            # Encode to base64 for JSON transmission
            audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
            
            return audio_base64
        
        except Exception as e:
            print(f"OpenAI TTS error: {e}")
            return ""
    
    async def _synthesize_elevenlabs(self, text: str, voice_id: str = "21m00Tcm4TlvDq8ikWAM") -> str:
        """Use ElevenLabs TTS (premium quality)"""
        try:
            import httpx
            
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
            
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": self.elevenlabs_key
            }
            
            data = {
                "text": text,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.5
                }
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=data, headers=headers)
                
                if response.status_code == 200:
                    audio_bytes = response.content
                    audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
                    return audio_base64
                else:
                    print(f"ElevenLabs error: {response.status_code}")
                    return ""
        
        except Exception as e:
            print(f"ElevenLabs TTS error: {e}")
            return ""
