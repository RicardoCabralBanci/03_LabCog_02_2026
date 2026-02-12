using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using DocumentFormat.OpenXml;
using DocumentFormat.OpenXml.Packaging;
using DocumentFormat.OpenXml.Wordprocessing;
using DocumentFormat.OpenXml.CustomProperties;
using DocumentFormat.OpenXml.VariantTypes;

namespace WordStitcher
{
    class Program
    {
        // Mapa Geográfico das Máquinas (Mantido por compatibilidade)
        private static readonly Dictionary<string, (int Start, int End)> MachineRanges = new Dictionary<string, (int, int)>
        {
            { "BTR", (5, 138) }, { "GTR", (142, 271) }, { "DVD", (277, 440) },
            { "PET", (446, 532) }, { "CIP", (538, 648) }, { "CMX", (654, 728) },
            { "CCMX", (734, 828) }, { "PLT", (834, 928) }, { "PCK", (933, 2027) }
        };

        static void Main(string[] args)
        {
            Console.WriteLine("--- NewEngine V2.1 (Two Worlds + Safe XML + Data Injection) ---");

            if (args.Length < 1)
            {
                Console.WriteLine("Uso: NewGeradorV2.exe <caminho_do_manifesto.csv>");
                return;
            }

            string manifestPath = args[0];
            
            try
            {
                if (!File.Exists(manifestPath)) { ShowError("Manifesto nao encontrado: " + manifestPath); return; }

                var result = ParseManifest(manifestPath);

                // --- Geracao de Nome Padrao (BA_Order_K_Machine_Lang) ---
                string pOrder = result.Metadata.ContainsKey("ORDER_NUMBER") ? result.Metadata["ORDER_NUMBER"] : "00000000";
                string pMachine = result.Metadata.ContainsKey("MACHINE_TYPE") ? result.Metadata["MACHINE_TYPE"] : "Machine";
                string pLang = result.Metadata.ContainsKey("LANGUAGE") ? result.Metadata["LANGUAGE"] : "XX";
                
                // Busca inteligente pelo K-Number (Tenta K_NUMBER especifico, ou qualquer chave K_ / K-)
                string pK = result.Metadata.ContainsKey("K_NUMBER") ? result.Metadata["K_NUMBER"] : "000000";
                if (pK == "000000")
                {
                    var kKey = result.Metadata.Keys.FirstOrDefault(k => k.StartsWith("K_") || k.StartsWith("K-"));
                    if (kKey != null) pK = result.Metadata[kKey];
                }

                string outputFileName = $"BA_{{pOrder}}_{pK}_{pMachine}_{pLang}.docx";
                // Limpeza de caracteres ilegais para garantir que o Windows aceite
                outputFileName = string.Join("", outputFileName.Split(Path.GetInvalidFileNameChars()));
                
                Console.WriteLine($"[CONFIG] Nome do arquivo definido: {outputFileName}");

                var filesToProcess = FilterFilesByRange(result.Files, result.Metadata.ContainsKey("MACHINE_TYPE") ? result.Metadata["MACHINE_TYPE"] : "GENERIC");

                if (filesToProcess.Count == 0) { ShowError("Nenhum arquivo valido."); return; }

                string fullOutputPath = Path.Combine(Path.GetDirectoryName(Path.GetFullPath(manifestPath)), outputFileName);
                
                if (!IsFileReady(fullOutputPath)) { ShowError("O arquivo de saida esta aberto. Feche-o."); return; }

                StitchDocuments(fullOutputPath, filesToProcess, result.Metadata);

                Console.WriteLine("\n[SUCESSO] Manual gerado: " + fullOutputPath);
            }
            catch (Exception ex)
            {
                ShowError("Falha critica: " + ex.Message + "\nStack: " + ex.StackTrace);
            }

            // Saida controlada pelo usuario
            Console.WriteLine("\nProcesso finalizado.");
            Console.WriteLine("Pressione qualquer tecla para fechar...");
            Console.ReadKey(true);
        }

