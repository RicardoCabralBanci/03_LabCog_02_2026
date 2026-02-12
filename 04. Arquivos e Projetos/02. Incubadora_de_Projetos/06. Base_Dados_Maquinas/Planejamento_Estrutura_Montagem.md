# Planejamento: Arquitetura de Montagem de Manuais (Lego System)

**Objetivo**: Definir como gerenciar a complexidade de manuais compostos por fragmentos (tópicos inteiros, parágrafos soltos, tabelas isoladas) reutilizáveis.

---

## 1. O Conceito: Biblioteca vs. Receita

Para evitar uma tabela monstruosa e ineditável, separamos o "O Que" (Arquivo) do "Onde/Como" (Estrutura).

### A. A Biblioteca (`tbl_Biblioteca_Modulos`)
*O Depósito de Peças.*
Esta tabela não sabe nada sobre capítulos, numeração ou ordem. Ela apenas sabe onde o arquivo está no disco.

| ID_Modulo (PK) | Nome_Interno | Caminho_Relativo | Tipo_Arquivo | Hash_Integridade |
| :--- | :--- | :--- | :--- | :--- |
| **MOD-001** | Texto_EPI_Padrao | `\Seguranca\Geral\uso_epis.docx` | DOCX | (Opcional) |
| **MOD-002** | Tabela_Torque_M8 | `\Tecnico\Tabelas\torques_m8.docx` | DOCX | ... |
| **MOD-003** | Diagrama_Eletrico_Gen | `\Esquemas\diagrama_base.jpg` | IMG | ... |

---

### B. A Receita Mestra (`tbl_Blueprint_Manual`)
*O Manual de Instruções de Montagem.*
Aqui definimos a hierarquia. Um registro aqui diz: "Pegue o Módulo 001, chame-o de 'Segurança', coloque-o na posição 1.0 e quebre a página antes".

| Campo | Descrição | Exemplo A (Capítulo) | Exemplo B (Sub-item) |
| :--- | :--- | :--- | :--- |
| **ID_Item** | Identificador único da linha. | 1 | 2 |
| **ID_Maq_Ref** | A qual máquina esta receita pertence. | `Innopal PB` | `Innopal PB` |
| **ID_Modulo_Ref** | Qual peça usar da biblioteca. | `MOD-001` | `MOD-002` |
| **Codigo_Hierarquia** | Define a estrutura lógica. | `1` | `1.1` |
| **Titulo_Secao** | O que vai aparecer no Índice. | "Segurança Geral" | "Tabela de Torques" |
| **Nivel_Outline** | Nível do Título no Word (H1, H2...). | 1 | 2 |
| **Quebra_Pagina** | Comportamento antes de inserir. | `TRUE` (Sim) | `FALSE` (Não) |

---

## 2. Cenários de Uso Real

### Cenário 1: O "Arquivo Tópico Completo"
O arquivo `Manutencao_Preventiva.docx` já tem o título "Manutenção", subtítulos, texto e tabelas.
*   **Na Receita**: Você insere ele com Nível Outline `0` (ou ajustado) e diz para não criar título novo, apenas colar o conteúdo.

### Cenário 2: O "Frankenstein" (Vários arquivos formando um capítulo)
Você quer um capítulo "Dados Técnicos" (H1) que contém:
1.  Texto introdutório (Arquivo A)
2.  Tabela de Consumo (Arquivo B)
3.  Desenho Dimensional (Arquivo C)

**Como fica na Tabela Receita:**

| ID | Modulo | Hierarquia | Titulo | Nivel | Obs |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 10 | (Null) | **2** | "Dados Técnicos" | 1 | Cria apenas o Título H1 vazio |
| 11 | MOD-A | **2.1** | (Vazio) | 0 | Cola o texto logo abaixo |
| 12 | MOD-B | **2.2** | "Consumos" | 2 | Insere tabela como H2 |
| 13 | MOD-C | **2.3** | "Dimensional" | 2 | Insere imagem como H2 |

---

## 3. O Desafio da Variabilidade (O "Problema das 1000 Linhas")

Se tivermos que criar uma receita de 500 linhas para *cada* máquina, vamos morrer de digitar.
**Solução: Herança de Receitas.**

Criamos "Receitas Base" (Templates de Estrutura).
1.  **Template "Paletizador Padrão"**: Tem a estrutura base (Segurança, Operação, Manutenção).
2.  **Receita "Innopal PB"**: Diz apenas: *"Herde tudo do Paletizador Padrão, MAS substitua o Módulo de 'Operação' pelo Módulo Específico PB e adicione o Módulo 'Opcional de Capa de Chuva' no final"*.

Isso exige uma lógica de "Delta" (Diferença), mas economiza 90% do trabalho de cadastro.

---

## 4. Próximos Passos para Validação
1.  Isso resolve o problema de granularidade?
2.  A ideia de "Herança" parece muito complexa para implementar agora ou é essencial? (Sem ela, teremos muito Copy/Paste de linhas no Excel).
