---
tags:
  - conceito
  - memoria
---
# Knowledge Graph

Um grafo de conhecimento é uma estrutura onde **nós** representam entidades (pessoas, conceitos, arquivos, ideias) e **arestas** representam relações entre elas.

## Diferença pra um banco de dados normal

- **Banco relacional**: tabelas com linhas e colunas. Ótimo pra dados estruturados. Péssimo pra navegar relações complexas.
- **Knowledge graph**: nós e arestas. Cada relação é um cidadão de primeira classe — tem tipo, direção e peso.

## Exemplo concreto no LabCog

Hoje temos wikilinks: `[[28_MemoryPalace]]`. Isso é um grafo primitivo — sabemos que A linka pra B, mas não sabemos *por quê*.

Um knowledge graph real teria:

```
[28_MemoryPalace] --resolve_problema--> [Memória entre sessões]
[29_Cognee]       --resolve_problema--> [Memória entre sessões]
[28_MemoryPalace] --concorre_com-----> [29_Cognee]
[30_Comparação]   --derivado_de------> [28_MemoryPalace]
[30_Comparação]   --derivado_de------> [29_Cognee]
```

As arestas têm **tipo** (`resolve_problema`, `concorre_com`, `derivado_de`), **direção** e opcionalmente **peso** (quão forte é a relação).

## Por que importa

- **Busca semântica**: "o que resolve o problema de memória?" encontra os dois, mesmo sem a palavra exata
- **Descoberta**: navegando o grafo, você encontra conexões que não faria manualmente
- **Contexto automático**: ao acessar um nó, o grafo traz os vizinhos relevantes junto

## No contexto das ferramentas analisadas

- [[28_MemoryPalace|Memory Palace]]: grafo em SQLite, edges tipadas, auto-linking por similaridade
- [[29_Cognee|Cognee]]: grafo em Neo4j, extração de entidades por LLM, consultas Cypher
