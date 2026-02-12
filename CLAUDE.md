## Projeto

Gestão de conhecimento pessoal. Arquivos `.md` com YAML frontmatter, wikilinks e tags. Linguagem: PT-BR.

## Workspace

Versão ativa: `0_LabCognitivo/`. Tudo fora disso é legado — não mexa.

```
0_LabCognitivo/
├── CHANGELOG.md
├── 00_Organization/   # Índices de navegação (sem conteúdo denso)
├── 01_Core/           # Conteúdo .md — estrutura PLANA, sem subpastas
├── 02_Tools/          # Scripts (.py, .ps1, .json)
└── 03_Memoria/        # Sessões transcritas
```

## 01_Core/ — Regras

- Sem subpastas. Nunca.
- Nomeação: `NN_NomeCamelCase.md` (ID sequencial)
- Classificação por tags YAML, não pelo nome
- Próximo ID = maior existente + 1
- Wikilinks com alias: [[NN_Arquivo|Nome legível]]

## Protocolo de sessão

### Ao iniciar (nesta ordem)
1. Leia `SOUL.md` (raiz)
2. Leia `01_DiarioDeBordo.md`
3. Liste `01_Core/` para próximo ID
4. Crie log: `NN_LogSessao...` (template: `01_TemplateLog.md`)
5. Registre no `01_DiarioDeBordo.md`
6. Só então inicie o trabalho

### Firewall
- Não leia arquivos antigos por conta própria. Economize tokens.
- Use `01_DiarioDeBordo.md` como único índice.
- Só leia outros arquivos se o usuário pedir.

### Durante a sessão
- Registre decisões no log da sessão.

## Tags YAML

Todo arquivo do Core precisa de frontmatter com tags. Tags são o único mecanismo de classificação.
Consulte [[26_ListaCanonicaTags|Lista Canônica de Tags]] apenas quando precisar classificar um arquivo.

## Ferramentas (`02_Tools/`)

| Script | Função |
|---|---|
| `scan_core.py` | Estado do Core, próximo ID, arquivos por tag |
| `transcrever_sessoes.py` | `.jsonl` -> `.md` em `03_Memoria/` |
| `iniciar.ps1` | Launcher: venv + transcrição + Claude Code |
