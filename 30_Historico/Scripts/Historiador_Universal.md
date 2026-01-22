# Historiador Universal de Sessões

**Script**: `Sincronizar_Memorias_Universal.py`
**Localização**: `[[30_Historico/Scripts/]]`

## O Que Este Script Faz?
Este script é um "Arqueólogo Digital" projetado para recuperar, organizar e preservar todas as interações realizadas com o Gemini CLI.

### Funcionalidades Chave:
1.  **Varredura Global**: Ele não olha apenas para a sessão atual. Ele vasculha recursivamente o diretório temporário do usuário (`.gemini/tmp`) em busca de *todas* as pastas de hash criadas pelo Gemini.
2.  **Unificação Temporal**: Coleta todos os arquivos JSON de todas as subpastas encontradas.
3.  **Ordenação Cronológica**: Lê a data interna (`startTime`) de cada sessão e ordena a lista do mais antigo para o mais recente.
4.  **Numeração Sequencial**: Gera arquivos Markdown numerados (`00001`, `00002`...) para criar uma linha do tempo perfeita e legível.
5.  **Tradução Rica**: Converte o JSON bruto em Markdown formatado, preservando "Pensamentos" e "Chamadas de Ferramentas" em blocos colapsáveis, sem truncar o conteúdo.

## Como Usar
Este script é executado automaticamente pelo arquivo de lote `[[30_Historico/ABRIR_GEMINI_FULL.bat]]` ao iniciar e encerrar o Gemini.

Para rodar manualmente:
```bash
python "C:\LabCogKHS_CLI\30_Historico\Scripts\Sincronizar_Memorias_Universal.py"
```

## Estrutura de Saída
Os arquivos são gerados na raiz de `[[30_Historico]]` com o formato:
`NNNNN. AAAA-MM-DD_Sessao_ID.md`

Exemplo:
`00035. 2025-12-29_Sessao_d0661cff.md`
