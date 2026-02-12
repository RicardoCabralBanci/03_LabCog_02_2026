import os
import json
import re

# Configuração
base_path = r"40_Personas\020. Bibliotecário\03. Paralelos\06. Excel_V3_MagnumOpus\01. Mapeamentos_V3"
output_dir = r"40_Personas\020. Bibliotecário\03. Paralelos\06. Excel_V3_MagnumOpus\03. Dados_JSON"

# Definição das Abas e Regras de Extração
tabs_config = [
    {
        "filename": "03_Signaling_Equipment.json",
        "name": "Signaling Equipment",
        "regex_section": r"####\s+(5\.\d+)\s+(Signaling equipment|Dispositivos de aviso)",
        "synonyms": {
            "Signal Lamp / Lâmpada": [r"Signal lamp", r"Signal light", r"Sinalizador", r"Lâmpada"],
            "Signal Horn / Buzina": [r"Signal horn", r"Buzina", r"Audible signal"]
        }
    },
    {
        "filename": "04_Operating_Controls.json",
        "name": "Operating Controls",
        "regex_section": r"####\s+(5\.\d+)\s+(Operating controls|Dispositivos de comando)",
        "synonyms": {
            "Overview / Visão Geral": [r"Overview", r"Visão geral"],
            "Main Switch / Chave Geral": [r"Main switch", r"Switch cabinet", r"Quadro elétrico"],
            "Emergency Stop / Emergência": [r"Emergency stop"],
            "Touchscreen / IHM": [r"Touchscreen", r"Tablet", r"Operator console", r"Console de operação"],
            "Feed Belt / Esteira": [r"Feed belt", r"Esteira de alimentação"],
            "ReDiS": [r"ReDiS"],
            "Pneumatics / Ar Comprimido": [r"Shut-off valve", r"Válvula de bloqueio", r"Compressed air"],
            "Manual Control / Jog": [r"Manual control", r"Unidade de comando manual", r"Jog"],
            "Folding / Dobra": [r"Folding"],
            "Wrapping / Envoltura": [r"Wrapping"],
            "Shrink Tunnel / Túnel": [r"Shrink tunnel", r"Tunnel", r"Manivela"],
            "Blank Magazine / Magazine": [r"Blank magazine", r"Loading conveyor"]
        }
    },
    {
        "filename": "05_Preparing_for_Operation.json",
        "name": "Preparing for Operation",
        "regex_section": r"####\s+(5\.\d+)\s+(Preparing|Estabelecer prontidão)",
        "synonyms": {
            "Switch On / Ligar": [r"Switch.*on", r"Ligar a máquina", r"Switching on the machine"],
            "Compressed Air / Ar": [r"Compressed air", r"Ar comprimido"],
            "Hot Melt / Cola": [r"Hot-melt", r"Hot melt", r"Glue", r"Cola", r"Pre-melting"],
            "Film / Filme": [r"Threading", r"Film", r"Inserir o filme"],
            "Blanks / Cartão": [r"Blank", r"Magazine"],
            "Shrink Tunnel / Túnel": [r"Tunnel", r"Túnel"],
            "Labels / Etiquetas": [r"Label", r"Etiqueta", r"Laminating"],
            "Adhesive Tape / Alça": [r"Adhesive tape", r"Carrying handle"]
        }
    },
    {
        "filename": "06_Production.json",
        "name": "Production",
        "regex_section": r"####\s+(5\.\d+)\s+(Production|Produção)",
        "synonyms": {
            "Safety / Segurança": [r"Safety", r"Segurança"],
            "Prerequisites / Requisitos": [r"Prerequisites", r"Requisitos", r"Conditions"],
            "Preparation / Preparação": [r"Preparation", r"Preparação"],
            "Start / Iniciar": [r"Start", r"Iniciar"],
            "Monitor / Monitorar": [r"Monitor"],
            "Stop / Parar": [r"Stop", r"Parar"],
            "Jog Mode / Toques": [r"Jog", r"Toques"],
            "End / Encerrar": [r"End", r"Terminating", r"Encerrar"],
            "Switch Off / Desligar": [r"Switch.*off", r"Desligar"]
        }
    },
    {
        "filename": "07_Setup.json",
        "name": "Setup",
        "regex_section": r"####\s+(5\.\d+)\s+(Setup|Changeover)",
        "synonyms": {
            "Safety / Segurança": [r"Safety", r"Segurança"],
            "Tablet / IHM": [r"Tablet", r"Screen", r"Guided"],
            "Adjustment Elements": [r"Adjustment elements", r"Elementos de ajuste"],
            "M01 Product Feed": [r"M01", r"Product feed", r"Alimentação"],
            "M02 Formatting": [r"M02", r"Formatting", r"Formatar", r"Collating"],
            "M03 Folding": [r"M03", r"Folding", r"Dobra"],
            "M04 Wrapping": [r"M04", r"Wrapping", r"Aplicar filme"],
            "M05 Turning": [r"M05", r"Turning", r"Giro"],
            "M07 Shrink": [r"M07", r"Shrink", r"Encolher", r"Retração"],
            "M09 Blank Feed": [r"M09", r"Blank"],
            "M5x Modules (Nature)": [r"M5\d", r"M6\d"],
            "Format Parts": [r"Format parts", r"Peças de formato"]
        }
    },
    {
        "filename": "08_Cleaning.json",
        "name": "Cleaning",
        "regex_section": r"####\s+(5\.\d+)\s+(Cleaning|Limpeza)",
        "synonyms": {
            "Instructions / Instruções": [r"Instructions", r"Instruções", r"Safety"],
            "Execution / Execução": [r"Execution", r"Execução", r"Performing"]
        }
    },
    {
        "filename": "09_Recommissioning.json",
        "name": "Recommissioning",
        "regex_section": r"####\s+(5\.\d+)\s+(Recommissioning|Ligar a máquina novamente|Resuming|Taking.*out)",
        "synonyms": {
            "Procedure": [r".*"] # Pega tudo
        }
    }
]

