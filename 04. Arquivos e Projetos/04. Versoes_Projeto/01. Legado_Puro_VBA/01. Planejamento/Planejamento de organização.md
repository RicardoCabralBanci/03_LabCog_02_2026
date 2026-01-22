# Planejamento de Organização e Desenvolvimento

## 1. Contexto
Este projeto tem como objetivo desenvolver uma ferramenta moderna para substituir e automatizar os processos anteriormente realizados por macros VBA (Visual Basic for Applications) e planilhas Excel. A reorganização atual visa estabelecer uma base sólida para este desenvolvimento.

## 2. Estrutura de Diretórios
A estrutura do projeto foi padronizada da seguinte forma:

*   **04. Arquivos e Projetos/**: Diretório raiz para a gestão do projeto.
    *   **01. Planejamento/**: Destinado a documentação estratégica, *to-do lists* e arquivos de organização como este.
    *   **02. Recursos_Legados/**: Armazena o material original (`Config_BA`), incluindo os geradores de manuais antigos, templates `.dotm` e planilhas de controle. Esta pasta serve como **referência de leitura** (Read-Only) para a lógica a ser portada.

## 3. Status Atual
*   O diretório `Config_BA` foi movido com sucesso para `02. Recursos_Legados`.
*   A análise preliminar de códigos (ex: `BTR.bas`) confirmou a viabilidade de leitura e portabilidade da lógica.

## 4. Próximos Passos (Sugestão)
1.  **Mapeamento de Funcionalidades**: Listar todas as funções críticas presentes nos arquivos da pasta `Recursos_Legados`.
2.  **Definição da Stack**: Confirmar as ferramentas para a nova CLI (ex: Python com bibliotecas `pandas` para Excel e `python-docx` para Word).
3.  **Desenvolvimento Incremental**: Começar portando a lógica de um módulo específico (ex: BTR) para provar o conceito.
