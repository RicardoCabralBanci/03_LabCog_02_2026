import win32com.client as win32
import os

pdf_path = r"Z:\B\BA_89408986_000300__Innopack Packer_EN.pdf"
docx_path = r"Z:\B\BA_89408986_000300__Innopack Packer_EN_NATIVE.docx"

print(f"Tentando converter: {pdf_path}")

try:
    word = win32.Dispatch("Word.Application")
    word.Visible = True # Vou deixar visível para vermos se abre
    
    print("Word aberto. Carregando PDF...")
    doc = word.Documents.Open(pdf_path, ConfirmConversions=False, ReadOnly=True)
    
    print("Salvando...")
    doc.SaveAs2(docx_path, FileFormat=16)
    
    print("Fechando...")
    doc.Close(False)
    word.Quit()
    print("SUCESSO ABSOLUTO.")
    
except Exception as e:
    print(f"ERRO: {e}")
