---
tags:
  - doc
  - estrutura
  - principio
---
# Principio da Dupla Interface

> O sistema deve funcionar bem para **dois usuarios**: a pessoa e a IA.

---

## O que isso significa

O LabCognitivo nao e um caderno pessoal comum. E um sistema de gestao de conhecimento operado por **dois agentes**:

1. **O usuario humano** — que cria, revisa, decide e precisa reencontrar suas ideias
2. **A IA (CLI)** — que le, contextualiza, sugere, cria arquivos e mantem a estrutura

Qualquer decisao de design do sistema deve considerar ambos. Uma estrutura que so faz sentido para humanos (ex: organizacao visual bonita mas sem metadados) falha para a IA. Uma estrutura que so faz sentido para a IA (ex: IDs puros sem nomes legiveis) falha para o humano.

## Implicacoes praticas

- **Metadados YAML** devem ser consistentes — e assim que a IA encontra e classifica notas
- **Nomes de arquivo** devem ser legiveis — e assim que o humano navega pelo explorador
- **Indices ativos** devem ser poucos e claros — para que a IA saiba o que priorizar ao iniciar sessao
- **Wikilinks com alias** — o link e para a IA resolver, o alias e para o humano ler
