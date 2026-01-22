import sys
import os
import zipfile
import xml.etree.ElementTree as ET

def detect_hierarchy(file_path):
    if not os.path.exists(file_path):
        return

    print(f"\n--- Analisando Hierarquia Profunda: {os.path.basename(file_path)} ---")

    try:
        with zipfile.ZipFile(file_path, 'r') as docx:
            xml_content = docx.read('word/document.xml')
            tree = ET.fromstring(xml_content)
            
            # Namespaces
            ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            
            for i, paragraph in enumerate(tree.findall('.//w:p', ns)):
                # Extrair texto
                text = "".join([node.text for node in paragraph.findall('.//w:t', ns) if node.text])
                
                if not text.strip():
                    continue

                # Propriedades do parágrafo
                pPr = paragraph.find('w:pPr', ns)
                
                is_numbered = False
                outline_level = "N/A"
                style_name = "Normal"
                
                if pPr is not None:
                    # Checar Numeração
                    numPr = pPr.find('w:numPr', ns)
                    if numPr is not None:
                        is_numbered = True
                    
                    # Checar Outline Level
                    outline = pPr.find('w:outlineLvl', ns)
                    if outline is not None:
                        outline_level = outline.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val')
                    
                    # Checar Estilo
                    pStyle = pPr.find('w:pStyle', ns)
                    if pStyle is not None:
                        style_name = pStyle.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val')

                # Filtro Inteligente: Só mostrar se tiver indícios de ser título
                # (Numerado OU Outline Level definido OU Estilo de Heading)
                # E conter texto relevante para não spamar
                relevant_keywords = ["Signal", "Sinal", "Horn", "Buzina", "Lamp", "Luz", "Acoustic", "Optical", "Aviso", "Warning"]
                
                if (is_numbered or outline_level != "N/A" or "Heading" in style_name) and any(k in text for k in relevant_keywords):
                    marker = "[NUM]" if is_numbered else "  "
                    lvl = f"Lvl:{outline_level}" if outline_level != "N/A" else "       "
                    
                    print(f"{marker} [{lvl}] Style:'{style_name}' -> {text.strip()}")

    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding='utf-8')
    detect_hierarchy(sys.argv[1])
