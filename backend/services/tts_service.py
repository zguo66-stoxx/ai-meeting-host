"""
Text-to-Speech Service
Uses GitHub Models TTS
"""
import os
import base64
from typing import Optional


class TTSService:
    def __init__(self):
        pass
    
    async def synthesize(self, text: str, voice: str = "alloy") -> str:
        """
        Convert text to speech using GitHub Models
        
        Args:
            text: Text to convert to speech
            voice: Voice ID (alloy, echo, fable, onyx, nova, shimmer)
        
        Returns:
            Base64 encoded audio data
        """
        return await self._synthesize_github(text, voice)
    
    async def _synthesize_github(self, text: str, voice: str) -> str:
        """Use GitHub Models TTS (via Azure OpenAI compatible endpoint)"""
        try:
            from openai import AsyncOpenAI
            
            client = AsyncOpenAI(
                base_url="https://models.inference.ai.azure.com",
                api_key=os.getenv("GITHUB_TOKEN")
            )
            
            response = await client.audio.speech.create(
                model="tts-1",
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
            print(f"GitHub Models TTS error: {e}")
            return ""
