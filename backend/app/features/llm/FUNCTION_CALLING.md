# Function Calling Enhancement - Resume Import

## Overview

The resume import pipeline has been enhanced to use **Groq's function calling** capability instead of just asking for JSON text responses. This provides:

✅ **Schema Enforcement** - Groq enforces the exact schema structure
✅ **Higher Success Rate** - No JSON parsing errors
✅ **Better Type Safety** - Direct mapping to Pydantic models
✅ **Deterministic Output** - Consistent data structure
✅ **Fallback Support** - Falls back to text parsing if needed

## How It Works

### Before (Text-based JSON)
```
Resume PDF
  ↓
Docling extracts text
  ↓
LLM generates JSON text
  ↓
parse("json text") → Pydantic model
  ↓ (error prone!)
Profile
```

### After (Function Calling)
```
Resume PDF
  ↓
Docling extracts text
  ↓
ResumeData schema converted to Groq function
  ↓
LLM calls function with structured arguments
  ↓
Groq enforces schema ✓
  ↓
Direct mapping to Pydantic model
  ↓
Profile
```

## Architecture

### 1. Pydantic to Groq Function Conversion

```python
# Automatic conversion
def pydantic_to_groq_function(model_class: Type[BaseModel]) -> Dict:
    """Converts Pydantic schema to Groq function definition"""
    # Extracts JSON schema from Pydantic model
    # Creates function definition with proper parameter types
```

**Example Output:**
```python
{
    "type": "function",
    "function": {
        "name": "resumedata",
        "description": "Extract resume data into ResumeData format",
        "parameters": {
            "type": "object",
            "properties": {
                "contact_info": {...},
                "education": [...],
                "skills": [...]
            },
            "required": [...]
        }
    }
}
```

### 2. Function Calling Request

```python
# Groq API call with function definitions
response = client.chat.completions.create(
    model="mixtral-8x7b-32768",
    messages=[{"role": "user", "content": resume_text}],
    tools=[function_definition],  # Pass ResumeData schema as tool
    tool_choice="auto"
)
```

### 3. Response Parsing

```python
# Groq either:
# A) Calls the function with structured arguments
if response.tool_calls:
    args = json.loads(tool_call.function.arguments)
    return ResumeData(**args)

# B) Falls back to text if function not called
else:
    return json.loads(response.content)
```

## Implementation Details

### Enhanced GroqProvider

**New Method:** `parse_with_function_calling()`
```python
async def parse_with_function_calling(
    self,
    prompt: str,
    model_class: Type[BaseModel],
    description: str = None
) -> Dict[str, Any]:
    """Use Groq's tool calling for schema-based parsing"""
    # Converts model_class to function definition
    # Sends to Groq with tool_choice="auto"
    # Extracts and returns structured arguments
```

### Enhanced LLMService

**New Method:** `parse_to_model_with_function_calling()`
```python
async def parse_to_model_with_function_calling(
    self,
    text: str,
    model_class: Type[BaseModel],
    instructions: str = None
) -> BaseModel:
    """Wrapper around provider's function calling"""
    # Calls provider.parse_with_function_calling()
    # Validates result against model_class
    # Returns Pydantic model instance
```

### Updated PDFParserService

```python
async def parse_cv_structure(self, file_path: str) -> Dict:
    # Extract PDF text
    raw_text = self.extract_text_from_file(file_path)

    # Use function calling (not just JSON response)
    resume_data = await self.llm_service.parse_to_model_with_function_calling(
        raw_text,
        ResumeData,
        self._get_parsing_instructions()
    )

    return self._convert_to_dict(resume_data)
```

## Benefits

### 1. **Reliability**
- Groq enforces schema compliance
- No partial/malformed JSON responses
- Structured fallback if function not called

### 2. **Accuracy**
- Direct to Pydantic validation
- Type checking at parse time
- Better handling of complex nested structures

### 3. **Performance**
- Fewer parsing errors = fewer retries
- Groq optimizes for function calling responses
- Cleaner data extraction

### 4. **Maintainability**
- Single source of truth (Pydantic schemas)
- Automatic function definition generation
- Easy to add new schemas

## Groq Model Support

**Recommended Models for Function Calling:**
- `mixtral-8x7b-32768` (8k context, recommended)
- `llama2-70b-4096` (4k context)

**Note:** Function calling support varies by model. Provider includes fallback to text-based parsing if model doesn't support it.

## Error Handling

```python
try:
    # Try function calling
    data = await provider.parse_with_function_calling(prompt, model)
    return model(**data)

except ValueError as e:
    # Schema validation failed
    logger.error(f"Validation error: {e}")
    raise

except Exception as e:
    # Fallback: try text-based parsing
    logger.warning(f"Function calling failed: {e}")
    response = await provider.generate_response(prompt)
    data = json.loads(response)
    return model(**data)
```

## Backward Compatibility

- Old `parse_to_model()` method still works with text-based JSON
- New `parse_to_model_with_function_calling()` uses function calling
- Provider automatically detects capability and falls back if needed
- No breaking changes to existing code

## Future Enhancements

1. **Multi-model Support** - Support OpenAI, Anthropic function calling
2. **Streaming** - Stream function call results as they arrive
3. **Parallel Extraction** - Call multiple functions simultaneously
4. **Confidence Scores** - LLM returns confidence for each extracted field
5. **Fallback Models** - Switch models if primary fails

## Testing

```bash
# Test function calling directly
curl -X POST /api/v1/resume-import/upload \
  -F "resume=@test.pdf" \
  -F "profile_id={uuid}" \
  -H "Authorization: Bearer {token}"

# Response will use function calling internally
```

## Migration Notes

If moving from old pipeline:
1. ✅ Backward compatible - no code changes needed
2. ✅ Automatic fallback if function calling unavailable
3. ✅ Can mix both methods in same application
4. ✅ No database schema changes
