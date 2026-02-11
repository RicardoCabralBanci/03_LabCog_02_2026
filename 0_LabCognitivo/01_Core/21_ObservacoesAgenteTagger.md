---
data: 2026-02-10
origem: "[[20_IdeiaAgenteTagger]]"
sessao: "[[19_LogSessao2026-02-10]]"
tags:
  - doc
  - planejamento
  - ia
  - estrutura
---
# Observações para o Agente Tagger

> Caderno de anotações: pontos importantes observados durante o exercício manual de classificação de tags, nota por nota. Servirá de base para especificar o comportamento do agente.

Contexto: [[20_IdeiaAgenteTagger|Ideia do Agente Tagger]]

---

## Critérios Observados

### Nota 1: "Uma cabeça boa" (FastNotes)
- Nota é simultaneamente divagação, introspecção e ideia
- A pasta onde estava ("FastNotes") já dava uma pista de tipo, mas não é suficiente
- Música aparece como contexto/gatilho, não como tema central — deveria ter tag `musica`?
- **Problema levantado**: tags "maiores" (amplas) vs. tags "menores" (específicas)?
  - Ex: `autoestima` é granular demais? Deveria ser `saude-mental`? Ou ter ambas?
  - Ter tags amplas E específicas torna complexa a manutenção e associação
- A nota mistura reflexão pessoal + ideia + referências — múltiplos tipos possíveis
- **Observação do usuário**: "claramente é uma divagação, mas também é uma introspecção"
  - Metalinguagem: analisa a própria mente
  - Difícil de classificar em categorias rígidas

## Padrões Recorrentes

*(preenchido durante o exercício)*

## Edge Cases / Dúvidas

1. **Tags amplas vs. específicas**: Ter ambas (hierarquia) ou escolher um nível só?
   - Se amplas: perde precisão, muitas notas na mesma tag
   - Se específicas: explosão de tags, difícil lembrar quais existem
   - Se ambas: complexidade de manutenção, o agente precisa saber a hierarquia

## Tags Canônicas Identificadas

### Por tipo
*(lista definitiva após o exercício)*

### Por tema
*(lista definitiva após o exercício)*

## Regras para o Agente

*(síntese final: regras claras que o agente deve seguir)*
