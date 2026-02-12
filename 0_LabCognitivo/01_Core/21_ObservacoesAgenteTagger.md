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

### Nota 2: "Socialmente bem" (FastNotes)
- Nota quase sem conteúdo — funciona como hub/índice manual de links
- É um proto-índice artesanal: exatamente o que 16_SolucaoIndicesAtivos propõe automatizar
- **Problema concreto**: esse tipo de nota "atrapalha" — parece útil na criação, mas na prática fica abandonada e desatualizada
- **Insight**: o agente tagger precisa reconhecer notas que são índices disfarçados
  - Opção A: taguear como `indice` e deixar o sistema de Índices Ativos absorver
  - Opção B: migrar os links para tags nas notas-alvo e aposentar a nota-hub
- A nota e "Uma cabeça boa" parecem ser pilares de um mesmo sistema (mente, social...)
  - Sugere agrupamento por "área de vida" — mas isso é tag ou é estrutura?

## Padrões Recorrentes

1. **Notas-hub manuais**: usuario criava mini-índices por instinto, antes de formalizar o conceito. O agente precisa saber o que fazer com elas (migrar, taguear, ignorar?)
2. **Teste da pasta**: uma tag boa é aquela que "funcionaria bem como pasta" (TagFolder). Se imaginar a tag como pasta virtual e fizer sentido agrupar as notas ali, a tag é válida.
3. **`pessoal` é válida**: nem tudo no vault é pessoal — haverá notas técnicas, acadêmicas, etc. Então `pessoal` funciona como filtro real.

## Edge Cases / Dúvidas

1. **Tags amplas vs. específicas**: Ter ambas (hierarquia) ou escolher um nível só?
   - Se amplas: perde precisão, muitas notas na mesma tag
   - Se específicas: explosão de tags, difícil lembrar quais existem
   - Se ambas: complexidade de manutenção, o agente precisa saber a hierarquia

## Schema do Frontmatter (definido na sessão)

Campos obrigatórios para toda nota:
```yaml
data:       # YYYY-MM-DD (criação)
status:     # ideia, em_andamento, concluido, descartado
ativo:      # true/false
sessao:     # wikilink da sessão que criou ("pré-sessões" para legado)
tags:       # lista de tags
trofeus:    # lista de conquistas/marcos da nota (opcional, gamificação)
```

Campos removidos do schema original (17_AutomacaoRelacoes):
- `titulo` — já existe no `# Heading`
- `origem` — removido
- `evolui_para` — removido
- `id`, `filename`, `links`, `updated_at`, `embedding` — extraídos automaticamente pelo DB/script

## Tags Canônicas Identificadas

### Por tipo
*(lista definitiva após o exercício)*

### Por tema
*(lista definitiva após o exercício)*

## Regras para o Agente

*(síntese final: regras claras que o agente deve seguir)*
