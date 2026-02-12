---
data: 2026-02-06
status: em_analise
tags:
  - planejamento
  - ia
  - memoria
---
# Sistema de Memória do Laboratório Cognitivo

## Visão Geral

Sistema em 3 camadas para manter contexto entre sessões do Claude Code:

```
Camada 3 (alto nível)  →  CHANGELOG.md              — evolução do sistema
Camada 2 (resumo)      →  MEMORY.md                  — estado atual (200 linhas, auto-loaded)
Camada 1 (detalhe)     →  03_Memoria/*.md             — conversas transcritas
                              ↓ (futuro)
                           RAG + embeddings
                              ↓
                           Query semântica → MEMORY.md
```

## Fonte dos dados

O Claude Code armazena conversas em JSONL:

```
C:\Users\ricar\.claude\projects\C--Lab-Cognitivo-Script\
├── <session-uuid-1>.jsonl
├── <session-uuid-2>.jsonl
└── ...
```

Cada `.jsonl` contém eventos por linha. Tipos relevantes para transcrição:

| Tipo | Conteúdo |
|---|---|
| `user` | Mensagens do usuário. `message.content` = string ou array |
| `assistant` | Respostas da IA. `message.content` = array de blocos `text` e `tool_use` |
| `system` | Mensagens de sistema (tool results) |

Campos úteis em cada evento: `type`, `message`, `timestamp`, `sessionId`, `uuid`.

## Entregas

### 1. Script de Transcrição (`02_Tools/transcrever_sessoes.py`)

**Input**: Pasta `.claude/projects/C--Lab-Cognitivo-Script/*.jsonl`
**Output**: `03_Memoria/NN_Sessao_YYYY-MM-DD_<resumo>.md` para cada sessão

**Lógica**:
1. Listar todos os `.jsonl` na pasta de conversas do Claude
2. Comparar com arquivos já existentes em `03_Memoria/` (por sessionId no frontmatter YAML)
3. Para cada sessão nova, transcrever:
   - Extrair apenas eventos `user` e `assistant`
   - De `assistant`, extrair só blocos `type: text` (ignorar `tool_use`)
   - Formatar como diálogo markdown legível
4. Gerar frontmatter YAML com: sessionId, data, tags

**Formato de saída (exemplo)**:
```markdown
---
sessionId: "5c234957-be3a-4354-80ef-f5953d501c49"
data: 2026-02-06
tags:
  - sessao
---
# Sessão 2026-02-06

## Usuario
[conteúdo da mensagem]

## Assistente
[conteúdo da resposta]

## Usuario
[próxima mensagem]
...
```

**Decisões em aberto**:
- [ ] Incluir tool_use como blocos de código ou ignorar completamente?
- [ ] Incluir mensagens `system` (resultados de ferramentas) ou só user/assistant?
- [ ] Limite de tamanho por arquivo? (sessões muito longas podem gerar .md enormes)
- [ ] Gerar o nome do arquivo automaticamente (resumo via primeira mensagem do usuário?)

### 2. Launcher para PowerShell 7 (`02_Tools/iniciar.ps1`)

Script que automatiza o início de uma sessão:

```powershell
# 1. Rodar transcrição de sessões novas
python "$PSScriptRoot\transcrever_sessoes.py"

# 2. Abrir Claude Code CLI
claude
```

**Uso**:
```powershell
.\0_LabCognitivo\02_Tools\iniciar.ps1
```

### 3. (Futuro) RAG sobre 03_Memoria — ver [[05_SistemaRagMemoria|Planejamento RAG]]

Quando `03_Memoria` tiver volume suficiente, implementar busca semântica para alimentar automaticamente o MEMORY.md com contexto relevante.

## Atualização na arquitetura

A pasta `03_Memoria/` entra na estrutura:

```
0_LabCognitivo/
├── 00_Organization/
├── 01_Core/
├── 02_Tools/
│   ├── scan_core.py
│   ├── transcrever_sessoes.py    ← NOVO
│   └── iniciar.ps1               ← NOVO
└── 03_Memoria/                   ← NOVO
    └── (sessões transcritas em .md)
```

CLAUDE.md precisa ser atualizado para incluir `03_Memoria` na arquitetura.
