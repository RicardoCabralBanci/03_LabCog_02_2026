from docx import Document
import sys
import os

# Caminho relativo ajustado
docx_path = os.path.join("40_Personas", "040. Mestre em VBA (A Garagem de Autópsias Digitais)", "03. Projetos", "00. Gerador_Automatico_Manuais", "07. Nome_Pendente", "02. Words", "BA_K-aaaaab_000000_PLT_XX.docx")

if not os.path.exists(docx_path):
    print(f"Erro: Arquivo não encontrado: {docx_path}")
    sys.exit(1)

try:
    doc = Document(docx_path)
    print(f"--- Auditoria Estrutural: {os.path.basename(docx_path)} ---\n")
    
    print("=== Primeiros 50 Parágrafos Não-Vazios (Estilo | Texto) ===")
    count = 0
    for p in doc.paragraphs:
        if not p.text.strip(): continue
        
        style = p.style.name
        preview = p.text[:60].replace('\n', ' ')
        print(f"Estilo: '{style:<25}' | Texto: {preview}...")
        
        count += 1
        if count >= 50: break

    print(f"\n=== Seções ({len(doc.sections)}) ===")
    for i, section in enumerate(doc.sections):
        # Converter twips/emus para algo legível se necessário, ou só mostrar o objeto raw
        print(f"Seção {i+1}: Start Type: {section.start_type}")

except Exception as e:
    print(f"Erro na análise: {e}")
