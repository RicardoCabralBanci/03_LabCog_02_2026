---
status: ideia
data: 2026-02-09
origem: "[[12_DiscussaoBaseDeDados]]"
sessao: "[[09_LogSessao2026-02-09]]"
tags:
  - ideia
  - planejamento
  - ferramentas
  - code
---
# Schema Final do DB — Versao Simplificada

Evolucao de: [[08_IdeiaBaseDeDados]] -> [[11_SchemaBaseDeDados]] -> [[12_DiscussaoBaseDeDados]] -> **esta nota**.

---

## Decisoes Finais

| Decisao | Escolha | Motivo |
|---|---|---|
| Quantas tabelas | **1 tabela principal** | Escala do LabCog nao justifica normalizacao. Adicionar tabelas quando doer. |
| Tags | Campo JSON na tabela | SQLite suporta `json_each()`. Migrar pra tabela `note_tags` e trivial se precisar. |
| Links | Campo JSON na tabela | Mesma logica das tags. |
| Embeddings | Coluna BLOB reservada | Preparacao para busca semantica e RAG ([[05_SistemaRagMemoria]]) |
| Versionamento | **Git** (nao o DB) | O DB cuida do estado atual. Git cuida do historico. Sem duplicacao. |
| Linguagem do sync | Python | Consistente com tooling existente (`scan_core.py`, etc.) |
| Linguagem do bot/API | TypeScript | Alinhado com OpenClaw para projetos futuros |
| Onde mora o `.db` | `02_Tools/` | Referenciado em [[03_Ferramentas]] |
| Quando sincroniza | No startup (`iniciar.ps1`) | DB sempre atualizado no inicio da sessao |

---

## Tabela `notes`

```sql
CREATE TABLE notes (
    id          INTEGER PRIMARY KEY,  -- ID sequencial (08, 09, 10...)
    filename    TEXT NOT NULL,         -- 08_IdeiaBaseDeDados.md
    title       TEXT,                  -- Titulo extraido do # Heading
    status      TEXT,                  -- ideia, em_andamento, concluido, descartado
    tags        TEXT,                  -- JSON array: ["ideia", "ia", "planejamento"]
    links       TEXT,                  -- JSON array: [10, 11, 12] (IDs referenciados)
    created_at  TEXT,                  -- Data de criacao (campo data: do YAML)
    updated_at  TEXT,                  -- Ultima modificacao do arquivo
    embedding   BLOB                  -- Vetor de embedding (reservado para RAG)
);
```

---

## Queries de Exemplo

```sql
-- Todas as notas com tag 'ideia'
SELECT * FROM notes, json_each(tags)
WHERE json_each.value = 'ideia';

-- Notas que ninguem referencia (orfas)
SELECT * FROM notes
WHERE id NOT IN (
    SELECT json_each.value FROM notes, json_each(links)
);

-- Notas com 2 tags especificas ao mesmo tempo
SELECT n.* FROM notes n
WHERE EXISTS (SELECT 1 FROM json_each(n.tags) WHERE value = 'ideia')
  AND EXISTS (SELECT 1 FROM json_each(n.tags) WHERE value = 'ia');

-- Quantas notas por status
SELECT status, COUNT(*) FROM notes GROUP BY status;
```

---

## Proximos Passos

- [ ] Implementar `sync_db.py` em Python (le frontmatter, popula SQLite)
- [ ] Adicionar chamada ao sync no `iniciar.ps1`
- [ ] Referenciar no [[03_Ferramentas]]
- [ ] Testar queries de exemplo com dados reais
- [ ] Quando necessario: gerar embeddings e popular a coluna BLOB
