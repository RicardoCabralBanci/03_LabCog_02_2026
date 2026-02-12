# Proposta de Atualização: mod_NewEngine_V7 (Separação de Tipo e Modelo)

**Data:** 26/01/2026
**Autor:** Mestre em VBA
**Status:** Solução Arquitetural
**Objetivo:** Separar a lógica de filtragem de arquivos (que usa códigos como "BTR") da lógica de exibição na capa (que usa nomes como "Innopal...").

```vba
Option Explicit

' ... (Declarações Iniciais permanecem iguais) ...

Private Sub ExportarParaNovoGerador(machineType As String)
    ' ... (Variáveis iniciais) ...
    
    ' Variáveis para Captura de Dados da Capa
    Dim valSapNr As String
    Dim valProjeto As String
    Dim valRevisao As String
    Dim valAno As String
    Dim valMaquinaFull As String ' Nova variável para o nome completo
    
    ' ... (Validações de ambiente permanecem iguais) ...
    
    ' 3. Construção do Manifesto
    csvContent = "CATEGORY;KEY;VALUE" & vbCrLf
    csvContent = csvContent & "META;EXPORT_DATE;" & Format(Now, "yyyy-mm-dd hh:mm:ss") & vbCrLf
    
    ' [IMPORTANTE] Mantém MACHINE_TYPE puro ("BTR", "PLT") para o C# filtrar os arquivos corretamente
    csvContent = csvContent & "META;MACHINE_TYPE;" & machineType & vbCrLf
    
    ' --- [INÍCIO] INJEÇÃO DE DADOS DA CAPA ---
    On Error Resume Next
    
    ' Valores padrão
    valSapNr = "N/A"
    valProjeto = "N/A"
    valRevisao = "0"
    valAno = Year(Now)
    valMaquinaFull = machineType ' Default se não achar no form
    
    ' Extração do Form Info
    If Not Info Is Nothing Then
        valSapNr = Info.SapNr.Value
        valProjeto = Info.Projeto.Value
        valRevisao = Info.Revisao.Value
        valAno = Info.Ano.Value
        ' Captura o nome comercial completo para a capa
        valMaquinaFull = Info.Maquina.Value 
    End If
    
    ' [NOVO] Envia o nome completo em uma chave separada para o C# usar na capa
    csvContent = csvContent & "META;MACHINE_NAME_FULL;" & valMaquinaFull & vbCrLf
    
    csvContent = csvContent & "META;SAP_NUMBER;" & valSapNr & vbCrLf
    csvContent = csvContent & "META;ORDER_NUMBER;" & valProjeto & vbCrLf
    csvContent = csvContent & "META;REVISION;" & valRevisao & vbCrLf
    csvContent = csvContent & "META;YEAR;" & valAno & vbCrLf
    
    On Error GoTo ErrorHandler
    ' --- [FIM] INJEÇÃO DE DADOS DA CAPA ---
    
    ' ... (Resto do código de varredura de arquivos permanece igual) ...
    
End Sub

' ... (Função SaveTextToFile permanece igual) ...
```
