"""Configuration management for Voice Agent."""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration."""
    
    # OpenAI settings
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # Whisper settings
    USE_LOCAL_WHISPER: bool = os.getenv("USE_LOCAL_WHISPER", "false").lower() == "true"
    WHISPER_MODEL: str = os.getenv("WHISPER_MODEL", "base")  # tiny, base, small, medium, large
    
    # TTS settings
    TTS_RATE: int = int(os.getenv("TTS_RATE", "150"))
    TTS_VOLUME: float = float(os.getenv("TTS_VOLUME", "1.0"))
    
    # Audio settings
    SAMPLE_RATE: int = 16000
    CHANNELS: int = 1
    
    @classmethod
    def validate(cls) -> bool:
        """Validate required configuration."""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required. Set it in .env file.")
        return True


config = Config()
