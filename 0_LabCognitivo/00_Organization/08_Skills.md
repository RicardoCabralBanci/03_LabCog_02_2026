# Skills Instaladas

Skills para agentes de IA instaladas via [Skills CLI](https://skills.sh/) (`npx skills`).

Local: `~\.agents\skills\`

---

## Ativas

*(nenhuma — removemos do autoload do Claude Code para economizar tokens)*

## Disponíveis (consultar quando necessário)

- **obsidian-markdown** — Referência completa do Obsidian Flavored Markdown (wikilinks, callouts, embeds, frontmatter, mermaid, LaTeX). Arquivo: `~\.agents\skills\obsidian-markdown\SKILL.md`
- **find-skills** — [[31_SkillsCLI|Referência]] — Package manager para descobrir e instalar novas skills (`npx skills find [query]`)

## Como usar

```bash
# Buscar skills
npx skills find [query]

# Instalar
npx skills add <owner/repo@skill> -g -y

# Ativar no Claude Code (symlink em ~\.claude\skills\)
# Desativar: remover o symlink
```
