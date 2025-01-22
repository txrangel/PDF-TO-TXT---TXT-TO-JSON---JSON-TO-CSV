# Conversor de PDF para CSV

Este repositório contém um script em Python que processa arquivos PDF de pedidos de compra, extrai informações estruturadas e gera um arquivo CSV formatado com os dados extraídos.

## Funcionalidades

1. **Extração de texto do PDF**: O script utiliza a biblioteca `pdfplumber` para extrair o conteúdo textual do PDF.
2. **Conversão para JSON**: O texto extraído é processado para identificar campos como CNPJ, pedido, produtos e outras informações relevantes.
3. **Geração de CSV**: Os dados estruturados são formatados e exportados para um arquivo CSV com delimitador `;`.

## Tecnologias Utilizadas

- Python 3.8+
- Bibliotecas:
  - `pdfplumber`
  - `re` (expressões regulares)
  - `json`
  - `csv`
  - `os`
  - `datetime`

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/txrangel/PDF-TO-TXT---TXT-TO-JSON---JSON-TO-CSV.git
   cd PDF-TO-TXT---TXT-TO-JSON---JSON-TO-CSV
   ```

2. Crie um ambiente virtual (opcional, mas recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate   # Windows
   ```

3. Instale as dependências:
   ```bash
   pip install pdfplumber
   ```

## Como Usar

1. Execute o script principal:
   ```bash
   python extract_data.py
   ```

2. Insira o caminho completo do arquivo PDF e o diretório onde deseja salvar o CSV:
   ```plaintext
   Digite o caminho completo do arquivo PDF: D:\txt import\spc26-ped.16343.pdf
   Digite o diretório para salvar o CSV: D:\txt import
   ```

3. O script irá:
   - Extrair o texto do PDF.
   - Converter os dados para JSON.
   - Gerar um arquivo CSV no formato desejado.

4. Verifique a saída no diretório especificado. O arquivo CSV terá o nome baseado no arquivo PDF original e a data/hora de execução:
   ```plaintext
   spc26-ped.16343_20250122_123456.csv
   ```

## Estrutura do CSV

O arquivo CSV gerado terá as seguintes colunas:

- `cnpj`
- `pedido cliente`
- `cod produto cliente`
- `codigo de barras`
- `descrição do produto`
- `especificações do produto`
- `quantidade`
- `valor`
- Coluna vazia (`;` reservado)
- `data de entrega`
- `não mapeado`
- `tipo de frete`
- `operacao`

## Exemplo de Saída

```csv
cnpj;pedido cliente;cod produto cliente;codigo de barras;descrição do produto;especificações do produto;quantidade;valor;;data de entrega;não mapeado;tipo de frete;operacao
75315333009408;145924;61607186;00000000000000;GRANOLA VILLAMAR LIGHT;CXA 0001X0012X1KG;000028;0000021758;;12122024;0000000000;CIF;COMPRA
75315333034194;145925;61608145;00000000000000;GRANOLA VILLAMAR TRADICIONAL;CXA 0001X0012X1KG;000084;0000021758;;12122024;0000000000;CIF;COMPRA
```

## Personalização

- Ajuste os campos fixos, como `pedido cliente`, `valor` e `data de entrega`, conforme necessário.
- Modifique as expressões regulares na função `txt_to_json` para adaptar a estrutura do PDF a outros formatos.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir um pull request ou relatar problemas na seção de issues.