        static void StitchDocuments(string outputPath, List<string> inputFiles, Dictionary<string, string> metadata)
        {
            Console.WriteLine("[INFO] Iniciando empilhamento Hibrido (Capa Isolada + Corpo Padronizado)...");
            Console.WriteLine("[INFO] Saida: " + outputPath);

            // --- 1. Captura layout do Manual Padrao ---
            string manualLayoutXml = null;
            try {
                string templatePath = FindTemplate(inputFiles[0]);
                if (templatePath != null && File.Exists(templatePath)) {
                    using (var doc = WordprocessingDocument.Open(templatePath, false)) {
                        var sectPr = doc.MainDocumentPart.Document.Body.Elements<SectionProperties>().LastOrDefault();
                        if (sectPr != null)
                        {
                            manualLayoutXml = sectPr.OuterXml;
                            Console.WriteLine("[CONFIG] Layout do 'manual.dotm' carregado.");
                        }
                    }
                } else {
                    Console.WriteLine("[AVISO] Template 'manual.dotm' nao foi localizado na arvore de diretorios.");
                }
            } catch { Console.WriteLine("[ERRO] Falha ao ler layout do manual.dotm."); }


            // --- 2. Construcao do Documento ---
            if (File.Exists(outputPath)) File.Delete(outputPath);
            File.Copy(inputFiles[0], outputPath);

            using (WordprocessingDocument mainDoc = WordprocessingDocument.Open(outputPath, true))
            {
                MainDocumentPart mainPart = mainDoc.MainDocumentPart;
                var body = mainPart.Document.Body;

                // --- CIRURGIA DE ISOLAMENTO (Destronar o layout original para isolar a Capa) ---
                // Pegamos o layout que veio com o arquivo da Capa
                var coverSectPr = body.Elements<SectionProperties>().LastOrDefault();
                string coverSectXml = coverSectPr?.OuterXml;
                
                // IMPORTANTE: Removemos ele do final do Body para que nao conflite com o layout final
                if (coverSectPr != null) coverSectPr.Remove();

                for (int i = 1; i < inputFiles.Count; i++)
                {
                    Console.WriteLine(" [+] Anexando: " + inputFiles[i]);
                    Paragraph separator;

                    if (i == 1)
                    {
                        // Criamos a muralha usando o DNA original da Capa
                        SectionProperties breakSectPr = !string.IsNullOrEmpty(coverSectXml) 
                            ? new SectionProperties(coverSectXml) 
                            : new SectionProperties();
                        
                        // Forca ser uma quebra de secao NextPage
                        var sType = breakSectPr.GetFirstChild<SectionType>();
                        if (sType == null) breakSectPr.AppendChild(new SectionType() { Val = SectionMarkValues.NextPage });
                        else sType.Val = SectionMarkValues.NextPage;

                        separator = new Paragraph(new ParagraphProperties(breakSectPr));
                        Console.WriteLine("     -> Capa isolada com seu DNA original.");
                    }
                    else
                    {
                        separator = new Paragraph(new Run(new Break() { Type = BreakValues.Page }));
                    }

                    body.AppendChild(separator);
                    AppendViaAltChunk(mainPart, inputFiles[i], "AltChunkId" + i);
                }

                // --- 3. Aplicacao da Lei do Manual (Novo Rei do Corpo) ---
                if (!string.IsNullOrEmpty(manualLayoutXml))
                {
                    var newSectPr = new SectionProperties(manualLayoutXml);
                    body.AppendChild(newSectPr);
                    Console.WriteLine("[CONFIG] Layout do Manual aplicado ao corpo.");
                }

                // --- 4. Injeção de Metadados (Capa) ---
                InjectMetadata(mainDoc, metadata);

                // Update Fields (Corrigido para evitar erro de reatribuicao de RootElement)
                var settingsPart = mainPart.DocumentSettingsPart ?? mainPart.AddNewPart<DocumentSettingsPart>();
                
                if (settingsPart.Settings == null)
                {
                    settingsPart.Settings = new Settings();
                }

                if (settingsPart.Settings.GetFirstChild<UpdateFieldsOnOpen>() == null)
                    settingsPart.Settings.Append(new UpdateFieldsOnOpen() { Val = true });

                mainPart.Document.Save();
            }
        }

