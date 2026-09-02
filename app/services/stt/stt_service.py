"""Whisper Speech-to-text service implementation"""

from openai import OpenAI
from app.services.stt_base import BaseSpeechToTextService, STTResponse
from app.config import config


class WhisperService(BaseSpeechToTextService):
    """OpenAI Whisper implementation of Speech to Text.

    Single Responsibility: Audio -> Text using Whisper API"""

    def __init__(self,model:str="whisper-1",language:str="en"):
        """Initialize Whisper Service.

        Args:
            model: Whisper model to use (default:whisper-1).
            language: Language code (e.g., 'en','es'). None for auto-detect.
            """

        self.model = model
        self.language=language
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)

    def transcribe(self, audio_path:str)->STTResponse:
        with open(audio_path,"rb") as audio_files:
            transcript = self.client.audio.transcriptions.create(
                model = self.model,
                file = audio_files,
                language = self.language
            )

        return STTResponse(
            text = transcript.text,
            language=self.language or "auto",
            confidence=1.0,
            model = self.model
        )

    def transcribe_from_bytes(self,audio_bytes: bytes,format:str="wav")->STTResponse:
        from io import BytesIO
        audio_file = BytesIO(audio_bytes)
        audio_file.name = f"audio.{format}"


        transcript = self.client.audio.transcriptions.create(
            model = self.model,
            file=audio_file,
            language=self.language
        ) 

        return STTResponse(
            text = transcript.text,
            language = self.language or "auto",
            confidence =1.0,
            model = self.model
        )

    def create_stt_service(language:str="en")->WhisperService:
        return WhisperService(language=language)    
