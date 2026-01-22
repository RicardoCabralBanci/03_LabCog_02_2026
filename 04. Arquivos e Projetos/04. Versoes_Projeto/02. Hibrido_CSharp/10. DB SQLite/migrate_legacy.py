import pandas as pd
import sqlite3
import os
import re

# Caminho Absoluto fornecido pelo usuário
DB_PATH = "manual_db.sqlite"
EXCEL_PATH = r"C:\LabCogKHS_CLI\04. Arquivos e Projetos\Criação Automatica de Manuais\02. Recursos_Legados\Config_BA\Gerador_V04\Gerador_V4  - Atualizado.xlsm"

def connect_db():
    return sqlite3.connect(DB_PATH)

def migrate_structure(conn):
    print("--- Iniciando Migracao da Estrutura do Manual ---")
    
    if not os.path.exists(EXCEL_PATH):
        print(f"Erro: Arquivo Excel nao encontrado em {EXCEL_PATH}")
        return

    try:
        # Lendo a aba 'Base de Dados' (Onde a lista real de arquivos reside)
        print("DEBUG: Lendo aba 'Base de Dados'...")
        df = pd.read_excel(EXCEL_PATH, sheet_name="Base de Dados", header=None)
        
        # O cabeçalho do projeto (SAP, etc) ainda pode estar em 'Dados Salvos'.
        # Para simplificar, vamos focar em extrair o catalogo de arquivos primeiro.
        # Se precisarmos do SAP, podemos ler a outra aba depois.
        
        # Vamos assumir um projeto placeholder se não lermos 'Dados Salvos'
        project_name = "Projeto Migrado"
        sap_nr = "MIG_001"
        revision = "00"
        
        # (Metadados removidos pois estamos na aba de catalogo)
        print(f"Usando Projeto Placeholder: {project_name} | SAP: {sap_nr}")
        
        cursor = conn.cursor()
        
        # Inserir Projeto
        try:
            cursor.execute("""
                INSERT INTO projects (sap_number, project_name, revision, machine_type)
                VALUES (?, ?, ?, ?)
            """, (sap_nr, project_name, revision, "DVD")) 
            project_id = cursor.lastrowid
            print(f"Projeto inserido com ID: {project_id}")
        except sqlite3.IntegrityError:
            print("Projeto ja existe. Buscando ID...")
            cursor.execute("SELECT id FROM projects WHERE sap_number = ?", (sap_nr,))
            res = cursor.fetchone()
            if res: project_id = res[0]
            else: 
                # Caso extremo de erro de integridade mas nao achou (ex: UNIQUE constraint em outro campo?)
                print("Erro critico: Nao consegui recuperar ID do projeto.")
                return

        # 2. Extrair Lista de Arquivos
        count_sections = 0
        print("DEBUG: Analisando linhas em busca de .docx...")
        
        for index, row in df.iterrows():
            if index < 4: continue 
            
            row_str = [str(x) for x in row.values]
            
            # Debug das primeiras linhas para entender a estrutura
            if index < 20:
                # Imprimir pares (indice, valor) para colunas nao nulas
                debug_row = [(i, x) for i, x in enumerate(row_str) if x != 'nan' and str(x).strip() != '']
                if debug_row: 
                    print(f"Row {index}: {debug_row}")

            file_path = None
            control_flag = "No" 
            section_name = "Secao Sem Nome"
            
            # Tentar achar o path
            for col_idx, cell_val in enumerate(row_str):
                # Procura frouxa por .doc
                if ".doc" in cell_val: 
                    file_path = cell_val.strip()
                    
                    # Tentar achar Yes/No na linha inteira
                    if any(x.strip() == "Yes" for x in row_str): control_flag = "Yes"
                    
                    # Tentar pegar um nome descritivo (geralmente colunas A ou B, indices 0 ou 1)
                    # Se a coluna 0 tiver texto valido, usa ela
                    potential_name = str(row_str[0]).strip()
                    if potential_name and potential_name != 'nan':
                        section_name = potential_name
                    else:
                        section_name = os.path.basename(file_path)
                    
                    break
            
            if file_path:
                # Inserir no Catalogo
                cursor.execute("SELECT id FROM manual_sections WHERE file_path_template = ?", (file_path,))
                res = cursor.fetchone()
                
                if res:
                    section_id = res[0]
                else:
                    cursor.execute("""
                        INSERT INTO manual_sections (machine_type, section_name, file_path_template, default_order)
                        VALUES (?, ?, ?, ?)
                    """, ("GLOBAL", section_name, file_path, index))
                    section_id = cursor.lastrowid
                
                # Inserir na Composição (Evitar duplicatas para o mesmo projeto)
                cursor.execute("""
                    SELECT id FROM project_composition WHERE project_id=? AND section_id=?
                """, (project_id, section_id))
                
                if not cursor.fetchone():
                    is_active = 1 if control_flag == "Yes" else 0
                    cursor.execute("""
                        INSERT INTO project_composition (project_id, section_id, is_active, custom_order)
                        VALUES (?, ?, ?, ?)
                    """, (project_id, section_id, is_active, index))
                    count_sections += 1

        conn.commit()
        print(f"Migracao concluida. {count_sections} secoes processadas.")

    except Exception as e:
        print(f"Erro durante migracao: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    conn = connect_db()
    migrate_structure(conn)
    conn.close()