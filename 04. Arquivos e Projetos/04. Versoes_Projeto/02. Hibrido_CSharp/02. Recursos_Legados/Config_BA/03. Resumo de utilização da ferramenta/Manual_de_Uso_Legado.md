# Manual de Utilização da Ferramenta (Legado VBA)
**Versão:** 1.0 (Final antes da Migração)
**Data de Criação:** 18/12/2025
**Status:** Depreciado (Use com cautela)

---

## 1. Introdução
Bem-vindo ao Gerador de Manuais Automatizado (Versão Legada). Esta ferramenta utiliza macros do Excel (VBA) para montar manuais técnicos no Word, combinando pedaços de textos, tabelas e imagens com base em uma lista de configuração.

> **⚠️ AVISO IMPORTANTE:** Esta ferramenta opera controlando o mouse e o teclado do seu computador "virtualmente". **NÃO toque no mouse ou teclado** enquanto a macro estiver rodando, ou você poderá corromper o documento gerado.

## 2. Pré-requisitos
Antes de começar, certifique-se de que:
1.  **Microsoft Office**: Você tem Excel e Word instalados (versões 2013 ou superiores recomendadas).
2.  **Acesso à Rede**: Você tem acesso às pastas de rede onde estão os modelos (`V:\Abteilungen\...`) ou está rodando tudo localmente na pasta `Config_BA`.
3.  **Habilitar Macros**: Ao abrir o arquivo Excel, você deve clicar em "Habilitar Conteúdo" ou "Habilitar Macros" na barra amarela de segurança.

## 3. Estrutura de Pastas
A ferramenta depende de uma estrutura rígida. Não renomeie as pastas principais!

*   `Config_BA/`: Pasta raiz da ferramenta.
    *   `BTR/`, `CMX/`, `PET/`: Contêm os **sub-documentos** (capítulos) específicos de cada máquina.
    *   `manual.dotm`: O modelo (template) base do Word com cabeçalho, rodapé e estilos.
    *   `Planilha [TIPO].xlsm`: O arquivo Excel controlador (ex: `Planilha BTR.xlsm`).

## 4. Passo a Passo: Gerando um Manual

### Passo 1: Preparação
1.  Abra a pasta correspondente ao tipo de máquina (ex: `BTR`).
2.  Abra o arquivo Excel mestre (ex: `Planilha BTR.xlsm`).
3.  Vá para a aba **"Dados do Projeto"** (ou similar, dependendo da versão).
4.  Preencha os campos obrigatórios:
    *   **Número do Projeto**: (ex: K-12345)
    *   **Cliente**: Nome do cliente.
    *   **Revisão**: Número da revisão (00, 01...).

### Passo 2: Configuração dos Capítulos
1.  Navegue para a aba principal de configuração (geralmente `Planilha3`).
2.  Você verá uma lista de capítulos/tópicos na Coluna B.
3.  **Coluna "Yes/No"**:
    *   Marque **"Yes"** nas linhas dos capítulos que devem entrar no manual.
    *   Marque **"No"** para os que devem ser ignorados.
    *   *Nota*: A coluna C contém o nome do arquivo `.docx` que será buscado. Não altere isso a menos que saiba o que está fazendo.

### Passo 3: Execução
1.  Localize o botão grande (geralmente escrito **"Gerar Manual"** ou um ícone de "Play").
2.  Clique no botão.
3.  **AFASTE-SE DO COMPUTADOR.**
    *   O Excel vai abrir o Word.
    *   Vai abrir e fechar vários arquivos.
    *   A tela pode piscar. Isso é "normal".
    *   O processo pode levar de 2 a 10 minutos dependendo do tamanho do manual.

### Passo 4: Finalização
1.  Uma mensagem aparecerá: *"Manual gerado com sucesso. Deseja revisar agora?"*.
2.  Clique em **Sim** para abrir o Word gerado.
3.  **Salve o arquivo imediatamente** com um novo nome para não perder o trabalho.

## 5. Resolução de Problemas Comuns (Troubleshooting)

| Problema | Causa Provável | Solução |
| :--- | :--- | :--- |
| **Erro "O arquivo não foi encontrado"** | Um dos capítulos marcados como "Yes" não existe na pasta ou foi renomeado. | Verifique se o nome na Coluna C da planilha bate exatamente com o nome do arquivo na pasta. |
| **O Word travou/ficou branco** | Você clicou em algo durante a execução ou o computador ficou sem memória. | Feche tudo pelo Gerenciador de Tarefas e tente novamente (sem tocar no mouse!). |
| **Erro "Aguardando ação OLE"** | O Excel está esperando o Word, mas o Word está travado ou com uma janela aberta escondida. | Tente Alt+Tab para achar a janela do Word pedindo confirmação. Se não achar, feche o Word pelo Gerenciador de Tarefas. |
| **As tabelas estão desformatadas** | O módulo de tabelas (`Tabela.bas`) falhou ao copiar o estilo. | Isso é um bug conhecido do legado. Ajuste manualmente no Word final. |
| **Erro de Depuração (Debug)** | O código VBA encontrou uma exceção não tratada. | Tire um print da tela, anote a linha amarela no código e chame o suporte técnico (ou o Mestre em VBA). |

---
**Nota Técnica:** Esta ferramenta está em processo de migração para uma nova arquitetura baseada em Python, que eliminará a necessidade de não tocar no mouse e reduzirá o tempo de geração para segundos. Aguarde novidades.
