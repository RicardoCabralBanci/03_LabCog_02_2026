using System;
using System.IO;
using System.Reflection;
using System.Runtime.InteropServices;

namespace PDFTools
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== Mestre em VBA: C# PDF Converter (Late Binding) ===");

            string pdfPath = @"Z:\B\BA_89408986_000300__Innopack Packer_EN.pdf";
            string docxPath = @"Z:\B\BA_89408986_000300__Innopack Packer_EN_CSHARP.docx";

            if (!File.Exists(pdfPath))
            {
                Console.WriteLine("ERRO: Arquivo PDF não encontrado: " + pdfPath);
                return;
            }

            object wordApp = null;
            object doc = null;
            
            try
            {
                Console.WriteLine("Procurando Word.Application no registro...");
                Type wordType = Type.GetTypeFromProgID("Word.Application");
                
                if (wordType == null)
                {
                    Console.WriteLine("ERRO: Word.Application não encontrado no registro.");
                    return;
                }

                Console.WriteLine("Instanciando Word...");
                wordApp = Activator.CreateInstance(wordType);
                
                // wordApp.Visible = true
                wordType.InvokeMember("Visible", BindingFlags.SetProperty, null, wordApp, new object[] { true });

                Console.WriteLine("Word Aberto. Carregando PDF (Aguarde)...");
                
                // Documents.Open(...)
                object documents = wordApp.GetType().InvokeMember("Documents", BindingFlags.GetProperty, null, wordApp, null);
                
                doc = documents.GetType().InvokeMember("Open", BindingFlags.InvokeMethod, null, documents, new object[] 
                { 
                    pdfPath, // FileName
                    false,   // ConfirmConversions
                    true,    // ReadOnly
                    false    // AddToRecentFiles
                    // Outros argumentos opcionais omitidos
                });

                Console.WriteLine("PDF Carregado. Salvando como DOCX...");

                // doc.SaveAs2(FileName, FileFormat=16)
                doc.GetType().InvokeMember("SaveAs2", BindingFlags.InvokeMethod, null, doc, new object[] 
                { 
                    docxPath, 
                    16 // wdFormatDocumentDefault
                });

                Console.WriteLine("SUCESSO! Salvo em: " + docxPath);

            }
            catch (Exception ex)
            {
                Console.WriteLine("ERRO FATAL: " + ex.Message);
                Console.WriteLine(ex.StackTrace);
            }
            finally
            {
                if (doc != null)
                {
                    try 
                    {
                        // doc.Close(false)
                        doc.GetType().InvokeMember("Close", BindingFlags.InvokeMethod, null, doc, new object[] { false });
                        Marshal.ReleaseComObject(doc);
                    } catch {}
                }
                
                if (wordApp != null)
                {
                    try 
                    {
                        Console.WriteLine("Fechando Word...");
                        // wordApp.Quit(false)
                        wordApp.GetType().InvokeMember("Quit", BindingFlags.InvokeMethod, null, wordApp, new object[] { false });
                        Marshal.ReleaseComObject(wordApp);
                    } catch {}
                }
            }
            
            Console.WriteLine("Pressione ENTER para sair...");
            Console.ReadLine();
        }
    }
}