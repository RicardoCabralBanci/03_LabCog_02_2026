import sys
import os
import zipfile
import xml.etree.ElementTree as ET

def read_docx_structure(file_path):
    """
    Lê a estrutura de um arquivo .docx extraindo diretamente do XML (document.xml),
    já que não podemos garantir que a lib python-docx esteja instalada.
    """
    if not os.path.exists(file_path):
        print(f"Erro: Arquivo não encontrado: {file_path}")
        return

    print(f"--- Analisando Estrutura: {os.path.basename(file_path)} ---")

    try:
        with zipfile.ZipFile(file_path, 'r') as docx:
            xml_content = docx.read('word/document.xml')
            tree = ET.fromstring(xml_content)
            
            # Namespaces comuns no Word XML
            ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            
            # Iterar pelos parágrafos
            for paragraph in tree.findall('.//w:p', ns):
                text = ""
                # Concatenar todos os runs de texto (w:t) dentro do parágrafo
                for node in paragraph.findall('.//w:t', ns):
                    if node.text:
                        text += node.text
                
                if text.strip():
                    # Tentar identificar se é título pelo estilo (pStyle)
                    style_val = "Normal"
                    pPr = paragraph.find('w:pPr', ns)
                    if pPr is not None:
                        pStyle = pPr.find('w:pStyle', ns)
                        if pStyle is not None:
                            style_val = pStyle.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val')
                    
                    # Imprimir apenas se tiver conteúdo relevante ou parecer título
                    # Limitando a saída para não poluir
                    prefix = ""
                    if "Heading" in style_val or "Título" in style_val or "Gliederung" in style_val:
                        prefix = f"[{style_val}] "
                        print(f"{prefix}{text}")
                    elif "Warning" in text or "Attention" in text or "Atenção" in text or "Perigo" in text or "Danger" in text:
                         print(f"[ALERTA POTENCIAL] {text}")
                    elif len(text) < 100: # Imprimir textos curtos que podem ser subtítulos não formatados
                         # print(f"   {text}") # Comentado para reduzir ruído, descomentar se necessário
                         pass

    except Exception as e:
        print(f"Erro ao ler .docx: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python read_word_structure.py <caminho_do_arquivo>")
    else:
        read_docx_structure(sys.argv[1])
