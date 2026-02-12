# Ferramentas do Laboratório Cognitivo

Índice das ferramentas disponíveis em `02_Tools/`.

---

## Launcher

### `iniciar.ps1`
Inicializador completo de sessão. Executa em sequência:
1. Ativa o virtual environment (`venv`)
2. Roda `transcrever_sessoes.py` (transcreve sessões anteriores)
3. Abre o Claude Code CLI

```powershell
powershell "0_LabCognitivo/02_Tools/iniciar.ps1"
```

---

## Scanner

### `scan_core.py`
Escaneia o `01_Core/` e retorna:
- Próximo ID disponível
- Total de arquivos
- Arquivos agrupados por tag YAML
- Demandas em aberto

```bash
python "0_LabCognitivo/02_Tools/scan_core.py"
```

---

## Transcrição de Sessões

### `transcrever_sessoes.py`
Converte sessões brutas do Claude Code (`.jsonl` em `~/.claude/projects/`) para Markdown legível em `03_Memoria/`.
- Detecta automaticamente a pasta de projetos do Claude
- Pula sessões já transcritas (compara por `sessionId`)
- Sanitiza tokens e credenciais antes de salvar
- Gera frontmatter YAML com metadados (data, hora, tokens, caracteres)

```bash
python "0_LabCognitivo/02_Tools/transcrever_sessoes.py"
```
