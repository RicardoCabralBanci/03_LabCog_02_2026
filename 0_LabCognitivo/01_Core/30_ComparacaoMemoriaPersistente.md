---
tags:
  - comparacao
  - ferramenta
  - memoria
---
# Comparação: Memory Palace vs Cognee

Duas soluções de memória persistente para agentes de IA. Mesmo problema, filosofias diferentes.

## Resumo rápido

| | [[28_MemoryPalace\|Memory Palace]] | [[29_Cognee\|Cognee]] |
| :--- | :--- | :--- |
| **Filosofia** | Local-first, leve, pessoal | Framework robusto, enterprise-ready |
| **Graph DB** | SQLite / PostgreSQL | Neo4j |
| **LLM** | Ollama (100% local) | OpenAI default, Ollama opcional |
| **Embeddings** | Ollama local | Múltiplos providers |
| **MCP** | Nativo (13 tools) | Nativo (cognify, search, save) |
| **Setup** | `pip install` + Ollama | Docker + Neo4j + config |
| **GPU** | Opcional (roda em CPU) | Depende do LLM escolhido |
| **Stars GitHub** | ~novo | ~12.3k |
| **Licença** | MIT | Apache 2.0 |

## Onde cada um brilha

### Memory Palace
- **100% local** — zero dependência de cloud, zero custo de API
- **Leve** — SQLite, sem Docker, sem Neo4j
- **Code indexing** — gera prosa a partir de código e busca sobre ela (técnica única)
- **Transcript reflection** — extrai memórias de logs JSONL automaticamente
- **Messaging entre instâncias** — pub/sub entre diferentes IAs
- **Centrality ranking** — score combina similaridade + frequência + centralidade no grafo
- **Baixa barreira de entrada** — roda em qualquer máquina com Python

### Cognee
- **Ingestão massiva** — 30+ fontes de dados (imagens, áudio, etc.)
- **Neo4j** — graph database real, mais poderoso para consultas complexas
- **Pipelines customizáveis** — define como o conhecimento é processado
- **Graph-aware embeddings** — embeddings que incorporam sinais do grafo
- **Ecossistema maduro** — mais stars, mais integrações, paper acadêmico publicado
- **Multi-LLM nativo** — troca de provider sem atrito
- **UI local** — interface visual em React

## Para o LabCog: qual faz mais sentido?

**Memory Palace parece o melhor fit inicial:**
- Rodamos local, sem budget pra APIs
- Setup simples — não queremos manter Neo4j + Docker
- O `memory_reflect` já faz o que nosso `transcrever_sessoes.py` tenta fazer
- 13 tools MCP prontas vs precisar montar pipelines
- Filosofia alinhada: memória pessoal, não enterprise

**Cognee faria sentido se:**
- Precisássemos ingerir formatos além de texto/código
- Quiséssemos consultas de grafo mais complexas (Cypher/Neo4j)
- O projeto crescesse pra algo multi-usuário
- Tivéssemos budget pra OpenAI ou GPU forte pra Ollama pesado

## Não são mutuamente exclusivos

Ambos são MCP servers. Em teoria, poderiam rodar em paralelo — Memory Palace pra memória leve do dia-a-dia, Cognee pra análise profunda quando necessário. Mas isso é over-engineering por enquanto.
