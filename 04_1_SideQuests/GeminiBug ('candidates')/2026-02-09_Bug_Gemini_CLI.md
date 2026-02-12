# Bug Gemini CLI v0.27.3 - candidates undefined

**Data:** 2026-02-09
**Status:** Aguardando fix do Google

## Erro

```
[API Error: Cannot read properties of undefined (reading 'candidates')]
```

## Diagnostico

- O CLI usa o endpoint `cloudcode-pa.googleapis.com` (Code Assist)
- O servidor esta retornando respostas vazias (`response = undefined`)
- O codigo em `code_assist/converter.js:31` nao faz null check antes de acessar `response.candidates`
- Nao e problema de auth, token ou configuracao local

## Issues no GitHub

- https://github.com/google-gemini/gemini-cli/issues/18621
- https://github.com/google-gemini/gemini-cli/issues/18622

## Conclusao

Bug do lado do Google, reportado por varios usuarios no mesmo dia. Solucao: aguardar patch ou usar Gemini pelo browser.
