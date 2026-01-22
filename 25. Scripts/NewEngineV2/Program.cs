using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using DocumentFormat.OpenXml;
using DocumentFormat.OpenXml.Packaging;
using DocumentFormat.OpenXml.Wordprocessing;

namespace NewEngineV2
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("--- NewEngineV2: Protocolo Two Worlds & Safe XML ---");
            
            if (args.Length < 3)
            {
                Console.WriteLine("Uso: NewEngineV2.exe <output.docx> <capa.docx> <manual_modelo.dotm> <doc1.docx> <doc2.docx> ...");
                return;
            }

            string outputPath = args[0];
            string capaPath = args[1];
            string templatePath = args[2];
            var sourceFiles = args.Skip(3).ToList();

            try
            {
                MergeDocuments(outputPath, capaPath, templatePath, sourceFiles);
                Console.WriteLine($"\n[SUCESSO] Documento gerado em: {outputPath}");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"\n[ERRO CRÍTICO] {ex.Message}");
                Console.WriteLine(ex.StackTrace);
            }
        }

        static void MergeDocuments(string output, string capa, string template, List<string> sources)
        {
            // 1. Extrair o DNA do Layout do Manual (Safe XML)
            string manualLayoutXml = ExtractSectionXml(template);
            Console.WriteLine("[INFO] DNA do Layout extraído do modelo.");

            // Criar o documento de destino baseado na Capa
            File.Copy(capa, output, true);

            using (WordprocessingDocument destDoc = WordprocessingDocument.Open(output, true))
            {
                MainDocumentPart mainPart = destDoc.MainDocumentPart ?? destDoc.AddMainDocumentPart();
                Body body = mainPart.Document.Body ?? mainPart.Document.AppendChild(new Body());

                // --- MUNDO 1: ISOLAMENTO DA CAPA ---
                // Inserimos uma quebra de seção (Próxima Página) logo após o conteúdo da capa
                // Isso garante que as margens da capa não vazem para o resto
                Console.WriteLine("[INFO] Isolando Mundo 1 (Capa)...");
                var sectionBreak = new Paragraph(
                    new ParagraphProperties(
                        new SectionProperties(
                            new SectionType() { Val = SectionMarkValues.NextPage }
                        )
                    )
                );
                body.AppendChild(sectionBreak);

                // --- MUNDO 2: O CORPO DO MANUAL ---
                Console.WriteLine("[INFO] Construindo Mundo 2 (Corpo)...");
                
                for (int i = 0; i < sources.Count; i++)
                {
                    string sourcePath = sources[i];
                    Console.WriteLine($" -> Inserindo: {Path.GetFileName(sourcePath)}");

                    string altChunkId = "AltChunkId" + i;
                    AlternativeFormatImportPart chunk = mainPart.AddAlternativeFormatImportPart(AlternativeFormatImportPartType.WordprocessingML, altChunkId);
                    
                    using (FileStream fs = FileStream.OpenRead(sourcePath))
                    {
                        chunk.FeedData(fs);
                    }

                    AltChunk altChunk = new AltChunk();
                    altChunk.Id = altChunkId;
                    body.AppendChild(altChunk);

                    // Se não for o último, podemos colocar um PageBreak simples (dentro da mesma seção)
                    if (i < sources.Count - 1)
                    {
                        body.AppendChild(new Paragraph(new Run(new Break() { Type = BreakValues.Page })));
                    }
                }

                // --- APLICAÇÃO DO LAYOUT FINAL (SAFE XML) ---
                if (!string.IsNullOrEmpty(manualLayoutXml))
                {
                    Console.WriteLine("[INFO] Aplicando DNA de Layout ao Mundo 2...");
                    // Renascemos o XML limpo para evitar erros de "Part Ownership"
                    body.AppendChild(new SectionProperties(manualLayoutXml));
                }

                // Habilitar atualização automática do Sumário ao abrir
                EnableUpdateFields(mainPart);
                
                mainPart.Document.Save();
            }
        }

        static string ExtractSectionXml(string docPath)
        {
            try
            {
                using (WordprocessingDocument doc = WordprocessingDocument.Open(docPath, false))
                {
                    var lastSection = doc.MainDocumentPart.Document.Body.Elements<SectionProperties>().LastOrDefault();
                    return lastSection?.OuterXml ?? "";
                }
            }
            catch { return ""; }
        }

        static void EnableUpdateFields(MainDocumentPart mainPart)
        {
            DocumentSettingsPart settingsPart = mainPart.DocumentSettingsPart ?? mainPart.AddNewPart<DocumentSettingsPart>();
            if (settingsPart.Settings == null) settingsPart.Settings = new Settings();
            
            settingsPart.Settings.Append(new UpdateFieldsOnOpen() { Val = true });
        }
    }
}
