import pandas as pd
import sys
import os

def transpose_sheet(file_path, sheet_name):
    print(f"--- Iniciando Transposição da aba '{sheet_name}' em: {os.path.basename(file_path)} ---")
    
    try:
        # 1. Ler a aba original
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        print(f"Dados originais carregados: {df.shape[0]} linhas x {df.shape[1]} colunas")
        
        # 2. Preparar para transposição
        # Assumindo que a primeira coluna (index 0) contém os rótulos que virarão cabeçalhos (ex: 'Componente')
        first_col_name = df.columns[0]
        df.set_index(first_col_name, inplace=True)
        
        # 3. Transpor
        df_transposed = df.T
        
        # 4. Ajustar índices
        # O index antigo (nomes das máquinas) vira uma coluna
        df_transposed.index.name = "Manual_Maquina"
        df_transposed.reset_index(inplace=True)
        
        print(f"Dados transpostos: {df_transposed.shape[0]} linhas x {df_transposed.shape[1]} colunas")
        
        # 5. Salvar de volta (Substituindo a aba antiga)
        # Usamos mode='a' (append) com replace para substituir apenas a aba específica se possível, 
        # mas o pandas replace em append às vezes cria Sheet1. O ideal é carregar tudo e salvar.
        # Para segurança, vamos usar openpyxl engine.
        
        with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            df_transposed.to_excel(writer, sheet_name=sheet_name, index=False)
            
        print("✅ Transposição salva com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro Crítico: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python transpose_sheet.py <caminho_excel> <nome_aba>")
    else:
        transpose_sheet(sys.argv[1], sys.argv[2])
