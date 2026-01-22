import sqlite3
import os
import subprocess
import sys
import csv

# Configuração de Caminhos
if getattr(sys, 'frozen', False):
    APP_DIR = os.path.dirname(sys.executable)
else:
    APP_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(APP_DIR, "manual_db.sqlite")
ENGINE_EXE = os.path.join(APP_DIR, "Engine", "NewGerador.exe") # C# Engine
OUTPUT_FILENAME = "Manual_Gerado.docx"

def get_files_from_csv(csv_path):
    """Lê o manifesto estruturado (CATEGORY;KEY;VALUE) gerado pelo VBA"""
    if not os.path.exists(csv_path):
        print(f"[ERRO] Arquivo de manifesto não encontrado: {csv_path}")
        return []

    selected_files = []
    print(f"--- Processando Manifesto: {os.path.basename(csv_path)} ---")

    try:
        # Lê com UTF-8-SIG para tratar BOM se houver, delimiter ;
        with open(csv_path, mode='r', encoding='utf-8-sig', newline='') as f:
            reader = csv.reader(f, delimiter=';')
            
            # Pula cabeçalho se existir (CATEGORY;KEY;VALUE)
            # Mas vamos checar linha a linha para ser robusto
            for row in reader:
                if len(row) < 3: continue
                
                cat = row[0].strip().upper()
                key = row[1].strip().upper()
                val = row[2].strip()

                if cat == "FILE" and key == "SELECTED":
                    # Sanitização Cirúrgica:
                    path_clean = val.replace("/", os.sep).replace("\\", os.sep)
                    
                    # 1. Se tiver V:\ ou caminho completo até Config_BA, corta fora
                    if "Config_BA" in path_clean:
                        path_clean = path_clean.split("Config_BA")[-1].lstrip(os.sep)
                    
                    # 2. Remove o ponto inicial se o banco/Excel mandou ".BTR/..."
                    if path_clean.startswith("."):
                        path_clean = path_clean.lstrip(".").lstrip(os.sep)
                    
                    # 3. Monta o caminho absoluto a partir da raiz Config_BA
                    # (APP_DIR é NewGerador, o pai é Config_BA)
                    CONFIG_BA_ROOT = os.path.abspath(os.path.join(APP_DIR, ".."))
                    final_path = os.path.normpath(os.path.join(CONFIG_BA_ROOT, path_clean))
                    
                    if os.path.exists(final_path):
                        selected_files.append(final_path)
                    else:
                        print(f"[AVISO] Arquivo físico não encontrado: {final_path}")
                
                elif cat == "META":
                    print(f"[INFO] Projeto: {key} = {val}")

    except Exception as e:
        print(f"[ERRO CRÍTICO] Falha ao ler CSV: {e}")

    return selected_files

def main():
    if len(sys.argv) < 2:
        print("Uso: orchestrator.exe <PATH_TO_CSV>")
        # Para debug, tenta procurar input_manifest.csv na pasta local
        local_csv = os.path.join(APP_DIR, "input_manifest.csv")
        if os.path.exists(local_csv):
             print(f"Descobri manifesto local: {local_csv}")
             files = get_files_from_csv(local_csv)
        else:
             return
    else:
        # Argumento 1 é o CSV
        csv_path = sys.argv[1]
        files = get_files_from_csv(csv_path)

    if not files:
        print("[ERRO] Nenhum arquivo para processar. Abortando.")
        return

    print(f"--- Iniciando Motor C# com {len(files)} arquivos ---")
    
    # Monta comando: Engine.exe output.docx file1 file2 ...
    cmd = [ENGINE_EXE, OUTPUT_FILENAME] + files
    
    try:
        # subprocess.run espera o processo terminar
        result = subprocess.run(cmd, capture_output=False) # capture_output=False deixa o C# escrever no console
        
        if result.returncode == 0:
            print("\n[SUCESSO] Manual gerado com êxito!")
            # Opcional: Abrir a pasta ou o arquivo
            os.startfile(OUTPUT_FILENAME)
        else:
            print(f"\n[FALHA] O motor retornou código de erro: {result.returncode}")
            
    except Exception as ex:
        print(f"[ERRO FATAL] Não foi possível iniciar o motor: {ex}")

if __name__ == "__main__":
    main()