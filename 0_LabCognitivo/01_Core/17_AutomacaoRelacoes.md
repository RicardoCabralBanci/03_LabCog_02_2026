---
status: ideia
data: 2026-02-09
origem: "[[16_SolucaoIndicesAtivos]]"
sessao: "[[09_LogSessao2026-02-09]]"
tags:
  - ideia
  - planejamento
  - ferramentas
  - code
  - estrutura
---
# Automacao de Relacoes via DB + Script

> Como concretizar a [[16_SolucaoIndicesAtivos|proposta de Indices Ativos]]: em vez de manter indices manuais, automatizar as relacoes entre notas com um script + banco de dados.

Evolucao de: [[08_IdeiaBaseDeDados]] -> [[13_SchemaFinalDB]] -> [[16_SolucaoIndicesAtivos]] -> **esta nota**

---

## O Problema (recapitulando)

Hoje, criar 1 nota exige editar manualmente 3-4 outros arquivos ([[15_ProblemasEstruturaAtual|ver analise completa]]):
1. Criar o .md no Core
2. Atualizar o indice tematico em 00_Organization
3. Atualizar o log da sessao
4. Atualizar o DiarioDeBordo

Isso e padronizado, previsivel e chato — candidato perfeito para automacao.

---

## A Solucao: Script de Criacao de Notas

Um script que recebe parametros e faz tudo automaticamente:

```bash
python create_note.py --title "MinhaIdeia" --tags ideia,ia --diario 09
```

### O que o script faz:

1. **Descobre o proximo ID** disponivel no Core
2. **Cria o .md** com frontmatter YAML preenchido (tags, data, diario, status)
3. **Registra no DB** (SQLite) com todas as relacoes
4. **Atualiza o DiarioDeBordo** automaticamente (adiciona referencia)
5. **Atualiza o log da sessao** (se informado)

### O que o usuario NAO precisa mais fazer:

- Abrir indices e adicionar links manualmente
- Lembrar qual e o proximo ID
- Copiar templates e preencher frontmatter
- Se preocupar com indices desatualizados

---

## Schema Atualizado do DB

```sql
CREATE TABLE notes (
    id          INTEGER PRIMARY KEY,  -- ID sequencial
    filename    TEXT NOT NULL,         -- 08_IdeiaBaseDeDados.md
    title       TEXT,                  -- Titulo do # Heading
    status      TEXT,                  -- ideia, em_andamento, concluido, descartado
    tags        TEXT,                  -- JSON: ["ideia", "ia", "planejamento"]
    links       TEXT,                  -- JSON: [10, 11, 12]
    diario      TEXT,                  -- "09_LogSessao2026-02-09" (sessao que criou)
    created_at  TEXT,                  -- Data de criacao
    updated_at  TEXT,                  -- Ultima modificacao
    embedding   BLOB                  -- Vetor para busca semantica (futuro)
);
```

A coluna `diario` vincula automaticamente cada nota a sessao que a criou. Nunca mais precisa fazer esse link manualmente.

---

## Indices que Sobrevivem vs. Indices Substituidos

| Indice | Destino | Motivo |
|--------|---------|--------|
| `00_Central` | Vira dashboard gerado | Pode ser reconstruido por query no DB |
| `01_DiarioDeBordo` | **Permanece** (atualizado pelo script) | Registro cronologico, valor humano |
| `02_Soltos` | Removido | `SELECT * FROM notes WHERE tags = '[]'` |
| `03_Ferramentas` | Removido | `SELECT * FROM notes WHERE tags LIKE '%ferramenta%'` |
| `04_DesenvolvimentoDeIdeias` | Removido | `SELECT * FROM notes WHERE tags LIKE '%ideia%'` |

---

## Propriedades que o Script Pode Gerenciar

Alem de `diario`, o script pode cuidar de outras relacoes automaticas:

| Propriedade | O que faz | Exemplo |
|---|---|---|
| `diario` | Vincula a nota a sessao que a criou | `09_LogSessao2026-02-09` |
| `origem` | De qual nota essa ideia nasceu | `08_IdeiaBaseDeDados` |
| `evolui_para` | Pra onde essa nota evoluiu | (preenchido depois pelo script) |
| `tipo` | Tipo principal (extraido da primeira tag de tipo) | `ideia`, `log`, `demanda` |
| `ativo` | Se esta em trabalho agora | `true` / `false` |

Todas essas relacoes que hoje sao feitas manualmente via wikilinks em indices passam a ser **colunas no DB**, gerenciadas pelo script.

---

## Fluxo Completo Proposto

```
Usuario pede pra criar nota
        │
        ▼
  Script (Python)
   ├── Descobre proximo ID
   ├── Cria .md com frontmatter
   ├── Insere no SQLite
   ├── Atualiza DiarioDeBordo.md
   └── Atualiza log da sessao
        │
        ▼
  Obsidian ve o arquivo novo
  Bases/Dataview mostram nas views
  DB permite queries externas
```

---

## Proximos Passos

- [ ] Implementar `create_note.py` com os parametros basicos
- [ ] Implementar `sync_db.py` para popular o DB a partir das notas existentes
- [ ] Testar o fluxo completo: script cria nota -> DB atualiza -> Obsidian mostra
- [ ] Migrar notas existentes (adicionar campo `diario` no frontmatter)
- [ ] Decidir: o CLI (Claude/Gemini) chama o script, ou o script e independente?
