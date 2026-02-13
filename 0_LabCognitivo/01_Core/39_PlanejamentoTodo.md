---
data: 2026-02-13
tags:
  - ideia
  - ferramenta
---
# Planejamento: Sistema de Afazeres / Task Management

Necessidade: Rastreamento de tarefas pendentes, sessões incompletas e próximos passos de forma estruturada.

## Opções Potenciais

**1. Taskwarrior + Timewarrior**
- CLI-based task management
- Tags, projetos, prioridades
- Sincronização via servidor próprio
- Tracking de tempo integrado
- Plain text backend (fácil de parsear)

**2. Org-mode (Emacs)**
- Formato texto simples
- Agenda com TODO/DONE states
- Arquivos `.org` podem viver no `01_Core/`
- Queries complexas via org-ql
- Exportação para Markdown

**3. Todo.txt**
- Formato extremamente simples: `(A) 2026-02-13 Tarefa com +projeto @contexto`
- Dezenas de clientes (CLI, mobile, web)
- Plain text, versionável via Git
- Ideal para integração com scripts Python

**4. TaskLite (Haskell CLI)**
- Inspirado no Taskwarrior, mais moderno
- SQLite backend
- CLI + biblioteca Python via subprocess
- Hooks para automação

**5. Sistema Próprio (Custom)**
- Formato YAML frontmatter + Markdown
- Arquivos `NN_Tarefa.md` no `01_Core/`
- Tag `tarefa` + metadata `status`, `prioridade`, `prazo`
- Scripts Python para dashboards
- Já integrado com workflow existente

## Proposta Inicial: Todo.txt + Script Python

**Por quê:**
- ✅ Formato simples (`todo.txt` na raiz)
- ✅ Git-friendly (um arquivo, fácil de versionar)
- ✅ CLI existente (`todo.sh`)
- ✅ Parser Python trivial (regex básico)
- ✅ Pode gerar relatórios Markdown para `00_Organization/`

**Estrutura:**
```
LabCogKHS_CLI/
├── todo.txt                    # Arquivo central de tarefas
├── done.txt                    # Histórico de tarefas completadas
└── 0_LabCognitivo/
    └── 02_Tools/
        └── todo_report.py      # Gera relatório Markdown
```

**Formato exemplo:**
```
(A) 2026-02-13 Testar instalação local do Memory Palace +LabCog @estudo
(B) 2026-02-13 Comparar Cognee vs Memory Palace +LabCog @pesquisa
x 2026-02-13 2026-02-13 Clonar repo memory-palace +LabCog @setup
```

## Próximos passos
- [ ] Decidir entre Todo.txt ou sistema próprio
- [ ] Criar script de integração
- [ ] Definir workflow (criar tarefas via CLI, visualizar em relatório Markdown)
