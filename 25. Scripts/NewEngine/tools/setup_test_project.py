import sqlite3
import os

DB_PATH = r"04. Arquivos e Projetos/Criação Automatica de Manuais/10. DB SQLite/manual_db.sqlite"

def setup_project():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    PROJECT_ID = 2
    
    print(f"--- Configurando Projeto ID {PROJECT_ID} para Teste ---")
    
    # 1. Limpar composição anterior
    cursor.execute("DELETE FROM project_composition WHERE project_id = ?", (PROJECT_ID,))
    print("Composição antiga limpa.")
    
    # 2. Selecionar ingredientes (Seções)
    # Vamos pegar: Capa, Sumário (Indice) e 3 arquivos normais (.docx)
    # O filtro LIKE garante que pegamos arquivos reais e não lixo
    queries = [
        ("CAPA", 1),
        ("SUMÁRIO", 2),
        ("S001", 3), # Algum capítulo técnico
        ("S001", 4), # Outro
        ("S001", 5)  # E mais um
    ]
    
    print("Inserindo novas seções...")
    for keyword, order in queries:
        # Pega o primeiro ID que bate com a keyword e que ainda não usamos (simplificação)
        cursor.execute(f"SELECT id, file_path_template FROM manual_sections WHERE file_path_template LIKE '%{keyword}%' AND file_path_template LIKE '%.docx' LIMIT 1 OFFSET {order-1}")
        row = cursor.fetchone()
        
        if row:
            sec_id = row[0]
            path = row[1]
            print(f" [Add] Ordem {order}: {os.path.basename(path)} (ID: {sec_id})")
            
            cursor.execute("""
                INSERT INTO project_composition (project_id, section_id, is_active, custom_order)
                VALUES (?, ?, 1, ?)
            """, (PROJECT_ID, sec_id, order))
        else:
            print(f" [Aviso] Não encontrei seção para keyword '{keyword}' no offset {order}")

    conn.commit()
    conn.close()
    print("--- Projeto Configurado com Sucesso ---")

if __name__ == "__main__":
    setup_project()
