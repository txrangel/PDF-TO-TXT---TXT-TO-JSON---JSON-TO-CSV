import re
import json
import csv
import os
import pdfplumber
from datetime import datetime

#Remove caracteres de controle e formata o texto.
def clean_text(text):
    text = re.sub(r'\x1b\[.*?m|\033&.*?T', '', text)  # Remove caracteres de controle
    text = re.sub(r'\s+', ' ', text)  # Remove múltiplos espaços
    return text.strip()

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
        
def txt_to_json(texto):
    try:
        pedido_cliente = re.search(r"Pedido EDI\.\.\: (\d+)", texto).group(1)
    except AttributeError:
        pedido_cliente = None
    try:
        cnpj = re.search(r"Local de Entrega: (\d+/\d+[-\d]+)", texto).group(1)
    except AttributeError:
        cnpj = None
    try:
        nao_mapeado = re.search(r"ATACADAO S\.A\.\s+(\d{2}/\d{2}/\d{2})", texto).group(1)
    except AttributeError:
        nao_mapeado = None
    try:
        tipo_frete = re.search(r"Frete:\s+(\w+)", texto).group(1)
    except AttributeError:
        tipo_frete = None
    try:
        operacao = re.search(r"Pedido EDI\.\.\: \d+\s+\*\*\s+(\w+)\s+\*\*", texto).group(1)
    except AttributeError:
        operacao = None
    try:
        produtos_brutos = texto.split("+-------------------------------------------------------------------------------------------------------------------------------------------+")[1:]
        if len(produtos_brutos)>=1:
            produtos_brutos = produtos_brutos[1].split("Pr Final N | | | |")[:-1]
        else:
            produtos_brutos = ['']
        regex_produto = re.compile(
            r'(?P<descricao>[^|]+?)\s+\d{2}/\d{2}\s+(?P<quantidade>\d+)\s+(?P<valor>[\d,]+).*?\|\s+\|\s+(?P<informacao>\d+/\d+)\s+(?P<especificacoes>CXA [^ ]+)\s+(?P<cod_produto_cliente>\d+)?'
        )
        resultado = []
        for produto in produtos_brutos:
            match = regex_produto.search(produto)
            if match:
                dados = match.groupdict()
                item = {
                    "cnpj": cnpj,
                    "pedido_cliente": pedido_cliente,
                    "cod_produto_cliente": dados.get("cod_produto_cliente", "") or "",
                    "codigo_barras": "00000000000000",
                    "descricao_produto": dados.get("descricao", "").strip(),
                    "especificacoes_produto": dados.get("especificacoes", ""),
                    "quantidade": float(dados.get("quantidade", 0)),
                    "valor": float(dados.get("valor", "0").replace(",", ".")),
                    "informacao": dados.get("informacao", ""),
                    "data_entrega": "0000000000",
                    "nao_mapeado": nao_mapeado,
                    "tipo_frete": tipo_frete,
                    "operacao": operacao,
                }
                resultado.append(item)
        return json.dumps(resultado, indent=2, ensure_ascii=False)
    except AttributeError:
        return json.dumps([], indent=2, ensure_ascii=False)

# Função para ajustar os campos no formato esperado
def ajustar_campos(item):
    return {
        "cnpj": item["cnpj"].replace("/", "").replace("-", ""),
        "pedido cliente": item["pedido_cliente"],
        "cod produto cliente": item["cod_produto_cliente"],
        "codigo de barras": item["codigo_barras"],
        "descrição do produto": item["descricao_produto"].ljust(35),
        "especificações do produto": item["especificacoes_produto"].ljust(20),
        "quantidade": f"{int(item['quantidade']):06d}",
        "valor": f"{int(item['valor'] * 100):010d}",
        "": "",  # Coluna vazia
        "data de entrega": item["data_entrega"],
        "não mapeado": item["nao_mapeado"].replace("/", ""),
        "tipo de frete": item["tipo_frete"],
        "operacao": item["operacao"]
    }

def parse_json_to_csv(saida_json, base_name,output_dir):
    try:
        dados_processados = [ajustar_campos(item) for item in json.loads(saida_json)]
        header = [
            "cnpj", "pedido cliente", "cod produto cliente", "codigo de barras", "descrição do produto",
            "especificações do produto", "quantidade", "valor", "", "data de entrega", "não mapeado",
            "tipo de frete", "operacao"
        ]
        timestamp       = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_filename    = os.path.join(output_dir, f"{base_name}_{timestamp}.csv")
        with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=header, delimiter=';')
            writer.writeheader()
            writer.writerows(dados_processados)
        print(f"CSV gerado com sucesso: {csv_filename}")
    except Exception as e:
        print(f"Erro ao processar os dados: {e}")
    
if __name__ == "__main__":
    pdf_path = input("Digite o caminho completo do arquivo PDF: ")
    output_dir = input("Digite o diretório para salvar o CSV: ")
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    arraytexto  = extract_text_from_pdf(pdf_path)
    texto       = arraytexto[1].replace("\n", " ")
    jsonretorno = txt_to_json(texto)
    parse_json_to_csv(jsonretorno,arraytexto[0],output_dir)