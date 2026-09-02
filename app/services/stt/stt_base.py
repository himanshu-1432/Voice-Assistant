from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class STTResponse:
    """Response from a Speech-to-Text service."""
    text:str
    language:str
    confidence:float=1.0
    model:str=""

class BaseSpeechToTextService(ABC):
    """Abstract base class for Speech-to-Text Services.

    Single Responsibility: Audio->Text
    """

    @abstractmethod
    def transcribe(self,audio_path:str) -> STTResponse:
        """Transcribe audio files to text.

        Args: audio_path: Path to audio file (MP3, WAV, etc.)

        Returns:
                STTResponse with transcribe text and metadata.
        """
        pass        

    @abstractmethod
    def transcribe_from_bytes(self,audio_bytes:bytes, format:str="wav")->STTResponse:
        """Transcribe audio from bytes to text.

        Args:
            audio_bytes: Raw audio data as bytes.
            format: Audio format(wav, mp3, etc.)

        Returns:
            STTResponse with transcribed text and metadata.
        """
        pass