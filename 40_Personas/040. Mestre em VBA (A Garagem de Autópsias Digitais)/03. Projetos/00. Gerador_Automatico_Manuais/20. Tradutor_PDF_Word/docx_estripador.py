import zipfile
import xml.etree.ElementTree as ET
import os
import shutil

# Namespaces do Word (OpenXML)
NS = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'xml': 'http://www.w3.org/XML/1998/namespace'
}

# Registrando namespaces para o ElementTree nao ficar louco gerando prefixos ns0, ns1...
for prefix, uri in NS.items():
    ET.register_namespace(prefix, uri)

class DocxEstripador:
    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path
        self.temp_dir = "temp_docx_extract"
        
    def _mock_translate(self, text):
        """Simula uma traducao. Substitua isso por uma chamada real de API depois."""
        if not text or len(text.strip()) < 2:
            return text # Ignora pontuacao ou espacos
        return f"[PT] {text}"

    def process(self):
        print(f"--- Iniciando Procedimento em: {self.input_path} ---")
        
        # 1. Deszipar
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
        with zipfile.ZipFile(self.input_path, 'r') as zip_ref:
            zip_ref.extractall(self.temp_dir)
            
        doc_xml_path = os.path.join(self.temp_dir, 'word', 'document.xml')
        
        # 2. Parsear XML
        tree = ET.parse(doc_xml_path)
        root = tree.getroot()
        
        paragraphs = root.findall('.//w:p', NS)
        print(f"Processando {len(paragraphs)} paragrafos...")
        
        count = 0
        for p in paragraphs:
            # Coletar todo o texto do paragrafo
            full_text = ""
            runs = p.findall('.//w:r', NS)
            
            # Se nao tem runs, ignora
            if not runs:
                continue
                
            original_texts = []
            for r in runs:
                t_nodes = r.findall('w:t', NS)
                for t in t_nodes:
                    if t.text:
                        full_text += t.text
                        original_texts.append(t.text)
            
            if not full_text.strip():
                continue

            # 3. Traduzir (Mock)
            translated_text = self._mock_translate(full_text)
            
            if translated_text == full_text:
                continue

            # 4. Cirurgia: Remover runs antigos e inserir um novo
            # Mantemos as propriedades do primeiro run (negrito, tamanho, etc) para o novo texto
            first_run = runs[0]
            rPr = first_run.find('w:rPr', NS) # Run Properties
            
            # Remove todos os runs existentes do paragrafo
            for r in runs:
                p.remove(r)
            
            # Cria o novo run
            new_run = ET.SubElement(p, f"{{{NS['w']}}}r")
            
            # Reinsere as propriedades se existirem
            if rPr is not None:
                new_run.append(rPr)
                
            # Cria o novo no de texto
            new_t = ET.SubElement(new_run, f"{{{NS['w']}}}t")
            # xml:space="preserve" e importante
            new_t.set(f"{{{NS['xml']}}}space", "preserve")
            new_t.text = translated_text
            
            count += 1
            if count % 1000 == 0:
                print(f"  - Processados: {count}")

        print(f"Total de paragrafos alterados: {count}")
        
        # 5. Salvar XML modificado
        tree.write(doc_xml_path, encoding='UTF-8', xml_declaration=True)
        
        # 6. Re-zipar
        print("Fechando o paciente (Re-zipando)...")
        with zipfile.ZipFile(self.output_path, 'w', zipfile.ZIP_DEFLATED) as docx:
            for foldername, subfolders, filenames in os.walk(self.temp_dir):
                for filename in filenames:
                    file_path = os.path.join(foldername, filename)
                    arcname = os.path.relpath(file_path, self.temp_dir)
                    docx.write(file_path, arcname)
        
        # Limpeza
        shutil.rmtree(self.temp_dir)
        print(f"--- Concluido! Salvo em: {self.output_path} ---")

if __name__ == "__main__":
    input_file = r"40_Personas\040. Mestre em VBA (A Garagem de Autópsias Digitais)\03. Projetos\00. Gerador_Automatico_Manuais\20. Tradutor_PDF_Word\BA 89503126_000100 _Innopal_EN.docx"
    output_file = r"40_Personas\040. Mestre em VBA (A Garagem de Autópsias Digitais)\03. Projetos\00. Gerador_Automatico_Manuais\20. Tradutor_PDF_Word\BA_Innopal_PT_TESTE.docx"
    
    ripper = DocxEstripador(input_file, output_file)
    ripper.process()
