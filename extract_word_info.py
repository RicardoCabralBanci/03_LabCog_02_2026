import zipfile
import xml.etree.ElementTree as ET
import sys
import os

def extract_text_from_docx(file_path):
    """Extrai texto de arquivos .docx/.docm/.dotm sem dependencias externas pesadas."""
    try:
        with zipfile.ZipFile(file_path) as docx:
            xml_content = docx.read('word/document.xml')
            tree = ET.fromstring(xml_content)
            
            # Namespaces comuns no Word XML
            namespaces = {
                'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
            }
            
            text_parts = []
            # Encontrar todos os parágrafos
            for p in tree.findall('.//w:p', namespaces):
                p_text = []
                # Encontrar todos os textos dentro do parágrafo
                for t in p.findall('.//w:t', namespaces):
                    if t.text:
                        p_text.append(t.text)
                if p_text:
                    text_parts.append(''.join(p_text))
            
            return '\n'.join(text_parts)
    except Exception as e:
        return f"ERRO AO LER ARQUIVO: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python extract_word_info.py <caminho_do_arquivo>")
        sys.exit(1)
        
    filepath = sys.argv[1]
    if not os.path.exists(filepath):
        print(f"Arquivo não encontrado: {filepath}")
        sys.exit(1)
        
    print(f"--- CONTEÚDO EXTRAÍDO DE: {os.path.basename(filepath)} ---")
    print(extract_text_from_docx(filepath))
