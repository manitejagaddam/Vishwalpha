import re
import openai
import json
from openai import OpenAI
from models.pydantic import ExamAnalysis
import os
from dotenv import load_dotenv

from groq import Groq
import streamlit as st

load_dotenv()




# client = openai.OpenAI(api_key=os.getenv("OPENAI_KEY"))  # v1 style client

# api_key = os.getenv("OPENAI_KEY")
api_key = os.getenv("GROQ_KEY")
# api_key = st.secrets["GROQ_KEY"]
if not api_key:
    raise ValueError("GROQ not found!")

# Set API key globally
# openai.api_key = api_key

# client = OpenAI(api_key=api_key)
client = Groq(api_key=api_key)




def clean_llm_output(raw_output: str) -> str:
    # Remove ```json ... ``` code block markers
    cleaned = re.sub(r"^```json\s*|\s*```$", "", raw_output.strip(), flags=re.MULTILINE)
    # Extract the first valid JSON object
    match = re.search(r"\{.*\}", cleaned, flags=re.DOTALL)
    if match:
        return match.group()
    else:
        raise ValueError("No valid JSON found in LLM output")

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
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}]
    )

    llm_output = response.choices[0].message.content
    data = ""
    
    

    try:
        # print(llm_output)
        # return llm_output
        cleaned_output = clean_llm_output(llm_output)
        # print(cleaned_output)
    
        print("data is being loaded currently raw")
        data = json.loads(cleaned_output)
        # data = json.loads(llm_output)
        # print(data)
        print("data loaded sucessfully")
    
        # Convert JSON to match Pydantic fields
        questions = []
        for q in data["questions"]:
            questions.append({
                "id": None,
                "question_text": q.get("question", ""),
                "answer_text": q.get("answer", ""),
                "blooms_level": q.get("bloom_level", "Unknown"),
                "score": q.get("score", 0),
                "pros": q.get("pros", []),
                "cons": q.get("cons", []),
                "feedback": q.get("feedback", "")
            })

        # Transform overall analysis
        summary = data.get("summary", {})
        overall_analysis = {
            "strengths": summary.get("overall_strengths", []),
            "weaknesses": summary.get("overall_weaknesses", []),
            "final_feedback": summary.get("notes", "")
        }

        
        exam_analysis = ExamAnalysis(
            questions=questions,
            overall_analysis=overall_analysis
        )
        print("data analysis completed")
        return exam_analysis
    except Exception as e:
        print(data)
        print("Failed to parse LLM output   :", e)
        # print("Raw output:", llm_output)
        return None
