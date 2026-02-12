---
tags:
  - template
---
# Template: Log de Sessão

> **Uso**: Copie o conteúdo abaixo para criar um novo arquivo `NN_LogSessao...` no `01_Core`.

---

```markdown
---
status: [concluido / em_andamento]
data: YYYY-MM-DD
contexto_anterior: "[[NN_LogAnterior]]"
ia_assistente: [Claude Code / Gemini / outro]
tags:
  - log
---
# Sessão YYYY-MM-DD (Assunto)

### Arquivos de Referência
- [[NN_Arquivo|Nome da Referência]]

### Objetivos do Dia
- [ ] Objetivo 1

### Decisões & Mudanças

| ID | Demanda (O Quê) | Solução (Onde) | Status |
| :--- | :--- | :--- | :--- |
| `NN` | [[NN_Demanda\|Demanda Complexa]] | [[NN_Solucao\|Solução]] | concluido / pendente |
| `—` | Descrição curta da demanda simples | [[NN_Arquivo\|Arquivo]] | concluido / pendente |

### Arquivos da Sessão (Output)
- [[NN_Arquivo|Nome]]

### Estado Atual & Próximos Passos
- **Onde paramos**:
- **O que o "Eu de amanhã" precisa saber**:
```
