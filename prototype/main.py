from models.pydantic import ExamAnalysis
from OCR.tesseract import extract_text_from_image
from OCR.tesseract import extract_text_from_pdf
from LLM.openai import analyze_with_llm

def analyze_exam(input_path: str, is_pdf=True) -> ExamAnalysis:
    if is_pdf:
        text = extract_text_from_pdf(input_path)
    else:
        text = extract_text_from_image(input_path)
    analysis = analyze_with_llm(text)
    return analysis


if __name__ == "__main__":
    input_file = "../SandBox/Images/pic1.jpg"
    result = analyze_exam(input_file, False)
    if result:
        print(result.json(indent = 2))