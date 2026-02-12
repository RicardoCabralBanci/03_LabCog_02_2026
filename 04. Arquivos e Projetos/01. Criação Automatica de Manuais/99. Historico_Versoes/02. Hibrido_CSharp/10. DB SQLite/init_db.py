import sqlite3
import os

DB_PATH = "manual_db.sqlite"
SCHEMA_PATH = "schema.sql"

def init_db():
    if os.path.exists(DB_PATH):
        print(f"O banco de dados '{DB_PATH}' ja existe. Removendo para recriacao limpa...")
        os.remove(DB_PATH)

    print(f"Criando novo banco de dados em '{DB_PATH}'...")
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        with open(SCHEMA_PATH, 'r') as f:
            schema_sql = f.read()
            
        cursor.executescript(schema_sql)
        conn.commit()
        
        print("Schema aplicado com sucesso!")
        
        # Verificação rápida
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"Tabelas criadas: {[t[0] for t in tables]}")
        
        conn.close()
        
    except Exception as e:
        print(f"Erro fatal ao criar banco: {e}")

if __name__ == "__main__":
    # Muda para o diretório do script para facilitar caminhos relativos
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    init_db()
