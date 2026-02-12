using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using DocumentFormat.OpenXml.Packaging;
using DocumentFormat.OpenXml.Wordprocessing;

namespace WordStitcher
{
    class Program
    {
        // Mapa Geográfico das Máquinas (Linha Inicial, Linha Final)
        private static readonly Dictionary<string, (int Start, int End)> MachineRanges = new Dictionary<string, (int, int)>
        {
            { "BTR", (5, 138) },
            { "GTR", (142, 271) },
            { "DVD", (277, 440) },
            { "PET", (446, 532) }, 
            { "CIP", (538, 648) },
            { "CMX", (654, 728) },
            { "CCMX", (734, 828) }
        };

        static void Main(string[] args)
        {
            if (args.Length < 1)
            {
                Console.WriteLine("Uso: NewGeradorV2.exe <caminho_do_manifesto.csv>");
                return;
            }

            string manifestPath = args[0];
            string outputFileName = "Manual_Gerado.docx";
            
            try
            {
                if (!File.Exists(manifestPath))
                {
                    ShowError("Manifesto nao encontrado: " + manifestPath);
                    return;
                }

                Console.WriteLine("--- Lendo Manifesto: " + Path.GetFileName(manifestPath) + " ---");
                
                var result = ParseManifest(manifestPath);
                string machineType = result.MachineType;
                var rawFiles = result.Files;

                Console.WriteLine("[INFO] Maquina Solicitada: " + machineType);
                Console.WriteLine("[INFO] Arquivos no Manifesto (Bruto): " + rawFiles.Count);

                var filesToProcess = FilterFilesByRange(rawFiles, machineType);

                if (filesToProcess.Count == 0)
                {
                    ShowError("Nenhum arquivo valido restou apos o filtro para a maquina '" + machineType + "'.");
                    return;
                }

                Console.WriteLine("[INFO] Arquivos para processar (Filtrados): " + filesToProcess.Count);

                string fullOutputPath = Path.Combine(Path.GetDirectoryName(Path.GetFullPath(manifestPath)), outputFileName);
                
                if (!IsFileReady(fullOutputPath))
                {
                    ShowError("O arquivo '" + outputFileName + "' esta aberto. Feche-o e tente novamente.");
                    return;
                }

                StitchDocuments(fullOutputPath, filesToProcess);

                Console.WriteLine("\n[SUCESSO] Manual gerado com exito!");
                Console.WriteLine("Local: " + fullOutputPath);
                System.Threading.Thread.Sleep(3000); 
            }
            catch (Exception ex)
            {
                ShowError("Falha critica: " + ex.Message);
            }
        }

        static List<string> FilterFilesByRange(List<(int Line, string Path)> rawFiles, string machineType)
        {
            string normalizedType = machineType.Split(' ')[0].ToUpper().Trim();

            if (!MachineRanges.ContainsKey(normalizedType))
            {
                Console.WriteLine("[AVISO] Tipo de maquina '" + machineType + "' nao mapeado. Processando TODOS os arquivos.");
                return rawFiles.Select(f => f.Path).ToList();
            }

            var range = MachineRanges[normalizedType];
            Console.WriteLine("[FILTRO] Aplicando filtro '" + normalizedType + "': Linhas " + range.Start + " a " + range.End);

            var validFiles = new List<string>();
            int excludedCount = 0;

            foreach (var item in rawFiles)
            {
                if (item.Line >= range.Start && item.Line <= range.End)
                {
                    validFiles.Add(item.Path);
                }
                else
                {
                    excludedCount++;
                }
            }

            if (excludedCount > 0)
            {
                Console.ForegroundColor = ConsoleColor.Yellow;
                Console.WriteLine("[FILTRO] Removidos " + excludedCount + " arquivos fora do intervalo da maquina.");
                Console.ResetColor();
            }

            return validFiles;
        }

