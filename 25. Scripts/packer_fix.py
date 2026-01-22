import os
import win32com.client as win32
import time

# Alvo específico
pdf_path = r"Z:\B\BA_89408986_000300__Innopack Packer_EN.pdf"
docx_path = r"Z:\B\BA_89408986_000300__Innopack Packer_EN_FINAL.docx"

def convert():
    print(f"--- Iniciando Operação Packer ---")
    print(f"Arquivo: {pdf_path}")
    
    if not os.path.exists(pdf_path):
        print("ERRO: O arquivo no drive Z: não foi encontrado. O drive está mapeado?")
        return

    word = None
    doc = None
    try:
        print("Tentando instanciar o Microsoft Word...")
        # Tenta o Dispatch comum primeiro, se falhar tenta o EnsureDispatch
        try:
            word = win32.gencache.EnsureDispatch("Word.Application")
        except:
            word = win32.Dispatch("Word.Application")
            
        word.Visible = True # Deixando visível para você ver o progresso
        
        print("Word detectado. Abrindo PDF (isso pode demorar para 234 páginas)...")
        # ConfirmConversions=False evita a caixa de diálogo chata
        doc = word.Documents.Open(pdf_path, ConfirmConversions=False, ReadOnly=True)
        
        print("Conversão concluída no Word. Salvando como DOCX...")
        doc.SaveAs2(docx_path, FileFormat=16)
        
        print(f"SUCESSO! Arquivo gerado: {docx_path}")
        
    except Exception as e:
        print(f"FALHA NA MISSÃO: {str(e)}")
        
    finally:
        if doc:
            doc.Close(False)
        if word:
            print("Encerrando Word...")
            word.Quit()

if __name__ == "__main__":
    convert()
