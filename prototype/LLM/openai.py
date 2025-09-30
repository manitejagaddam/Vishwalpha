import openai
import json
from models.pydantic import ExamAnalysis
import os
from dotenv import load_dotenv

load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_KEY"))  # v1 style client

def analyze_with_llm(extracted_text: str) -> ExamAnalysis:
    prompt = f"""
You are an AI exam analyzer.

Given the extracted exam content below (questions + student answers):

{extracted_text}

Tasks:
1. Identify each question and its answer.
2. Assign Bloom's taxonomy level for each question.
3. Score each answer (0–5).
4. Give pros, cons, and feedback for each answer.
5. Summarize overall strengths and weaknesses.

Return JSON output only. We'll validate and parse it in Python.
"""

    response = client.chat.completions.create(
        model="oai-oss-20b",
        messages=[{"role": "user", "content": prompt}]
    )

    llm_output = response.choices[0].message.content

    try:
        data = json.loads(llm_output)
        analysis = ExamAnalysis(**data)
        return analysis
    except Exception as e:
        print("Failed to parse LLM output:", e)
        print("Raw output:", llm_output)
        return None
