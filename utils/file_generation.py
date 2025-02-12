import os
import csv
import json
from datetime import datetime
from .data_conversion import ajustar_campos

#Converte de JSON para CSV e Grava o Arquivo
def parse_json_to_csv(json_data, base_name, output_dir):
    try:
        if isinstance(json_data, str):
            json_data = json.loads(json_data)
        if isinstance(json_data, list) and len(json_data) == 1 and isinstance(json_data[0], str):
            json_data = json.loads(json_data[0])
        print(f"Total de itens no JSON: {len(json_data)}")  # Depuração
        dados_processados = [ajustar_campos(item) for item in json_data]
        # Gera o nome do arquivo CSV com timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_filename = os.path.join(output_dir, f"{base_name}_{timestamp}.csv")
        # Escreve os dados no arquivo CSV
        with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=dados_processados[0].keys(), delimiter=';')
            writer.writeheader()  # Escreve o cabeçalho
            for row in dados_processados:
                writer.writerow(row)
        print(f"CSV gerado com sucesso: {csv_filename}")
    except Exception as e:
        print(f"Erro ao processar os dados: {e}")
        
#Converte de JSON para TXT e Grava o Arquivo
def parse_json_to_txt(json_data, base_name, output_dir):
    try:
        if isinstance(json_data, list) and len(json_data) == 1:
            json_data = json_data[0]
        if isinstance(json_data, str):
            json_data = json.loads(json_data)
        for json in json_data:
            # print(f"Total de itens no JSON: {len(json)}")  # Depuração
            dados_processados = [ajustar_campos(item) for item in json]
            # Gera o nome do arquivo TXT com timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            txt_filename = os.path.join(output_dir, f"{base_name}_{timestamp}.txt")
            # Escreve os dados no arquivo TXT
            with open(txt_filename, "w", encoding="utf-8") as txtfile:
                # Escreve o cabeçalho
                cabecalho = ";".join(dados_processados[0].keys())
                txtfile.write(cabecalho + "\n")
                # Escreve as linhas de dados
                for row in dados_processados:
                    linha = ";".join(str(value) for value in row.values())
                    txtfile.write(linha + "\n")
            print(f"TXT gerado com sucesso: {txt_filename}")
    except Exception as e:
        print(f"Erro ao processar os dados: {e}")