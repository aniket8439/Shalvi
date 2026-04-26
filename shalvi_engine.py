"""
Core engine: personality, memory, and LLM integration.
"""

import os
import json
import asyncio
import tempfile
import edge_tts
from datetime import datetime
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = """You are SHALVI, a personal AI assistant created exclusively for Aniket — much like FRIDAY was for Tony Stark.

Your personality:
- You are female, warm, gentle, and deeply loyal to Aniket.
- You address him casually — "Aniket" or "boss" occasionally, but keep it natural.
- You are witty but never sarcastic toward him. You can be playful.
- You are concise by default — no walls of text unless asked to elaborate.
- You speak naturally, like a close companion who genuinely cares.
- When Aniket seems stressed or frustrated, you respond with calm reassurance.
- You are proactive: if you notice something in the conversation, gently offer help.

Rules:
- Keep responses SHORT (1-3 sentences) unless more detail is requested.
- Use natural conversational language — no corporate speak.
- Never say "As an AI" or "I'm just a language model". You are Shalvi.
- If you don't know something, say so honestly but offer to help figure it out.
- Current date/time context: {datetime}
"""


class ShalviEngine:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.voice = os.getenv("SHALVI_VOICE", "en-US-AriaNeural")
        self.conversation_history = []
        self.max_history = 20  # Keep last 20 exchanges for context

    def _get_system_prompt(self):
        return SYSTEM_PROMPT.format(datetime=datetime.now().strftime("%A, %B %d, %Y — %I:%M %p"))

    def chat(self, user_message: str) -> str:
        """Send a message to Shalvi and get a text response."""
        self.conversation_history.append({"role": "user", "content": user_message})

        # Trim history
        if len(self.conversation_history) > self.max_history * 2:
            self.conversation_history = self.conversation_history[-self.max_history * 2:]

        messages = [{"role": "system", "content": self._get_system_prompt()}] + self.conversation_history

        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                temperature=0.7,
                max_tokens=512,
            )
            reply = response.choices[0].message.content.strip()
        except Exception as e:
            reply = f"I'm having trouble connecting right now, Aniket. Error: {str(e)}"

        self.conversation_history.append({"role": "assistant", "content": reply})
        return reply

    async def text_to_speech(self, text: str) -> str:
        """Convert text to speech using Edge TTS (free). Returns path to audio file."""
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3", dir=tempfile.gettempdir())
        tmp.close()
        communicate = edge_tts.Communicate(text, self.voice, rate="+5%", pitch="+0Hz")
        await communicate.save(tmp.name)
        return tmp.name

    def tts_sync(self, text: str) -> str:
        """Synchronous wrapper for TTS."""
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(self.text_to_speech(text))
        finally:
            loop.close()

    def clear_history(self):
        self.conversation_history = []
