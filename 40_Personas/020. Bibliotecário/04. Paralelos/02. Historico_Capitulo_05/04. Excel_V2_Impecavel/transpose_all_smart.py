import pandas as pd
import sys
import os
import openpyxl

def transpose_all(file_path):
    print(f"--- 🔄 Iniciando Transposição Global em: {os.path.basename(file_path)} ---")
    
    try:
        # Carregar o arquivo Excel
        xls = pd.ExcelFile(file_path, engine='openpyxl')
        sheet_names = xls.sheet_names
        print(f"Abas encontradas: {sheet_names}")
        
        with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            for sheet in sheet_names:
                print(f"\n>> Analisando aba: '{sheet}'...")
                
                # Ler a aba
                df = pd.read_excel(xls, sheet_name=sheet)
                
                # Verificar se está vazia
                if df.empty:
                    print("   ⚠️ Aba vazia. Pulando.")
                    continue

                # Verificar a primeira coluna para decidir se transpõe
                first_col = df.columns[0]
                
                if first_col == "Manual_Maquina":
                    print("   ✅ Já está transposta (Eixo Y = Máquinas). Mantendo como está.")
                    # Reescrevemos ela para garantir que nada se perca, ou simplesmente não fazemos nada.
                    # Como o mode='a' com replace substitui se escrevermos, se não escrevermos ele mantém.
                    continue
                
                print(f"   🔄 Transpondo (Eixo Y era '{first_col}')...")
                
                try:
                    # Preparar para transposição
                    df.set_index(first_col, inplace=True)
                    
                    # Transpor
                    df_transposed = df.T
                    
                    # Ajustar índices
                    df_transposed.index.name = "Manual_Maquina"
                    df_transposed.reset_index(inplace=True)
                    
                    # Salvar
                    df_transposed.to_excel(writer, sheet_name=sheet, index=False)
                    print(f"   ✨ Sucesso! Nova estrutura: {df_transposed.shape[0]} linhas x {df_transposed.shape[1]} colunas")
                    
                except Exception as e:
                    print(f"   ❌ Erro ao transpor aba '{sheet}': {e}")
                    
        print("\n🏁 Processo Global Finalizado!")
        
    except Exception as e:
        print(f"❌ Erro Crítico ao abrir arquivo: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python transpose_all_smart.py <caminho_excel>")
    else:
        transpose_all(sys.argv[1])