# Função para extrair dados
def extract_section_data(config):
    machines_data = {}
    all_found_columns = set()
    
    map_files = [f for f in os.listdir(base_path) if f.endswith(".md")]

    for filename in map_files:
        machine_key = filename.replace("_Map_V3.md", "").replace("_Map_V3_ERRO_CONGRUENCIA.md", "")
        file_path = os.path.join(base_path, filename)
        machines_data[machine_key] = {} 

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Encontrar a seção principal
            match = re.search(config["regex_section"], content, re.IGNORECASE)
            
            if match:
                section_num = match.group(1)
                
                # Definir limites de busca (até o próximo capítulo 5.x)
                # Ex: se achou 5.4, busca até 5.5
                next_section_num_part = int(section_num.split('.')[1]) + 1
                next_section_pattern = f"#### 5.{next_section_num_part}"
                
                # Recortar o conteúdo da seção
                start_idx = match.end()
                end_match = re.search(fr"#### 5\.{next_section_num_part}|#", content[start_idx:])
                
                if end_match:
                    section_content = content[start_idx : start_idx + end_match.start()]
                else:
                    section_content = content[start_idx:]

                # Procurar sub-itens dentro da seção ( * **5.x.x Nome** )
                # Regex flexível para pegar 5.X.X ou 5.X.X.X
                sub_items = re.findall(r"\*\s+\*\*(5\.\d+(?:\.\d+)+)\s+(.*?)\*\*", section_content)
                
                if not sub_items:
                    # Se não achou subitens explícitos no markdown, marca apenas a seção principal
                    machines_data[machine_key]["(Main Section)"] = section_num
                
                for ref_num, title in sub_items:
                    title_clean = title.strip()
                    
                    # Normalização
                    column_name = title_clean # Default
                    matched = False
                    
                    for col_key, patterns in config["synonyms"].items():
                        for pattern in patterns:
                            if re.search(pattern, title_clean, re.IGNORECASE):
                                column_name = col_key
                                matched = True
                                break
                        if matched: break
                    
                    all_found_columns.add(column_name)
                    
                    # Concatenar se já existir
                    if column_name in machines_data[machine_key]:
                        machines_data[machine_key][column_name] += f" | {ref_num}"
                    else:
                        machines_data[machine_key][column_name] = f"{ref_num}"

    # Ordenar colunas (Synonyms primeiro, depois o resto)
    sorted_columns = list(config["synonyms"].keys()) + [c for c in all_found_columns if c not in config["synonyms"].keys()]
    
    return {
        "meta_info": {"tab_name": config["name"]},
        "columns_definition": sorted_columns,
        "machines": machines_data
    }

print("Iniciando geração em lote...")

for config in tabs_config:
    print(f"Processando: {config['name']}...")
    json_data = extract_section_data(config)
    
    # Salvar
    full_out_path = os.path.join(output_dir, config["filename"])
    with open(full_out_path, 'w', encoding='utf-8') as json_file:
        json.dump(json_data, json_file, indent=4, ensure_ascii=False)

print("Todos os JSONs foram gerados com sucesso!")
