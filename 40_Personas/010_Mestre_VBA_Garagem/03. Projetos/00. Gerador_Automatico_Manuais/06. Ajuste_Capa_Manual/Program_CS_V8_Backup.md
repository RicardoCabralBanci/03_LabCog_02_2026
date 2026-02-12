# Backup do Motor C# - Versão 8 (Injeção Dupla de Metadados)

Este arquivo contém o código fonte do `Program.cs` após a correção do "Cisma da Capa". 

```csharp
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using DocumentFormat.OpenXml.Packaging;
using DocumentFormat.OpenXml.CustomProperties;
using DocumentFormat.OpenXml.VariantTypes;

namespace NewGerador
{
    class Program
    {
        // Dicionário de intervalos de linhas por tipo de máquina
        private static readonly Dictionary<string, (int Start, int End)> MachineRanges = new Dictionary<string, (int Start, int End)>
        {
            { "BTR", (734, 828) },
            { "DTR", (734, 828) },
            { "CCMX", (734, 828) },
            { "CMX", (734, 828) },
            { "CIP", (734, 828) },
            { "PET", (734, 828) },
            { "GTR", (734, 828) },
            { "DVD", (734, 828) },
            { "PLT", (1, 10000) },
            { "PCK", (1, 10000) }
        };

        static void Main(string[] args)
        {
            if (args.Length < 1) return;
            string manifestPath = args[0];
            if (!File.Exists(manifestPath)) return;
            try { ProcessManifest(manifestPath); }
            catch (Exception ex) { Console.WriteLine(ex.Message); }
        }

        static void ProcessManifest(string manifestPath)
        {
            var (metadata, files) = ParseManifest(manifestPath);
            if (files.Count == 0) return;

            string machineType = metadata.ContainsKey("MACHINE_TYPE") ? metadata["MACHINE_TYPE"] : "GENERIC";
            var filesToProcess = FilterFilesByRange(files, machineType);
            if (filesToProcess.Count == 0) return;

            string templatePath = filesToProcess[0];
            string outputPath = Path.Combine(Path.GetDirectoryName(templatePath), $"Gerado_{Path.GetFileName(templatePath)}");
            File.Copy(templatePath, outputPath, true);

            using (WordprocessingDocument mainDoc = WordprocessingDocument.Open(outputPath, true))
            {
                InjectMetadata(mainDoc, metadata);
                var mainPart = mainDoc.MainDocumentPart;
                for (int i = 1; i < filesToProcess.Count; i++)
                {
                    AppendDocument(mainPart, filesToProcess[i]);
                }
                mainPart.Document.Save();
            }
        }

        static void InjectMetadata(WordprocessingDocument mainDoc, Dictionary<string, string> metadata)
        {
            var customPropsPart = mainDoc.CustomFilePropertiesPart ?? mainDoc.AddCustomFilePropertiesPart();
            if (customPropsPart.Properties == null) customPropsPart.Properties = new Properties();

            var map = new Dictionary<string, string>
            {
                { "MACHINE_TYPE", "MachineType" },
                { "SAP_NUMBER", "MachineNumber" },
                { "ORDER_NUMBER", "Order" },
                { "REVISION", "Revision" },
                { "YEAR", "MachineYear" }
            };

            foreach (var kvp in map)
            {
                if (metadata.ContainsKey(kvp.Key))
                    UpsertProperty(customPropsPart.Properties, kvp.Value, metadata[kvp.Key]);
            }

            if (metadata.ContainsKey("MACHINE_NAME_FULL"))
            {
                string fullName = metadata["MACHINE_NAME_FULL"];
                UpsertProperty(customPropsPart.Properties, "MachineType", fullName);
                UpsertProperty(customPropsPart.Properties, "MachineModel", fullName);
            }
            customPropsPart.Properties.Save();
        }

        static void UpsertProperty(Properties props, string propName, string value)
        {
            var prop = props.Where(p => ((CustomDocumentProperty)p).Name.Value == propName).FirstOrDefault();
            if (prop != null) prop.Remove();

            var newProp = new CustomDocumentProperty
            {
                Name = propName,
                FormatId = "{D5CDD505-2E9C-101B-9397-08002B2CF9AE}",
                PropertyId = 2 + props.Count()
            };
            newProp.VTLPWSTR = new VTLPWSTR(value);
            props.AppendChild(newProp);
        }

        static void AppendDocument(MainDocumentPart mainPart, string sourcePath)
        {
            string altChunkId = "AltChunkId" + Guid.NewGuid().ToString().Substring(0, 8);
            AlternativeFormatImportPart chunk = mainPart.AddAlternativeFormatImportPart(AlternativeFormatImportPartType.WordprocessingML, altChunkId);
            using (FileStream fileStream = File.Open(sourcePath, FileMode.Open)) { chunk.FeedData(fileStream); }
            AltChunk altChunk = new AltChunk { Id = altChunkId };
            mainPart.Document.Body.AppendChild(altChunk);
        }

        static (Dictionary<string, string> Metadata, List<string> Files) ParseManifest(string manifestPath)
        {
            var metadata = new Dictionary<string, string>();
            var files = new List<(int Row, string Path)>();
            foreach (var line in File.ReadAllLines(manifestPath))
            {
                var parts = line.Split(';');
                if (parts.Length < 3) continue;
                if (parts[0] == "META") metadata[parts[1]] = parts[2];
                else if (parts[0] == "FILE") files.Add((int.Parse(parts[1]), parts[2]));
            }
            return (metadata, files.OrderBy(f => f.Row).Select(f => f.Path).ToList());
        }

        static List<string> FilterFilesByRange(List<string> rawFiles, string machineType)
        {
            string prefix = machineType.Split(' ')[0].ToUpper();
            if (!MachineRanges.ContainsKey(prefix)) return rawFiles;
            return rawFiles;
        }
    }
}
```
