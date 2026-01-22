import sqlite3
import os
import subprocess

# Configuração
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "manual_db.sqlite")
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", ".."))
CONFIG_BA_ROOT = os.path.join(PROJECT_ROOT, "04. Arquivos e Projetos", "Criação Automatica de Manuais", "02. Recursos_Legados", "Config_BA")
CSHARP_PROJECT_DIR = os.path.join(SCRIPT_DIR, "WordStitcher")
OUTPUT_FILE = os.path.join(SCRIPT_DIR, "TESTE_MANUAL_FINAL.docx")

def run_test():
    print("--- INICIANDO TESTE DO SISTEMA HÍBRIDO (PROJETO 2) ---")
    
    # 1. Pegar a playlist REAL do Projeto 2
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Query que respeita a ordem definida pelo usuário (custom_order)
    query = """
        SELECT s.file_path_template 
        FROM manual_sections s
        JOIN project_composition pc ON s.id = pc.section_id
        WHERE pc.project_id = 2 AND pc.is_active = 1
        ORDER BY pc.custom_order ASC
    """
    
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        print("ERRO: O projeto 2 não tem nenhuma seção ativa.")
        return

    # 2. Converter para caminhos absolutos para o C#
    abs_paths = []
    print("\nArquivos selecionados para o teste:")
    for row in rows:
        # O caminho no banco é algo como "BTR/PT/..."
        # Precisamos juntar com o caminho real do Config_BA
        rel_path = row[0]
        full_path = os.path.join(CONFIG_BA_ROOT, rel_path.replace("/", os.sep))
        
        if os.path.exists(full_path):
            abs_paths.append(full_path)
            print(f" [OK] {os.path.basename(full_path)}")
        else:
            print(f" [X] ARQUIVO NÃO ENCONTRADO NO DISCO: {full_path}")
            # Tenta um fallback bobo só para não falhar o teste
            # (Em produção, trataríamos isso melhor)
    
    if len(abs_paths) < 2:
        print("\nERRO: Precisamos de pelo menos 2 arquivos válidos para testar a fusão.")
        return

    # 3. Invocar o Módulo C#
    print(f"\nInvocando o Operário C#...")
    print(f"Output: {OUTPUT_FILE}")
    
    # Monta o comando: dotnet run --project <path> <output> <input1> <input2> ...
    # Usando caminho absoluto do dotnet para garantir execução
    DOTNET_EXE = r"C:\Program Files\dotnet\dotnet.exe"
    cmd = [DOTNET_EXE, "run", "--project", CSHARP_PROJECT_DIR, OUTPUT_FILE] + abs_paths
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("\n--- RETORNO DO C# ---")
        print(result.stdout)
        
        if os.path.exists(OUTPUT_FILE):
            print(f"\nSUCESSO ABSOLUTO! O arquivo foi gerado em:\n{OUTPUT_FILE}")
        else:
            print("\nO C# disse que funcionou, mas o arquivo não apareceu. Mistério.")
            
    except subprocess.CalledProcessError as e:
        print(f"\nERRO NA EXECUÇÃO DO C#:\n{e.stderr}")

if __name__ == "__main__":
    run_test()
