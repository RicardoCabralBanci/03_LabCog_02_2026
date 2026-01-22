import os
import json
import re

# Configuração de Caminhos
base_path = r"40_Personas\020. Bibliotecário\03. Paralelos\06. Excel_V3_MagnumOpus\01. Mapeamentos_V3"
output_dir = r"40_Personas\020. Bibliotecário\03. Paralelos\06. Excel_V3_MagnumOpus\03. Dados_JSON"
output_file = os.path.join(output_dir, "01_Safety_Instructions.json")

# Lista de arquivos mapeados (Excluindo ERRO e arquivos não md)
map_files = [
    "CarryStripPacker_Map_V3.md",
    "Folienrollenhubwagen_Map_V3.md",
    "Innopack_Packer_EN_Map_V3.md",
    "NatureMultiPacker_Map_V3.md",
    "RS2_Map_V3_ERRO_CONGRUENCIA.md",
    "ShrinkPacker_Map_V3.md",
    "TrayPacker_Map_V3_ERRO_CONGRUENCIA.md",
    "TrayShrinkPacker_Map_V3.md",
    "WraparoundPacker_Map_V3.md",
    "WraparoundShrinkPacker_Map_V3.md",
    "Zufuhrband_Map_V3.md"
]

data_structure = {
    "meta_info": {
        "tab_name": "Safety Instructions",
        "description": "Seção dedicada aos avisos de segurança gerais (Nível 1)."
    },
    "columns_definition": [
        "Safety Instructions (Ref)",
        "Original Title"
    ],
    "machines": {}
}

print("Iniciando extração para Safety Instructions...")

for filename in map_files:
    machine_key = filename.replace("_Map_V3.md", "").replace("_Map_V3_ERRO_CONGRUENCIA.md", "")
    file_path = os.path.join(base_path, filename)
    
    if not os.path.exists(file_path):
        print(f"Arquivo não encontrado: {file_path}")
        continue

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
        # Regex para capturar #### 5.1 ...
        # Ex: "#### 5.1 Safety instructions" ou "#### 5.1 Avisos de segurança"
        match = re.search(r"####\s+(5\.1.*?)$", content, re.MULTILINE)
        
        if match:
            full_line = match.group(1).strip()
            # Tentar separar número e texto
            # Ex: "5.1 Safety instructions" -> parts[0]="5.1", parts[1]="Safety instructions"
            parts = full_line.split(' ', 1)
            ref_num = parts[0]
            title = parts[1] if len(parts) > 1 else ""
            
            data_structure["machines"][machine_key] = {
                "Safety Instructions (Ref)": ref_num,
                "Original Title": title
            }
        else:
            # Caso não encontre (ex: Folienrollenhubwagen pode ser 5.1 também?)
            # Vou logar para verificação manual depois
            data_structure["machines"][machine_key] = {
                "Safety Instructions (Ref)": "Not Found",
                "Original Title": "Check Map"
            }

# Salvar JSON
with open(output_file, 'w', encoding='utf-8') as json_file:
    json.dump(data_structure, json_file, indent=4, ensure_ascii=False)

print(f"JSON gerado com sucesso: {output_file}")
