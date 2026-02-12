import pypdf
import sys
import os

pdf_path = r"03_LabCog_02_2026\04_Integracao_Rockwell_SEW\01_Especificacoes_Tecnicas\Manuais\TechnicalData_Kinetix5700.pdf"

reader = pypdf.PdfReader(pdf_path)

for i in range(5):
    print("--- Page " + str(i+1) + " ---")
    try:
        text = reader.pages[i].extract_text()
        print(text)
    except:
        print("Error reading page")