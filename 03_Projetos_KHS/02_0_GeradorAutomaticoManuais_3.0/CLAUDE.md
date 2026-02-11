# G.A.M. 3.0 -- Gerador Automatico de Manuais

> Motor de geracao de manuais industriais KHS.
> Evolucao do legado VBA puro, agora com integracao C#.

## Objetivo

Montar manuais tecnicos KHS a partir de **blocos modulares de conteudo** (templates Word),
controlados por uma planilha Excel de configuracao e gerados via VBA + C#.

## Estrutura

```
02_GeradorAutomaticoManuais_3.0\
├── CLAUDE.md              # Este arquivo -- visao geral e arquitetura
├── 01_Codigo_Atual\       # Codigo vivo (VBA, C#) -- ver CLAUDE.md para mapa de modulos
├── 02_Documentacao\       # Docs do sistema atual -- ver CLAUDE.md para indice
└── 80_Legado\             # Mapa do sistema antigo -- ver CLAUDE.md para referencias
```

### Escopo deste CLAUDE
Arquitetura, fluxo e maquinas. Para detalhes de:
- **Modulos VBA e motor C#** -> `01_Codigo_Atual\CLAUDE.md`
- **Planilhas, bases de dados, specs de UI** -> `02_Documentacao\CLAUDE.md`
- **Sistema antigo** -> `80_Legado\CLAUDE.md`

## Arquitetura do Sistema

```
┌─────────────────────────────────────────────────────────┐
│  RIBBON (Interface)                                     │
│  Botoes no Excel: Mec, El, IHM, Gerar por maquina      │
├─────────────────────────────────────────────────────────┤
│  PAGINAS (Navegacao)                                    │
│  60+ Planilhas organizadas por maquina e tipo           │
├──────────────┬──────────────────────────────────────────┤
│  UI ZONA A   │  UI ZONA B                              │
│  Galeria IHM │  Detalhes + Documentos                  │
│  Filtros     │  Hardware panel + Doc list               │
├──────────────┴──────────────────────────────────────────┤
│  mod_NewEngine_V5 (MOTOR PRINCIPAL)                     │
│  Gera manifesto CSV -> chama NewGeradorV2.exe (C#)      │
├─────────────────────────────────────────────────────────┤
│  LEGADO: Imagem + Tabela + Send + Controle              │
│  Substituicao de figuras/tabelas em Word, email, utils  │
└─────────────────────────────────────────────────────────┘
```

## Fluxo de Geracao (Excel -> C#)

1. Usuario clica botao no **Ribbon** (ex: "Gerar BTR")
2. Ribbon chama `mod_NewEngine_V5.Gerar_BTR()` -> `ExportarParaNovoGerador("BTR")`
3. Motor le aba **"Base de Dados"** (coluna C = caminho, coluna B = ativo)
4. Monta **manifesto CSV** (`input_manifest.csv`) com separador `;`:
   - `META`: tipo maquina, SAP number, projeto, revisao, ano, nome completo
   - `TABLE_ROW`: dados das tabelas dinamicas
   - `FILE`: lista de .docx ativos com indice da linha
5. Salva CSV em UTF-8 via ADODB.Stream
6. Executa **`NewGeradorV2.exe`** passando o caminho do CSV
7. Motor C# processa o manifesto e monta o documento Word final

## Maquinas Suportadas

**Legado**: BTR (8pg), GTR (8pg), DVD (5pg), PET (3pg), CIP (6pg), CMX (3pg), CCMX (5pg)
**Novas (IHM)**: PLT (5pg), DPL (5pg, pendente), PCK (5pg), DPK (5pg, pendente)

## Convencoes

- Nomear arquivos sem espacos (usar `_`).
- Todo codigo novo em C# deve ter equivalencia documentada com o modulo VBA original.
- Ao trazer funcionalidade do legado, registrar qual modulo VBA foi a origem.
