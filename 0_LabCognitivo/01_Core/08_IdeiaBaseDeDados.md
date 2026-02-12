---
status: ideia
data: 2026-02-07
origem: "[[07_LogSessao2026-02-07]]"
tags:
  - ideia
  - obsidian
  - ferramentas
---
# Ideia: Base de Dados para as Notas do Vault

Criar uma visualização tipo banco de dados para as notas do `01_Core/`, aproveitando o frontmatter YAML que já existe (tags, status, data). Isso permitiria filtrar, ordenar e agrupar notas em tabelas dinâmicas — sem precisar abrir cada arquivo.

---

## Plugins Candidatos no Obsidian

### Dataview
- Motor de queries sobre notas
- Permite criar tabelas, listas e calendários usando uma linguagem própria (DQL) ou JavaScript
- Lê campos do frontmatter YAML automaticamente
- Exemplo: listar todas as notas com tag `demanda` e status `pendente` numa tabela
- [Documentação](https://blacksmithgu.github.io/obsidian-dataview/)
- [GitHub](https://github.com/blacksmithgu/obsidian-dataview)

### Database Folder
- Interface estilo Notion
- Cria views de tabela editável baseadas em pastas, tags ou queries Dataview
- Permite editar campos direto na tabela sem abrir a nota
- [Documentação](https://rafaelgb.github.io/obsidian-db-folder/)
- [GitHub](https://github.com/RafaelGB/obsidian-db-folder)

---

## Por que faz sentido para o LabCog

- O `01_Core/` já usa frontmatter YAML padronizado (tags de tipo e tema)
- Uma view de tabela daria visão geral instantânea do vault sem depender do `scan_core.py`
- Combinaria bem com o DiarioDeBordo (queries de logs por data, demandas pendentes, etc.)

---

## Próximos Passos

- [ ] Testar o Dataview no Obsidian com uma query simples sobre o `01_Core/`
- [ ] Avaliar se o Database Folder agrega valor ou se o Dataview puro já resolve
- [ ] Definir quais campos do frontmatter seriam colunas padrão da tabela
