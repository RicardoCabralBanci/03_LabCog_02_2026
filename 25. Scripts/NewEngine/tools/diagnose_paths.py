import sqlite3
import os
from pathlib import Path

# Configuração
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "manual_db.sqlite")
ROOT_SEARCH_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..")) # Sobe para "Criação Automatica de Manuais"

def find_file(filename, search_path):
    for root, dirs, files in os.walk(search_path):
        if filename in files:
            return os.path.join(root, filename)
    return None

def diagnose():
    if not os.path.exists(DB_PATH):
        print(f"ERRO CRÍTICO: Banco de dados não encontrado em {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("--- INICIANDO DIAGNÓSTICO DE CAMINHOS ---")
    
    # Pegar caminhos únicos para não validar duplicatas
    cursor.execute("SELECT DISTINCT file_path_template FROM manual_sections WHERE file_path_template IS NOT NULL AND file_path_template != ''")
    rows = cursor.fetchall()
    
    total_files = len(rows)
    found_count = 0
    missing_count = 0
    
    print(f"Total de caminhos únicos no DB: {total_files}")
    print(f"Iniciando busca em: {ROOT_SEARCH_DIR} (isso pode levar alguns segundos...)\n")
    
    results = []

    for row in rows:
        original_path = row[0]
        filename = os.path.basename(original_path.replace('\\', '/')) # Normaliza separadores para extrair nome
        
        # Ignorar linhas vazias ou sem extensão .doc
        if not filename or ('.doc' not in filename.lower()):
            continue

        local_path = find_file(filename, ROOT_SEARCH_DIR)
        
        if local_path:
            found_count += 1
            status = "ENCONTRADO"
            # Calcular caminho relativo para futura sugestão de correção
            rel_path = os.path.relpath(local_path, start=os.getcwd())
        else:
            missing_count += 1
            status = "PERDIDO"
            rel_path = "N/A"
            
        results.append({
            'status': status,
            'filename': filename,
            'original': original_path,
            'new_local': rel_path
        })

    # Relatório Resumido
    print("-" * 60)
    print(f"RELATÓRIO FINAL:")
    print(f"Arquivos Encontrados: {found_count}")
    print(f"Arquivos Perdidos:    {missing_count}")
    print(f"Taxa de Sucesso:      {found_count/total_files*100:.1f}%" if total_files > 0 else "0%")
    print("-" * 60)
    
    # Amostra de Erros
    if missing_count > 0:
        print("\nAMOSTRA DE ARQUIVOS NÃO ENCONTRADOS (TOP 5):")
        for res in [r for r in results if r['status'] == 'PERDIDO'][:5]:
            print(f" [X] {res['filename']} (Origem: {res['original']})")

    # Amostra de Sucessos
    if found_count > 0:
        print("\nAMOSTRA DE ARQUIVOS ENCONTRADOS (TOP 5):")
        for res in [r for r in results if r['status'] == 'ENCONTRADO'][:5]:
            print(f" [OK] {res['filename']}")
            print(f"      -> Sugestão de novo caminho: {res['new_local']}")

    conn.close()

if __name__ == "__main__":
    diagnose()
