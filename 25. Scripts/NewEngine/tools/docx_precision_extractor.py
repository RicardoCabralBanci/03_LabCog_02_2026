import zipfile
import xml.etree.ElementTree as ET
import sys
import os
import re

def extract_docx_structure(docx_path):
    if not os.path.exists(docx_path):
        print(f"Error: File not found: {docx_path}")
        return

    # Namespaces do OpenXML
    ns = {
        'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    }

    try:
        with zipfile.ZipFile(docx_path) as z:
            with z.open('word/document.xml') as f:
                tree = ET.parse(f)
                root = tree.getroot()

            paragraphs = root.findall('.//w:p', ns)
            
            for p in paragraphs:
                # --- Extração de Texto ---
                text_nodes = p.findall('.//w:t', ns)
                text = "".join([node.text for node in text_nodes if node.text]).strip()

                if not text:
                    continue

                # --- Metadados XML (A "Verdade" Oficial) ---
                outline_lvl = p.find('.//w:pPr/w:outlineLvl', ns)
                style = p.find('.//w:pPr/w:pStyle', ns)
                style_id = style.get(f'{{{ns["w"]}}}val') if style is not None else None
                
                # Checagem de Negrito (pode estar no pPr global ou nos runs individuais)
                # Simplificação: verifica se existe algum w:b/w:bCs no parágrafo
                is_bold = False
                # Verifica negrito geral do parágrafo
                if p.find('.//w:pPr/w:rPr/w:b', ns) is not None:
                    is_bold = True
                else:
                    # Verifica se TODOS os runs de texto têm negrito (ou a maioria)
                    # Para simplificar, se encontrar negrito em runs de texto, consideramos candidato
                    if p.find('.//w:r/w:rPr/w:b', ns) is not None:
                         is_bold = True

                level = 9 # Padrão: Body Text
                is_heading = False
                origin = "Text"

                # 1. Prioridade: Outline Level Explicito
                if outline_lvl is not None:
                    val = outline_lvl.get(f'{{{ns["w"]}}}val')
                    if val is not None:
                        level = int(val)
                        is_heading = True
                        origin = "XML-Outline"

                # 2. Prioridade: Estilo Conhecido
                elif style_id:
                    if "Heading" in style_id or "Titulo" in style_id or "Title" in style_id:
                        digits = "".join([c for c in style_id if c.isdigit()])
                        if digits:
                            level = int(digits) - 1
                            is_heading = True
                            origin = f"XML-Style({style_id})"

                # 3. Heurística: Numeração no Texto (Regex)
                # Padrão: Começa com número, pontos e espaço (ex: "5.1 ", "5.1.2 ")
                if not is_heading:
                    match = re.match(r'^(\d+(\.\d+)+)\s+', text)
                    if match:
                        num_part = match.group(1)
                        # Calcular nível baseado na profundidade (pontos)
                        # "5.1" (1 ponto) -> Nível 1? 
                        # Vamos assumir que Capitulo 5 é Nivel 0 ou 1 dependendo da convenção.
                        # Geralmente: X (H1), X.Y (H2), X.Y.Z (H3)
                        dots = num_part.count('.')
                        level = dots # 5.1 (1 ponto) = Nivel 1. 5.1.1 (2 pontos) = Nivel 2.
                        is_heading = True
                        origin = "Regex-Num"
                    
                    # Caso especial: apenas "5. Operation" (Nivel 0)
                    elif re.match(r'^\d+\.\s+', text):
                         level = 0
                         is_heading = True
                         origin = "Regex-Num-H1"

                # 4. Heurística: Texto Curto + Negrito (Titulos sem número)
                if not is_heading and is_bold:
                    if len(text) < 80 and not text.endswith('.'):
                        # Candidato forte a subtítulo de nível inferior (ex: Nivel 3 ou 4)
                        level = 3 # Assumimos um nível genérico de "tópico"
                        is_heading = True
                        origin = "Bold-Heuristic"

                # --- Saída Formatada ---
                # Exibir apenas se for Heading ou se quisermos debug total
                # Para nosso uso, queremos ver tudo mas marcando o que é titulo
                
                prefix = f"[{level}]"
                if is_heading:
                    prefix = f"[{level}:{origin}]"
                
                print(f"{prefix} {text}")

    except Exception as e:
        print(f"Error processing {docx_path}: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python docx_precision_extractor.py <path_to_docx>")
    else:
        extract_docx_structure(sys.argv[1])
