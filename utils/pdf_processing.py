import os
import pdfplumber
from .text_processing import clean_text

# Extrai texto estruturado de um arquivo PDF e retorna um array com base_name e um array com os textos das páginas.
def extract_text_from_pdf(pdf_path):
    try:
        retorno = []
        if not os.path.exists(pdf_path):
            print(f"O arquivo {pdf_path} não foi encontrado.")
            return retorno
        with pdfplumber.open(pdf_path) as pdf:
            pages_text = []
            for page in pdf.pages:
                pages_text.append(clean_text(page.extract_text() or ""))
        retorno.append(os.path.basename(pdf_path).replace(".pdf", ""))
        retorno.append(pages_text)
        return retorno
    except Exception as e:
        print(f"Erro ao processar o PDF: {e}")
        return retorno
