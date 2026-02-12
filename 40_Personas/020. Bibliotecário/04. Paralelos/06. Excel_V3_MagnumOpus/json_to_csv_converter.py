import os
import json
import csv

# Configuração
input_dir = r"40_Personas\020. Bibliotecário\03. Paralelos\06. Excel_V3_MagnumOpus\03. Dados_JSON"
output_dir = r"40_Personas\020. Bibliotecário\03. Paralelos\06. Excel_V3_MagnumOpus\02. Dados_Estruturados_CSV"

# Garantir saída
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Lista de máquinas na ordem desejada
machine_order = [
    "CarryStripPacker",
    "Folienrollenhubwagen",
    "Innopack_Packer_EN",
    "NatureMultiPacker",
    "RS2",
    "ShrinkPacker",
    "TrayPacker",
    "TrayShrinkPacker",
    "WraparoundPacker",
    "WraparoundShrinkPacker",
    "Zufuhrband"
]

print("Iniciando conversão JSON -> CSV (Padrão Universal: Vírgula + Aspas)...")

json_files = [f for f in os.listdir(input_dir) if f.endswith(".json")]

for json_file in json_files:
    input_path = os.path.join(input_dir, json_file)
    csv_filename = json_file.replace(".json", ".csv")
    output_path = os.path.join(output_dir, csv_filename)
    
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    headers = ["Machine"] + data["columns_definition"]
    rows = []
    
    for machine in machine_order:
        row_data = {"Machine": machine}
        machine_info = data["machines"].get(machine, {})
        
        for col in data["columns_definition"]:
            val = machine_info.get(col, "--")
            if val is None or val == "":
                val = "--"
            row_data[col] = val
            
        rows.append(row_data)
        
    # CONFIGURAÇÃO DE OURO:
    # delimiter=',' -> Padrão que o VS Code entende.
    # quotechar='"' -> Protege textos.
    # quoting=csv.QUOTE_ALL -> Força aspas em TUDO. Evita ambiguidade.
    with open(output_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.DictWriter(
            csvfile, 
            fieldnames=headers, 
            delimiter=',', 
            quotechar='"', 
            quoting=csv.QUOTE_ALL
        )
        writer.writeheader()
        writer.writerows(rows)
        
    print(f"CSV Gerado: {csv_filename}")

print("Conversão concluída! Agora deve abrir perfeitamente. 🚀")
