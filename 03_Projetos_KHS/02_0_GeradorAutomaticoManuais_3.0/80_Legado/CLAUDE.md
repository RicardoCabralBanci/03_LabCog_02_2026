# 80_Legado -- Mapa do Sistema Antigo

> Esta pasta NAO contem os arquivos originais. Ela documenta e aponta para eles.
> Os arquivos fisicos permanecem em `04. Arquivos e Projetos\01. Criação Automatica de Manuais\`.

## O que era o sistema legado

Gerador de manuais industriais KHS baseado em VBA puro, operando dentro do Excel/Word.
Uma planilha Excel controlava a configuracao, e macros VBA montavam documentos Word
a partir de templates modulares organizados por Capitulo/Pagina/Secao.

## Modulos VBA (.bas)

Localizados em: `04. Arquivos e Projetos\01. Criação Automatica de Manuais\02. Recursos_Legados\Config_BA\00.VBA_MODULES\`

| Modulo | Arquivo | Descricao |
|---|---|---|
| BTR | `BTR.bas` | Logica de geracao para Belt Transport |
| CCMX | `CCMX.bas` | -- |
| CIP | `CIP.bas` | -- |
| CMX | `CMX.bas` | -- |
| Controle | `Controle.bas` | Modulo de controle geral |
| DVD | `DVD.bas` | Logica de geracao para DVD |
| GTR | `GTR.bas` | -- |
| Imagem | `Imagem.bas` | Manipulacao de imagens nos documentos |
| Paginas | `Páginas.bas` | Controle de paginacao |
| PET | `PET.bas` | -- |
| Ribbon | `Ribbon.bas` | Interface do ribbon no Excel |
| Send | `Send.bas` | Envio/exportacao de documentos |
| Tabela | `Tabela.bas` | Manipulacao de tabelas |

> Descricoes marcadas com `--` precisam ser preenchidas ao analisar cada modulo.

## Documentacao existente (MDs do legado)

### Resumos dos arquivos Word
Caminho: `04. Arquivos e Projetos\01. Criação Automatica de Manuais\03. Resumo dos arquivos Word\`
- `002. Mapeamento_Word_BTR.md`
- `003. Mapeamento_Word_DVD.md`
- `004. BTR_Capitulo_3_Estrutura.md`
- `004. Glossario_Tecnico_KHS_Decifrado.md`
- `005. BTR_Capitulo_4_Montagem.md`
- `006. BTR_Capitulo_6_Manutencao.md`
- `007. DVD_Capitulo_3_Estrutura.md`

### Analises tecnicas
Caminho: `04. Arquivos e Projetos\01. Criação Automatica de Manuais\02. Recursos_Legados\Config_BA\`
- `02. Estrutura\Analise_Tecnica_Legado.md`
- `02. Estrutura\Analise_Modulos_VBA.md`
- `02. Estrutura\0100. Planejamento_Hibrido_VBA_Python.md`
- `02. Estrutura\0200. Mapeamento_Dados_Excel.md`
- `03. Resumo de utilização da ferramenta\Manual_de_Uso_Legado.md`

### Codigo VBA documentado em MD
Caminho: `99. Historico_Versoes\01. Legado_Puro_VBA\02. Recursos_Legados\Config_BA\01. VBA_MODULES_SCRIPTS\`
- `0100. Script_BTR.md` + `0101. Analise_BTR.md`
- `0200. Script_CCMX.md`
- `0300. Script_CIP.md`
- `0400. Script_CMX.md`
- `0500. Script_Controle.md` + `0501. Analise_Detalhada_Controle.md`
- `0600. Script_DVD.md`
- `0700. Script_GTR.md` + `0701. Analise_GTR.md` + `0702. Analise_Detalhada_GTR.md`
- `0800. Script_Imagem.md` + `0801. Analise_Detalhada_Imagem.md`
- `0900. Script_Paginas.md` + `0901. Analise_Detalhada_Paginas.md`
- `1000. Script_PET.md`
- `1100. Script_Ribbon.md`
- `1200. Script_Send.md`
- `1300. Script_Tabela.md`

## Estrutura dos templates Word

Padrao: `Config_BA\BTR\PT\C{capitulo}\P{pagina}\S{secao}\PT{codigo}.docx`

Exemplo: `PTC2P3S001.docx` = Capitulo 2, Pagina 3, Secao 001

## Outros recursos legados

- `VBA_Extracted_Code.md` -- codigo VBA extraido em formato MD
- `00. Planejamento_Migracao_DB.md` -- planejamento inicial de migracao para SQLite
- `000. MAPA_DO_CONHECIMENTO.md` -- mapa geral do projeto antigo
