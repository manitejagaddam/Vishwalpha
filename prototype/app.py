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
            # print(type(cleaned_output))
            st.success("Analysis Complete  ! ")
            # st.text_area("LLM Output", value=raw_output, height=400)
            
            for idx, q in enumerate(raw_output.questions, start=1):
                st.subheader(f"Question {idx}")
                st.markdown(f"**Question:** {q.question_text}")
                st.markdown(f"**Answer:** {q.answer_text or 'No answer provided'}")
                st.markdown(f"**Bloom's Taxonomy:** {q.blooms_level}")
                st.markdown(f"**Score:** {q.score}")

                if q.pros:
                    st.markdown("**Pros:**")
                    for pro in q.pros:
                        st.markdown(f"- {pro}")

                if q.cons:
                    st.markdown("**Cons:**")
                    for con in q.cons:
                        st.markdown(f"- {con}")

                if q.feedback:
                    st.markdown(f"**Feedback:** {q.feedback}")

                st.markdown("---")

            # Overall strengths and weaknesses
            st.subheader("Overall Strengths")
            for s in raw_output.overall_analysis.strengths:
                st.markdown(f"- {s}" if s else "No strengths identified.")

            st.subheader("Overall Weaknesses")
            for w in raw_output.overall_analysis.weaknesses:
                st.markdown(f"- {w}" if w else "No weaknesses identified.")
        except Exception as e:
            st.error(f"Error analyzing the exam: {e}")