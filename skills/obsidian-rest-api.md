# Skill: Obsidian Local REST API

> Interagir com o vault Obsidian via HTTP REST API.

## Conexao

- **Endpoint**: `https://127.0.0.1:27124`
- **API Key**: `c66d870ab3b303c639e4e9d111a8c39e11930820d38b56ba2d65187021cb0723`
- **Auth header**: `Authorization: Bearer <API_KEY>`
- **curl flag**: sempre usar `-k` (certificado auto-assinado)

## Teste de conectividade

```bash
curl -s -k https://127.0.0.1:27124/ -H "Authorization: Bearer c66d870ab3b303c639e4e9d111a8c39e11930820d38b56ba2d65187021cb0723"
```

Resposta esperada: JSON com `"authenticated": true`

Se falhar: pedir ao usuario para abrir o Obsidian e verificar se o plugin Local REST API esta ativo.

## Endpoints

### Listar arquivos

```bash
# Listar raiz do vault
curl -s -k https://127.0.0.1:27124/vault/ -H "Authorization: Bearer <KEY>"

# Listar pasta especifica
curl -s -k https://127.0.0.1:27124/vault/03_LabCog_02_2026/ -H "Authorization: Bearer <KEY>"
```

### Ler nota

```bash
# Conteudo markdown
curl -s -k https://127.0.0.1:27124/vault/caminho/arquivo.md -H "Authorization: Bearer <KEY>"

# Com metadados (frontmatter, tags, stat)
curl -s -k https://127.0.0.1:27124/vault/caminho/arquivo.md \
  -H "Authorization: Bearer <KEY>" \
  -H "Accept: application/vnd.olrapi.note+json"
```

### Criar ou substituir nota

```bash
curl -s -k -X PUT https://127.0.0.1:27124/vault/caminho/novo-arquivo.md \
  -H "Authorization: Bearer <KEY>" \
  -H "Content-Type: text/markdown" \
  -d "# Titulo

Conteudo da nota"
```

### Adicionar conteudo ao final

```bash
curl -s -k -X POST https://127.0.0.1:27124/vault/caminho/arquivo.md \
  -H "Authorization: Bearer <KEY>" \
  -H "Content-Type: text/markdown" \
  -d "

Nova linha adicionada ao final"
```

### Editar por heading, bloco ou frontmatter (PATCH)

```bash
# Append sob um heading especifico
curl -s -k -X PATCH https://127.0.0.1:27124/vault/arquivo.md \
  -H "Authorization: Bearer <KEY>" \
  -H "Content-Type: text/markdown" \
  -H "Operation: append" \
  -H "Target-Type: heading" \
  -H "Target: Nome do Heading" \
  -d "Conteudo adicionado sob o heading"

# Headings aninhados (delimitador padrao: ::)
# Target: "Heading 1::Subheading 1.1"

# Operacoes: append, prepend, replace
# Target-Types: heading, block, frontmatter
```

### Busca

```bash
# Busca textual simples
curl -s -k -X POST "https://127.0.0.1:27124/search/simple/?query=meu+termo&contextLength=100" \
  -H "Authorization: Bearer <KEY>"

# Busca Dataview DQL (requer plugin Dataview)
curl -s -k -X POST https://127.0.0.1:27124/search/ \
  -H "Authorization: Bearer <KEY>" \
  -H "Content-Type: application/vnd.olrapi.dataview.dql+txt" \
  -d "TABLE file.name FROM \"03_LabCog_02_2026\""
```

### Abrir arquivo no Obsidian

```bash
curl -s -k -X POST https://127.0.0.1:27124/open/caminho/arquivo.md \
  -H "Authorization: Bearer <KEY>"
```

### Listar e executar comandos

```bash
# Listar comandos disponiveis
curl -s -k https://127.0.0.1:27124/commands/ -H "Authorization: Bearer <KEY>"

# Executar comando
curl -s -k -X POST https://127.0.0.1:27124/commands/global-search:open/ \
  -H "Authorization: Bearer <KEY>"
```

## Content-Types

| Content-Type | Uso |
|---|---|
| `text/markdown` | Conteudo de notas |
| `application/json` | Dados estruturados |
| `application/vnd.olrapi.note+json` | Nota com metadados (Accept header) |
| `application/vnd.olrapi.dataview.dql+txt` | Queries Dataview |

## Codigos de resposta

| Codigo | Significado |
|---|---|
| 200 | Sucesso com conteudo |
| 204 | Sucesso sem corpo |
| 400 | Requisicao invalida |
| 404 | Arquivo nao encontrado |