        static void InjectMetadata(WordprocessingDocument mainDoc, Dictionary<string, string> metadata)
        {
            Console.WriteLine("[METADATA] Iniciando injecao de dados...");

            var customPropsPart = mainDoc.CustomFilePropertiesPart;
            if (customPropsPart == null)
            {
                customPropsPart = mainDoc.AddCustomFilePropertiesPart();
                customPropsPart.Properties = new Properties();
            }

            // Mapeamento Chave do Manifesto -> Propriedade do Word
            var map = new Dictionary<string, string>
            {
                { "MACHINE_TYPE", "MachineType" }, // Mantido para compatibilidade, mas sera sobrescrito se MACHINE_NAME_FULL existir
                { "SAP_NUMBER", "MachineNumber" },
                { "ORDER_NUMBER", "Order" },
                { "REVISION", "Revision" },
                { "YEAR", "MachineYear" }
            };

            foreach (var kvp in map)
            {
                if (metadata.ContainsKey(kvp.Key))
                {
                    UpsertProperty(customPropsPart.Properties, kvp.Value, metadata[kvp.Key]);
                    Console.WriteLine($"  -> Set: {kvp.Value} = {metadata[kvp.Key]}");
                }
            }

            // [NOVO] Logica Especial para Nome Completo da Maquina (Preenche ambos os campos para compatibilidade total)
            if (metadata.ContainsKey("MACHINE_NAME_FULL"))
            {
                string fullName = metadata["MACHINE_NAME_FULL"];
                Console.WriteLine($"  -> [SPECIAL] MACHINE_NAME_FULL detectado: {fullName}");
                
                // 1. Atualiza MachineType (Usado pelos novos templates)
                UpsertProperty(customPropsPart.Properties, "MachineType", fullName);
                Console.WriteLine($"  -> Set: MachineType = {fullName}");

                // 2. Atualiza MachineModel (Usado pelos templates legados tipo Innopack)
                UpsertProperty(customPropsPart.Properties, "MachineModel", fullName);
                Console.WriteLine($"  -> Set: MachineModel = {fullName}");
            }
        }

        static void UpsertProperty(Properties props, string propName, string propValue)
        {
            var prop = props.Where(p => ((CustomDocumentProperty)p).Name.Value == propName).FirstOrDefault();
            
            if (prop != null)
            {
                // Atualiza
                var vpw = prop.FirstChild as DocumentFormat.OpenXml.VariantTypes.VTLPWSTR;
                if (vpw != null) vpw.Text = propValue;
                else 
                {
                    prop.RemoveAllChildren(); // Limpa se for outro tipo
                    prop.AppendChild(new DocumentFormat.OpenXml.VariantTypes.VTLPWSTR(propValue)); 
                }
            }
            else
            {
                // Cria
                var newProp = new CustomDocumentProperty() 
                { 
                    FormatId = "{D5CDD505-2E9C-101B-9397-08002B2CF9AE}", // GUID padrao para Custom Props
                    Name = propName
                };
                
                // Calcula PID seguro (Max + 1)
                int maxPid = 1;
                foreach (CustomDocumentProperty p in props)
                {
                    if (p.PropertyId != null && p.PropertyId > maxPid) maxPid = p.PropertyId;
                }
                newProp.PropertyId = maxPid + 1;

                newProp.AppendChild(new DocumentFormat.OpenXml.VariantTypes.VTLPWSTR(propValue));
                props.AppendChild(newProp);
            }
        }

        // --- Helpers ---

