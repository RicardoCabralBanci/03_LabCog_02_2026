---
tags:
  - conceito
  - memoria
  - knowledge-graph
  - estudo
---
# Como Funciona o Memory Palace

Análise técnica do repositório [jeffpierce/memory-palace](https://github.com/jeffpierce/memory-palace) baseada na leitura de `docs/architecture.md`, `docs/README.md`, `memory_palace/services/graph_service.py` e `memory_palace/database.py`.

## Repositório Local

Cópia completa em: `0_LabCognitivo/04_Referencias/memory-palace/`

## 1. Arquitetura Geral

**Problema**: Cada sessão de IA começa do zero. Context windows são finitos, sessões terminam e conhecimento morre.

**Solução**: Memória não fica DENTRO do modelo — fica AO LADO dele.

```
Claude/Gemini/Qwen (modelos)
       ↓
   MCP (protocolo aberto)
       ↓
  Memory Palace (camada de memória)
       ↓
  SQLite/PostgreSQL + Embeddings
```

### Conceito Chave

- **Context window** = memória de trabalho (scratchpad temporário)
- **Memory Palace** = armazenamento de longo prazo (persistente)

Igual cérebro humano: buffer de curto prazo + recuperação de longo prazo.

## 2. Knowledge Graph

Memórias não são isoladas — relacionam-se via **arestas tipadas, direcionais e pesadas**.

### Tipos de Relação Padrão

| Tipo | Descrição | Direcional? |
|------|-----------|-------------|
| `supersedes` | Nova memória substitui antiga | Sim |
| `relates_to` | Associação geral | Geralmente bidirecional |
| `derived_from` | Derivada de outra | Sim |
| `contradicts` | Conflito entre memórias | Bidirecional |
| `exemplifies` | Exemplo de conceito | Sim |
| `refines` | Adiciona detalhe/nuance | Sim |

**Tipos customizados são permitidos** — use nomes descritivos como `caused_by`, `blocks`, `spawned_by`.

### Exemplo de Uso

```python
# Criar link: Memória 42 → "derivada de" → Memória 17
link_memories(source_id=42, target_id=17, relation_type="derived_from")

# Traversar grafo: partir de 42, profundidade 2, só arestas de saída
traverse_graph(start_id=42, max_depth=2, direction="outgoing")
```

### Traversal (BFS)

Implementação usa **Breadth-First Search**:
- Começa de um nó inicial
- Explora vizinhos em camadas (depth 1, 2, 3...)
- Respeita filtros: tipo de relação, força mínima da aresta, direção
- Evita ciclos (marca nós visitados)

**Arquivo**: `memory_palace/services/graph_service.py:304` (função `traverse_graph`)

## 3. Busca Semântica com Centralidade

**Fórmula de ranking**:

```
score = (similaridade_semântica × 0.7)
      + (log(acessos + 1) × 0.15)
      + (centralidade_in_degree × 0.15)
```

### O Que Cada Componente Significa

1. **Similaridade semântica (70%)**: Embeddings próximos no espaço vetorial via Ollama
2. **Acessos (15%)**: Memórias frequentemente acessadas sobem no ranking
3. **Centralidade (15%)**: Nós com muitas conexões de entrada (hubs) são mais importantes

**Insight**: Memória com 10 conexões de entrada > memória isolada com texto similar.

## 4. Dual-Memory para Código

**Problema**: Embeddings de código cru produzem matches ruins. Query "como fazemos retry?" não casa com `def retry_logic(...)`.

**Solução**: Cada arquivo vira **2 memórias linkadas**:

1. **Prosa** (embedded) → Descrição em linguagem natural gerada por LLM
2. **Código** (stored, não embedded) → Implementação real

### Fluxo de Retrieval

```
Query: "como prevenimos duplicate payments?"
  ↓ (busca semântica na prosa)
Prosa: "PaymentService usa outbox pattern..."
  ↓ (graph traversal)
Código: [código completo do PaymentService.ts]
```

**Por que funciona**:
- Busca semântica acerta a prosa ("duplicate charges" casa com "prevent duplicate charges")
- Graph traversal puxa o código linkado sob demanda
- Context window pequeno: só carrega código dos arquivos relevantes

## 5. Database

Abstração sobre **SQLite** (pessoal) ou **PostgreSQL** (equipe/empresa).

| Backend | Casos de Uso | Agentes Concorrentes | Features |
|---------|--------------|----------------------|----------|
| SQLite | Pessoal | 1-10 | Write lock, zero config, arquivo único |
| PostgreSQL | Equipe/Empresa | 10-10.000+ | MVCC, pgvector, replicas |

**Troca de backend = 1 linha de config**, zero mudança de código.

### Arquivo

`memory_palace/database.py` → re-exporta de `database_v3.py`

Funções principais:
- `get_session()` → sessão do SQLAlchemy
- `session_scope()` → context manager com commit/rollback automático
- `pg_listen()` / `pg_notify()` → pub/sub para PostgreSQL

## 6. Auto-Linking

Novas memórias automaticamente encontram similares e criam arestas.

### Sistema de Dois Níveis

| Similaridade | Comportamento |
|--------------|---------------|
| ≥ 0.75 | **Auto-link criado** — LLM classifica o tipo de relação |
| 0.675-0.75 | **Sugerido** para revisão humana — sem aresta automática |

**Resultado**: O grafo se organiza sozinho conforme você adiciona memórias.

## 7. Handoff System (Mensagens entre Agentes)

Agentes podem se comunicar via mensagens tipadas.

### Exemplo

```python
# Desktop → Code
message(action="send",
        from_instance="desktop",
        to_instance="code",
        content="Indexe os arquivos de auth")

# Code checa mensagens
message(action="get", instance_id="code")

# Code responde
message(action="send",
        from_instance="code",
        to_instance="desktop",
        content="Indexados 12 arquivos. Veja memórias 200-212")
```

### Implementação por Backend

- **PostgreSQL**: `LISTEN`/`NOTIFY` (real-time push)
- **SQLite**: polling (verificação periódica)

## Pontos-Chave para o LabCog

1. **Memória persistente entre sessões** — resolve "cada dia começo do zero"
2. **Knowledge graph automático** — wikilinks + relações semânticas tipadas
3. **Busca semântica** — encontra por significado, não por palavra exata
4. **Centralidade como sinal de importância** — hubs pesam mais no ranking
5. **Local-first** — roda 100% na máquina (Ollama), zero dependência de cloud
6. **MCP protocol** — qualquer IA compatível pode usar
7. **Backend agnostic** — SQLite para uso pessoal, PostgreSQL para equipes

## Diferenças vs. LabCog Atual

| Aspecto | LabCog Atual | Memory Palace |
|---------|--------------|---------------|
| Relações | Wikilinks simples `[[arquivo]]` | Arestas tipadas + direção + peso |
| Busca | Grep/texto literal | Embeddings semânticos + centralidade |
| Persistência | Arquivos `.md` manuais | Banco de dados com auto-linking |
| Sessões | Logs escritos manualmente | `memory_reflect` extrai de transcripts |
| Interface | Editor de texto | MCP tools via Claude Desktop/Code |

## Próximos Passos Potenciais

- [ ] Testar instalação local do Memory Palace
- [ ] Explorar `memory_reflect` como substituto do `transcrever_sessoes.py`
- [ ] Avaliar uso como backend do LabCog
- [ ] Estudar schema do banco (tabelas `memories`, `memory_edges`)
- [ ] Comparar com [[29_Cognee|Cognee]] (alternativa em Neo4j)

## Referências Técnicas

- **Arquitetura**: `04_Referencias/memory-palace/docs/architecture.md`
- **Documentação**: `04_Referencias/memory-palace/docs/README.md`
- **Graph Service**: `04_Referencias/memory-palace/memory_palace/services/graph_service.py`
- **Database Layer**: `04_Referencias/memory-palace/memory_palace/database.py`

## Ver Também

- [[28_MemoryPalace|Memory Palace - Visão Inicial]]
- [[33_KnowledgeGraph|Knowledge Graph - Conceitos]]
- [[29_Cognee|Cognee - Alternativa Neo4j]]
