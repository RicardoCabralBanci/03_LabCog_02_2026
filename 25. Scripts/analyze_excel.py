import pandas as pd
import openpyxl
import os
import sys

# Caminho padrão (fallback)
default_path = r"04. Arquivos e Projetos\Criação Automatica de Manuais\02. Recursos_Legados\Config_BA\Gerador_V04\Gerador_V4  - Atualizado.xlsm"

def analyze_excel(path):
    if not os.path.exists(path):
        print(f"Erro: Arquivo não encontrado: {path}")
        return

    print(f"--- Analisando: {os.path.basename(path)} ---")
    
    try:
        # Carregar a workbook para ver nomes das abas (Sheet Names)
        wb = openpyxl.load_workbook(path, data_only=True)
        sheet_names = wb.sheetnames
        print(f"Abas encontradas ({len(sheet_names)}): {sheet_names}")
        
        for sheet in sheet_names:
            print(f"\n[Aba: {sheet}]")
            try:
                # Ler apenas o cabeçalho e primeiras linhas
                df = pd.read_excel(path, sheet_name=sheet, nrows=10)
                print(f"Conteúdo (Top 10 linhas, {len(df.columns)} colunas):")
                print(df.to_string())
                
            except Exception as e:
                print(f"Erro ao ler aba {sheet}: {e}")
                
    except Exception as e:
        print(f"Erro fatal ao abrir arquivo Excel: {e}")

if __name__ == "__main__":
    # Se um argumento foi passado, usa ele. Se não, usa o padrão.
    file_to_analyze = sys.argv[1] if len(sys.argv) > 1 else default_path
    analyze_excel(file_to_analyze)
