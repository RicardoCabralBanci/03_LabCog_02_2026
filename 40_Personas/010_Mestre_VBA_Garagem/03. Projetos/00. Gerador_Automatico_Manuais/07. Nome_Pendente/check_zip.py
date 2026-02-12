import zipfile
import sys
import os

docx_path = os.path.join("40_Personas", "040. Mestre em VBA (A Garagem de Autópsias Digitais)", "03. Projetos", "00. Gerador_Automatico_Manuais", "07. Nome_Pendente", "02. Words", "BA_K-aaaaab_000000_PLT_XX.docx")

if not zipfile.is_zipfile(docx_path):
    print("ERRO FATAL: O arquivo não é um ZIP válido. Não é um .docx real.")
    # Tenta ler os primeiros bytes para ver o que é
    try:
        with open(docx_path, 'rb') as f:
            header = f.read(20)
            print(f"Cabeçalho do arquivo (hex): {header.hex()}")
            print(f"Cabeçalho (texto): {header}")
    except:
        pass
    sys.exit(1)

print("O arquivo é um ZIP válido. Estrutura interna parece OK?")
try:
    with zipfile.ZipFile(docx_path, 'r') as z:
        critical_files = ['word/document.xml', '[Content_Types].xml', 'word/_rels/document.xml.rels']
        found = []
        for name in z.namelist():
            if name in critical_files:
                found.append(name)
        
        print(f"Arquivos críticos encontrados: {found}")
        
        if 'word/document.xml' in found:
            # Tentar ler o início do XML para ver se tem cara de XML
            with z.open('word/document.xml') as f:
                head = f.read(100)
                print(f"Início do document.xml: {head}")

except Exception as e:
    print(f"Erro ao ler ZIP: {e}")
