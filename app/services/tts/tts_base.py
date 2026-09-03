"""Abstract base class and data structures for Text-to-Speech services."""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class TTSResponse:
    """Response metadata from Text-to-Speech synthesis."""
    audio_path: str | None = None
    text: str = ""
    voice: str = ""


class BaseTTSService(ABC):
    """Abstract base class for Text-to-Speech services.
    
    Single Responsibility: Text -> Audio
    """

    @abstractmethod
    def speak(self, text: str) -> None:
        """Synthesize text and play audio directly.
        
        Args:
            text: Text to be spoken.
        """
        pass

    @abstractmethod
    def synthesize_to_file(self, text: str, output_path: str) -> TTSResponse:
        """Synthesize text and save audio output to a file.
        
        Args:
            text: Text to synthesize.
            output_path: File path to save the generated audio.
            
        Returns:
            TTSResponse with synthesis details.
        """
        pass
