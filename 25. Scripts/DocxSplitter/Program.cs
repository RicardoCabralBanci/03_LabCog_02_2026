using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using DocumentFormat.OpenXml;
using DocumentFormat.OpenXml.Packaging;
using DocumentFormat.OpenXml.Wordprocessing;

namespace DocxSplitter
{
    class Program
    {
        static void Main(string[] args)
        {
            string sourceFile = @"C:\LabCogKHS_CLI\40_Personas\040. Mestre em VBA (A Garagem de Autópsias Digitais)\03. Projetos\00. Gerador_Automatico_Manuais\20. Tradutor_PDF_Word\BA 89503126_000100 _Innopal_EN.docx";
            string outputDir = Path.Combine(Path.GetDirectoryName(sourceFile), "Split_Chapters");

            if (!File.Exists(sourceFile))
            {
                Console.WriteLine($"Error: File not found at {sourceFile}");
                return;
            }

            if (!Directory.Exists(outputDir)) Directory.CreateDirectory(outputDir);

            // TEMPLATE CONFIGURATION
            // Priority 1: Script Directory (Hardcoded as requested)
            string templatePath = @"C:\LabCogKHS_CLI\25. Scripts\DocxSplitter\manual.dotm";
            
            // Priority 2: Source Directory (Backup)
            if (!File.Exists(templatePath)) 
            {
                 templatePath = Path.Combine(Path.GetDirectoryName(sourceFile) ?? "", "manual.dotm");
            }

            bool useTemplate = File.Exists(templatePath);
            SectionProperties templateSectPr = null;

            if (useTemplate) 
            {
                Console.WriteLine($"Using Template: {templatePath}");
                // Pre-load Template Section Properties (Margins, Page Size)
                try
                {
                    using (var tDoc = WordprocessingDocument.Open(templatePath, false))
                    {
                        templateSectPr = tDoc.MainDocumentPart.Document.Body.Elements<SectionProperties>().LastOrDefault()?.CloneNode(true) as SectionProperties;
                    }
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"Warning: Failed to read template layout. {ex.Message}");
                }
            }
            else Console.WriteLine("Warning: 'manual.dotm' not found. Formatting will be limited.");

            // 16pt no Word = 32 no OpenXML (unidade é half-points)
            const string TargetFontSize = "32"; 
            
            var expectedChapters = new Dictionary<int, string[]>
            {
                {1, new[] {"General", "General information"}},
                {2, new[] {"Safety"}},
                {3, new[] {"Layout and function", "Design and function"}},
                {4, new[] {"Assembly", "Installation"}},
                {5, new[] {"Operation"}},
                {6, new[] {"Servicing", "Maintenance", "Care and maintenance"}},
                {7, new[] {"Faults", "Troubleshooting"}},
                {8, new[] {"Technical data"}}
            };

            Console.WriteLine($"Analyzing: {sourceFile}");
            Console.WriteLine($"Strategy: Strict Size ({TargetFontSize}) + Sequence + FULL TEMPLATE INJECTION");

            var finalChapters = new List<ChapterInfo>();
            
            using (WordprocessingDocument doc = WordprocessingDocument.Open(sourceFile, false))
            {
                var body = doc.MainDocumentPart.Document.Body;
                var elements = body.Elements().ToList();
                
                int currentTargetChapter = 1;

                for (int i = 0; i < elements.Count; i++)
                {
                    if (elements[i] is Paragraph p)
                    {
                        var run = p.Elements<Run>().FirstOrDefault();
                        var size = run?.RunProperties?.FontSize?.Val?.Value;

                        if (size != TargetFontSize) continue;
                        string text = p.InnerText.Trim();
                        if (string.IsNullOrEmpty(text)) continue;

                        if (currentTargetChapter <= 8)
                        {
                            if (CheckChapterMatch(text, currentTargetChapter, expectedChapters, elements, i))
                            {
                                Console.WriteLine($"[MATCH] Chapter {currentTargetChapter} found at index {i}: '{{text}}'");

                                if (finalChapters.Count > 0) finalChapters.Last().EndIndex = i - 1;

                                string title = expectedChapters[currentTargetChapter][0];
                                finalChapters.Add(new ChapterInfo 
                                {
                                    Title = $"{currentTargetChapter:00}_{title}", 
                                    StartIndex = i 
                                });

                                currentTargetChapter++; 
                            }
                        }
                    }
                }
                if (finalChapters.Count > 0) finalChapters.Last().EndIndex = elements.Count - 1;
            }

