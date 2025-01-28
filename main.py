import os
from utils.pdf_processing import extract_text_from_pdf
from utils.data_conversion import txt_to_json
from utils.file_generation import parse_json_to_csv, parse_json_to_txt

if __name__ == "__main__":
    pdf_path    = input("Digite o caminho completo do arquivo PDF: ")
    output_dir  = input("Digite o diretório para salvar o CSV: ")
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    arraytexto  = extract_text_from_pdf(pdf_path)
    texto       = arraytexto[1].replace("\n", " ")
    jsonretorno = txt_to_json(texto)
    
    opcao_saida = input("Digite 1 para CSV e 2 para TXT: ")
    while (opcao_saida!="1" and opcao_saida!="2"):
        opcao_saida = input("Digite 1 para CSV e 2 para TXT: ")
    if (opcao_saida=="1"):
        parse_json_to_csv(jsonretorno,arraytexto[0],output_dir)
    elif(opcao_saida=="2"):
        parse_json_to_txt(jsonretorno,arraytexto[0],output_dir)