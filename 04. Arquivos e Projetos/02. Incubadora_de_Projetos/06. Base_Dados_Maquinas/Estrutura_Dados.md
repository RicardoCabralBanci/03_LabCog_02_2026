# Especificação de Estrutura de Dados: Máquinas, Centros de Custo e Arquivos

**Status**: Rascunho / Planejamento V2
**Autor**: Mestre em VBA (Persona)
**Data**: 28/01/2026

## 1. Conceito Relacional
Utilizamos um modelo relacional para separar **Categorias** (Centros de Custo), **Especificações** (Máquinas) e **Ativos Digitais** (Arquivos Word). Isso permite montar manuais dinamicamente sem depender da estrutura física de pastas.

---

## 2. Definição das Tabelas

### Tabela A: `tbl_CentrosCusto` (A Família)
Define as grandes categorias funcionais.

| Campo (Coluna) | Tipo de Dado | Descrição | Exemplo |
| :--- | :--- | :--- | :--- |
| **ID_CC** (PK) | Inteiro (Auto) | Identificador único. | `10` |
| **Codigo_CC** | Texto (Curto) | Código interno. | `CC-PAL` |
| **Nome_Funcional** | Texto | Nome legível. | `Paletização` |

### Tabela B: `tbl_Maquinas` (O Modelo)
Define os modelos específicos.

| Campo (Coluna) | Tipo de Dado | Descrição | Exemplo |
| :--- | :--- | :--- | :--- |
| **ID_Maq** (PK) | Inteiro (Auto) | Identificador único. | `1001` |
| **ID_CC_Ref** (FK) | Inteiro | Liga à Família (`tbl_CentrosCusto`). | `10` |
| **Modelo_Comercial** | Texto | Nome de venda. | `Innopal PB` |
| **Descricao_Tecnica** | Texto | Detalhes. | `High-Bed Palletizer` |

### Tabela C: `tbl_Arquivos_Base` (O Bibliotecário)
**A Nova Tabela.** Mapeia onde estão os arquivos físicos e a quem eles pertencem.

| Campo (Coluna) | Tipo de Dado | Descrição | Exemplo |
| :--- | :--- | :--- | :--- |
| **ID_Arquivo** (PK) | Inteiro (Auto) | Identificador único do arquivo. | `500` |
| **ID_Maq_Ref** (FK) | Inteiro | Se preenchido, é exclusivo desta máquina. Se `Null`, é genérico. | `1001` (ou Vazio) |
| **ID_CC_Ref** (FK) | Inteiro | Se preenchido (e Maq for Null), serve para toda a família. | `10` |
| **Nome_Display** | Texto | Título amigável para UI. | `Cap 01 - Segurança` |
| **Caminho_Relativo** | Texto | Caminho a partir da pasta raiz de Templates. | `\Paletizacao\Geral\Seguranca_V2.docx` |
| **Tipo_Conteudo** | Texto | Tag para filtragem. | `Operação`, `Manutenção`, `Peças` |
| **Idioma** | Texto | Código ISO. | `PT-BR` |
| **Ordem_Padrao** | Inteiro | Define a sequência lógica de montagem. | `10` (Vem primeiro), `20`, `30`... |

---

## 3. Lógica de Seleção (A Inteligência)

Ao montar um manual para a máquina `Innopal PB` (ID 1001), o algoritmo fará a seguinte consulta (Query):

**"Traga-me todos os arquivos onde:"**
1.  `ID_Maq_Ref` = 1001 **(Específicos da Máquina)**
2.  **OU** (`ID_Maq_Ref` É NULO **E** `ID_CC_Ref` = 10) **(Genéricos da Família)**
3.  **E** `Idioma` = 'PT-BR'

**Resultado:** O sistema monta um manual híbrido automaticamente, misturando capítulos genéricos de Paletização (que você só escreve uma vez) com capítulos específicos do modelo PB.

---

## 4. Exemplo de Dados `tbl_Arquivos_Base`

| ID | ID_Maq | ID_CC | Caminho | Tipo | Ordem |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 500 | *Null* | **10** | `\Paletizacao\Seguranca_Geral.docx` | Segurança | 05 |
| 501 | *Null* | **10** | `\Paletizacao\Limpeza_Basica.docx` | Manutenção | 50 |
| 600 | **1001** | 10 | `\Innopal_PB\Operacao_TouchPanel.docx` | Operação | 20 |
| 601 | **1001** | 10 | `\Innopal_PB\Lubrificacao_Eixos.docx` | Manutenção | 55 |

*Neste cenário, o manual da Innopal PB teria a Segurança Geral (herdada) e a Operação específica.*

---

## 5. Vantagens desta Abstração
1.  **Reutilização**: Um arquivo de "Segurança em Eletricidade" pode ser vinculado ao ID_CC de todas as máquinas elétricas, sem precisar copiar o .docx.
2.  **Versionamento**: Se o manual de segurança mudar, você substitui um único arquivo na pasta e todos os manuais gerados a partir dali saem atualizados.
3.  **Flexibilidade de Caminhos**: Você pode reorganizar suas pastas como quiser. Desde que atualize o campo `Caminho_Relativo` no Excel, o sistema continua funcionando.