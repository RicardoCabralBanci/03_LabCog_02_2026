import sys
import os
import zipfile
import xml.etree.ElementTree as ET
import re

def find_51(file_path):
    if not os.path.exists(file_path):
        return

    print(f"\n--- 🔍 Sonar em: {os.path.basename(file_path)} ---")

    try:
        with zipfile.ZipFile(file_path, 'r') as docx:
            xml_content = docx.read('word/document.xml')
            tree = ET.fromstring(xml_content)
            ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            
            for paragraph in tree.findall('.//w:p', ns):
                text = "".join([node.text for node in paragraph.findall('.//w:t', ns) if node.text])
                
                if text.strip():
                    # Procura por "5.1" no início do parágrafo ou qualquer menção a Safety/Segurança/Avisos
                    if re.match(r'^5\.1\b', text.strip()) or "Safety instructions" in text or "Instruções de segurança" in text:
                        print(f"✅ ENCONTRADO: {text.strip()}")
                        # Retornar o primeiro achado para economizar tempo
                        # return 

    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    for arg in sys.argv[1:]:
        find_51(arg)
