# 99. Todo - Estrutura da Pasta

Esta pasta organiza as tarefas pendentes, em andamento e concluídas do subprojeto.

## Estrutura

```
99. Todo/
  ├── README.md              ← Este arquivo
  ├── 01. Pendente/          ← Tarefas ainda não iniciadas
  ├── 02. Em Andamento/      ← Tarefas sendo trabalhadas no momento
  └── 03. Concluído/         ← Tarefas finalizadas (histórico)
```

## Como usar

1. Novas tarefas entram em `01. Pendente/` como arquivos `.md`
2. Ao iniciar uma tarefa, mover para `02. Em Andamento/`
3. Ao finalizar, mover para `03. Concluído/`

## Formato dos arquivos de tarefa

Cada tarefa é um arquivo `.md` nomeado com data e descrição curta:
- Exemplo: `2026-02-06_Leitura_Arquivos_Legado.md`

## Prioridade

Usar prefixo numérico para indicar prioridade quando necessário:
- `01_` = Urgente
- `02_` = Normal
- `03_` = Baixa prioridade
