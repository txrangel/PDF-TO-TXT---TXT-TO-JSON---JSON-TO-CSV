import os
from utils.pdf_processing import extract_text_from_pdf
from utils.data_conversion import txt_to_json
from utils.file_generation import parse_json_to_csv, parse_json_to_txt

if __name__ == "__main__":
    pdf_path    = input("Digite o caminho completo do arquivo PDF: ")
    output_dir  = input("Digite o diretório para salvar o arquivo: ")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    arraytexto  = extract_text_from_pdf(pdf_path)
    if arraytexto:
        base_name   = arraytexto[0]
        opcao_saida = input("Digite 1 para CSV e 2 para TXT: ")
        while (opcao_saida!="1" and opcao_saida!="2"):
            opcao_saida = input("Digite 1 para CSV e 2 para TXT: ")
        jsons_gerados = []
        for texto_pagina in arraytexto[1]:
            json_retorno = txt_to_json(texto_pagina)
            if json_retorno:
                jsons_gerados.append(json_retorno)
        if (opcao_saida=="1"):
            parse_json_to_csv(jsons_gerados,base_name,output_dir)
        elif(opcao_saida=="2"):
            parse_json_to_txt(jsons_gerados,base_name,output_dir)