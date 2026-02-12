---
tags:
  - ferramenta
  - ideia
  - memoria
---
# Cognee

- **Repo**: [topoteretes/cognee](https://github.com/topoteretes/cognee)
- **Licença**: Apache 2.0
- **Stack**: Python 3.10-3.13, Neo4j, OpenAI/Ollama/Claude, Docker
- **Stars**: ~12.3k

## O que é

Framework open-source que transforma dados brutos em memória persistente para agentes de IA. Combina busca vetorial + knowledge graph (Neo4j) para criar repositórios de conhecimento interconectados e semanticamente pesquisáveis.

## Como funciona (3 estágios)

1. **`add`** — Ingestão de dados (30+ fontes: texto, arquivos, imagens, áudio)
2. **`cognify`** — LLM extrai entidades e relações → monta grafo no Neo4j
3. **`memify`** — Algoritmos adicionam relações semânticas e padrões ao grafo

Busca combina similaridade vetorial + travessia de grafo.

## Features principais

| Feature | Detalhe |
| :--- | :--- |
| Knowledge graph | Neo4j, entidades e relações extraídas por LLM |
| Vector search | Múltiplos backends (Weaviate, Qdrant, etc.) |
| 30+ fontes de dados | Conversas, arquivos, imagens, transcrições de áudio |
| Pipelines customizáveis | Blocos de conhecimento modulares, tarefas definidas pelo usuário |
| MCP nativo | Tools: cognify, save_interaction, search |
| Multi-LLM | OpenAI (default), Ollama (local), Claude, outros |
| Graph-aware embeddings | Fusão de vetores semânticos com sinais do grafo (hierarquia, tempo, tipo) |
| UI local | Frontend React/TypeScript |

## Por que interessa ao LabCog

- Ingestão de 30+ formatos — nossos .md, transcrições, etc.
- Knowledge graph real (Neo4j) vs wikilinks manuais
- MCP server — plugaria no Claude Code
- Pipelines customizáveis — podemos definir como o conhecimento é estruturado
- Multi-LLM — não fica preso a um provider

## Pontos de atenção

- **Depende de Neo4j** — mais pesado que SQLite, precisa de Docker ou instância separada
- **LLM cloud por default** — OpenAI é o default, Ollama é alternativa mas não é o foco
- **Mais enterprise** — arquitetura mais complexa que o memory-palace
- **Benchmark próprio** — a comparação que fazem com concorrentes tem viés reconhecido