            if (finalChapters.Count == 0)
            {
                Console.WriteLine("No chapters found.");
                return;
            }

            Console.WriteLine($"\nSplitting into {finalChapters.Count} files...");
            foreach (var chapter in finalChapters)
            {
                string cleanTitle = SanitizeFilename(chapter.Title);
                string newFileName = $"{cleanTitle}.docx";
                string destPath = Path.Combine(outputDir, newFileName);
                
                Console.WriteLine($"Saving: {newFileName}");
                File.Copy(sourceFile, destPath, true);
                
                // 1. Prune Content AND Inject Template Layout
                PruneAndFormat(destPath, chapter.StartIndex, chapter.EndIndex, templateSectPr);

                // 2. Apply Template Styles
                if (useTemplate) ApplyTemplateStyles(destPath, templatePath);
            }
            Console.WriteLine("Done!");
        }

        static void PruneAndFormat(string filePath, int keepStart, int keepEnd, SectionProperties templateSectPr)
        {
            using (WordprocessingDocument doc = WordprocessingDocument.Open(filePath, true))
            {
                var body = doc.MainDocumentPart.Document.Body;
                var elements = body.Elements().ToList();

                // Remove content
                for (int i = elements.Count - 1; i > keepEnd; i--) elements[i].Remove();
                for (int i = 0; i < keepStart; i++) elements[i].Remove();

                // INJECT TEMPLATE LAYOUT (Margins/Size)
                if (templateSectPr != null)
                {
                    // Remove existing SectPr (from original doc)
                    var existingSectPr = body.Elements<SectionProperties>().LastOrDefault();
                    if (existingSectPr != null) existingSectPr.Remove();
                    
                    // Add Template SectPr
                    body.Append(templateSectPr.CloneNode(true));
                }
                
                doc.Save();
            }
        }

        static void ApplyTemplateStyles(string targetPath, string templatePath)
        {
            try
            {
                using (var templateDoc = WordprocessingDocument.Open(templatePath, false))
                using (var targetDoc = WordprocessingDocument.Open(targetPath, true))
                {
                    // Replace Styles
                    var templateStyles = templateDoc.MainDocumentPart.StyleDefinitionsPart;
                    var targetStyles = targetDoc.MainDocumentPart.StyleDefinitionsPart;

                    if (templateStyles != null && targetStyles != null)
                    {
                        using (StreamReader reader = new StreamReader(templateStyles.GetStream()))
                        {
                            string styleContent = reader.ReadToEnd();
                            using (StreamWriter writer = new StreamWriter(targetStyles.GetStream(FileMode.Create)))
                            {
                                writer.Write(styleContent);
                            }
                        }
                    }
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error applying template: {ex.Message}");
            }
        }

        static bool CheckChapterMatch(string text, int targetNum, Dictionary<int, string[]> dictionary, List<OpenXmlElement> elements, int currentIndex)
        {
            string cleanText = text.Replace(".", "").Trim();
            string targetNumStr = targetNum.ToString();

            // Padrão: "1 General information"
            if (cleanText.StartsWith(targetNumStr))
            {
                foreach (var keyword in dictionary[targetNum])
                {
                    if (cleanText.Contains(keyword, StringComparison.OrdinalIgnoreCase)) return true;
                }
            }

            // Padrão: "1" em uma linha e "General information" na próxima
            if (cleanText == targetNumStr && currentIndex + 1 < elements.Count)
            {
                string nextText = elements[currentIndex + 1].InnerText.Trim();
                foreach (var keyword in dictionary[targetNum])
                {
                    if (nextText.Contains(keyword, StringComparison.OrdinalIgnoreCase)) return true;
                }
            }

            return false;
        }

        static string SanitizeFilename(string name)
        {
            foreach (char c in Path.GetInvalidFileNameChars()) name = name.Replace(c, '_');
            if (name.Length > 50) name = name.Substring(0, 50);
            return name.Trim();
        }

        class ChapterInfo
        {
            public string Title { get; set; } 
            public int StartIndex { get; set; }
            public int EndIndex { get; set; }
        }
    }
}