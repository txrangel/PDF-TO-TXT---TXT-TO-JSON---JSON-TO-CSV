import re
import json

def txt_to_json(texto):
    try:
        if "P E D I D O D E C O M P R A" in texto:
            return extrair_modelo_1(texto)
        elif "Pedido de Compra" in texto:
            return extrair_modelo_2(texto)
        return None
    except AttributeError:
        return None

def extrair_modelo_1(texto):
    texto = texto.replace("\n", " ")
    try:
        pedido_cliente = re.search(r"Numero: (\d+)", texto).group(1)
    except AttributeError:
        pedido_cliente = None
    try:
        cnpj = re.search(r"Local de Entrega: (\d+/\d+[-\d]+)", texto).group(1)
    except AttributeError:
        cnpj = None
    try:
        data_pedido = re.search(r"ATACADAO S\.A\.\s+(\d{2}/\d{2}/\d{2})", texto).group(1)
    except AttributeError:
        data_pedido = "0000000000"
    try:
        tipo_frete = re.search(r"Frete:\s+(\w+)", texto).group(1)
    except AttributeError:
        tipo_frete = None
    try:
        operacao = re.search(r"Pedido EDI\.\.\: \d+\s+\*\*\s+(\w+)\s+\*\*", texto).group(1)
    except AttributeError:
        operacao = None
    try:
        produtos_brutos = texto.split("+------------------------------------------------------+------------------------------------------------------------------------------------+ | M E R C A D O R I A Dt.Ent Qtde Unitario I.P.I. IcmSubs B.C.Subs Des.Com Des.Ad Vendor Frete Verba Outros Peso Kg CP| +-------------------------------------------------------------------------------------------------------------------------------------------+")[1:]
        resultado       = []
        regex_produto   = regex_produto = re.compile(r'(?P<descricao>[^|]+?)\s+(?P<data_entrega>\d{2}/\d{2})\s+(?P<quantidade>\d+)\s+(?P<valor>[\d,]+).*?\|\s+\|\s+(?P<cod_produto_cliente>\d+/\d+)\s+(?P<especificacoes>CXA [^ ]+)\s+(?P<cod_barras_produto>\d+)?')
        if produtos_brutos:
            for produto_bruto in produtos_brutos:
                produtos_brutos_completo = produto_bruto.split("+-------------------------------------------------------------------------------------------------------------------------------------------+ | TOTAIS -> ")[:-1]
                for produto_bruto_completo in produtos_brutos_completo:
                    produtos_linhas = produto_bruto_completo.split("Pr Final N | | | |")
                    if produtos_linhas:
                        for produto_linha in produtos_linhas:
                            match = regex_produto.search(produto_linha)
                            if match:
                                dados                   = match.groupdict()
                                descricao_produto       = dados.get("descricao", "")
                                especificacoes_produto  = dados.get("especificacoes", "")
                                item = {
                                    "cnpj":                     cnpj,
                                    "pedido_cliente":           pedido_cliente,
                                    "cod_produto_cliente":      dados.get("cod_produto_cliente", "").replace("/", ""),
                                    "codigo_barras":            dados.get("cod_barras_produto", "") or "00000000000000",
                                    "descricao_produto":        descricao_produto,
                                    "especificacoes_produto":   especificacoes_produto,
                                    "quantidade":               float(dados.get("quantidade", 0)),
                                    "valor":                    float(dados.get("valor", "0").replace(",", ".")),
                                    "informacao":               dados.get("informacao", ""),
                                    "data_pedido":              str(data_pedido if data_pedido else "0000000000"),
                                    "data_entrega":             str(dados.get("data_entrega", "0000000000")),
                                    "tipo_frete":               tipo_frete,
                                    "operacao":                 operacao,
                                }
                                resultado.append(item)  
            return resultado
        else:
            return []
    except AttributeError:
        return []

