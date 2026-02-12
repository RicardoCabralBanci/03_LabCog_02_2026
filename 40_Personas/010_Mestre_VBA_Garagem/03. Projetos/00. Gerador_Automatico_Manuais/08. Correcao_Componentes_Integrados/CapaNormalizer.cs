using System;
using System.IO;
using System.Linq;
using DocumentFormat.OpenXml;
using DocumentFormat.OpenXml.Packaging;
using DocumentFormat.OpenXml.Wordprocessing;

namespace WordStitcher
{
    class CapaNormalizer
    {
        public static void Run(string capaPath, string templatePath, string outputPath)
        {
            Console.WriteLine("--- Normalizador de Capa ---");
            Console.WriteLine("Capa (Conteudo): " + Path.GetFileName(capaPath));
            Console.WriteLine("Template (Formato): " + Path.GetFileName(templatePath));

            // 1. Cria uma cópia do Template para ser o arquivo de saída
            File.Copy(templatePath, outputPath, true);

            using (WordprocessingDocument doc = WordprocessingDocument.Open(outputPath, true))
            {
                // Se for .dotm, converte para .docx
                doc.ChangeDocumentType(DocumentFormat.OpenXml.WordprocessingDocumentType.Document);

                MainDocumentPart mainPart = doc.MainDocumentPart;
                var body = mainPart.Document.Body;

                // 2. Captura a "Alma" do Template (Configurações de Seção: Margens, Tamanho)
                // A última SectionProperties define o layout do documento todo.
                SectionProperties templateProps = body.Elements<SectionProperties>().LastOrDefault();
                SectionProperties savedProps = null;

                if (templateProps != null)
                {
                    savedProps = (SectionProperties)templateProps.CloneNode(true);
                    Console.WriteLine("[INFO] Formato do Template capturado.");
                }
                else
                {
                    Console.WriteLine("[AVISO] Template sem definicoes de secao explicitas. Usando padrao do Word.");
                }

                // 3. Evisceração: Limpa todo o conteúdo do template
                body.RemoveAllChildren();

                // 4. Transplante: Insere a Capa como AltChunk
                string altChunkId = "CapaChunk";
                AlternativeFormatImportPart chunk = mainPart.AddAlternativeFormatImportPart(
                    AlternativeFormatImportPartType.WordprocessingML, altChunkId);

                using (FileStream fs = File.Open(capaPath, FileMode.Open, FileAccess.Read))
                {
                    chunk.FeedData(fs);
                }

                AltChunk altChunk = new AltChunk { Id = altChunkId };
                body.AppendChild(altChunk);
                Console.WriteLine("[INFO] Conteudo da Capa inserido.");

                // 5. Imposição de Regras: Força o layout do Template no final
                if (savedProps != null)
                {
                    // Adiciona as propriedades do template DEPOIS da capa.
                    // Isso diz ao Word: "A seção que acabou de passar (a capa) deve ter ESTAS margens."
                    body.AppendChild(savedProps);
                    Console.WriteLine("[INFO] Formato do Template forçado sobre a Capa.");
                }

                mainPart.Document.Save();
            }

            Console.WriteLine("[SUCESSO] Nova capa gerada em: " + outputPath);
        }
    }
}
