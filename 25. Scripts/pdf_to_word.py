import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
from pdf2docx import Converter

def convert_pdf_to_word(pdf_path):
    """
    Converte um arquivo PDF para Word (.docx) preservando layout.
    """
    if not os.path.exists(pdf_path):
        print(f"Erro: Arquivo não encontrado: {pdf_path}")
        return False

    docx_path = os.path.splitext(pdf_path)[0] + ".docx"
    print(f"--- Iniciando conversão: {os.path.basename(pdf_path)} ---")
    
    try:
        cv = Converter(pdf_path)
        cv.convert(docx_path, start=0, end=None)
        cv.close()
        print(f"Sucesso! Salvo em: {docx_path}")
        return True
    except Exception as e:
        print(f"Erro na conversão: {e}")
        return False

def batch_convert(folder_path):
    """
    Converte todos os PDFs de uma pasta.
    """
    if not os.path.exists(folder_path):
        print(f"Erro: Pasta não encontrada: {folder_path}")
        return 0

    pdfs = [f for f in os.listdir(folder_path) if f.lower().endswith('.pdf')]
    
    if not pdfs:
        print("Nenhum arquivo PDF encontrado nesta pasta.")
        return 0
    
    print(f"Encontrados {len(pdfs)} arquivos PDF. Iniciando lote...")
    
    count = 0
    for pdf in pdfs:
        full_path = os.path.join(folder_path, pdf)
        if convert_pdf_to_word(full_path):
            count += 1
    return count

# --- GUI FUNCTIONS ---

def gui_select_file():
    filepath = filedialog.askopenfilename(
        title="Selecione o PDF",
        filetypes=[("Arquivos PDF", "*.pdf")]
    )
    if filepath:
        if convert_pdf_to_word(filepath):
            messagebox.showinfo("Sucesso", f"Arquivo convertido!\nSalvo em: {os.path.splitext(filepath)[0]}.docx")
        else:
            messagebox.showerror("Erro", "Falha na conversão. Verifique o console.")

def gui_select_folder():
    folderpath = filedialog.askdirectory(title="Selecione a Pasta com PDFs")
    if folderpath:
        count = batch_convert(folderpath)
        if count > 0:
            messagebox.showinfo("Sucesso", f"{count} arquivos convertidos com sucesso!")
        else:
            messagebox.showwarning("Aviso", "Nenhum arquivo convertido (ou pasta vazia).")

def start_gui():
    root = tk.Tk()
    root.title("Conversor do Mestre")
    root.geometry("300x150")
    
    lbl = tk.Label(root, text="O que vamos converter hoje?", pady=10)
    lbl.pack()
    
    btn_file = tk.Button(root, text="Selecionar Arquivo Único (PDF)", command=gui_select_file, width=25, height=2)
    btn_file.pack(pady=5)
    
    btn_folder = tk.Button(root, text="Selecionar Pasta Inteira", command=gui_select_folder, width=25, height=2)
    btn_folder.pack(pady=5)
    
    root.mainloop()

if __name__ == "__main__":
    # Se houver argumentos, usa modo CLI (Silencioso/Hacker)
    if len(sys.argv) > 1:
        target = " ".join(sys.argv[1:]).strip().replace('"', '')
        print("=== Modo CLI ===")
        if os.path.isfile(target):
            convert_pdf_to_word(target)
        elif os.path.isdir(target):
            batch_convert(target)
        else:
            print(f"Caminho inválido: {target}")
    
    # Se NÃO houver argumentos, abre a GUI (Modo Usuário)
    else:
        print("=== Iniciando Interface Gráfica... ===")
        start_gui()