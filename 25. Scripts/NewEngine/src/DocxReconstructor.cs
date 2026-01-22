using System;
using System.Collections.Generic;
using System.IO;
using System.IO.Compression;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using System.Xml;
using System.Xml.Linq;

namespace DocxReconstructor
{
    // --- Estruturas de Dados para Numeração ---

    public class AbstractNum
    {
        public string AbstractNumId { get; set; }
        // Key: ilvl (0-8), Value: LevelDefinition
        public Dictionary<int, LevelDef> Levels { get; set; }

        public AbstractNum()
        {
            Levels = new Dictionary<int, LevelDef>();
        }
    }

    public class LevelDef
    {
        public string NumFmt { get; set; } // decimal, lowerLetter, bullet...
        public string LvlText { get; set; } // %1.%2
        public int StartVal { get; set; }
    }

    public class NumInstance
    {
        public string NumId { get; set; }
        public string AbstractNumId { get; set; }
    }

    public class CounterState
    {
        public int[] Counters { get; set; }

        public CounterState()
        {
            Counters = new int[9]; // Níveis 0 a 8
            for (int i = 0; i < 9; i++) Counters[i] = 1; // Default start
        }
    }

    class Program
    {
        static void Main(string[] args)
        {
            if (args.Length == 0)
            {
                Console.WriteLine("Usage: DocxReconstructor.exe <docx_path>");
                return;
            }

            string filePath = args[0];
            if (!File.Exists(filePath))
            {
                Console.WriteLine("File not found: " + filePath);
                return;
            }

            try
            {
                ProcessDocx(filePath);
            }
            catch (Exception ex)
            {
                Console.WriteLine("Error: " + ex.Message);
                Console.WriteLine(ex.StackTrace);
            }
        }

        static void ProcessDocx(string filePath)
        {
            // Dicionários de lookup
            Dictionary<string, AbstractNum> abstractNums = new Dictionary<string, AbstractNum>();
            Dictionary<string, NumInstance> numInstances = new Dictionary<string, NumInstance>();
            // Mapa para rastrear contadores ativos por NumId (cada lista tem seu estado)
            Dictionary<string, CounterState> activeCounters = new Dictionary<string, CounterState>();

            using (FileStream fs = new FileStream(filePath, FileMode.Open, FileAccess.Read, FileShare.ReadWrite))
            using (ZipArchive archive = new ZipArchive(fs, ZipArchiveMode.Read))
            {
                XNamespace w = "http://schemas.openxmlformats.org/wordprocessingml/2006/main";

                // 1. Ler Numbering.xml (se existir)
                var numberingEntry = archive.GetEntry("word/numbering.xml");
                if (numberingEntry != null)
                {
                    using (Stream s = numberingEntry.Open())
                    {
                        XDocument xdoc = XDocument.Load(s);
                        
                        // Carregar Definições Abstratas
                        foreach (var abs in xdoc.Descendants(w + "abstractNum"))
                        {
                            var absId = abs.Attribute(w + "abstractNumId").Value;
                            var def = new AbstractNum { AbstractNumId = absId };

                            foreach (var lvl in abs.Descendants(w + "lvl"))
                            {
                                int ilvl = int.Parse(lvl.Attribute(w + "ilvl").Value);
                                var lvlDef = new LevelDef();
                                
                                var numFmt = lvl.Element(w + "numFmt");
                                lvlDef.NumFmt = numFmt != null ? numFmt.Attribute(w + "val").Value : "decimal";

                                var lvlText = lvl.Element(w + "lvlText");
                                lvlDef.LvlText = lvlText != null ? lvlText.Attribute(w + "val").Value : "";

                                var start = lvl.Element(w + "start");
                                lvlDef.StartVal = start != null ? int.Parse(start.Attribute(w + "val").Value) : 1;

                                def.Levels[ilvl] = lvlDef;
                            }
                            abstractNums[absId] = def;
                        }

                        // Carregar Instâncias Concretas
                        foreach (var num in xdoc.Descendants(w + "num"))
                        {
                            var numId = num.Attribute(w + "numId").Value;
                            var absRef = num.Element(w + "abstractNumId");
                            if (absRef != null)
                            {
                                numInstances[numId] = new NumInstance
                                {
                                    NumId = numId,
                                    AbstractNumId = absRef.Attribute(w + "val").Value
                                };
                                // Inicializar contadores para essa lista
                                activeCounters[numId] = new CounterState();
                            }
                        }
                    }
                }

                // 2. Ler Document.xml
                var docEntry = archive.GetEntry("word/document.xml");
                if (docEntry == null) return;

                using (Stream s = docEntry.Open())
                {
                    XDocument doc = XDocument.Load(s);

                    foreach (var p in doc.Descendants(w + "p"))
                    {
                        // --- Extração de Dados do Parágrafo ---
                        string text = p.Value; // XElement.Value pega todo o texto concatenado
                        if (string.IsNullOrWhiteSpace(text)) continue;

                        string generatedNumber = "";
                        string numId = null;
                        int ilvl = 0;
                        bool hasNumbering = false;
                        int outlineLvl = 9;

                        var pPr = p.Element(w + "pPr");
                        if (pPr != null)
                        {
                            // Checar Outline Level (Nivel de Topico Real)
                            var outline = pPr.Element(w + "outlineLvl");
                            if (outline != null)
                            {
                                outlineLvl = int.Parse(outline.Attribute(w + "val").Value);
                            }
                            else
                            {
                                // Checar Estilo para fallback (Heading X)
                                var pStyle = pPr.Element(w + "pStyle");
                                if (pStyle != null)
                                {
                                    string styleVal = pStyle.Attribute(w + "val").Value;
                                    if (styleVal.StartsWith("Heading") || styleVal.StartsWith("Ttulo"))
                                    {
                                        // Extração simples de digito
                                        var match = Regex.Match(styleVal, @"\d+");
                                        if (match.Success) outlineLvl = int.Parse(match.Value) - 1;
                                    }
                                }
                            }

                            // Checar Numeração
                            var numPr = pPr.Element(w + "numPr");
                            if (numPr != null)
                            {
                                var xNumId = numPr.Element(w + "numId");
                                var xIlvl = numPr.Element(w + "ilvl");

                                if (xNumId != null)
                                {
                                    numId = xNumId.Attribute(w + "val").Value;
                                    if (xIlvl != null) ilvl = int.Parse(xIlvl.Attribute(w + "val").Value);
                                    
                                    // Tentar gerar o numero
                                    if (numInstances.ContainsKey(numId))
                                    {
                                        hasNumbering = true;
                                        generatedNumber = GenerateNumberString(numId, ilvl, numInstances, abstractNums, activeCounters);
                                    }
                                }
                            }
                        }

                        // --- Lógica de Decisão ---
                        // Se tem numeração, o nível hierárquico muitas vezes é o proprio ilvl
                        int finalLevel = outlineLvl;
                        
                        // Se for texto normal (9), mas tem numeração hierarquica, promovemos
                        if (finalLevel == 9 && hasNumbering)
                        {
                            // Assumimos que ilvl 0 = Heading 1 (aprox) se for numerado
                            // Mas cuidado com bullets.
                            if (!generatedNumber.Contains("•") && !generatedNumber.Contains("●"))
                            {
                                finalLevel = ilvl; 
                            }
                        }

                        string prefix = "";
                        if (hasNumbering) prefix = generatedNumber + " ";

                        // Output Formatado: [Level] Texto Completo
                        Console.WriteLine(string.Format("[{0}] {1}{2}", finalLevel, prefix, text));
                    }
                }
            }
        }

