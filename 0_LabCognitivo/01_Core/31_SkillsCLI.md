---
tags:
  - ferramenta
  - ideia
---
# Skills CLI (find-skills)

- **Site**: [skills.sh](https://skills.sh/)
- **Comando**: `npx skills`
- **Fonte**: ClawdHub

## O que é

Package manager para skills de agentes de IA. Skills são pacotes modulares que estendem as capacidades de agentes com conhecimento especializado, workflows e ferramentas.

## Comandos principais

- `npx skills find [query]` — busca skills por keyword
- `npx skills add <owner/repo@skill>` — instala uma skill
- `npx skills check` — verifica atualizações
- `npx skills update` — atualiza todas
- `npx skills init` — cria uma skill nova

## Categorias de skills

- Web dev (react, nextjs, typescript, tailwind)
- Testing (jest, playwright, e2e)
- DevOps (deploy, docker, kubernetes, ci-cd)
- Docs (readme, changelog, api-docs)
- Code quality (review, lint, refactor)
- Design (ui, ux, accessibility)
- Productivity (workflow, automation, git)

## Por que interessa ao LabCog

- Ecossistema aberto de skills pra agentes — pode ter coisas úteis pra gestão de conhecimento
- Modelo de distribuição interessante (GitHub-based, `npx` pra instalar)
- Podemos tanto consumir skills existentes quanto criar as nossas
- Integra com Claude Code e outros agentes MCP-compatíveis
