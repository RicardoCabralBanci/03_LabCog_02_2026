---
data: 2026-02-06
status: 🟡 Planejamento
tags:
  - PLANEJAMENTO
  - ia
  - memoria
  - rag
---
# Planejamento: Sistema RAG para Memória de Longo Prazo

## Problema

O MEMORY.md do Claude Code tem limite de 200 linhas no system prompt. Conforme o Core cresce (centenas de notas), a IA perde capacidade de manter contexto relevante entre sessões.

## Solução proposta

Pipeline de RAG (Retrieval Augmented Generation) local que:
1. Indexa todas as notas do Core como embeddings
2. Na inicialização de sessão, busca apenas o contexto relevante
3. Injeta um resumo compacto no MEMORY.md ou diretamente no prompt

## Arquitetura conceitual

```
01. Core/*.md
       ↓
   Chunking (por nota ou por seção)
       ↓
   Embedding model (sentence-transformers local ou API)
       ↓
   Vector DB (LanceDB / ChromaDB / FAISS)
       ↓
   Query agent (busca semântica por contexto)
       ↓
   Resumo compacto → MEMORY.md ou prompt
```

## Componentes necessários

- **Indexador**: Script que lê o Core, faz chunking e gera embeddings. Roda após mudanças (pode integrar com vault_watcher).
- **Vector DB**: Armazenamento local dos embeddings. LanceDB é candidato (leve, sem servidor).
- **Query agent**: Recebe o contexto da sessão e retorna os chunks mais relevantes.
- **Gerador de resumo**: Compacta os chunks recuperados em um resumo de poucas linhas para o MEMORY.md.

## Decisões em aberto

- [ ] Escolher embedding model (local vs API — custo vs qualidade)
- [ ] Definir estratégia de chunking (nota inteira? por seção? por parágrafo?)
- [ ] Definir trigger de re-indexação (a cada save? a cada sessão? manual?)
- [ ] Decidir se o resumo vai no MEMORY.md ou direto no prompt via script

## Pré-requisitos

- Estrutura básica do Lab Cognitivo estabilizada
- Volume suficiente de notas no Core para justificar o investimento

## Referências

- LanceDB já presente no projeto ClawdBot (`001.1 projetos/00. ClawdBot/`)
- `find_orphan_notes.py` e `scan_core.py` como base para o indexador
