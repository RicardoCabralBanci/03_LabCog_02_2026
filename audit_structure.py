import os
import re
import subprocess
import difflib
import sys

# --- Configuração ---
# Caminhos relativos a partir da raiz do projeto (CWD)
CWD = os.getcwd()
BASE_DIR = os.path.join(CWD, "40_Personas", "020. Bibliotecário", "03. Paralelos", "03. Reestruturacao_Cap_05")
MAP_DIR = os.path.join(BASE_DIR, "02. Mapeamento_Subtitulos_C5")
WORD_DIR = os.path.join(BASE_DIR, "01. Inopack Cap05_Word_Files")

# Caminho para o executável C# que catalogamos no inventário
TOOL_PATH = os.path.join(CWD, "25. Scripts", "NewEngine", "tools", "DocxReconstructor.exe")

# Mapa: MD -> DOCX
FILE_MAP = {
    "CarryingHandle_Map.md": "Chapter_5_Operation.docx",
    "NatureMultiPacker_Map.md": "BA_89409041_000400__Innopack NatureMultiPacker_EN__Chapter_05_Operation-1-51.docx",
    "Innopack_Packer_EN_Map.md": "Innopack_Packer_EN_05_Operation.docx",
    "Folienrollenhubwagen_Map.md": "Innopack_Folienrollenhubwagen_05_Operacao.docx",
    "RS2_Map.md": "RS2 - Capítulo 05 - Operação.docx",
    "ShrinkPacker_Map.md": "ShrinkPacker - Capítulo 05 - Operação.docx",
    "TrayPacker_Map.md": "TrayPacker - Capítulo 5 - Operation.docx",
    "TrayShrinkPacker_Map.md": "TrayShrinkPacker - Capítulo 5 - Operation.docx",
    "WraparoundPacker_Map.md": "WraparoundPacker - 05_Operation.docx",
    "WraparoundShrinkPacker_Map.md": "WraparoundShrinkPacker - Chapter 5 - Operation.docx",
    "Zufuhrband_Map.md": "Zufuhrband - Chapter 5 - Operation.docx"
}

def normalize_text(text):
    """Remove pontuação, números iniciais e coloca em lowercase para comparação."""
    # Remove numeração inicial (ex: "5.1", "1.1", "5.2.1")
    text = re.sub(r'^\s*[\d\.]+\s+', '', text)
    # Remove caracteres especiais
    text = re.sub(r'[^\w\s]', '', text)
    return text.strip().lower()

def parse_markdown_map(md_path):
    """Extrai títulos esperados do arquivo Markdown."""
    expected_titles = []
    if not os.path.exists(md_path):
        return []

    with open(md_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # Pega linhas que começam com # ou * seguido de número (ex: #### 5.1 ou * 5.1)
            match = re.search(r'^(?:#+|\*)\s+(\d+(?:\.\d+)*)\s+(.+)$', line)
            if match:
                num = match.group(1)
                text = match.group(2).strip()
                # Limpa anotações comuns nos mapas
                text = re.sub(r'\*\*.*?\*\*', '', text) 
                text = re.sub(r'\(.*?\)', '', text)     
                
                expected_titles.append({
                    'num': num,
                    'text': text.strip(),
                    'norm': normalize_text(text)
                })
    return expected_titles

def run_reconstructor(docx_path):
    """Executa o DocxReconstructor.exe e processa o output."""
    if not os.path.exists(docx_path):
        print(f"❌ Word file not found: {os.path.basename(docx_path)}")
        return []

    # Chamada subprocess segura para Windows
    cmd = [TOOL_PATH, docx_path]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', shell=False)
        
        if result.returncode != 0:
            print(f"❌ Error running tool: {result.stderr}")
            return []
        
        extracted_titles = []
        for line in result.stdout.splitlines():
            # O output do C# é: [Nivel] Numeração Texto
            match = re.match(r'^\[(\d+)\]\s+(.*?)$', line)
            if match:
                lvl = int(match.group(1))
                content = match.group(2)
                
                # Remove IDs de bookmark (números longos no inicio)
                content = re.sub(r'^\d{8,}', '', content).strip()
                if not content: continue

                # Só nos importamos com Níveis hierárquicos (0..8), ignoramos texto corpo (9)
                if lvl < 9:
                    # Tenta separar "1.1 Texto"
                    num_match = re.match(r'^(\d+(?:\.\d+)*)\s+(.+)$', content)
                    if num_match:
                        extracted_titles.append({
                            'level': lvl,
                            'num': num_match.group(1),
                            'text': num_match.group(2).strip(),
                            'norm': normalize_text(num_match.group(2))
                        })
                    else:
                        # Título sem numeração explícita no texto extraído, mas com nível hierárquico
                        extracted_titles.append({
                            'level': lvl,
                            'num': '?',
                            'text': content.strip(),
                            'norm': normalize_text(content)
                        })
                        
        return extracted_titles

    except Exception as e:
        print(f"❌ Exception: {e}")
        return []

def compare_structures(map_titles, word_titles):
    matches = 0
    
    if not map_titles:
        print("   ⚠️ Map file is empty or has no numbered titles.")
        return

    print("\n   🔍 DETAILED MATCH LOG:")
    for m_item in map_titles:
        found = False
        best_score = 0
        best_match = None
        
        for w_item in word_titles:
            # 1. Match Exato Normalizado
            if m_item['norm'] == w_item['norm']:
                found = True
                best_match = w_item
                break
            
            # 2. Fuzzy Match (para pequenas variações de OCR ou digitação)
            if abs(len(m_item['norm']) - len(w_item['norm'])) < 15: # Otimização de performance
                ratio = difflib.SequenceMatcher(None, m_item['norm'], w_item['norm']).ratio()
                if ratio > 0.85:
                    if ratio > best_score:
                        best_score = ratio
                        best_match = w_item

        if found:
            matches += 1
            print(f"     ✅ MATCH:  Map[{m_item['num']}] '{m_item['text']}' == Word[{best_match['num']}] '{best_match['text']}'")
        elif best_match:
             matches += 1
             print(f"     ⚠️ FUZZY:  Map[{m_item['num']}] '{m_item['text']}' ~= Word[{best_match['num']}] '{best_match['text']}' ({best_score:.2f})")
        else:
            print(f"     ❌ MISSING: Map[{m_item['num']}] '{m_item['text']}' not found in Word.")

    score = (matches / len(map_titles)) * 100
    print(f"\n   🏁 Final Score: {score:.1f}% ({matches}/{len(map_titles)})")

def main():
    print("🚀 Iniciando Auditoria 'Cara-Crachá' em Massa com DocxReconstructor...\n")
    
    for md_file, word_file in FILE_MAP.items():
        print(f"📂 AUDITING SET: {md_file}")
        
        md_full = os.path.join(MAP_DIR, md_file)
        word_full = os.path.join(WORD_DIR, word_file)
        
        expected = parse_markdown_map(md_full)
        real = run_reconstructor(word_full)
        
        if expected and real:
             print(f"   📊 Stats: Map({len(expected)}) vs Word({len(real)}) items.")
             compare_structures(expected, real)
        elif not expected:
             print(f"   ⚠️ Map file not found or empty: {md_file}")
        elif not real:
             print(f"   ⚠️ Word file processing failed or empty: {word_file}")
        
        print("-" * 60 + "\n")

if __name__ == "__main__":
    main()
