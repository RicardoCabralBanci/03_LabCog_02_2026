---
status: ideia
data: 2026-02-10
origem: "[[16_SolucaoIndicesAtivos]]"
sessao: "[[19_LogSessao2026-02-10]]"
tags:
  - ideia
  - planejamento
  - ia
  - estrutura
---
# Ideia: Agente Especializado em Classificação de Tags

> Um agente (prompt especializado ou script) que, ao criar ou encontrar uma nota existente, analisa seu conteúdo e adiciona automaticamente as tags YAML que fazem sentido.

Evolução de: [[16_SolucaoIndicesAtivos|Índices Ativos]] → **esta nota**

---

## Motivação

No modelo de Índices Ativos, tags são o único mecanismo de organização. Isso significa que a **qualidade das tags** determina a qualidade da navegação. Se uma nota não tem as tags certas, ela fica invisível para queries Dataview e TagFolder.

O problema: humanos são inconsistentes ao taguear. Esquecem tags, usam sinônimos, ou simplesmente não param pra pensar em todas as tags relevantes no momento da criação.

---

## O que o Agente faz

1. **Na criação de nota**: Recebe o conteúdo (título, corpo, contexto da sessão) e sugere/aplica tags
2. **Em notas existentes**: Escaneia notas com poucas tags ou tags genéricas e sugere complementos
3. **Consistência**: Usa a lista canônica de tags para evitar sinônimos e variantes

---

## Abordagem: Aprender pelo Exemplo

Antes de implementar, vamos **fazer manualmente** — nota por nota — o exercício de classificação. Isso serve para:

- Entender quais critérios usamos para decidir tags
- Identificar padrões e regras que podem ser codificados
- Descobrir edge cases (notas que não se encaixam bem)
- Definir a lista canônica de tags na prática, não na teoria

As observações ficam em [[21_ObservacoesAgenteTagger|Caderno de Observações]].

---

## Próximos Passos

- [ ] Exercício manual: classificar notas existentes do Core (sessão 2026-02-10)
- [ ] Documentar critérios e padrões em [[21_ObservacoesAgenteTagger]]
- [ ] Definir lista canônica de tags (resultado do exercício)
- [ ] Especificar o prompt/comportamento do agente
- [ ] Decidir: agente = prompt no Claude Code, script Python, ou ambos?
