import logging
from typing import Any, Dict, List, Type
from pydantic import BaseModel
import json
from features.llm.interfaces import LLMProvider
from features.llm.providers.groq import GroqProvider

logger = logging.getLogger(__name__)

class LLMService:
    """Service for LLM operations with strategy pattern."""
    
    def __init__(self, provider: LLMProvider = None):
        self.provider = provider or GroqProvider()
    
    def set_provider(self, provider: LLMProvider):
        """Change the LLM provider."""
        self.provider = provider
    
    
    async def parse_to_model(self, text: str, model_class: Type[BaseModel], instructions: str = None) -> BaseModel:
        """Parse text into a Pydantic model using LLM."""
        if instructions is None:
            instructions = f"""Analyze the following resume text and extract information into JSON format that matches this schema: {model_class.model_json_schema()}

Be thorough and extract all relevant information from the resume text."""

        prompt = f"{instructions}\n\nResume text:\n{text}\n\nReturn only valid JSON that matches the schema."

        response = await self.provider.generate_response(prompt)

        # Try to parse JSON
        try:
            data = json.loads(response)
            return model_class(**data)
        except (json.JSONDecodeError, ValueError) as e:
            raise ValueError(f"Failed to parse LLM response into {model_class.__name__}: {e}")
    
    async def parse_to_model_with_function_calling(
        self,
        text: str,
        model_class: Type[BaseModel],
        instructions: str = None,
        tool_name: str = None
    ) -> BaseModel:
        """
        Parse text into a Pydantic model using Groq's function calling.

        This is more reliable than text-based JSON parsing as Groq enforces
        the schema structure directly through function definitions.

        Args:
            text: The text to parse
            model_class: The Pydantic model to parse into
            instructions: Optional parsing instructions
            tool_name: Optional custom name for the tool

        Returns:
            Instance of model_class with extracted data
        """
        if instructions is None:
            instructions = f"""You are an expert at parsing resumes. Analyze the following resume text and extract all relevant information into the provided schema format.

Return ONLY the structured data - extract everything you can from the resume."""

        prompt = f"{instructions}\n\n--- Resume Text ---\n{text}"

        # Use function calling for more reliable parsing
        if hasattr(self.provider, 'parse_with_function_calling'):
            data = await self.provider.parse_with_function_calling(
                prompt,
                model_class,
                description=f"Extract resume data into {model_class.__name__} format",
                tool_name=tool_name
            )
        else:
            # Fallback to regular method if provider doesn't support function calling
            response = await self.provider.generate_response(prompt)
            try:
                data = json.loads(response)
            except json.JSONDecodeError as e:
                raise ValueError(f"Failed to parse LLM response: {e}")

        logger.info(f"LLM raw extracted data keys: {list(data.keys()) if isinstance(data, dict) else type(data)}")
        logger.info(f"LLM extracted data (truncated): {str(data)[:1000]}")

        try:
            # Use model_validate (Pydantic v2) to properly coerce nested dicts into sub-models
            return model_class.model_validate(data)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Failed to create {model_class.__name__} from extracted data: {e}")

    async def parse_multiple_models(self, text: str, model_configs: List[Dict[str, Any]]) -> List[BaseModel]:
        """Parse text into multiple Pydantic models."""
        results = []
        for config in model_configs:
            model_class = config['model_class']
            instructions = config.get('instructions')
            try:
                model = await self.parse_to_model(text, model_class, instructions)
                results.append(model)
            except ValueError:
                # Skip if parsing fails
                continue
        return results