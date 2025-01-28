import os
import csv
import json
from datetime import datetime
from .data_conversion import ajustar_campos

#Converte de JSON para CSV e Grava o Arquivo
def parse_json_to_csv(saida_json, base_name, output_dir):
    try:
        dados_processados = [ajustar_campos(item) for item in json.loads(saida_json)]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_filename = os.path.join(output_dir, f"{base_name}_{timestamp}.csv")
        with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=dados_processados[0].keys(), delimiter=';')
            for row in dados_processados:
                writer.writerow(row)
        print(f"CSV gerado com sucesso: {csv_filename}")
    except Exception as e:
        print(f"Erro ao processar os dados: {e}")

#Converte de JSON para TXT e Grava o Arquivo
def parse_json_to_txt(saida_json, base_name, output_dir):
    try:
        dados_processados = [ajustar_campos(item) for item in json.loads(saida_json)]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        txt_filename = os.path.join(output_dir, f"{base_name}_{timestamp}.txt")
        with open(txt_filename, "w", encoding="utf-8") as txtfile:
            for row in dados_processados:
                linha = ";".join(str(value) for value in row.values())
                txtfile.write(linha + "\n")  
        print(f"TXT gerado com sucesso: {txt_filename}")
    except Exception as e:
        print(f"Erro ao processar os dados: {e}")