        static string FindTemplate(string refFile)
        {
            string startDir = Path.GetDirectoryName(Path.GetFullPath(refFile));
            DirectoryInfo dir = new DirectoryInfo(startDir);
            
            Console.WriteLine("[BUSCA] Procurando 'manual.dotm' a partir de: " + startDir);

            while (dir != null) {
                string templatePath = Path.Combine(dir.FullName, "manual.dotm");
                Console.WriteLine("  [?] Tentando: " + templatePath);
                
                if (File.Exists(templatePath)) {
                    Console.WriteLine("  [!] SUCESSO: Encontrado em " + templatePath);
                    return templatePath;
                }

                // Se chegamos na raiz do projeto (Config_BA), paramos de subir
                if (dir.Name.Equals("Config_BA", StringComparison.OrdinalIgnoreCase)) break;
                
                dir = dir.Parent;
            }
            
            return null; // Retorna null se nao achar nada
        }

        static void AppendViaAltChunk(MainDocumentPart mainPart, string filePath, string chunkId)
        {
            AlternativeFormatImportPart chunk = mainPart.AddAlternativeFormatImportPart(
                AlternativeFormatImportPartType.WordprocessingML, chunkId);
            using (FileStream fileStream = File.Open(filePath, FileMode.Open, FileAccess.Read))
            {
                chunk.FeedData(fileStream);
            }
            AltChunk altChunk = new AltChunk { Id = chunkId };
            mainPart.Document.Body.AppendChild(altChunk);
        }

        static List<string> FilterFilesByRange(List<(int Line, string Path)> rawFiles, string machineType)
        {
            // Logica simplificada de filtro (Mantida do original)
            string normalizedType = machineType.Split(' ')[0].ToUpper().Trim();
            if (!MachineRanges.ContainsKey(normalizedType)) return rawFiles.Select(f => f.Path).ToList();
            var range = MachineRanges[normalizedType];
            return rawFiles.Where(x => x.Line >= range.Start && x.Line <= range.End).Select(x => x.Path).ToList();
        }

        static (Dictionary<string, string> Metadata, List<(int Line, string Path)> Files) ParseManifest(string manifestPath)
        {
            // Logica de parse (Mantida do original)
            var files = new List<(int, string)>();
            var metadata = new Dictionary<string, string>();
            string manifestDir = Path.GetDirectoryName(Path.GetFullPath(manifestPath));
            string configBaRoot = Directory.GetParent(manifestDir)?.FullName ?? manifestDir;
            if (Path.GetFileName(manifestDir).Equals("NewGeradorV2", StringComparison.OrdinalIgnoreCase))
                configBaRoot = Directory.GetParent(manifestDir)?.FullName;

            foreach (var line in File.ReadAllLines(manifestPath, Encoding.UTF8))
            {
                var parts = line.Split(';');
                if (parts.Length < 3) continue;
                string key = parts[1].Trim().ToUpper();
                string val = parts[2].Trim();
                if (parts[0].Trim().ToUpper() == "META") metadata[key] = val;
                else if (parts[0].Trim().ToUpper() == "FILE")
                {
                    int ln = 0; int.TryParse(key, out ln);
                    if (key == "SELECTED") ln = 0;
                    string path = SanitizePath(val, configBaRoot);
                    if (File.Exists(path)) files.Add((ln, path));
                }
            }
            return (metadata, files);
        }

        static string SanitizePath(string rawPath, string rootPath)
        {
            string clean = rawPath.Replace('/', Path.DirectorySeparatorChar).Replace('\\', Path.DirectorySeparatorChar);
            if (clean.Length > 1 && clean[1] == ':') clean = clean.Substring(2);
            int index = clean.IndexOf("Config_BA", StringComparison.OrdinalIgnoreCase);
            if (index != -1) clean = clean.Substring(index + 9);
            return Path.Combine(rootPath, clean.TrimStart(Path.DirectorySeparatorChar));
        }

        static void ShowError(string msg) { Console.ForegroundColor = ConsoleColor.Red; Console.WriteLine("\n[ERRO] " + msg); Console.ResetColor(); }
        static bool IsFileReady(string f) { if (!File.Exists(f)) return true; try { using (File.Open(f, FileMode.Open, FileAccess.Read, FileShare.None)) return true; } catch { return false; } }
    }
}
