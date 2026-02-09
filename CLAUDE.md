# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## O que e este projeto

O **Laboratorio Cognitivo** (LabCog) e um sistema de gestao de conhecimento pessoal inspirado em Zettelkasten. Usa estrutura **plana** de arquivos `.md` com metadados YAML, wikilinks `[[]]` e tags para organizacao. A IA (Claude Code) e parte ativa: mantem indices, sugere links, classifica notas e automatiza manutencao.

---

## Estrutura do Workspace

O diretorio raiz `C:\Lab_Cognitivo_Script` contem multiplas "geracoes" do projeto e ferramentas auxiliares:

| Diretorio                    | Proposito                                                                                          |
| ---------------------------- | -------------------------------------------------------------------------------------------------- |
| **`0_LabCognitivo/`**        | **Versao ativa** — Zettelkasten flat, onde todo o trabalho atual acontece.                          |
| `000. LabCognitivo/`         | Versao anterior (flat notes com IDs de 5 digitos, sistema de indices `00.xx`). Legado.             |
| `0000. LabCogLocalV1/`       | Primeira versao local (com subpastas por categoria). Legado.                                       |
| `001. LabCognitivo Folders/` | Variante com organizacao por pastas tematicas. Legado.                                             |
| `001.1 projetos/`            | Projetos externos (ex: ClawdBot). Nao faz parte do LabCog.                                        |
| `00.-Tarde-de-Domingo-/`     | Personas para Gemini CLI (Bibliotecario, Historiador, etc.).                                       |
| `Obsidian_S9_Fe/`            | Vault Obsidian pessoal (notas diarias, entretenimento, academico).                                 |
| `13. AI Notes/`              | Saida do script `find_orphan_notes.py` (relatorios).                                               |
| `50_RandNotes/`              | Notas avulsas organizadas por subpastas tematicas.                                                 |

### Versao Ativa: `0_LabCognitivo/`

```
0_LabCognitivo/
├── CHANGELOG.md           # Registro de evolucao do sistema
├── 00_Organization/       # APENAS indices de navegacao (proibido conteudo denso)
│   ├── 00_Central.md      # Ponto de entrada principal
│   ├── 01_DiarioDeBordo.md # Historico de sessoes
│   ├── 02_Soltos.md       # Indice de arquivos sem categoria
│   └── 03_Ferramentas.md  # Indice das ferramentas em 02_Tools/
├── 01_Core/               # ESTRUTURA PLANA — todo conteudo .md (SEM subpastas, nunca)
├── 02_Tools/              # Scripts e ferramentas (.py, .ps1, .json)
└── 03_Memoria/            # Sessoes do Claude Code transcritas em .md
```

**Regras criticas do `01_Core/`:**
- Estrutura 100% plana (sem subpastas). Se alguem sugerir criar subpastas aqui, recuse.
- Arquivos nomeados `NN_NomeCamelCase.md` (ID sequencial + CamelCase)
- Classificacao feita por tags YAML, nao pelo nome do arquivo
- Para descobrir o proximo ID disponivel, liste os arquivos e use o maior ID + 1

---

## Protocolo de sessao (para a IA)

### Ao iniciar (OBRIGATORIO, nesta ordem)
1. Este arquivo (CLAUDE.md) ja foi lido automaticamente.
2. Leia o `0_LabCognitivo/00_Organization/01_DiarioDeBordo.md` para situar o contexto recente.
3. Liste os arquivos do `0_LabCognitivo/01_Core/` para saber o proximo ID disponivel.
4. **CRIE IMEDIATAMENTE** o log da sessao (`NN_LogSessao...`) usando o template `01_TemplateLog.md`.
5. Registre a nova entrada no `01_DiarioDeBordo.md`.
6. **SOMENTE APOS O REGISTRO**, inicie o trabalho solicitado pelo usuario.

### Protocolo de Contencao (Firewall)
- **NAO** leia o conteudo de logs antigos ou outros arquivos do Core por conta propria.
- Consulte **apenas** o `01_DiarioDeBordo.md` (indice) para entender a linha do tempo.
- So leia arquivos internos do Core se o **usuario solicitar explicitamente**.
- **Motivo**: Evitar alucinacoes de contexto ao carregar informacao desnecessaria.

### Durante a sessao
- Ao criar arquivos no Core, use o proximo ID sequencial e nome em CamelCase.
- Use wikilinks com alias para legibilidade: `[[NN_Arquivo|Nome legivel]]`
- Registre decisoes e mudancas no log da sessao.

### Ao encerrar
- Atualize o `0_LabCognitivo/CHANGELOG.md` com o resumo do que mudou.
- Atualize o log da sessao com "Onde paramos" e "Proximos passos".
- Registre a nova entrada no `01_DiarioDeBordo.md` (se ainda nao registrada).

---

## Tags YAML (sistema de classificacao)

Todo arquivo no Core deve ter frontmatter YAML com pelo menos uma tag. As tags sao o **unico mecanismo de classificacao** — use quantas fizer sentido.

```yaml
---
tags:
  - [tipo: log, doc, demanda, solucao, nota, ideia, planejamento, code, template]
  - [tema: o que quiser — python, obsidian, pessoal, estudo, musica, etc.]
---
```

Uma nota pode ser simultaneamente `ideia` + `planejamento` + `ia`. Sem limitacao.

---

## Convencoes

- **Pastas**: `NN_NomeDaPasta` (underscore, sem espacos)
- **Arquivos Core**: `NN_NomeCamelCase.md`
- **Nao usar prefixos de tipo no nome.** A classificacao vem das tags YAML.
- **Wikilinks**: usar alias para legibilidade: `[[NN_Arquivo|Nome legivel]]`
- **Linguagem**: Projeto em portugues brasileiro. Codigo, logs e documentacao em PT-BR.

---

## Comandos

```bash
# Ativar virtual environment
cd C:\Lab_Cognitivo_Script
.\venv\Scripts\activate        # PowerShell
# ou: source venv/Scripts/activate  # Git Bash

# Escanear o Core (estado atual, proximo ID, arquivos por tag)
python "0_LabCognitivo/02_Tools/scan_core.py"

# Transcrever sessoes do Claude Code (.jsonl -> .md em 03_Memoria/)
python "0_LabCognitivo/02_Tools/transcrever_sessoes.py"

# Launcher completo (venv + transcricao + abre Claude Code)
powershell "0_LabCognitivo/02_Tools/iniciar.ps1"

# Encontrar notas orfas no vault LabCognitivo (sem links de entrada)
python find_orphan_notes.py

# Vigiar mudancas no vault e re-executar orphan scan automaticamente
python vault_watcher.py
```

---

## Scripts na Raiz

| Script | Funcao |
|--------|--------|
| `ai_linker_script.py` | Cria a estrutura inicial do vault (pastas + notas indice vazias). Bootstrap one-shot. |
| `find_orphan_notes.py` | Escaneia `LabCognitivo/` por notas sem links de entrada (orfas). Gera relatorio em `13. AI Notes/`. |
| `vault_watcher.py` | Usa `watchdog` para monitorar mudancas em `.md` e re-executar `find_orphan_notes.py`. |

**Dependencia Python**: `watchdog` (para `vault_watcher.py`)
