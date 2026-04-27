import os
import json
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

tools = [
    {
        "type": "function",
        "function": {
            "name": "test_null",
            "description": "Test if Groq accepts array types with null",
            "parameters": {
                "type": "object",
                "properties": {
                    "field": {
                        "type": ["string", "null"],
                        "description": "A field that can be null"
                    }
                },
                "required": []
            }
        }
    }
]

try:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": "Call test_null with field=null"}],
        tools=tools,
        tool_choice="required"
    )
    print("SUCCESS: Groq accepted type: ['string', 'null']")
    print(response.choices[0].message.tool_calls[0].function.arguments)
except Exception as e:
    print(f"FAILED: {e}")
