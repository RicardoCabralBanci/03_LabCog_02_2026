# LabCog -- LabCogKHS_CLI

> Vault Obsidian + repositorio Git.
> Este arquivo e carregado automaticamente pelo Claude Code em toda sessao.

## Contexto

- **Raiz / Vault Obsidian**: `C:\LabCogKHS_CLI\`
- **Branch principal**: `main`
- **Plataforma**: Windows

## Estrutura do Repositorio

```
C:\LabCogKHS_CLI\
├── CLAUDE.md                       # << ESTE ARQUIVO (contexto global)
├── skills\                         # Skills reutilizaveis (API keys, ferramentas, instrucoes)
├── 03_LabCog_02_2026\              # Versao atual de organizacao do LabCog
│   ├── 02_GeradorAutomaticoManuais_3.0\  # Projeto ativo (tem seu proprio CLAUDE.md)
│   │   ├── 01_Codigo_Atual\       # Codigo vivo (VBA, C#) -- tem CLAUDE.md
│   │   ├── 02_Documentacao\       # Docs do sistema atual -- tem CLAUDE.md
│   │   └── 80_Legado\             # Mapa do sistema antigo -- tem CLAUDE.md
│   └── 99_AFAZERES\               # Tarefas: AFAZERES.md (pendentes) + FEITOS.md (concluidos)
├── 999. Imagens\                   # Pasta compartilhada de imagens
├── 04. Arquivos e Projetos\        # LEGADO
├── 40_Personas\                    # LEGADO
├── 25. Scripts\                    # LEGADO
├── 30_Historico\                   # LEGADO
└── 31_Historicos_Resumidos\        # LEGADO
```

## Regras Operacionais

### Economia de Contexto
- **NAO abra arquivos legados** sem solicitacao explicita do usuario.
- **Conheca a existencia** das pastas legadas para referencia rapida.
- Quando precisar de contexto historico, pergunte antes de explorar.

### Hierarquia de CLAUDEs
Cada CLAUDE.md cuida do seu escopo. NAO duplique informacao entre niveis.
- **Este arquivo (raiz)**: mapa geral do vault, regras globais, convencoes.
- **GAM CLAUDE**: arquitetura, fluxo de geracao, maquinas suportadas. NAO detalhar modulos ou planilhas.
- **01_Codigo_Atual CLAUDE**: mapa dos modulos VBA e motor C#. Dono das tabelas de modulos.
- **02_Documentacao CLAUDE**: orientacao minima. Docs detalhados vivem como .md proprios na pasta.
- **80_Legado CLAUDE**: mapa do sistema antigo.

### Pasta 999. Imagens
- Caminho: `C:\LabCogKHS_CLI\999. Imagens\`
- Nomenclatura sequencial: `00000. Descricao.png`, `00001. Descricao.png`, etc.
- Usada para trocar imagens com o CLI (screenshots, diagramas, referencias).
- Ao criar ou solicitar nova imagem, seguir a sequencia numerica existente.

### Referencia: OpenClaw
- Caminho: `04. Arquivos e Projetos\02. Incubadora_de_Projetos\05. ClawdBot_IA\02. OpenClaw\`
- Tecnicas e ferramentas serao trazidas gradualmente, avaliadas uma por uma.

## Stack

- **TypeScript** para agentes, automacoes e ferramentas relacionadas ao OpenClaw.

## Convencoes

- Prefixos numericos em pastas para ordenacao: `01_`, `02_`, `03_`...
- CLAUDE.md em subprojetos quando houver contexto especifico relevante.
- Commits em portugues quando o contexto e PT-BR.
- Nomes de pasta/arquivo sem espacos em projetos novos (usar `_`).
