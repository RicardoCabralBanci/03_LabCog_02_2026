import pypdf
import sys
import os

pdf_path = r"03_LabCog_02_2026\04_Integracao_Rockwell_SEW\01_Especificacoes_Tecnicas\Manuais\TechnicalData_Kinetix5700.pdf"

if not os.path.exists(pdf_path):
    print(f"Error: File not found at {pdf_path}")
    sys.exit(1)

try:
    reader = pypdf.PdfReader(pdf_path)
    print(f"Total Pages: {len(reader.pages)}")
    
    print("--- Outline ---")
    if reader.outline:
        for item in reader.outline:
            if isinstance(item, list):
                # Nested outline
                pass 
            else:
                try:
                    title = item.title
                    page_num = reader.get_destination_page_number(item)
                    print(f"Chapter: {title} - Starts at Page: {page_num}")
                except Exception as e:
                    pass
    else:
        print("No outline found.")

except Exception as e:
    print(f"Error reading PDF: {e}")