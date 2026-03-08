"""
LLM Service for generating intelligent meeting responses
Uses GitHub Models for context-aware responses
"""
import os
from typing import List, Optional, Dict
from openai import AsyncOpenAI

# Initialize GitHub Models client
client = AsyncOpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=os.getenv("GITHUB_TOKEN")
)


class LLMService:
    def __init__(self):
        self.model = "gpt-4o"  # GitHub Models GPT-4o
        self.system_prompt = """You are an AI meeting host assistant. 
Your role is to:
- Facilitate smooth meeting flow
- Provide brief, professional responses
- Keep responses under 30 seconds when spoken
- Be helpful but not interrupt the natural conversation
- Reference the meeting agenda and context when relevant

Keep your language natural and conversational, as if you're a professional meeting facilitator."""
    
    async def generate_response(
        self,
        transcripts: List[str],
        current_topic: Optional[Dict],
        agenda: Dict,
        custom_context: str = ""
    ) -> str:
        """
        Generate an intelligent response based on meeting context
        
        Args:
            transcripts: Recent meeting transcriptions
            current_topic: Current topic being discussed
            agenda: Full meeting agenda
            custom_context: Additional context or specific prompt
        
        Returns:
            Generated response text
        """
        try:
            # Build context
            context_parts = []
            
            if current_topic:
                context_parts.append(f"Current topic: {current_topic['title']} (led by {current_topic['lead']})")
            
            if transcripts:
                recent_discussion = "\n".join(transcripts[-5:])
                context_parts.append(f"Recent discussion:\n{recent_discussion}")
            
            context_parts.append(f"Meeting agenda: {agenda['title']}")
            
            if custom_context:
                context_parts.append(f"Specific request: {custom_context}")
            
            context = "\n\n".join(context_parts)
            
            # Generate response
            response = await client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": f"{context}\n\nProvide a brief, helpful response as the meeting host."}
                ],
                max_tokens=150,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            print(f"LLM generation error: {e}")
            return "I'm here if you need anything. Please continue."
    
    async def generate_summary(self, transcripts: List[str], topic: Dict) -> str:
        """
        Generate a summary of the discussion for a topic
        
        Args:
            transcripts: All transcripts for the topic
            topic: Topic information
        
        Returns:
            Summary text
        """
        try:
            discussion = "\n".join(transcripts)
            
            response = await client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {
                        "role": "user",
                        "content": f"Summarize this discussion about '{topic['title']}' in 2-3 sentences:\n\n{discussion}"
                    }
                ],
                max_tokens=100,
                temperature=0.5
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            print(f"Summary generation error: {e}")
            return ""
