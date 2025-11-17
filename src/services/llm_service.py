from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field
from typing import Literal, List
from src.core.config import config

GEMINI_API_KEY = config.GEMINI_API_KEY

class BehavioralQuestions(BaseModel):
    questions: List[str] = Field(..., description="A list of 5 behavioral questions.")

llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", google_api_key=GEMINI_API_KEY)
structured_llm = llm.with_structured_output(
    schema=BehavioralQuestions.model_json_schema(), 
    method="json_schema"
)
response = structured_llm.invoke(
    "Generate 5 behavioral interview questions for a Senior Python role." 
)

for i, q in enumerate(response['questions']):
    print(f"Question {i+1}: {q}")