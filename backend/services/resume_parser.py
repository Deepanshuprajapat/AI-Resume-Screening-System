import os
from pdfminer.high_level import extract_text

def parse_resume_from_pdf(pdf_path):
    """
    Extract text from a PDF resume and return the raw text,
    along with any specific extracted skills.
    """
    try:
        text = extract_text(pdf_path)
        # We will add NLTK/Spacy skill extraction logic later
        skills = "Python, React, Machine Learning" # Dummy implementation
        return text.strip(), skills
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
        return "", ""
