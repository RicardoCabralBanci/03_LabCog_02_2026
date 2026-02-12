import pandas as pd
import sys
import os

def refactor_safety_sheet(file_path):
    sheet_name = "Avisos de segurança"
    print(f"--- ♻️ Reconstruindo Aba '{sheet_name}' em: {os.path.basename(file_path)} ---")
    
    try:
        # Carregar o arquivo Excel
        # Usamos engine='openpyxl' para garantir compatibilidade
        with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
            # Não conseguimos deletar colunas facilmente com overlay, então vamos ler tudo, modificar e substituir.
            pass
        
        # Leitura completa para memória
        xls = pd.ExcelFile(file_path, engine='openpyxl')
        all_sheets = pd.read_excel(xls, sheet_name=None)
        
        if sheet_name not in all_sheets:
            print(f"❌ Erro: Aba '{sheet_name}' não encontrada!")
            return

        df_old = all_sheets[sheet_name]
        print(f"Estrutura Antiga: {df_old.columns.tolist()}")
        
        # Criar novo DataFrame apenas com a coluna de Máquinas
        # Assumindo que a primeira coluna é 'Manual_Maquina' (já transposta)
        first_col = df_old.columns[0]
        machines = df_old[first_col]
        
        df_new = pd.DataFrame()
        df_new[first_col] = machines
        
        # Adicionar a nova coluna "Título da Seção"
        # Preencher com valores placeholder baseados no idioma provável, para ajudar
        titulos = []
        for maquina in machines:
            if "(PT)" in str(maquina):
                titulos.append("5.1 Instruções de segurança (A Validar)")
            else:
                titulos.append("5.1 Safety instructions (To Validate)")
        
        df_new["Título da Seção"] = titulos
        
        print(f"Nova Estrutura: {df_new.columns.tolist()}")
        print(df_new)
        
        # Atualizar o dicionário de abas
        all_sheets[sheet_name] = df_new
        
        # Salvar TUDO de volta (é o jeito mais seguro de substituir uma aba completamente sem deixar lixo)
        with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
            for nome_aba, df_aba in all_sheets.items():
                df_aba.to_excel(writer, sheet_name=nome_aba, index=False)
                
        print("✅ Reconstrução salva com sucesso!")

    except Exception as e:
        print(f"❌ Erro Crítico: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python refactor_safety_sheet.py <caminho_excel>")
    else:
        refactor_safety_sheet(sys.argv[1])
