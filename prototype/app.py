import re
import streamlit as st
from models.pydantic import ExamAnalysis
from OCR.tesseract import extract_text_from_image, extract_text_from_pdf
from LLM.openai_client import analyze_with_llm

def analyze_exam(input_path: str, is_pdf=True) -> ExamAnalysis:
    if is_pdf:
        text = extract_text_from_pdf(input_path)
    else:
        text = extract_text_from_image(input_path)
    analysis = analyze_with_llm(text)
    return analysis


def clean_llm_output(raw_output: str) -> str:
    # Remove ```json ... ``` code block markers if present
    cleaned = re.sub(r"^```json\s*|\s*```$", "", raw_output.strip(), flags=re.MULTILINE)
    return cleaned


# --- Streamlit UI ---
st.title("Exam Paper Analyzer")

# File uploader (supports PDF and images)
uploaded_file = st.file_uploader("Upload an exam paper (PDF or Image)", type=["pdf", "jpg", "jpeg", "png"])


if uploaded_file is not None:
    is_pdf = uploaded_file.type == "application/pdf"
    temp_path = f"temp_uploaded_file.{uploaded_file.name.split('.')[-1]}"
    
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    with st.spinner("Analyzing exam paper..."):
        try:
            raw_output = analyze_exam(temp_path, is_pdf)
            # cleaned_output = clean_llm_output(raw_output)
            st.success("Analysis Complete  !")
            st.text_area("LLM Output", value=raw_output, height=400)
        except Exception as e:
            st.error(f"Error analyzing the exam: {e}")