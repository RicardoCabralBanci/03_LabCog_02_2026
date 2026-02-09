---
tags:
  - template
---
# Template: Registro de Demanda

> **Propósito**: Documentar o "Porquê" e o "Como" de cada tarefa complexa antes da execução.
> **Uso**: Copie o conteúdo abaixo para criar um novo arquivo `NN_NomeDaDemanda.md` no `01_Core`.
> **Fluxo**: Usuário Pede → IA Propõe → IA Documenta → Discussão → Usuário Aprova → IA Executa.

---

```markdown
---
status: em_analise
data: YYYY-MM-DD
log_origem: "[[NN_LogSessao]]"
tags:
  - demanda
---
# [Nome Curto da Demanda]

## 1. Checklist de Entrega
- [ ] **Ação 1**: Descrição.
- [ ] **Ação 2**: Descrição.

## 2. Diagnóstico (Contexto & Porquês)
*Por que estamos fazendo isso? Qual o problema ou necessidade?*

## 3. Plano de Execução
*Como vamos resolver? Quais passos?*

### Arquivos Impactados
- [[NN_Arquivo|Nome]]
```
