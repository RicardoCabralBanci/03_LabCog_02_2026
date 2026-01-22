import sqlite3
import os

# Configuração
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "manual_db.sqlite")

# Onde os arquivos moram REALMENTE (Caminho relativo a partir da raiz do projeto)
# Como este script está em "10. DB SQLite", a raiz do projeto está 3 níveis acima
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", ".."))
TARGET_REL_PATH = "04. Arquivos e Projetos/Criação Automatica de Manuais/02. Recursos_Legados/Config_BA"

def sanitize():
    if not os.path.exists(DB_PATH):
        print(f"ERRO: Banco não encontrado em {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("--- INICIANDO SANITIZAÇÃO PARA CAMINHOS RELATIVOS ---")
    
    # Buscar todos os caminhos para processar (agora pega tudo que tem Config_BA, mesmo se já foi alterado)
    cursor.execute("SELECT id, file_path_template FROM manual_sections WHERE file_path_template LIKE '%Config_BA%'")
    rows = cursor.fetchall()
    
    print(f"Encontrados {len(rows)} caminhos candidatos para normalização.")
    
    updated_count = 0
    errors = 0
    
    for row in rows:
        row_id, old_path = row
        
        # A Mágica do Pivô: Tudo depois de "Config_BA" é o que nos interessa
        if "Config_BA" in old_path:
            parts = old_path.split("Config_BA")
            suffix = parts[1].strip("\\/") # Pega "BTR\PT\..."
            
            # CAMINHO PORTÁTIL: Armazenamos apenas "BTR/PT/..." no banco.
            # Assim, a pasta Config_BA pode ser movida para qualquer lugar.
            new_rel_path = suffix.replace("\\", "/")
            
            # Para validar se existe, precisamos reconstruir o caminho completo no sistema atual
            # PROJECT_ROOT + TARGET_REL_PATH + suffix
            abs_check_path = os.path.join(PROJECT_ROOT, TARGET_REL_PATH, suffix)
            
            if os.path.exists(abs_check_path):
                cursor.execute("UPDATE manual_sections SET file_path_template = ? WHERE id = ?", (new_rel_path, row_id))
                updated_count += 1
            else:
                print(f"[ERRO] Arquivo físico não encontrado em Config_BA: {suffix}")
                errors += 1
        else:
            print(f"[PULAR] Caminho não contém 'Config_BA': {old_path}")
            
    conn.commit()
    conn.close()
    
    print("-" * 50)
    print(f"Processo Concluído.")
    print(f"Atualizados com sucesso: {updated_count}")
    print(f"Erros (arquivos não achados): {errors}")
    print("-" * 50)

if __name__ == "__main__":
    sanitize()
