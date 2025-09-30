import pytesseract
from PIL import Image
import fitz
import json
import easyocr


def extract_text_from_image(image_path: str) -> str:
    image = Image.open(image_path)
    
    try:
        # Try Tesseract first
        text = pytesseract.image_to_string(Image.open(image_path))
        if text.strip() == "":
            raise Exception("Empty OCR output")
        return text
    except Exception:
        # Fallback to EasyOCR
        reader = easyocr.Reader(['en'])
        result = reader.readtext(image_path)
        return " ".join([r[1] for r in result])
    
    return pytesseract.image_to_string(image)

def extract_text_from_pdf(pdf_path: str) -> str:
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text("text") + "\n"
    return text