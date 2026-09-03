from app.services.llm.llm_base import LLMResponse, BaseLLMService
from openai import OpenAI 
from app.config import config


class LLMService(BaseLLMService):
    def __init__(self, model: str | None = None):
        self.model = model or config.LLM_MODEL
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)

    def generate_response(self, text: str) -> LLMResponse:
        """Generate response for a single prompt."""
        if not text.strip():
            raise ValueError("Prompt cannot be empty.")

        messages = [
            {"role": "system", "content": config.SYSTEM_PROMPT},
            {"role": "user", "content": text.strip()}
        ]
        return self.generate_chat_response(messages=messages)

    def generate_chat_response(
        self,
        messages: list[dict[str, str]],
        system_prompt: str | None = None
    ) -> LLMResponse:
        """Generate response given conversation messages."""
        if not messages:
            raise ValueError("Messages list cannot be empty.")

        sys_instruction = system_prompt or config.SYSTEM_PROMPT
        payload_messages = []

        # Add system prompt if not already present
        if not any(m.get("role") == "system" for m in messages):
            payload_messages.append({"role": "system", "content": sys_instruction})

        payload_messages.extend(messages)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=payload_messages,
        )

        content = response.choices[0].message.content or ""

        return LLMResponse(
            output_text=content.strip(),
            model=self.model,
        )


def create_llm_service(model: str | None = None) -> BaseLLMService:
    """Factory function to create an LLM service instance."""
    return LLMService(model=model)