def extrair_modelo_2(texto):
    try:
        pedido_cliente = re.search(r"Pedido:(\d+)", texto).group(1)
    except AttributeError:
        pedido_cliente = None
    try:
        cnpj = re.search(r"Local de Entrega:\s+(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})", texto).group(1)
    except AttributeError:
        cnpj = None
    try:
        data_pedido = re.search(r"Dt Elab:(\d{2}/\d{2}/\d{4})", texto).group(1)
    except AttributeError:
        data_pedido = "0000000000"
    try:
        tipo_frete = re.search(r"Frete: (\w+)", texto).group(1)
    except AttributeError:
        tipo_frete = None
    try:
        operacao = re.search(r"Operação: (\w+)", texto).group(1)
    except AttributeError:
        operacao = None
    try:
        produtos_brutos = texto.split("SeqCódigo Descrição Embalagem Pr. F Dt Entr Qtde Vlr. Unit I.P.I. IcmSubs B.C. Subs Des.Com Des.Adi Vlr.Verba Inc Outros Peso Kg Plt")[1:]
        resultado       = []
        regex_produto   = re.compile(r'(?P<cod_produto_cliente>\d+-\d+)\s+(?P<descricao>[\w\s\.]+?)\s+(?P<especificacoes>CXA \d+ X \d+ \d+G)\s+(?P<pr_final>\w+)\s+(?P<data_entrega>\d{2}/\d{2}/\d{2})\s+(?P<quantidade>\d+)\s+(?P<valor>[\d,]+)')
        if produtos_brutos:
            for produto_bruto in produtos_brutos:
                produtos_brutos_completo = produto_bruto.split("TOTAIS:")[:-1]
                for produto_bruto_completo in produtos_brutos_completo:
                    produtos_linhas = produto_bruto_completo.split("\n")
                    if produtos_linhas:
                        for produto_linha in produtos_linhas:
                            match = regex_produto.search(produto_linha)
                            if match:
                                dados                   = match.groupdict()
                                descricao_produto       = dados.get("descricao", "").strip()
                                especificacoes_produto  = dados.get("especificacoes", "").strip()
                                item = {
                                    "cnpj":                     cnpj,
                                    "pedido_cliente":           pedido_cliente,
                                    "cod_produto_cliente":      dados.get("cod_produto_cliente", "").replace("-", ""),
                                    "codigo_barras":            "00000000000000",  # Não há código de barras no Modelo 2
                                    "descricao_produto":        descricao_produto,
                                    "especificacoes_produto":   especificacoes_produto,
                                    "quantidade":               float(dados.get("quantidade", 0)),
                                    "valor":                    float(dados.get("valor", "0").replace(",", ".")),
                                    "informacao":               dados.get("informacao", ""),
                                    "data_pedido":              str(data_pedido),
                                    "data_entrega":             str(dados.get("data_entrega", "0000000000")),
                                    "tipo_frete":               tipo_frete,
                                    "operacao":                 operacao,
                                }
                                resultado.append(item)  
            return resultado
        else:
            return []
    except Exception as e:
        return []

# Função para ajustar os campos no formato esperado
def ajustar_campos(item):
    try:
        data_pedido = ajuste_data(item["data_pedido"],"00000000")
        data = {
            "cnpj":                     item["cnpj"].replace("/", "").replace("-", "").replace(".", ""),
            "pedido_cliente":           item["pedido_cliente"],
            "cod_produto_cliente":      item["cod_produto_cliente"],
            "codigo_barras":            item["codigo_barras"],
            "descricao_produto":        item["descricao_produto"].ljust(35),
            "especificacoes_produto":   item["especificacoes_produto"].replace(" ", "").ljust(20),
            "quantidade":               f"{int(item['quantidade']):06d}",
            "valor":                    f"{int(item['valor'] * 100):010d}",
            "informacao":               item["informacao"],
            "data_pedido":              data_pedido,
            "data_entrega":             ajuste_data(item["data_entrega"],data_pedido),
            "tipo_frete":               item["tipo_frete"],
            "operacao":                 item["operacao"]
        }
        return data
    except AttributeError:
        return []
def ajuste_data(data,data_pedido):
    data = str(data).replace("/", "")  # Garante que é string e remove barras
    if not data.isdigit():  # Verifica se a string contém apenas números
        return "00000000"
    dia_mes = data[:4]
    ano_curto = data[4:]
    if len(ano_curto) == 2:
        ano_completo = "20" + ano_curto if int(ano_curto) <= 99 else "21" + ano_curto
    else:
        ano_completo = data_pedido[4:]
    if len(data) == 4:
        data_completa = data + ano_completo
    elif len(data) == 6:
        data_completa = dia_mes + ano_completo
    elif len(data) != 8:
        data_completa = "00000000"
    else:
        data_completa = data
    return data_completa

