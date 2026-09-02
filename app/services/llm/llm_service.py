from app.services.llm.llm_base import LLMResponse, BaseLLMService
from openai import OpenAI 
from app.config import config


class LLMService(BaseLLMService):
    def __init__(self, model: str | None = None):
        self.model = model or config.LLM_MODEL
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)

    def generate_response(self, text: str) -> LLMResponse:
        if not text.strip():
            raise ValueError("Prompt cannot be empty.")

        response = self.client.responses.create(
            model=self.model,
            input=text,
        )

        return LLMResponse(
            output_text=response.output_text,
            model=self.model,
        )