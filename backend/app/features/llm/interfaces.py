from abc import ABC, abstractmethod
from typing import Protocol

class LLMProvider(Protocol):
    """Protocol for LLM providers."""
    
    @abstractmethod
    async def generate_response(self, prompt: str) -> str:
        """Generate a response from the LLM."""
        pass