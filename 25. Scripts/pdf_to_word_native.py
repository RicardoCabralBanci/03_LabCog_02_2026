import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
import win32com.client as win32

def convert_pdf_to_word_native(pdf_path):
    """
    Usa o Microsoft Word via COM para converter PDF em DOCX.
    Melhor fidelidade visual.
    """
    if not os.path.exists(pdf_path):
        print(f"Erro: Arquivo não encontrado: {pdf_path}")
        return False

    # Caminhos absolutos são obrigatórios para o Word COM
    pdf_path = os.path.abspath(pdf_path)
    docx_path = os.path.splitext(pdf_path)[0] + ".docx"
    
    print(f"--- Iniciando conversão NATIVA (Word Engine): {os.path.basename(pdf_path)} ---")
    
    word = None
    doc = None
    try:
        # Inicia o Word (invisível para ser mais rápido, mas visível ajuda a ver erros)
        word = win32.Dispatch("Word.Application")
        word.Visible = False 
        
        # Abre o PDF (O Word vai converter automaticamente)
        print("Abrindo PDF no Word...")
        doc = word.Documents.Open(pdf_path, ConfirmConversions=False, ReadOnly=True)
        
        # Salva como DOCX (FileFormat 16 = wdFormatDocumentDefault)
        print("Salvando como DOCX...")
        doc.SaveAs2(docx_path, FileFormat=16)
        
        print(f"Sucesso! Salvo em: {docx_path}")
        return True
        
    except Exception as e:
        print(f"ERRO CRÍTICO NA ENGINE DO WORD: {e}")
        return False
        
finally:
    if doc:
        try:
            doc.Close(False) # Fecha sem salvar mudanças no original
        except:
            pass
    if word:
        try:
            word.Quit() # Fecha o Word
        except:
            pass

def batch_convert_native(folder_path):
    if not os.path.exists(folder_path):
        print(f"Erro: Pasta não encontrada: {folder_path}")
        return 0

    pdfs = [f for f in os.listdir(folder_path) if f.lower().endswith('.pdf')]
    if not pdfs:
        print("Nenhum arquivo PDF encontrado.")
        return 0
    
    print(f"Encontrados {len(pdfs)} arquivos. Iniciando lote NATIVO...")
    count = 0
    for pdf in pdfs:
        full_path = os.path.join(folder_path, pdf)
        if convert_pdf_to_word_native(full_path):
            count += 1
    return count

# --- GUI ---

def gui_select_file():
    filepath = filedialog.askopenfilename(
        title="Selecione o PDF (Engine Word Nativa)",
        filetypes=[("Arquivos PDF", "*.pdf")]
    )
    if filepath:
        if convert_pdf_to_word_native(filepath):
            messagebox.showinfo("Sucesso", f"Convertido com Engine Word!\nSalvo em: {os.path.splitext(filepath)[0]}.docx")
        else:
            messagebox.showerror("Erro", "Falha na conversão. Verifique se o Word está instalado/fechado.")

def gui_select_folder():
    folderpath = filedialog.askdirectory(title="Selecione Pasta (Engine Word Nativa)")
    if folderpath:
        count = batch_convert_native(folderpath)
        messagebox.showinfo("Relatório", f"{count} arquivos convertidos via Word.")

def start_gui():
    root = tk.Tk()
    root.title("Conversor NATIVO (Mestre em VBA)")
    root.geometry("350x150")
    
    lbl = tk.Label(root, text="Conversão de Alta Fidelidade (Usa o Word)", pady=10)
    lbl.pack()
    
    btn_file = tk.Button(root, text="Selecionar Arquivo (PDF)", command=gui_select_file, width=30, height=2)
    btn_file.pack(pady=5)
    
    root.mainloop()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target = " ".join(sys.argv[1:]).strip().replace('"', '')
        if os.path.isfile(target):
            convert_pdf_to_word_native(target)
        elif os.path.isdir(target):
            batch_convert_native(target)
    else:
        start_gui()