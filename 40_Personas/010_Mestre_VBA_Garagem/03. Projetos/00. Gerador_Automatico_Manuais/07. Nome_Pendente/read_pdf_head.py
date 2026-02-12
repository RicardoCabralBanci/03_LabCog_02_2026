import sys
import os

# Tentar importar pypdf ou PyPDF2
try:
    import pypdf
except ImportError:
    try:
        import PyPDF2 as pypdf
    except ImportError:
        print("Erro: Bibliotecas pypdf/PyPDF2 não encontradas. Instale com 'pip install pypdf'.")
        sys.exit(1)

# Caminho relativo ajustado para o contexto de execução
pdf_path = os.path.join("40_Personas", "040. Mestre em VBA (A Garagem de Autópsias Digitais)", "03. Projetos", "00. Gerador_Automatico_Manuais", "07. Nome_Pendente", "01. PDF's", "BA 89503126_000100 _Innopal_EN.pdf")

if not os.path.exists(pdf_path):
    print(f"Erro: Arquivo não encontrado: {pdf_path}")
    sys.exit(1)

try:
    reader = pypdf.PdfReader(pdf_path)
    num_pages = min(7, len(reader.pages))
    
    print(f"--- Lendo as primeiras {num_pages} páginas de: {os.path.basename(pdf_path)} ---")
    for i in range(num_pages):
        page = reader.pages[i]
        text = page.extract_text()
        print(f"\n=== PÁGINA {i+1} ===\n")
        print(text.encode('utf-8', errors='ignore').decode('utf-8')) # Tratamento básico de encoding
        
except Exception as e:
    print(f"Erro Crítico: {e}")
