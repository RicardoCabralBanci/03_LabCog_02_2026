---
tags:
  - planejamento
  - ia
---
# Orientacao para Escrever o CLAUDE.md

O CLAUDE.md e injetado no system prompt toda sessão. Cada linha custa tokens. Trate como código, não como documentação bonita.

## Princípios

1. **Tokens sao dinheiro.** Se uma linha nao muda o comportamento da IA, delete.
2. **Sem decoracao.** Separadores `---`, titulos redundantes (`# CLAUDE.md`), bold excessivo — tudo isso e gordura visual que a IA ignora.
3. **Uma informacao, um lugar.** Se "CamelCase" aparece em duas secoes, uma delas e lixo.
4. **Negativos > positivos.** Dizer "nao crie subpastas" e mais util que explicar a filosofia por tras da estrutura plana.
5. **Contexto minimo necessario.** A IA nao precisa saber a historia do projeto. Precisa saber o que fazer e o que nao fazer.
6. **Tabelas e listas > paragrafos.** Mais denso, menos tokens.
7. **Legado = uma frase.** "Tudo fora de `0_LabCognitivo/` e legado, nao mexa." Nao precisa de tabela com 4 entradas.
8. **Secoes vazias nao existem.** Se nao tem conteudo, nao tem secao.
9. **Tom direto.** A IA obedece "faca X" igual a "**OBRIGATORIO**: faca X". Sem gritar.
10. **Teste mental:** pra cada bloco, pergunte "se eu remover isso, a IA vai errar?" Se nao, remova.

## Anti-padroes

- Explicar *por que* o sistema existe (a IA nao se importa com motivacao)
- Formatacao bonita pro humano (quem le e a maquina)
- Repetir regras em secoes diferentes
- Manter secoes placeholder "para o futuro"
- Horizontal rules como separadores visuais

## Referencia

- [[25_LogSessao2026-02-11b|Sessao onde isso foi discutido]]
