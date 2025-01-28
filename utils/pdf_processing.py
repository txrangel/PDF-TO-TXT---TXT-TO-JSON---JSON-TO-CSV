import os
import pdfplumber
from .text_processing import clean_text

# Extrai texto estruturado de um arquivo PDF e retorna um array com base_name e texto.
def extract_text_from_pdf(pdf_path):
    if not os.path.exists(pdf_path):
        print(f"O arquivo {pdf_path} não foi encontrado.")
        return []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = clean_text(page.extract_text() or "")
                text += page_text + "\n\n"
        base_name = os.path.basename(pdf_path).replace(".pdf", "")
        return [base_name, text]
    except Exception as e:
        print(f"Erro ao processar o PDF: {e}")
        return []
