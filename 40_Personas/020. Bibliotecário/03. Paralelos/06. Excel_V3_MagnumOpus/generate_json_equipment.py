import os
import json
import re

# Configuração
base_path = r"40_Personas\020. Bibliotecário\03. Paralelos\06. Excel_V3_MagnumOpus\01. Mapeamentos_V3"
output_dir = r"40_Personas\020. Bibliotecário\03. Paralelos\06. Excel_V3_MagnumOpus\03. Dados_JSON"
output_file = os.path.join(output_dir, "02_Safety_Equipment.json")

# Dicionário de Sinônimos (Normalização de Colunas)
# Chave = Nome da Coluna Final (Inglês)
# Valor = Lista de termos encontrados nos manuais (Regex patterns)
synonyms = {
    "Emergency Stop": [r"Emergency stop.*", r"Botão de parada.*", r"Parada de emergência.*"],
    "Hoods / Coberturas": [r"Hoods", r"Coberturas", r"Turrets"],
    "Safety Doors": [r"Safety door.*", r"Portas de proteção.*", r"Portas de segurança.*", r"Safety fence.*", r"Escudo de proteção.*", r"Protection shield.*"],
    "Repair Switch": [r"Repair switch.*", r"Chave de reparo.*"],
    "Safety Light Curtain": [r"Safety light curtain.*", r"Cortina de luz.*"],
    "Manivela / Hand Crank": [r"Manivela.*", r"Hand crank.*"],
    "Delimitador / Access Limiter": [r"Delimitador.*", r"Access limiter.*"],
    "Trava / Lock": [r"Trava.*", r"Lock.*"]
}

# Lista de arquivos
map_files = [f for f in os.listdir(base_path) if f.endswith(".md")]

machines_data = {}
all_found_columns = set()

print("Iniciando extração para Safety Equipment (5.2)...")

for filename in map_files:
    machine_key = filename.replace("_Map_V3.md", "").replace("_Map_V3_ERRO_CONGRUENCIA.md", "")
    file_path = os.path.join(base_path, filename)
    
    machines_data[machine_key] = {} # Inicializa a máquina

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
        # Estratégia: Encontrar o bloco 5.2 até o próximo 5.x
        # Captura tudo entre "#### 5.2" e "#### 5.3" (ou fim de arquivo)
        section_match = re.search(r"#### 5\.2\s+.*?(?=#### 5\.3|#### 5\.|#|$)", content, re.DOTALL)
        
        if section_match:
            section_content = section_match.group(0)
            
            # Procurar sub-itens: * **5.2.X Nome**
            sub_items = re.findall(r"\*\s+\*\*(5\.2\.\d+)\s+(.*?)\*\*", section_content)
            
            for ref_num, title in sub_items:
                title_clean = title.strip()
                
                # Tentar normalizar o título usando o dicionário
                column_name = "Outros / Others" # Default
                matched = False
                
                for col_key, patterns in synonyms.items():
                    for pattern in patterns:
                        if re.search(pattern, title_clean, re.IGNORECASE):
                            column_name = col_key
                            matched = True
                            break
                    if matched: break
                
                # Se não bateu com nada conhecido, usa o próprio título como coluna (para não perder dados)
                if not matched:
                    column_name = title_clean

                all_found_columns.add(column_name)
                
                # Guardar no dicionário da máquina (pode haver múltiplas safety doors, então guardamos como lista ou string concatenada?)
                # Para simplificar o Excel, se houver duplicata na mesma categoria, concatenamos.
                if column_name in machines_data[machine_key]:
                    machines_data[machine_key][column_name] += f" | {ref_num} ({title_clean})"
                else:
                    machines_data[machine_key][column_name] = f"{ref_num}" # Apenas o número para começar, ou numero + titulo se for generico

# Ordenar colunas (Padrão + Descobertas)
final_columns = list(synonyms.keys()) + [c for c in all_found_columns if c not in synonyms.keys()]

# Montar JSON final
json_output = {
    "meta_info": {
        "tab_name": "Safety Equipment",
        "description": "Dispositivos de proteção (Nível 5.2)."
    },
    "columns_definition": final_columns,
    "machines": machines_data
}

with open(output_file, 'w', encoding='utf-8') as json_file:
    json.dump(json_output, json_file, indent=4, ensure_ascii=False)

print(f"JSON Equipment gerado: {output_file}")
