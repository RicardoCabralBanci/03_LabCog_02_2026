import pandas as pd
import sys
import os

def update_titles(file_path):
    sheet_name = "Avisos de segurança"
    print(f"--- 🖋️ Atualizando Títulos em: {os.path.basename(file_path)} ---")
    
    try:
        # Carregar todas as abas para não perder dados das outras
        xls = pd.ExcelFile(file_path, engine='openpyxl')
        all_sheets = pd.read_excel(xls, sheet_name=None)
        
        if sheet_name not in all_sheets:
            print(f"❌ Erro: Aba '{sheet_name}' não encontrada!")
            return

        df = all_sheets[sheet_name]
        
        # Mapeamento de Títulos Reais
        # Chave: Nome da Máquina no Excel, Valor: Título Real no Word
        mapping = {
            "ShrinkPacker (PT)": "Avisos de segurança",
            "TrayPacker (EN)": "Safety instructions",
            "Wraparound (EN)": "Safety instructions",
            "NatureMulti (EN)": "Safety instructions",
            "Packer_EN (EN)": "Safety instructions"
        }
        
        # Aplicar o mapeamento
        def get_real_title(row):
            machine = row["Manual_Maquina"]
            return mapping.get(machine, "Safety instructions") # Default if not found

        df["Título da Seção"] = df.apply(get_real_title, axis=1)
        
        print("Novos valores aplicados:")
        print(df[["Manual_Maquina", "Título da Seção"]])
        
        # Atualizar o dicionário
        all_sheets[sheet_name] = df
        
        # Salvar de volta
        with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
            for nome_aba, df_aba in all_sheets.items():
                df_aba.to_excel(writer, sheet_name=nome_aba, index=False)
                
        print("✅ Títulos atualizados com sucesso!")

    except Exception as e:
        print(f"❌ Erro Crítico: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python update_safety_titles.py <caminho_excel>")
    else:
        update_titles(sys.argv[1])
