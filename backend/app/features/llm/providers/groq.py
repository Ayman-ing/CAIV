import os
import asyncio
import json
import logging
import re
from groq import Groq
from pydantic import BaseModel
from typing import Type, Any, Dict, List, Optional
from features.llm.interfaces import LLMProvider


logger = logging.getLogger(__name__)


def _inline_defs(schema: Dict[str, Any], defs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Recursively inline $ref pointers from $defs.
    Groq/OpenAI tool calling often fails with $ref pointers in nested schemas.
    """
    if not isinstance(schema, dict):
        return schema

    if "$ref" in schema:
        ref_path = schema["$ref"]
        # Handle #/$defs/ModelName or #/definitions/ModelName
        ref_key = ref_path.split("/")[-1]
        if ref_key in defs:
            # Inline the definition and continue recursing
            inlined = dict(defs[ref_key])
            # Merge other keys (like description) if present in the ref object
            for k, v in schema.items():
                if k != "$ref":
                    inlined[k] = v
            return _inline_defs(inlined, defs)

    return {
        k: (
            _inline_defs(v, defs)
            if isinstance(v, dict)
            else [_inline_defs(i, defs) for i in v]
            if isinstance(v, list)
            else v
        )
        for k, v in schema.items()
    }


def _simplify_schema_for_groq(schema: Dict[str, Any]) -> Dict[str, Any]:
    """
    Recursively simplify a Pydantic JSON schema for Groq compatibility.
    - Groq does not support anyOf with null variants (Optional fields in Pydantic v2).
    - Strips the null branch, keeping only the actual type.
    """
    if not isinstance(schema, dict):
        return schema

    # Handle anyOf: [<real_type_dict>, {"type": "null"}]  →  convert to type: [real_type, "null"]
    if "anyOf" in schema:
        variants = schema["anyOf"]
        # If one of the variants is null, we want to make the field nullable
        has_null = any(v == {"type": "null"} for v in variants)
        non_null_variants = [v for v in variants if v != {"type": "null"}]
        
        if len(non_null_variants) == 1:
            # Simple optional field
            base_schema = dict(non_null_variants[0])
            
            if has_null:
                if "type" in base_schema:
                    # Primitive type or object/array with explicit type: use type array
                    original_type = base_schema["type"]
                    if isinstance(original_type, list):
                        if "null" not in original_type:
                            base_schema["type"] = original_type + ["null"]
                    else:
                        base_schema["type"] = [original_type, "null"]
                elif "$ref" in base_schema:
                    # Reference: we must keep anyOf or it will lose nullability after inlining
                    # But we should simplify the ref variant itself
                    return {
                        "anyOf": [_simplify_schema_for_groq(base_schema), {"type": "null"}],
                        **{k: v for k, v in schema.items() if k not in ("anyOf", "type")}
                    }
            
            # Merge top-level metadata
            for key in ("description", "title", "default"):
                if key in schema and key not in base_schema:
                    base_schema[key] = schema[key]
            
            return _simplify_schema_for_groq(base_schema)
        
        # If there are multiple non-null variants, keep anyOf but simplify each
        return {
            "anyOf": [_simplify_schema_for_groq(v) for v in non_null_variants] + ([{"type": "null"}] if has_null else []),
            **{k: v for k, v in schema.items() if k != "anyOf"}
        }

    return {
        k: (
            _simplify_schema_for_groq(v)
            if isinstance(v, dict)
            else [_simplify_schema_for_groq(i) for i in v]
            if isinstance(v, list)
            else v
        )
        for k, v in schema.items()
    }


def pydantic_to_groq_function(
    model_class: Type[BaseModel], name: str = None, description: str = None
) -> Dict[str, Any]:
    """
    Convert a Pydantic model to a Groq-compatible function definition.
    Ensures that anyOf null variants (common in Pydantic v2 Optional fields)
    are cleaned up as Groq's tool calling doesn't support them well.
    Also inlines any $ref definitions.
    """
    # 1. Get raw schema
    raw_schema = model_class.model_json_schema()
    defs = raw_schema.get("$defs", {})
    
    # 2. Simplify (remove anyOf nulls)
    simplified = _simplify_schema_for_groq(raw_schema)
    
    # 3. Inline all $ref pointers
    # Note: We pass the simplified version of defs too
    simplified_defs = {k: _simplify_schema_for_groq(v) for k, v in defs.items()}
    inlined = _inline_defs(simplified, simplified_defs)

    parameters: Dict[str, Any] = {
        "type": "object",
        "properties": inlined.get("properties", {}),
        "required": inlined.get("required", []),
    }

    return {
        "type": "function",
        "function": {
            "name": name or model_class.__name__.lower(),
            "description": description
            or f"Extract data into {model_class.__name__} format",
            "parameters": parameters,
        },
    }


class GroqProvider(LLMProvider):
    """Groq LLM provider implementation with function calling support."""

    def __init__(self, api_key: str = None, model: str = "llama-3.3-70b-versatile"):
        from core.config import get_settings

        settings = get_settings()
        self.api_key = settings.GROQ_API_KEY
        if not self.api_key:
            raise ValueError("GROQ_API_KEY environment variable is required")
        self.client = Groq(api_key=self.api_key)
        self.model = model

    async def generate_response(self, prompt: str) -> str:
        """Generate response using Groq API (text mode)."""
        response = await asyncio.to_thread(
            self.client.chat.completions.create,
            messages=[{"role": "user", "content": prompt}],
            model=self.model,
            response_format={"type": "json_object"},
        )
        return response.choices[0].message.content

    async def parse_with_function_calling(
        self, prompt: str, model_class: Type[BaseModel], description: str = None, tool_name: str = None
    ) -> Dict[str, Any]:
        """
        Use Groq's function calling to parse text into a structured format.
        """
        function_def = pydantic_to_groq_function(model_class, name=tool_name, description=description)

        try:
            response = await asyncio.to_thread(
                self.client.chat.completions.create,
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                tools=[function_def],
                tool_choice="required",
                max_tokens=4096,
            )

            message = response.choices[0].message
            logger.info(f"Groq raw message choice: {message}")

            raw_json_str = ""
            if message.tool_calls:
                raw_json_str = message.tool_calls[0].function.arguments
            elif message.content:
                raw_json_str = message.content

            if raw_json_str:
                logger.info(f"Attempting to parse JSON from response (length: {len(raw_json_str)})")
                
                # 1. Try direct parse
                try:
                    return json.loads(raw_json_str)
                except json.JSONDecodeError:
                    pass

                # 2. Try cleaning common escaping issues
                try:
                    # Fix escaped single quotes (common in LLM outputs)
                    cleaned = raw_json_str.replace("\\'", "'")
                    return json.loads(cleaned)
                except json.JSONDecodeError:
                    pass

                # 3. Try regex extraction (find the main JSON block)
                try:
                    # Strip markdown block markers if present
                    content = raw_json_str.strip()
                    if "```" in content:
                        # Extract content between markers
                        match = re.search(r'```(?:json)?\s*(.*?)\s*```', content, re.DOTALL)
                        if match:
                            content = match.group(1)
                    
                    # Find potential JSON block (first { to last })
                    match = re.search(r'(\{.*\})', content, re.DOTALL)
                    if match:
                        potential_json = match.group(1)
                        # Remove problematic custom tags that some models might add
                        potential_json = re.sub(r'</?function>', '', potential_json)
                        
                        try:
                            return json.loads(potential_json)
                        except json.JSONDecodeError:
                            # Final attempt: fix internal escaped quotes in the regex match
                            try:
                                return json.loads(potential_json.replace("\\'", "'"))
                            except json.JSONDecodeError:
                                logger.error("Regex matched a block but it's still not valid JSON")
                except Exception as e:
                    logger.error(f"Regex extraction error: {e}")

            logger.error(f"Failed to extract valid JSON from Groq response. Raw start: {raw_json_str[:500]}")
            return {}

        except Exception as e:
            logger.error(f"Groq API call failed: {str(e)}", exc_info=True)
            raise

        return {}
