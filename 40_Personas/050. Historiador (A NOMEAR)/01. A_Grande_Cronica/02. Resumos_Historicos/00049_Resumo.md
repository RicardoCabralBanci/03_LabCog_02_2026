---
id_sessao: 00049
data: 2026-01-12
persona_ativa: Mestre em VBA / Arquiteto Web
tags: [Web, React, FastAPI, Bugfix, Paletizador]
consultas_realizadas: 0
classificacao: ?? Classe A (Engrenagem)
---

# Resumo da Sessão 049

**Link Original**: [[30_Historico/00049. 2026-01-12_Sessao_7914b88f.md]]

## CONTEXTO (O Problema)
O usuário relatou um bloqueio na interface de IHM das máquinas DVD: um popup informava que "apenas Clearline estava registrada" e impedia a abertura da tela. Além disso, surgiu a necessidade de criar um módulo totalmente novo para o **Paletizador**, que nunca existiu no sistema legado.

## 🛠️ INTERVENÇÕES TÉCNICAS (A Solução)
*   **Autópsia do Bloqueio**: Identificou-se que o erro de IHM era um bloqueio proposital (*hardcoded*) na `Sub IHM3` do script da Ribbon.
*   **Fundação Web**: Decisão de não criar o módulo Paletizador no Excel velho, mas sim iniciar uma aplicação Web moderna.
*   **Scaffolding**: Início da criação da estrutura em `25. Scripts/NewEngine/src/web` com:
    *   **Frontend**: React + Vite + Material UI.
    *   **Backend**: FastAPI (Python).
*   **Componentização**: Criação do componente `PaletizadorIHM.tsx` para replicar e melhorar a UX do seletor de IHM.

## 🧠 INSIGHTS & DESCOBERTAS (O Aprendizado)
*   **Dívida Técnica Intencional**: Descobriu-se que o sistema legado simulava erros de banco de dados para esconder funcionalidades não implementadas.
*   **Barreiras de Ambiente**: Enfrentamos dificuldades com políticas de execução do NPM e restrições de rede corporativa, contornadas pelo uso de `npx` e `cmd /c`.

## ⚖️ VEREDITO & LEGADO
*   **Status**: Em Desenvolvimento (A infraestrutura foi montada, mas a primeira execução falhou por arquivos não encontrados).
*   **Artefatos**: [[PaletizadorIHM.tsx]], [[main.py]] (Backend inicial).
