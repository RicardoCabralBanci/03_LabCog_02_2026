"""
scan_core.py — Scanner do Laboratório Cognitivo
Escaneia o 01. Core e retorna um resumo do estado atual.
Classifica arquivos pelas tags YAML, não pelo nome.
Uso: python scan_core.py
"""

import os
import re

CORE_PATH = os.path.join(os.path.dirname(__file__), "..", "01_Core")


def get_files():
    """Lista todos os .md do Core com seus IDs extraídos."""
    files = []
    for f in os.listdir(CORE_PATH):
        if f.endswith(".md"):
            match = re.match(r"^(\d+)_(.+)\.md$", f)
            if match:
                files.append({
                    "id": int(match.group(1)),
                    "name": match.group(2),
                    "filename": f
                })
    files.sort(key=lambda x: x["id"])
    return files


def extract_tags(filepath):
    """Extrai tags do frontmatter YAML de um arquivo .md."""
    tags = []
    try:
        with open(filepath, "r", encoding="utf-8") as fh:
            content = fh.read()
            # Busca o bloco YAML entre ---
            yaml_match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
            if yaml_match:
                yaml_block = yaml_match.group(1)
                # Extrai itens da lista tags:
                tag_matches = re.findall(r"^\s*-\s+(.+)$", yaml_block, re.MULTILINE)
                for tag in tag_matches:
                    tag = tag.strip().strip('"').strip("'")
                    if tag and tag != "tags:":
                        tags.append(tag)
    except Exception as e:
        print(f"Erro ao ler {filepath}: {e}")
    return tags


def scan_open_demands(files):
    """Lê arquivos com tag DEMANDA e retorna os que estão em aberto."""
    open_demands = []
    for f in files:
        filepath = os.path.join(CORE_PATH, f["filename"])
        tags = extract_tags(filepath)
        if "demanda" in [t.lower() for t in tags]:
            with open(filepath, "r", encoding="utf-8") as fh:
                content = fh.read()
                if "\u0001f6a7" in content or "Em Análise" in content:
                    open_demands.append(f)
    return open_demands


def main():
    files = get_files()
    last_id = max(f["id"] for f in files) if files else 0

    # Classificar por tags YAML
    categories = {}
    for f in files:
        filepath = os.path.join(CORE_PATH, f["filename"])
        tags = extract_tags(filepath)
        if not tags:
            tags = ["SEM_TAG"]
        for tag in tags:
            categories.setdefault(tag.upper(), []).append(f)

    open_demands = scan_open_demands(files)

    print("=" * 50)
    print("  SCAN DO CORE — Laboratório Cognitivo")
    print("=" * 50)
    print()
    print(f"  Próximo ID disponível: {last_id + 1}")
    print(f"  Total de arquivos:     {len(files)}")
    print()
    print("-" * 50)
    print("  ARQUIVOS POR TAG")
    print("-" * 50)
    for cat in sorted(categories.keys()):
        items = categories[cat]
        print(f"\n  [{cat}] ({len(items)} arquivos)")
        for f in items:
            print(f"    {f['id']:03d}. {f['name']}")

    print()
    print("-" * 50)
    print("  DEMANDAS EM ABERTO")
    print("-" * 50)
    if open_demands:
        for f in open_demands:
            print(f"    {f['id']:03d}. {f['name']}")
    else:
        print("    Nenhuma demanda em aberto.")

    print()
    print("=" * 50)


if __name__ == "__main__":
    main()
