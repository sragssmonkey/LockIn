import fitz  # PyMuPDF

import fitz  # PyMuPDF

def extract_text_from_pdf(file_obj):
    pdf_data = file_obj.read()

    # open PDF from bytes
    doc = fitz.open(stream=pdf_data, filetype="pdf")

    full_text = ""

    for page in doc:
        full_text += page.get_text()

    return full_text

import pytesseract
from django.conf import settings

pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_CMD
