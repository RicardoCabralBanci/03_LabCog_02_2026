using System;
using System.IO;
using System.Linq;
using DocumentFormat.OpenXml.Packaging;
using DocumentFormat.OpenXml.CustomProperties;
using DocumentFormat.OpenXml.VariantTypes;

class Program
{
    static void Main(string[] args)
    {
        if (args.Length < 1)
        {
            Console.WriteLine("Uso: DebugProperties.exe <caminho_do_docx>");
            return;
        }

        string filePath = args[0];
        Console.WriteLine($"[DEBUG] Analisando: {filePath}");

        try
        {
            using (var doc = WordprocessingDocument.Open(filePath, false)) // Abre como somente leitura primeiro
            {
                var props = doc.CustomFilePropertiesPart;
                if (props == null || props.Properties == null)
                {
                    Console.WriteLine("[AVISO] Nenhuma propriedade customizada encontrada.");
                }
                else
                {
                    Console.WriteLine("--- Propriedades Atuais ---");
                    foreach (var p in props.Properties)
                    {
                        var prop = (CustomDocumentProperty)p;
                        Console.WriteLine($"Nome: '{prop.Name}' | Valor: '{prop.InnerText}'");
                    }
                }
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"[ERRO] {ex.Message}");
        }
    }
}
