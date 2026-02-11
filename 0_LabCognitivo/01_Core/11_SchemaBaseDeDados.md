---
status: ideia
data: 2026-02-09
origem: "[[08_IdeiaBaseDeDados]]"
sessao: "[[09_LogSessao2026-02-09]]"
tags:
  - ideia
  - planejamento
  - ferramentas
  - code
---
# Schema do Banco de Dados para o LabCog

Evolucao da [[08_IdeiaBaseDeDados|ideia original]]. Aqui definimos a estrutura concreta de um **SQLite local** que funciona como indice estruturado do `01_Core/`, sincronizado a partir do frontmatter YAML.

> **Principio**: O Markdown continua sendo a fonte da verdade. O DB e um indice derivado — um cache inteligente que permite queries que o YAML sozinho nao aguenta.

---

## Tabela `notes` — cada nota do Core e um registro

| Coluna | Tipo | Descricao |
|--------|------|-----------|
| `id` | INTEGER PK | O ID sequencial (08, 09, 10...) |
| `filename` | TEXT | `08_IdeiaBaseDeDados.md` |
| `title` | TEXT | Titulo extraido do `# Heading` |
| `status` | TEXT | `ideia`, `em_andamento`, `concluido`, `descartado` |
| `created_at` | DATETIME | Data de criacao (campo `data:` do YAML) |
| `updated_at` | DATETIME | Ultima modificacao do arquivo |

---

## Tabela `tags` — tabela normalizada de tags

| Coluna | Tipo | Descricao |
|--------|------|-----------|
| `id` | INTEGER PK | Auto-increment |
| `name` | TEXT UNIQUE | `ideia`, `log`, `ia`, `python`... |

---

## Tabela `note_tags` — relacao muitos-para-muitos

| Coluna | Tipo | Descricao |
|--------|------|-----------|
| `note_id` | INTEGER FK | -> notes.id |
| `tag_id` | INTEGER FK | -> tags.id |

Permite queries tipo: *"todas as notas que sao `ideia` E `ia` ao mesmo tempo"*.

---

## Tabela `links` — o grafo de wikilinks

| Coluna | Tipo | Descricao |
|--------|------|-----------|
| `id` | INTEGER PK | Auto-increment |
| `source_id` | INTEGER FK | Nota que contem o `[[link]]` |
| `target_id` | INTEGER FK | Nota referenciada |
| `context` | TEXT | Trecho ao redor do link (opcional, pra saber *por que* foi linkado) |

Queries possiveis:
- **Notas orfas**: target_id que nunca aparece
- **Hubs**: notas com mais links de entrada
- **Clusters**: grupos de notas muito interligadas

---

## Tabela `note_history` — versionamento de campos

| Coluna        | Tipo       | Descricao                                                   |
| ------------- | ---------- | ----------------------------------------------------------- |
| `id`          | INTEGER PK | Auto-increment                                              |
| `note_id`     | INTEGER FK | -> notes.id                                                 |
| `field`       | TEXT       | Qual campo mudou: `status`, `title`, `tags`...              |
| `old_value`   | TEXT       | Valor anterior                                              |
| `new_value`   | TEXT       | Valor novo                                                  |
| `changed_at`  | DATETIME   | Quando mudou                                                |
| `session_log` | TEXT       | Qual sessao causou a mudanca (ex: `09_LogSessao2026-02-09`) |

Exemplos do que responde:
- *"Quando essa ideia virou demanda?"* — `field='status'`, `new_value='em_andamento'`
- *"Que tags a nota 05 ja teve?"* — historico completo de reclassificacoes
- *"O que mudou na sessao de hoje?"* — filtra por `session_log`

---

## Diagrama de Relacionamentos

```
notes ──< note_tags >── tags
  │
  ├──< links (source)
  ├──< links (target)
  │
  └──< note_history
```

---

## Proximos Passos

- [ ] Decidir onde mora o `.db` (`02_Tools/` ou raiz do `0_LabCognitivo/`)
- [ ] Criar script Python `sync_db.py` que le o frontmatter e popula/atualiza o SQLite
- [ ] Definir com que frequencia o sync roda (manual? no `iniciar.ps1`? watcher?)
- [ ] Criar queries uteis de exemplo (orfas, hubs, timeline de mudancas)
