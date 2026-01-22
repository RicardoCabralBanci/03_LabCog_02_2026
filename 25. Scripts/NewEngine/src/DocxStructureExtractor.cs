using System;
using System.IO;
using System.IO.Compression;
using System.Xml;
using System.Text;
using System.Collections.Generic;
using System.Linq;

namespace DocxExtractor
{
    class Program
    {
        static void Main(string[] args)
        {
            if (args.Length == 0)
            {
                Console.WriteLine("Usage: DocxExtractor.exe <path_to_docx>");
                return;
            }

            string filePath = args[0];
            if (!File.Exists(filePath))
            {
                Console.WriteLine("Error: File not found: " + filePath);
                return;
            }

            try
            {
                ExtractStructure(filePath);
            }
            catch (Exception ex)
            {
                Console.WriteLine("Error processing file: " + ex.Message);
                Console.WriteLine(ex.StackTrace);
            }
        }

        static void ExtractStructure(string filePath)
        {
            using (FileStream fs = new FileStream(filePath, FileMode.Open, FileAccess.Read, FileShare.ReadWrite))
            using (ZipArchive archive = new ZipArchive(fs, ZipArchiveMode.Read))
            {
                var documentEntry = archive.GetEntry("word/document.xml");
                if (documentEntry == null)
                {
                    Console.WriteLine("Error: Invalid docx file (missing word/document.xml)");
                    return;
                }

                var numberingEntry = archive.GetEntry("word/numbering.xml");
                Dictionary<string, string> numberingMap = new Dictionary<string, string>();
                if (numberingEntry != null)
                {
                    // Basic numbering parsing could be added here, but it's complex.
                    // For now, we focus on Outline Levels and Styles.
                }

                using (Stream stream = documentEntry.Open())
                using (XmlReader reader = XmlReader.Create(stream))
                {
                    XmlNamespaceManager nsManager = new XmlNamespaceManager(reader.NameTable);
                    nsManager.AddNamespace("w", "http://schemas.openxmlformats.org/wordprocessingml/2006/main");

                    while (reader.Read())
                    {
                        if (reader.NodeType == XmlNodeType.Element && reader.Name == "w:p")
                        {
                            ProcessParagraph(reader, nsManager);
                        }
                    }
                }
            }
        }

        static void ProcessParagraph(XmlReader reader, XmlNamespaceManager nsManager)
        {
            string styleId = null;
            string outlineLevel = null;
            string numId = null;
            string ilvl = null;
            StringBuilder textBuilder = new StringBuilder();

            // Read the entire paragraph node into an XElement or similar strictly for this subtree
            // Or use a sub-reader. Since we are using XmlReader for speed/no-dep, we manually traverse.
            
            using (XmlReader pReader = reader.ReadSubtree())
            {
                while (pReader.Read())
                {
                    if (pReader.NodeType == XmlNodeType.Element)
                    {
                        switch (pReader.Name)
                        {
                            case "w:pStyle":
                                styleId = pReader.GetAttribute("w:val", nsManager.LookupNamespace("w"));
                                break;
                            case "w:outlineLvl":
                                outlineLevel = pReader.GetAttribute("w:val", nsManager.LookupNamespace("w"));
                                break;
                            case "w:numId":
                                numId = pReader.GetAttribute("w:val", nsManager.LookupNamespace("w"));
                                break;
                            case "w:ilvl":
                                ilvl = pReader.GetAttribute("w:val", nsManager.LookupNamespace("w"));
                                break;
                            case "w:t":
                                pReader.Read(); // Move to text content
                                if (pReader.NodeType == XmlNodeType.Text)
                                {
                                    textBuilder.Append(pReader.Value);
                                }
                                break;
                        }
                    }
                }
            }

            string text = textBuilder.ToString().Trim();

            // Determine if it's a heading
            bool isHeading = false;
            int level = 9; // Body text default

            if (!string.IsNullOrEmpty(outlineLevel))
            {
                if (int.TryParse(outlineLevel, out int parsedLvl))
                {
                    level = parsedLvl; // 0-based in XML (0 = Heading 1)
                    isHeading = true;
                }
            }
            else if (!string.IsNullOrEmpty(styleId))
            {
                // Fallback: check style names (standard Word styles)
                if (styleId.StartsWith("Heading") || styleId.StartsWith("Ttulo"))
                {
                    // Try to extract number from style name "Heading1" -> 1
                    string numberPart = new string(styleId.Where(char.IsDigit).ToArray());
                    if (int.TryParse(numberPart, out int styleLvl))
                    {
                        level = styleLvl - 1; // Convert to 0-based
                        isHeading = true;
                    }
                }
            }

            if (isHeading || !string.IsNullOrEmpty(text)) // Output headings or non-empty text
            {
                // Format output for easy parsing: [Level] Text
                // Level 9 = Body Text
                Console.WriteLine("[" + level + "] " + text);
            }
        }
    }
}
