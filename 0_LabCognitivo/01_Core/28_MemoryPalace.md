---
tags:
  - ferramenta
  - ideia
  - memoria
---
# memory-palace

- **Repo**: [jeffpierce/memory-palace](https://github.com/jeffpierce/memory-palace)
- **Licença**: MIT
- **Stack**: Python 3.10+, Ollama (local), SQLite / PostgreSQL + pgvector

## O que é

Camada de memória semântica persistente para agentes de IA. Funciona como MCP server — qualquer cliente compatível (Claude Desktop, Claude Code) pode usar.

A tese central: memória não pertence ao modelo, pertence ao lado dele. Context window = memória de trabalho. Memory Palace = armazenamento de longo prazo.

## Por que interessa ao LabCog

- Resolve exatamente o problema de "cada sessão começa do zero"
- Roda 100% local (embeddings, LLM, tudo via Ollama)
- Knowledge graph com edges tipadas e direcionais entre memórias
- Extração automática de memórias a partir de transcrições (JSONL → memórias)
- Busca semântica com ranking por centralidade no grafo
- Multi-projeto: memórias podem pertencer a vários projetos ao mesmo tempo
- Messaging entre instâncias de IA (desktop, code, web)

## Features principais

| Feature | Detalhe |
| :--- | :--- |
| Semantic search | Embeddings locais via Ollama, busca por significado |
| Knowledge graph | Edges tipadas, pesadas, direcionais, auto-linking |
| Centrality ranking | Score = 70% similaridade + 15% frequência + 15% centralidade |
| Code indexing | Gera descrição em prosa do código, busca semântica sobre a prosa |
| Transcript reflection | Extrai memórias de logs de conversa (.jsonl) |
| Multi-instance messaging | Pub/sub entre instâncias de IA |
| 13 tools MCP | remember, recall, get, recent, archive, link, unlink, message, code, audit, reembed, stats, reflect |

## Requisitos

- Python 3.10+
- Ollama
- GPU NVIDIA 4GB+ VRAM (recomendado, não obrigatório)
- Modelos: nomic-embed-text + qwen3:1.7b (mínimo, roda em CPU)

## Relevância para implementação

- O `memory_reflect` pode substituir/complementar nosso `transcrever_sessoes.py`
- O knowledge graph é o que falta no nosso sistema de wikilinks — relações semânticas automáticas
- Poderia ser o backend de memória do LabCog em vez de arquivos .md soltos
- A arquitetura de serviços (memory, graph, message, maintenance, code, reflection) é referência de design
