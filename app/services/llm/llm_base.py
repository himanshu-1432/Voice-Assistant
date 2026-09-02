from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class LLMResponse:
    output_text: str
    model: str

class BaseLLMService(ABC):

    @abstractmethod
    def generate_response(self, text: str) -> LLMResponse:
        pass

