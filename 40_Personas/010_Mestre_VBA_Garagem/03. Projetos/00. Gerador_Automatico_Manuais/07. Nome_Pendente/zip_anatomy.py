import zipfile
import os

docx_path = os.path.join("40_Personas", "040. Mestre em VBA (A Garagem de Autópsias Digitais)", "03. Projetos", "00. Gerador_Automatico_Manuais", "07. Nome_Pendente", "02. Words", "BA_K-aaaaab_000000_PLT_XX.docx")

print(f"--- Anatomia do ZIP: {os.path.basename(docx_path)} ---")
try:
    with zipfile.ZipFile(docx_path, 'r') as z:
        for info in z.infolist():
            # Mostra arquivos grandes ou com nomes suspeitos
            print(f"{info.filename:<50} | {info.file_size:>10} bytes")
except Exception as e:
    print(f"Erro: {e}")