        static (string MachineType, List<(int Line, string Path)> Files) ParseManifest(string manifestPath)
        {
            var files = new List<(int, string)>();
            string machineType = "GENERIC";
            
            string manifestDir = Path.GetDirectoryName(Path.GetFullPath(manifestPath));
            string configBaRoot = Directory.GetParent(manifestDir)?.FullName ?? manifestDir;

            if (Path.GetFileName(manifestDir).Equals("NewGeradorV2", StringComparison.OrdinalIgnoreCase))
            {
                configBaRoot = Directory.GetParent(manifestDir)?.FullName;
            }

            var lines = File.ReadAllLines(manifestPath, Encoding.UTF8);

            foreach (var line in lines)
            {
                var parts = line.Split(';');
                if (parts.Length < 3) continue;

                string category = parts[0].Trim().ToUpper();
                string key = parts[1].Trim().ToUpper();
                string value = parts[2].Trim();

                if (category == "META" && key == "MACHINE_TYPE")
                {
                    machineType = value;
                }
                else if (category == "FILE")
                {
                    int lineIndex = -1;
                    if (int.TryParse(key, out int parsedLine))
                    {
                        lineIndex = parsedLine;
                    }

                    if (key == "SELECTED") lineIndex = 0;

                    string sanitized = SanitizePath(value, configBaRoot);
                    
                    if (File.Exists(sanitized))
                    {
                        files.Add((lineIndex, sanitized));
                    }
                }
            }
            return (machineType, files);
        }

        static string SanitizePath(string rawPath, string rootPath)
        {
            // Substitui todas as barras pela barra do sistema atual
            string clean = rawPath.Replace('/', Path.DirectorySeparatorChar).Replace('\\', Path.DirectorySeparatorChar);
            
            // Remove prefixo de drive (X:)
            if (clean.Length > 1 && clean[1] == ':')
            {
                clean = clean.Substring(2);
            }

            string tag = "Config_BA";
            int index = clean.IndexOf(tag, StringComparison.OrdinalIgnoreCase);
            
            if (index != -1)
            {
                clean = clean.Substring(index + tag.Length);
            }
            
            // Remove barras iniciais
            clean = clean.TrimStart(Path.DirectorySeparatorChar);
            
            return Path.Combine(rootPath, clean);
        }

        static void ShowError(string message)
        {
            Console.ForegroundColor = ConsoleColor.Red;
            Console.WriteLine("\n[ERRO] " + message);
            Console.ResetColor();
            Console.WriteLine("\nPressione qualquer tecla para sair...");
            Console.ReadKey();
        }

        static bool IsFileReady(string filename)
        {
            if (!File.Exists(filename)) return true;
            try
            {
                using (FileStream inputStream = File.Open(filename, FileMode.Open, FileAccess.Read, FileShare.None))
                {
                    return true;
                }
            }
            catch (IOException)
            {
                return false;
            }
        }

        static void StitchDocuments(string outputPath, List<string> inputFiles)
        {
            if (File.Exists(outputPath)) File.Delete(outputPath);

            Console.WriteLine("Iniciando fusao com base: " + Path.GetFileName(inputFiles[0]));
            File.Copy(inputFiles[0], outputPath);

            using (WordprocessingDocument mainDoc = WordprocessingDocument.Open(outputPath, true))
            {
                MainDocumentPart mainPart = mainDoc.MainDocumentPart;
                if (mainPart == null) throw new Exception("Documento base invalido.");

                for (int i = 1; i < inputFiles.Count; i++)
                {
                    mainPart.Document.Body.AppendChild(new Paragraph(
                        new ParagraphProperties(
                            new SectionProperties(new SectionType() { Val = SectionMarkValues.NextPage })
                        )
                    ));

                    string altChunkId = "AltChunkId" + i;
                    AlternativeFormatImportPart chunk = mainPart.AddAlternativeFormatImportPart(
                        AlternativeFormatImportPartType.WordprocessingML, altChunkId);
                    
                    using (FileStream fileStream = File.Open(inputFiles[i], FileMode.Open, FileAccess.Read))
                    {
                        chunk.FeedData(fileStream);
                    }

                    AltChunk altChunk = new AltChunk { Id = altChunkId };
                    mainPart.Document.Body.AppendChild(altChunk);
                }
                mainPart.Document.Save();
            }
        }
    }
}