        static string GenerateNumberString(string numId, int ilvl, 
            Dictionary<string, NumInstance> instances, 
            Dictionary<string, AbstractNum> abstracts,
            Dictionary<string, CounterState> counters)
        {
            if (!counters.ContainsKey(numId)) return "";
            if (!instances.ContainsKey(numId)) return "";

            var instance = instances[numId];
            if (!abstracts.ContainsKey(instance.AbstractNumId)) return "";
            var abs = abstracts[instance.AbstractNumId];

            if (!abs.Levels.ContainsKey(ilvl)) return "";
            var lvlDef = abs.Levels[ilvl];

            var state = counters[numId];

            // 1. Incrementar contador atual
            // Se esta é a primeira vez que tocamos neste contador, deve ser StartVal.
            // Simplificação: apenas incrementamos. Lógica real de StartVal é complexa.
            // Para "reconstrução visual", assumimos fluxo sequencial.
            
            // Lógica de Reset: Se estamos no nivel 1, resetamos contadores 2, 3, 4...
            for (int i = ilvl + 1; i < 9; i++) state.Counters[i] = 1; // Ou StartVal do nivel i

            int currentVal = state.Counters[ilvl];
            
            // Preparar incremento para o PRÓXIMO item deste nível
            state.Counters[ilvl]++; 

            // 2. Formatar String (ex: %1.%2)
            if (lvlDef.NumFmt == "bullet") return "•"; // Simplificação para bullets
            
            string result = lvlDef.LvlText;
            
            // Substituir %1, %2, etc. pelos valores dos contadores
            // Regex para encontrar %1, %2...
            // Cuidado: %1 pega o contador do nivel 0. %2 pega o do nivel 1.
            
            // Precisamos dos valores ATUAIS dos níveis superiores (que não foram resetados)
            // Mas o contador do nível atual JÁ foi incrementado para o próximo?
            // Correção: O valor a exibir é o currentVal. O state armazena o PRÓXIMO.
            // Para os níveis superiores, o state armazena o PRÓXIMO, então temos que subtrair 1 para saber o atual?
            // Não, níveis superiores só incrementam quando ELES aparecem. Então o valor "state" deles é o valor "corrente" da sessão pai.
            // Vamos usar state.Counters[i] - 1? Não, melhor:
            // Counters[i] guarda o PRÓXIMO valor a ser usado.
            // Então o valor "atual" do pai é (Counters[i] - 1). Se for 0, é pq ainda não começou?
            // Vamos simplificar: 
            // Valor a usar no nível K = (se K == ilvl) ? currentVal : (state.Counters[K] - 1);
            // E garantir minimo de 1.

            for (int k = 0; k <= ilvl; k++)
            {
                int valToUse;
                if (k == ilvl) valToUse = currentVal;
                else valToUse = Math.Max(1, state.Counters[k] - 1); // Valor "ativo" do pai

                string placeholder = "%" + (k + 1); // %1, %2
                if (result.Contains(placeholder))
                {
                    result = result.Replace(placeholder, valToUse.ToString());
                }
            }

            return result;
        }
    }
}
