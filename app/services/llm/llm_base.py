from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class LLMResponse:
    output_text: str
    model: str


class BaseLLMService(ABC):
    """Abstract base class for LLM generation services.
    
    Single Responsibility: Prompt/Context -> Response Text
    """

    @abstractmethod
    def generate_response(self, text: str) -> LLMResponse:
        """Generate a response from a single text prompt."""
        pass

    @abstractmethod
    def generate_chat_response(
        self,
        messages: list[dict[str, str]],
        system_prompt: str | None = None
    ) -> LLMResponse:
        """Generate a response given a list of conversation messages.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'.
            system_prompt: Optional system instructions.
            
        Returns:
            LLMResponse with output text.
        """
        pass

