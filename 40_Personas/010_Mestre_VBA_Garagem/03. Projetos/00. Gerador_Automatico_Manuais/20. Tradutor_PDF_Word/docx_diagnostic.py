import zipfile
import xml.etree.ElementTree as ET
import os

def diagnose_docx(file_path):
    print(f"--- Iniciando Diagnostico em: {os.path.basename(file_path)} ---")
    
    if not os.path.exists(file_path):
        print(f"ERRO: Arquivo nao encontrado: {file_path}")
        return

    try:
        with zipfile.ZipFile(file_path, 'r') as docx:
            # Listar arquivos para garantir que e um docx valido
            files = docx.namelist()
            if 'word/document.xml' not in files:
                print("ERRO: Estrutura invalida. 'word/document.xml' nao encontrado.")
                return
            
            # Ler o XML principal
            xml_content = docx.read('word/document.xml')
            root = ET.fromstring(xml_content)
            
            # Namespaces (o pesadelo do XML)
            ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            
            # Contagens
            paragraphs = len(root.findall('.//w:p', ns))
            runs = len(root.findall('.//w:r', ns))
            text_nodes = len(root.findall('.//w:t', ns))
            
            # Verificar Caixas de Texto (TextBoxes)
            # Elas geralmente estao dentro de w:drawing ou w:pict -> v:shape -> v:textbox -> w:txbxContent
            # Simplificando a busca por w:txbxContent
            textboxes = len(root.findall('.//w:txbxContent', ns))
            
            print(f"Estatisticas da Autopsia:")
            print(f"  - Paragrafos (<w:p>): {paragraphs}")
            print(f"  - Execucoes (<w:r>): {runs}")
            print(f"  - Nos de Texto (<w:t>): {text_nodes}")
            print(f"  - Caixas de Texto Detectadas (<w:txbxContent>): {textboxes}")
            
            if textboxes > 0:
                print("\nALERTA CRITICO: Este arquivo contem Caixas de Texto.")
                print("Isso e comum em conversoes de PDF. O texto pode estar fragmentado.")
                print("A traducao precisara iterar recursivamente dentro dessas estruturas.")
            else:
                print("\nDiagnostico: Estrutura limpa (texto em fluxo continuo). Cirurgia sera mais simples.")

            # Amostra de texto (primeiros 5 nos)
            print("\nAmostra de Texto (Primeiros 5 nos):")
            count = 0
            for t_node in root.findall('.//w:t', ns):
                if count >= 5: break
                text = t_node.text
                if text and text.strip():
                    print(f"  [{count+1}] '{text}'")
                    count += 1

    except Exception as e:
        print(f"ERRO FATAL durante a autopsia: {e}")

if __name__ == "__main__":
    # Caminho hardcoded para o teste rapido, baseado no contexto atual
    target_file = r"40_Personas\040. Mestre em VBA (A Garagem de Autópsias Digitais)\03. Projetos\00. Gerador_Automatico_Manuais\20. Tradutor_PDF_Word\BA 89503126_000100 _Innopal_EN.docx"
    diagnose_docx(target_file)
