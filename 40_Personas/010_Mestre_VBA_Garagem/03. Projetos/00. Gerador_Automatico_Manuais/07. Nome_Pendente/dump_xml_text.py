import zipfile
import re
import os

docx_path = os.path.join("40_Personas", "040. Mestre em VBA (A Garagem de Autópsias Digitais)", "03. Projetos", "00. Gerador_Automatico_Manuais", "07. Nome_Pendente", "02. Words", "BA_K-aaaaab_000000_PLT_XX.docx")

try:
    with zipfile.ZipFile(docx_path, 'r') as z:
        xml_content = z.read('word/document.xml').decode('utf-8', errors='ignore')

    # Regex para achar texto dentro de tags <w:t>
    texts = re.findall(r'<w:t[^>]*>(.*?)</w:t>', xml_content)

    print(f"--- Extração Bruta de Texto ({len(texts)} fragmentos encontrados) ---")
    print("Mostrando os primeiros 50 fragmentos para ver se achamos o Índice ou Títulos:")
    for i, t in enumerate(texts[:50]):
        print(f"{i}: {t}")

except Exception as e:
    print(f"Erro: {e}")
