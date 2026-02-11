---
status: ideia
data: 2026-02-09
origem: "[[11_SchemaBaseDeDados]]"
sessao: "[[09_LogSessao2026-02-09]]"
tags:
  - ideia
  - planejamento
  - ferramentas
---
# Discussao e Decisoes sobre o DB do LabCog

Continuacao da [[11_SchemaBaseDeDados|definicao do schema]]. Aqui registramos duvidas levantadas, decisoes tomadas e esclarecimentos.

---

## O que o Obsidian ja faz (nao reinventar a roda)

O Obsidian ja possui mecanismos nativos para parte do que o DB faria:

| Funcionalidade | Como o Obsidian resolve |
|---|---|
| Ver tags de uma nota | Painel de tags (tag pane) |
| Filtrar notas por tag | Clique na tag ou busca `tag:#ideia` |
| Notas que referenciam a nota ativa | Painel de **Backlinks** |
| Notas referenciadas pela nota ativa | Painel de **Outgoing Links** |
| Visualizar relacoes entre notas | **Graph View** (grafo visual) |
| Queries sobre frontmatter | Plugin **Dataview** (DQL ou JS) |

### Entao por que um DB?

O DB **nao substitui** essas funcoes visuais do Obsidian. Ele serve para:

- **Acesso programatico** — scripts Python podem consultar o DB sem abrir o Obsidian
- **Queries complexas** que o Dataview nao faz bem (cruzamentos, historico, agregacoes)
- **Integracao com outros projetos** — ex: o [[10_IdeiaCLITelegram|bot Telegram]] poderia consultar o DB para responder perguntas sobre o vault
- **Tracking historico** — o Obsidian mostra o estado atual, o DB guarda a evolucao

---

## Esclarecimento: Versionamento

O `note_history` rastreia apenas **mudancas em propriedades YAML** (status, tags, titulo), nao conteudo textual.

| O que mudou | Quem rastreia |
|---|---|
| Propriedades (status, tags, titulo) | `note_history` no DB — estruturado, facil de consultar |
| Conteudo (texto reescrito, paragrafos) | **git** — cada commit e um snapshot, `git diff` mostra o que mudou |

Sao **complementares**:
- DB responde: *"quando essa ideia virou demanda?"*
- Git responde: *"o que exatamente foi reescrito no dia X?"*

---

## O que e uma Query?

Uma **query** e uma pergunta feita ao banco de dados em SQL (Structured Query Language).

Exemplos:

| Pergunta | Query SQL |
|---|---|
| Quais notas tem a tag `ideia`? | `SELECT * FROM notes JOIN note_tags ... WHERE tag = 'ideia'` |
| Quantas notas criei por mes? | `SELECT strftime('%Y-%m', created_at), COUNT(*) FROM notes GROUP BY 1` |
| Quais notas ninguem referencia? | `SELECT * FROM notes WHERE id NOT IN (SELECT target_id FROM links)` |

Voce faz uma pergunta estruturada, o banco responde com uma tabela. Vamos aprender SQL na pratica quando implementarmos!

---

## Decisoes Tomadas

| Decisao | Escolha | Motivo |
|---|---|---|
| Onde mora o `.db` | `02_Tools/` | Junto com os outros scripts, com referencia no [[03_Ferramentas]] |
| Linguagem do sync | Python | Ja e a linguagem dos outros scripts do lab |
| Quando sincronizar | No `iniciar.ps1` (startup) | Garante DB atualizado no inicio de cada sessao |
| Versionamento de conteudo | Git (ja configurado) | Complementa o `note_history` que cuida so de propriedades YAML |

---

## Proximos Passos

- [ ] Pesquisar como o Obsidian (Dataview) indexa tags e links internamente — entender o que ja existe
- [ ] Implementar `sync_db.py` com as 5 tabelas do [[11_SchemaBaseDeDados|schema]]
- [ ] Adicionar chamada ao sync no `iniciar.ps1`
- [ ] Referenciar a ferramenta no [[03_Ferramentas|indice de ferramentas]]
- [ ] Criar queries uteis de exemplo e documentar em nota propria
