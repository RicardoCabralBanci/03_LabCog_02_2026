import zipfile
import xml.etree.ElementTree as ET
import os
import sys

def read_docx(file_path):
    try:
        with zipfile.ZipFile(file_path) as docx:
            xml_content = docx.read('word/document.xml')
            tree = ET.XML(xml_content)
            TEXT_NS = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
            paragraphs = []
            # Iterar por parágrafos para tentar manter alguma quebra de linha
            for p in tree.iter(TEXT_NS + 'p'):
                texts = [node.text for node in p.iter(TEXT_NS + 't') if node.text]
                if texts:
                    paragraphs.append(''.join(texts))
            return '\n'.join(paragraphs)
    except Exception as e:
        return f"Error reading DOCX: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        print("Usage: python debug_word_read.py <path_to_docx>")
        sys.exit(1)

    if os.path.exists(path):
        content = read_docx(path)
        print(content) # Mostra todo o conteúdo
    else:
        print(f"File not found: {path}")