---
status: implementado
data: 2026-02-11
origem: "Anúncio oficial Obsidian (@obsdmd)"
ultima_atualizacao: 2026-02-11
logs_relacionados: "[[24_LogSessao2026-02-11|Log 2026-02-11]]"
tags:
  - ideia
  - obsidian
  - cli
  - automacao
  - ferramentas
  - api-rest
  - testado
---
# Ideia: Integração do Obsidian CLI no Projeto LabCog

Utilizar o **Obsidian CLI** (lançado em fevereiro de 2026 na versão 1.12.0 Desktop) para automatizar operações no vault, integrar com scripts externos e possibilitar controle programático do Obsidian via terminal.

---

## O que é o Obsidian CLI

O Obsidian CLI é uma interface de linha de comando oficial que permite:
- Controlar o Obsidian diretamente do terminal
- Executar qualquer operação que pode ser feita na GUI
- Automatizar workflows e integrações
- Criar scripts para manipulação do vault
- Integrar com ferramentas de automação (Claude Code, Python, PowerShell, etc.)

**Anúncio oficial**: [@obsdmd no Twitter](https://x.com/obsdmd/status/2021241384057930224)

---

## Por que faz sentido para o LabCog

### Automação de Sessões
- Criar arquivos de log automaticamente via script
- Atualizar `01_DiarioDeBordo.md` programaticamente
- Executar o protocolo de sessão (leitura + criação de log) via CLI

### Integração com Claude Code
- Claude pode invocar comandos CLI diretamente via Bash tool
- Criar e editar notas no Core sem precisar usar Write/Edit tools
- Manter consistência com os plugins do Obsidian (Dataview, Database Folder, etc.)

### Scripts de Manutenção
- Automatizar escaneamento do Core (`scan_core.py` pode chamar CLI)
- Atualizar índices automaticamente
- Validar estrutura YAML dos arquivos
- Gerar relatórios e estatísticas do vault

### Workflows Avançados
- Integração com ferramentas externas (Telegram, webhooks, etc.)
- Processar notas em batch
- Sincronizar com bases de dados externas
- Criar pipelines de processamento de conhecimento

---

## Casos de Uso Específicos para LabCogKHS_CLI

### 1. Protocolo de Sessão Automatizado
```bash
# Iniciar sessão automaticamente
obsidian open "C:\LabCogKHS_CLI\03_LabCog_02_2026"
obsidian run-command "criar-log-sessao"
obsidian open-note "01_DiarioDeBordo.md"
```

### 2. Criar Notas via Script
```python
# Python script que usa Obsidian CLI
import subprocess
import datetime

def criar_nota_core(titulo, tags, conteudo):
    id_proximo = obter_proximo_id()
    arquivo = f"{id_proximo}_{titulo}.md"
    # Usar CLI ao invés de manipular arquivos diretamente
    subprocess.run(["obsidian", "create-note", arquivo, "--content", conteudo])
```

### 3. Sincronizar com Projetos Técnicos
- Criar notas Zettelkasten sobre desenvolvimento do GAM 3.0
- Referenciar `[[../03_Projetos_KHS/...]]` via CLI
- Automatizar criação de índices cruzados

### 4. Integração com Claude Code
- Claude pode executar comandos CLI durante sessões
- Atualizar memória de longo prazo automaticamente
- Criar links bidirecionais entre notas

---

## Comandos Potenciais (Baseado na Descrição)

> **Nota**: Documentação oficial em [help.obsidian.md/cli](https://help.obsidian.md/cli)

Comandos esperados:
- `obsidian open <vault-path>` - Abrir vault
- `obsidian create-note <nome>` - Criar nota
- `obsidian search <query>` - Buscar no vault
- `obsidian run-command <comando>` - Executar comando/plugin
- `obsidian open-note <nota>` - Abrir nota específica
- Possível integração com plugins (Dataview, Templater, etc.)

---

## ✅ Resultados dos Testes (2026-02-11)

> Ver detalhes completos em [[24_LogSessao2026-02-11|Log da Sessão 2026-02-11]]

### Status da Versão Obsidian

**Versão Instalada**: 1.11.7 (estável público)
**Versão com CLI Oficial**: 1.12.1+ (Catalyst/Early Access apenas)
**Conclusão**: CLI oficial ainda não disponível na versão pública

### Métodos de Automação Testados

#### 1. ❌ CLI Oficial (Obsidian 1.12+)
- **Status**: Não disponível (requer v1.12+)
- **Disponibilidade**: Apenas para usuários Catalyst ($25 USD)
- **Previsão**: Aguardar release público (sem data definida)

#### 2. ✅ Obsidian URI Schemes
- **Protocolo**: `obsidian://`
- **Vault ID**: `cd909d30a06e644a`
- **Vault Path**: `C:\LabCogKHS_CLI`

**Comandos testados**:
```bash
# ✅ Abrir vault (FUNCIONA)
start "obsidian://open?vault=cd909d30a06e644a"

# ✅ Abrir nota específica (FUNCIONA)
start "obsidian://open?vault=cd909d30a06e644a&file=03_LabCog_02_2026/CLAUDE.md"

# ⚠️ Criar nota com conteúdo (LIMITADO)
# Parâmetro 'content' não funciona como esperado
start "obsidian://new?vault=cd909d30a06e644a&file=path/nota.md"
```

**Avaliação**: Bom para navegação, limitado para automação de conteúdo.

#### 3. ✅ Local REST API (SOLUÇÃO MEIO MAIS OU MENOS!)

**Plugin**: `obsidian-local-rest-api` v3.4.3
**Status**: ✅ Instalado, habilitado e FUNCIONANDO
**Endpoint**: `https://127.0.0.1:27124`
**Método de Autenticação**: Bearer Token

**Configuração**:
```json
{
  "port": 27124,
  "apiKey": "c66d870ab3b303c639e4e9d111a8c39e11930820d38b56ba2d65187021cb0723"
}
```

**Comandos testados com SUCESSO**:

```bash
# ✅ Listar arquivos do vault
curl -k -X GET https://127.0.0.1:27124/vault/ \
  -H "Authorization: Bearer c66d870ab3b303c639e4e9d111a8c39e11930820d38b56ba2d65187021cb0723"

# ✅ Criar nota com conteúdo YAML + Markdown
curl -k -X POST https://127.0.0.1:27124/vault/03_LabCog_02_2026/0_LabCognitivo/01_Core/23_TesteAPICLI.md \
  -H "Authorization: Bearer c66d870ab3b303c639e4e9d111a8c39e11930820d38b56ba2d65187021cb0723" \
  -H "Content-Type: text/markdown" \
  --data-binary $'---\ntags:\n  - teste\n---\n# Título\n\nConteúdo aqui'

# ✅ Ler nota existente
curl -k -X GET https://127.0.0.1:27124/vault/path/to/note.md \
  -H "Authorization: Bearer c66d870ab3b303c639e4e9d111a8c39e11930820d38b56ba2d65187021cb0723"

# ✅ Buscar no vault (endpoint search)
curl -k -X POST https://127.0.0.1:27124/search/ \
  -H "Authorization: Bearer c66d870ab3b303c639e4e9d111a8c39e11930820d38b56ba2d65187021cb0723" \
  -H "Content-Type: application/json" \
  -d '{"query":"termo de busca"}'
```

**Resultado**: [[23_TesteAPICLI|Nota criada com sucesso via REST API]]

### Comparação dos Métodos

| Método          | Disponível | Criar Notas | Editar | Buscar      | Automação                                             | Complexidade |
| --------------- | ---------- | ----------- | ------ | ----------- | ----------------------------------------------------- | ------------ |
| **CLI Oficial** | ❌ (v1.12+) | ✅           | ✅      | ✅           | ✅ Excelente                                           | Baixa        |
| **URI Schemes** | ✅          | ⚠️ Limitado | ❌      | ⚠️ Abre GUI | ⚠️ Limitada                                           | Baixa        |
| **REST API**    | ✅          | ✅           | ✅      | ✅           | ✅ Excelente mas perde qualidade da forma que fizemos  | Média        |

**Vencedor**: **REST API** (disponível agora, completo, estável)

### Exemplo Python com REST API

```python
import requests
import json

# Configuração
OBSIDIAN_API = "https://127.0.0.1:27124"
API_KEY = "c66d870ab3b303c639e4e9d111a8c39e11930820d38b56ba2d65187021cb0723"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "text/markdown"
}

def criar_nota_core(id_nota, titulo, tags, conteudo):
    """Cria nota no Core do Zettelkasten via REST API"""

    # Montar frontmatter YAML
    frontmatter = f"""---
tags:
{chr(10).join(f'  - {tag}' for tag in tags)}
---
# {titulo}

{conteudo}
"""

    # Path da nota
    path = f"03_LabCog_02_2026/0_LabCognitivo/01_Core/{id_nota}_{titulo}.md"
    url = f"{OBSIDIAN_API}/vault/{path}"

    # Criar via POST
    response = requests.post(
        url,
        headers=HEADERS,
        data=frontmatter.encode('utf-8'),
        verify=False  # SSL self-signed
    )

    return response.status_code == 200

# Exemplo de uso
criar_nota_core(
    id_nota=25,
    titulo="TestePython",
    tags=["teste", "python", "api"],
    conteudo="Esta nota foi criada via script Python!"
)
```

### Recursos da REST API Disponíveis

- ✅ **CRUD de notas**: Create, Read, Update, Delete
- ✅ **Busca**: Search endpoint com queries
- ✅ **Listar vault**: Explorar estrutura de pastas
- ✅ **Executar comandos**: Invocar comandos do Obsidian
- ✅ **Periodic notes**: Criar/buscar daily/weekly notes
- ✅ **PATCH endpoint**: Inserir conteúdo em seções específicas

**Documentação completa**: [API Docs](https://coddingtonbear.github.io/obsidian-local-rest-api/)

---

## Próximos Passos

### Concluídos ✅
- [x] Verificar se Obsidian CLI está disponível na instalação atual → **Não (requer v1.12+)**
- [x] Testar comandos básicos no terminal → **URI e REST API testados**
- [x] Habilitar Local REST API plugin → **Funcionando**
- [x] Criar nota de teste via API → [[23_TesteAPICLI|Sucesso]]

### Em Andamento 🔄
- [ ] Criar scripts Python de exemplo usando REST API
- [ ] Integrar REST API com protocolo de sessão do Zettelkasten
- [ ] Criar wrapper Python para simplificar chamadas à API

### Futuro 📅
- [ ] Aguardar release público da v1.12 para testar CLI oficial
- [ ] Explorar plugin Advanced URI para funcionalidades extras
- [ ] Documentar todos os endpoints REST API úteis
- [ ] Criar aliases bash/PowerShell para comandos comuns
- [ ] Integrar com `02_Tools/` (scripts de manutenção)
- [ ] Automatizar criação de logs de sessão via API
- [ ] Explorar integração com Dataview via API

---

## Limitações Conhecidas

### REST API - Encoding de Caracteres
⚠️ **Problema**: Caracteres especiais (emojis, acentos) podem não ser codificados corretamente via curl no Windows.

**Workaround**:
```python
# Usar Python/requests ao invés de curl para melhor suporte UTF-8
import requests
response = requests.post(url, data=conteudo.encode('utf-8'), ...)
```

### CLI Oficial - Disponibilidade
⚠️ **Limitação**: Requer Obsidian v1.12+ (Catalyst/Early Access)
- Versão pública atual: 1.11.7
- Solução: Usar REST API enquanto aguarda release público

---

## Referências

### Documentação Oficial
- [Obsidian CLI - Help](https://help.obsidian.md/cli) (v1.12+)
- [Obsidian URI](https://help.obsidian.md/Extending+Obsidian/Obsidian+URI)
- [Obsidian Changelog](https://obsidian.md/changelog/)
- [Early Access / Catalyst](https://help.obsidian.md/early-access)

### REST API Plugin
- [GitHub - Local REST API](https://github.com/coddingtonbear/obsidian-local-rest-api)
- [Documentação Interativa](https://coddingtonbear.github.io/obsidian-local-rest-api/)
- Plugin no Obsidian: `obsidian-local-rest-api` v3.4.3

### Advanced URI Plugin
- [GitHub - Advanced URI](https://github.com/Vinzent03/obsidian-advanced-uri)
- [Getting Started](https://vinzent03.github.io/obsidian-advanced-uri/getting_started)

### Comunidade & Discussões
- [New Obsidian CLI - Forum](https://forum.obsidian.md/t/new-obsidian-cli/105614)
- [DeepakNess: Obsidian CLI Overview](https://deepakness.com/raw/obsidian-cli/)
- [Obsidian Stats: Plugin Updates 2026](https://www.obsidianstats.com/posts/2026-02-08-weekly-updates)
- Tweet oficial: [@obsdmd](https://x.com/obsdmd/status/2021241384057930224)

### Ferramentas Alternativas (Community)
- [Yakitrak/obsidian-cli](https://github.com/Yakitrak/obsidian-cli) - Go-based CLI
- [davidpp/obsidian-cli](https://github.com/davidpp/obsidian-cli) - AI-optimized Python CLI
- [Bip901/obsidian-cli](https://github.com/Bip901/obsidian-cli) - Python CLI com uv

---

## Relações
- [[24_LogSessao2026-02-11|Log Sessão 2026-02-11]] - Testes e descobertas
- [[23_TesteAPICLI|Teste REST API]] - Primeira nota criada via API
- [[08_IdeiaBaseDeDados|Base de Dados]] - REST API pode automatizar queries Dataview
- [[10_IdeiaCLITelegram|CLI Telegram]] - Possível integração via Obsidian API
- [[05_SistemaRagMemoria|Sistema RAG]] - API para alimentar memória automaticamente

---

## Conclusão

A **REST API** é a solução definitiva para automação do Obsidian no momento:
- ✅ Disponível imediatamente (plugin gratuito)
- ✅ Funcionalidade completa (CRUD, busca, comandos)
- ✅ Bem documentada e estável
- ✅ Integrável com Python, curl, e outras ferramentas

O **CLI oficial** (v1.12+) será testado quando disponível na versão pública, mas a REST API já atende todas as necessidades do projeto.
