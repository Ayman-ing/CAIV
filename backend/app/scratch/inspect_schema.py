import json
import sys
import os

# Add the app directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "backend/app")))

from features.resume_import.pdf_parser_service import ResumeDataLenient
from features.llm.providers.groq import pydantic_to_groq_function

tool = pydantic_to_groq_function(ResumeDataLenient)
print(json.dumps(tool, indent=2))
