# 01_Codigo_Atual -- G.A.M. 3.0

> Codigo vivo do Gerador Automatico de Manuais. Tudo que esta em uso ou desenvolvimento ativo fica aqui.
> Para arquitetura geral, fluxo de geracao e planilhas-chave, ver o CLAUDE.md pai:
> `03_LabCog_02_2026\02_GeradorAutomaticoManuais_3.0\CLAUDE.md`

## O que vive aqui

A subpasta `_md\` contem os modulos VBA do Excel, convertidos para `.md` para leitura facil pelo CLI.
Sao o codigo-fonte real -- nao resumos ou analises.

## Motor C# -- `NewGeradorV2\`

O motor que recebe o manifesto CSV e monta o documento Word final.
Origem: `25. Scripts\NewEngine\src\csharp\` (legado, copiado para ca).

| Arquivo | Funcao |
|---|---|
| `Program.cs` | Arquivo unico. Parseia manifesto CSV, pre-processa tabelas dinamicas nos .docx e empilha documentos via AltChunk (OpenXml) |
| `NewGerador.csproj` | Projeto .NET 8. Dependencias: `DocumentFormat.OpenXml 3.3.0`, `OpenXmlPowerTools 4.5.3.2` |

Build: `dotnet publish -c Release -r win-x64` (gera `NewGeradorV2.exe`)
Uso: `NewGeradorV2.exe <caminho_do_manifesto.csv>`

## Modulos VBA -- `_md\`

### Novos (v3 -- prefixo `mod_`)

| Arquivo | Funcao | Depende de |
|---|---|---|
| `mod_NewEngine_V5.md` | Motor principal. Gera manifesto CSV (META + TABLE_ROW + FILE) e chama `NewGeradorV2.exe` (C#) | -- |
| `mod_Shared_Definitions.md` | Constantes globais: paleta de cores industrial, tipos `T_Card_Master` e `T_Doc_Item` | -- |
| `mod_UI_ZoneA.md` | Galeria de modelos IHM (sidebar com filtros Clearline/Siemens/Rockwell, cards com imagens) | mod_Shared_Definitions, mod_UI_ZoneB |
| `mod_UI_ZoneB.md` | Painel de detalhes: imagem ampliada, specs, lista de documentos por capitulo com validacao | mod_Shared_Definitions |
| `mod_Teleporte.md` | Utilitario: busca fuzzy de abas por nome/CodeName/indice (atalho `F`) | -- |

### Legado (nomes originais mantidos)

| Arquivo | Funcao |
|---|---|
| `Ribbon.md` | Callbacks do ribbon customizado. Mapeia 11 maquinas com botoes Mec/El/IHM/Gerar |
| `Páginas.md` | Navegacao hardcoded entre 60+ planilhas por maquina (BTRPG1-8, GTRPG1-8, etc.) |
| `Controle.md` | Utilitarios: mostrar abas ocultas, deletar shapes, centralizar imagens, listar macros |
| `Imagem.md` | Le alt-text de InlineShapes de um .docx e substitui figuras por novos arquivos |
| `Tabela.md` | Le titulos de tabelas de um .docx e substitui por tabela de arquivo externo |
| `Send.md` | Monta e envia email via Outlook COM com status de preenchimento por maquina |

## Convencoes

- Modulos novos usam prefixo `mod_`. Legado mantem nome original.
- Nomes de arquivo sem espacos (usar `_`).
- Ao adicionar um arquivo, registrar sua origem (se veio do legado, qual modulo).
- Todo codigo novo em C# deve ter equivalencia documentada com o modulo VBA original.
