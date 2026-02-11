---
tags:
  - ideia
  - planejamento
  - estrutura
---
# Solucao: Indices Ativos (Tags como Pastas)

> Proposta para substituir o sistema atual de indices estaticos por um modelo dinamico baseado em tags.

**Problema que resolve**: [[15_ProblemasEstruturaAtual|Ver analise completa dos problemas]]
**Implementacao tecnica**: [[17_AutomacaoRelacoes|Automacao via DB + Script]]
**Principio fundador**: [[18_PrincipioDuplaInterface|Dupla Interface (usuario + IA)]]

---

## Principio Central

> **Tags SAO as pastas. Indices sao VIEWS temporarias, nao artefatos permanentes.**

No Zettelkasten flat, a estrutura nao vem de pastas fisicas nem de indices manuais — vem das **tags YAML** que cada nota ja carrega. Um "indice" nada mais e do que uma **consulta filtrada por tag**, materializada temporariamente quando necessario.

---

## 1. Indice = Manifesto da Tag

Cada tag importante tem um arquivo-guia que funciona como **orientacao**:
- O que essa tag significa
- Quando usar
- Quais notas ativas pertencem a ela (via Dataview, gerado automaticamente)

O nome do indice E o nome da tag. Ex: a tag `ideia` tem um arquivo chamado `IDX_ideia.md`.

Isso resolve o problema 5 (confusao indice vs. conteudo): o indice NAO e um mapa de links manual. E um manifesto + query automatica.

---

## 2. Apenas Indices Ativos existem no painel de navegacao

Em vez de manter N indices permanentes, o `00_Organization/` (ou como se chame no futuro) contem **apenas o que esta ativo agora**:

- **O que estou pensando/fazendo neste momento** tem indice visivel
- **O que nao esta ativo** nao precisa de indice — as tags nas notas + Dataview/TagFolder permitem encontrar

Quando um tema "esfria", seu indice sai do painel ativo. As notas continuam encontraveis pelas tags. Quando o tema "reaquece", o indice volta — possivelmente com uma query Dataview que se auto-atualiza.

---

## 3. Questao em aberto: Tags atomicas vs. compostas

**Cenario**: Quero ver todas as notas sobre "desenvolvimento do LabCognitivo".

**Opcao A — Tag composta**: `#dev-labcog`
- Um indice direto: `IDX_dev-labcog.md`
- Problema: nao componivel. Se quiser ver "todo desenvolvimento" ou "tudo sobre labcog" separadamente, precisa de tags extras.

**Opcao B — Tags atomicas**: `#desenvolvimento` + `#labcognitivo`
- Componivel: posso ver so `#desenvolvimento`, so `#labcognitivo`, ou a intersecao
- Indices: `IDX_desenvolvimento.md` e `IDX_labcognitivo.md` existem separadamente
- Intersecao: resolvida por query Dataview (`FROM #desenvolvimento AND #labcognitivo`)
- Problema: como o indice de uma tag "conversa" com o de outra?

**Opcao C — Tags hierarquicas (nativas do Obsidian)**: `#projeto/labcog`
- O Obsidian suporta tags aninhadas: `#projeto/labcog`, `#projeto/clawdbot`
- A busca por `#projeto` retorna todas as sub-tags
- Problema: adiciona complexidade, pode nao compor bem com TagFolder

**Decisao pendente**: Qual abordagem usar? Possivelmente um hibrido — tags atomicas para tipo (`ideia`, `log`, `demanda`) e tags hierarquicas para tema (`projeto/labcog`, `tema/ia`).

---

## 4. Ferramental: Obsidian + Plugins

Dois plugins resolvem grande parte da mecanica:

### TagFolder
> Tags literalmente viram pastas no painel lateral.

- Cada tag aparece como uma pasta virtual
- Notas com multiplas tags aparecem em multiplas "pastas"
- Suporta combinacoes de tags (intersecoes visuais)
- Pinning de tags prioritarias (= indices ativos!)
- Link: https://github.com/vrtmrz/obsidian-tagfolder

### Dataview
> Transforma o vault em banco de dados consultavel.

Indices automaticos dentro de qualquer nota:

```dataview
TABLE status, data
FROM #desenvolvimento AND #labcognitivo
SORT data DESC
```

- Indices se auto-atualizam — resolve problemas 1 e 2
- Pode gerar dashboards, listas de tarefas, mapas de notas
- Complementa o script de automacao proposto em [[17_AutomacaoRelacoes]]
- Link: https://github.com/blacksmithgu/obsidian-dataview

### Como se encaixam

| Necessidade | Ferramenta |
|-------------|------------|
| Navegar tags como pastas (visual) | TagFolder |
| Indices dinamicos dentro de notas | Dataview |
| Criacao automatizada de notas | Script Python ([[17_AutomacaoRelacoes]]) |
| Busca semantica (futuro) | DB SQLite com embeddings |

---

## 5. Templates por tipo de tag

Cada tipo de tag tem um template sugerido. A ideia e que um **agente especializado** possa ser desenvolvido para cada tag, sabendo exatamente como criar e manter notas daquele tipo.

| Tag | Template | Agente |
|-----|----------|--------|
| `ideia` | Titulo, Descricao, Status, Links | Agente de ideias: classifica, sugere conexoes |
| `demanda` | Titulo, Contexto, Criterio de aceite | Agente de demandas: rastreia status, prioriza |
| `solucao` | Demanda que resolve, Implementacao | Agente de solucoes: vincula a demandas |
| `log` | Data, Objetivos, Decisoes | Agente de sessao: cria automaticamente |
| `doc` | Titulo, Conteudo, Referencias | Agente de documentacao: mantem atualizado |
| `principio` | Enunciado, Implicacoes | Agente de principios: verifica consistencia |

**Nota**: "agente" aqui pode ser um prompt especializado, um script, ou uma combinacao. O importante e que cada tag tem um **comportamento esperado** associado.

---

## 6. Fluxo simplificado de criacao de nota

**Antes (atual)**:
1. Criar nota no Core
2. Abrir indice Central → adicionar link
3. Abrir indice tematico → adicionar link
4. Abrir Desenvolvimento de Ideias → adicionar link
5. (Desistir no passo 3)

**Depois (proposto)**:
1. Criar nota no Core com tags YAML apropriadas
2. **Fim.** Dataview e TagFolder cuidam da visibilidade.

---

## Proximos passos

- [ ] **Decidir estrategia de tags**: atomicas, compostas ou hierarquicas?
- [ ] **Instalar e testar TagFolder** no vault do Obsidian
- [ ] **Instalar e testar Dataview** — escrever primeiras queries
- [ ] Definir a lista de tags canonicas (tipo + tema)
- [ ] Criar/atualizar os templates por tipo de tag no Core
- [ ] Implementar script de criacao de notas ([[17_AutomacaoRelacoes]])
- [ ] Migrar notas existentes para o novo modelo
- [ ] Renomear `00_Organization/` para refletir o novo papel

---

## Status

**Em discussao** — refinando o modelo conceitual antes de implementar.
