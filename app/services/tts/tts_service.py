"""Text-to-Speech service implementations."""

import os
import tempfile
from openai import OpenAI
import pyttsx3

from app.config import config
from app.services.audio_recorder import play_audio
from app.services.tts.tts_base import BaseTTSService, TTSResponse


class Pyttsx3TTSService(BaseTTSService):
    """Offline Text-to-Speech using pyttsx3.
    
    Single Responsibility: Text -> Audio via local engine.
    """

    def __init__(self, rate: int | None = None, volume: float | None = None, voice_id: str | None = None):
        self.rate = rate if rate is not None else config.TTS_RATE
        self.volume = volume if volume is not None else config.TTS_VOLUME
        self.voice_id = voice_id

    def _init_engine(self) -> pyttsx3.Engine:
        """Initialize and configure a pyttsx3 engine instance."""
        engine = pyttsx3.init()
        engine.setProperty("rate", self.rate)
        engine.setProperty("volume", self.volume)
        if self.voice_id:
            engine.setProperty("voice", self.voice_id)
        return engine

    def speak(self, text: str) -> None:
        """Speak text directly using local audio output."""
        if not text or not text.strip():
            return
        engine = self._init_engine()
        engine.say(text)
        engine.runAndWait()
        engine.stop()

    def synthesize_to_file(self, text: str, output_path: str) -> TTSResponse:
        """Synthesize text and save audio output to file."""
        if not text or not text.strip():
            raise ValueError("Text to synthesize cannot be empty.")

        engine = self._init_engine()
        engine.save_to_file(text, output_path)
        engine.runAndWait()
        engine.stop()

        return TTSResponse(
            audio_path=output_path,
            text=text,
            voice=self.voice_id or "default"
        )


class OpenAITTSService(BaseTTSService):
    """Cloud Text-to-Speech using OpenAI Audio Speech API.
    
    Single Responsibility: Text -> Audio via OpenAI TTS.
    """

    def __init__(
        self,
        model: str | None = None,
        voice: str | None = None
    ):
        self.model = model or config.TTS_MODEL
        self.voice = voice or config.TTS_VOICE
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)

    def speak(self, text: str) -> None:
        """Synthesize text using OpenAI and play back audio."""
        if not text or not text.strip():
            return

        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
            temp_path = temp_file.name

        try:
            self.synthesize_to_file(text, temp_path)
            play_audio(temp_path)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def synthesize_to_file(self, text: str, output_path: str) -> TTSResponse:
        """Synthesize text and write output audio file."""
        if not text or not text.strip():
            raise ValueError("Text to synthesize cannot be empty.")

        response = self.client.audio.speech.create(
            model=self.model,
            voice=self.voice,
            input=text
        )

        response.stream_to_file(output_path)

        return TTSResponse(
            audio_path=output_path,
            text=text,
            voice=self.voice
        )


def create_tts_service(provider: str | None = None) -> BaseTTSService:
    """Factory function to instantiate the configured TTS service."""
    selected_provider = (provider or config.TTS_PROVIDER).lower()
    if selected_provider == "openai":
        return OpenAITTSService()
    return Pyttsx3TTSService()
