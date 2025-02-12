import re

#Remove caracteres de controle e formata o texto.
def clean_text(text):
    text = re.sub(r'\x1b\[.*?m|\033&.*?T', '', text)  # Remove caracteres de controle
    # text = re.sub(r'\s+', ' ', text)  # Remove múltiplos espaços
    return text.strip()
