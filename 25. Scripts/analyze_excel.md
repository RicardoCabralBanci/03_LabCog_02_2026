# Script de Análise de Excel (Diagnóstico)

**Arquivo**: `analyze_excel.py`
**Localização**: `25. Scripts/`
**Linguagem**: Python 3.x
**Dependências**: `pandas`, `openpyxl`

---

## 1. Objetivo
Este script foi desenvolvido para realizar uma "autópsia" em arquivos Excel complexos (`.xlsm`) usados como configuradores no sistema legado de geração de manuais. O objetivo é mapear a estrutura interna (abas, nomes de colunas, dados de configuração) sem depender da abertura manual do Excel.

## 2. Funcionalidades
*   **Listagem de Abas**: Identifica todas as planilhas visíveis e ocultas no arquivo.
*   **Amostragem de Dados**: Lê as primeiras 5 linhas de cada aba para fornecer um "cheiro" do conteúdo.
*   **Detecção de Padrões**: Tenta identificar automaticamente quais abas são de configuração (`Info`, `Dados Salvos`) e quais são de dados técnicos baseando-se em palavras-chave como "Projeto", "SapNr", "Dispositivos".

## 3. Como Usar
1.  Certifique-se de ter as dependências instaladas:
    ```bash
    pip install pandas openpyxl
    ```
2.  Edite a variável `file_path` no script para apontar para o arquivo Excel alvo.
3.  Execute via terminal:
    ```bash
    python 25. Scripts/analyze_excel.py
    ```

## 4. Estrutura do Código
*   `analyze_excel(path)`: Função principal que orquestra a leitura.
*   Usa `openpyxl` para obter a lista de abas (mais leve que carregar tudo no pandas de uma vez).
*   Usa `pandas.read_excel` para extrair os DataFrames de amostra.

---
*Este arquivo serve como documentação técnica para o artefato de migração.*
