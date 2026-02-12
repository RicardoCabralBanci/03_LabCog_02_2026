using System;
using System.Linq;
using System.Collections.Generic;
using DocumentFormat.OpenXml;
using DocumentFormat.OpenXml.Packaging;
using DocumentFormat.OpenXml.Wordprocessing;

namespace TableTest
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("--- POC: OpenXML Table Filler ---");

            string workDir = @"C:\LabCogKHS_CLI\40_Personas\040. Mestre em VBA (A Garagem de Autópsias Digitais)\03. Projetos\00. Gerador_Automatico_Manuais\08. Correcao_Componentes_Integrados\POC_Validation";
            string templatePath = System.IO.Path.Combine(workDir, "Template.dotm");
            string outputPath = System.IO.Path.Combine(workDir, "Resultado_Tabela.docx");

            // 1. Cria um Template Dummy se não existir (para facilitar seu teste)
            if (!System.IO.File.Exists(templatePath))
            {
                Console.WriteLine("[ERRO] Template.dotm não encontrado na pasta de execução.");
                return;
            }

            // 2. Dados Simulados (4 colunas completas)
            var dados = new List<string[]>
            {
                new string[] { "Esteira de Entrada", "KHS", "1001", "Setor A" },
                new string[] { "Enchedora Master", "KHS", "2002", "Setor B" },
                new string[] { "Inspetor de Nível", "Heuft", "3003", "Setor C" }
            };

            // 3. Executa o Transplante e Preenchimento
            try
            {
                // Variável para guardar a tabela clonada em memória
                Table clonedTable = null;

                // FASE 1: Extração (Roubar a tabela do Template)
                Console.WriteLine("[FASE 1] Extraindo tabela do Template...");
                using (WordprocessingDocument sourceDoc = WordprocessingDocument.Open(templatePath, false))
                {
                    var body = sourceDoc.MainDocumentPart.Document.Body;

                    // Procura a tabela (Primeira tabela ou por Alt Text)
                    var table = body.Descendants<Table>().FirstOrDefault(t => 
                        (t.GetFirstChild<TableProperties>()?.TableCaption?.Val == "Componentes integrados") ||
                        (t.GetFirstChild<TableProperties>()?.TableDescription?.Val == "Componentes integrados")
                    );
                    
                    if (table == null) 
                    {
                        Console.WriteLine("[AVISO] Tabela alvo não encontrada por nome. Pegando a primeira tabela visível.");
                        table = body.Descendants<Table>().FirstOrDefault();
                    }

                    if (table != null)
                    {
                        // Clona a tabela inteira para a memória
                        clonedTable = (Table)table.CloneNode(true);
                        Console.WriteLine("[SUCESSO] Tabela clonada para a memória.");
                    }
                    else
                    {
                        Console.WriteLine("[ERRO CRÍTICO] Nenhuma tabela encontrada no Template!");
                        return;
                    }
                }

                // FASE 2: Preenchimento (Trabalhando na cópia em memória)
                if (clonedTable != null)
                {
                    Console.WriteLine("[FASE 2] Preenchendo dados na memória...");
                    FillTable(clonedTable, dados);
                }

                // FASE 3: Transplante (Criar Doc Novo e Colar)
                Console.WriteLine("[FASE 3] Criando novo documento e injetando a tabela...");
                using (WordprocessingDocument newDoc = WordprocessingDocument.Create(outputPath, WordprocessingDocumentType.Document))
                {
                    MainDocumentPart mainPart = newDoc.AddMainDocumentPart();
                    mainPart.Document = new Document();
                    Body body = mainPart.Document.AppendChild(new Body());

                    // Adiciona um título só para ficar bonito
                    body.Append(new Paragraph(new Run(new Text("Tabela Transplantada via OpenXML"))));

                    // Injeta a tabela clonada
                    // IMPORTANTE: O OpenXML exige que importemos o nó para o contexto do novo documento?
                    // Geralmente CloneNode cria um nó órfão que pode ser anexado. 
                    // Se houver estilos customizados, eles podem se perder se não copiarmos os estilos também.
                    // Para este teste, vamos assumir estilos inline ou padrão.
                    
                    body.Append(clonedTable);
                    
                    mainPart.Document.Save();
                }

                Console.WriteLine($"[FIM] Arquivo gerado DO ZERO: {outputPath}");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"[CRITICAL] Erro: {ex.Message}");
                Console.WriteLine(ex.StackTrace);
            }
            
            // Console.ReadKey();
        }

        static void FillTable(Table table, List<string[]> data)
        {
            var rows = table.Elements<TableRow>().ToList();
            if (rows.Count < 1) return;

            // 1. Identifica a linha de cabeçalho e a linha de modelo
            var headerRow = rows.First();
            var templateRow = rows.Count > 1 ? rows[1] : rows[0];
            TableRow rowMolde = (TableRow)templateRow.CloneNode(true);

            // 2. Determina a largura dos dados (quantas colunas vamos manter)
            int targetCols = data.Count > 0 ? data[0].Length : 0;
            if (targetCols == 0) return;

            // 3. LIMPEZA DE COLUNAS NO CABEÇALHO (Ajusta o cabeçalho para bater com os dados)
            var headerCells = headerRow.Elements<TableCell>().ToList();
            if (headerCells.Count > targetCols)
            {
                for (int i = headerCells.Count - 1; i >= targetCols; i--)
                {
                    headerRow.RemoveChild(headerCells[i]);
                }
                Console.WriteLine($"[DEBUG] Cabeçalho reduzido de {headerCells.Count} para {targetCols} colunas.");
            }

            // 4. LIMPEZA DE LINHAS ANTIGAS
            int headerCount = 1; 
            foreach (var row in rows.Skip(headerCount).ToList())
            {
                table.RemoveChild(row);
            }

            // 5. PREENCHIMENTO DINÂMICO
            foreach (var rowData in data)
            {
                TableRow newRow = (TableRow)rowMolde.CloneNode(true);
                var cells = newRow.Elements<TableCell>().ToList();

                // Ajusta a linha clonada para ter o número exato de colunas dos dados
                if (cells.Count > targetCols)
                {
                    for (int i = cells.Count - 1; i >= targetCols; i--)
                    {
                        newRow.RemoveChild(cells[i]);
                    }
                }

                // Preenche as células restantes
                var finalCells = newRow.Elements<TableCell>().ToList();
                for (int i = 0; i < finalCells.Count; i++)
                {
                    var cell = finalCells[i];
                    string textToInsert = i < rowData.Length ? rowData[i] : "";

                    var textElement = cell.Descendants<Text>().FirstOrDefault();
                    if (textElement != null)
                    {
                        textElement.Text = textToInsert;
                        var extraTexts = cell.Descendants<Text>().Skip(1).ToList();
                        foreach (var et in extraTexts) et.Remove();
                    }
                    else
                    {
                        var p = cell.Elements<Paragraph>().FirstOrDefault() ?? cell.AppendChild(new Paragraph());
                        var r = p.Elements<Run>().FirstOrDefault() ?? p.AppendChild(new Run());
                        r.AppendChild(new Text(textToInsert));
                    }
                }

                table.AppendChild(newRow);
            }
        }

        // Helper desativado (já temos template real)
        static void CreateDummyTemplate(string path) { }
        static TableCell CreateCell(string text, bool bold) { return null; }
    }
}
