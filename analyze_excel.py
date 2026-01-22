import pandas as pd
import os

file_path = r"c:\LabCogKHS_CLI\40_Personas\020. Bibliotecário\03. Paralelos\02. Historico_Capitulo_05\03. Reestruturacao_Cap_05\Analise_Detalhada_Cap05.xlsx"

print(f"--- Analyzing: {os.path.basename(file_path)} ---")

try:
    xl = pd.ExcelFile(file_path)
    print(f"\nSheets found: {xl.sheet_names}")

    for sheet in xl.sheet_names:
        print(f"\n[Sheet: {sheet}]")
        df = xl.parse(sheet, nrows=5) # Read first 5 rows to get headers and sample
        print("Columns:", list(df.columns))
        print(f"Total Rows (approx): {len(xl.parse(sheet))}")
        print("First 3 rows sample:")
        print(df.head(3).to_string())
        print("-" * 30)

except Exception as e:
    print(f"Error reading Excel file: {e}")
