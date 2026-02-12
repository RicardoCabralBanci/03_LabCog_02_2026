Attribute VB_Name = "mod_NewEngine"
Option Explicit

' ==========================================================================================
' MÓDULO: mod_NewEngine
' DESCRIÇÃO: Ponte entre o Excel e o Motor de Geração C# (.NET 10)
' AUTOR: Mestre em VBA (via Gemini CLI)
' DATA: 23/12/2025
' ==========================================================================================

' CONFIGURAÇÕES GERAIS - VERIFIQUE ESTAS COLUNAS NO SEU EXCEL!
Private Const TARGET_SHEET_NAME As String = "Dados Salvos"   ' Nome da aba que contém a lista de arquivos
Private Const COL_PATH As String = "G"                       ' Coluna com o caminho do arquivo (Ajustar conforme real)
Private Const COL_ACTIVE As String = "B"                     ' Coluna com o flag de ativação (Yes/No/X/TRUE)
Private Const START_ROW As Integer = 5                       ' Linha onde começam os dados

' CAMINHOS RELATIVOS (Baseados na pasta do Excel)
Private Const EXE_REL_PATH As String = "\NewGerador\Engine\NewGerador.exe"
Private Const CSV_FILENAME As String = "input_manifest.csv"

Sub ExportarParaNovoGerador()
    Dim ws As Worksheet
    Dim lastRow As Long, i As Long
    Dim csvContent As String
    Dim fPath As String, fActive As String
    Dim csvPath As String, exePath As String
    Dim totalFiles As Integer
    
    On Error GoTo ErrorHandler
    
    ' 1. Localizar a Aba Mestra
    Set ws = GetWorksheet(TARGET_SHEET_NAME)
    If ws Is Nothing Then
        MsgBox "ERRO CRÍTICO: Aba '" & TARGET_SHEET_NAME & "' não encontrada." & vbCrLf & _
               "Verifique se o nome da aba está correto no código VBA.", vbCritical
        Exit Sub
    End If
    
    ' 2. Definir Caminhos
    csvPath = ThisWorkbook.Path & "\" & CSV_FILENAME
    exePath = ThisWorkbook.Path & EXE_REL_PATH
    
    ' Validação de Existência do Motor
    If Dir(exePath) = "" Then
        ' Tenta caminho alternativo (desenvolvimento)
        exePath = ThisWorkbook.Path & "\bin\Debug\net10.0\NewGerador.exe"
        If Dir(exePath) = "" Then
            MsgBox "O executável do gerador não foi encontrado em:" & vbCrLf & _
                   ThisWorkbook.Path & EXE_REL_PATH, vbCritical, "Motor Ausente"
            Exit Sub
        End If
    End If
    
    ' 3. Construir o Manifesto (CSV)
    csvContent = "CATEGORY;KEY;VALUE" & vbCrLf ' Header obrigatório
    csvContent = csvContent & "META;EXPORT_DATE;" & Format(Now, "yyyy-mm-dd hh:mm:ss") & vbCrLf
    csvContent = csvContent & "META;USER;" & Application.UserName & vbCrLf
    
    lastRow = ws.Cells(ws.Rows.Count, COL_PATH).End(xlUp).Row
    totalFiles = 0
    
    ' Loop de Leitura
    For i = START_ROW To lastRow
        fPath = Trim(ws.Range(COL_PATH & i).Value)
        fActive = UCase(Trim(ws.Range(COL_ACTIVE & i).Value))
        
        ' DEBUG: Se for a primeira linha e estiver vazio, avisa o usuário
        If i = START_ROW And fPath = "" And fActive = "" Then
             If MsgBox("AVISO DE DIAGNÓSTICO:" & vbCrLf & vbCrLf & _
                       "Na linha " & START_ROW & ":" & vbCrLf & _
                       "- Coluna " & COL_ACTIVE & " (Ativo) está vazia." & vbCrLf & _
                       "- Coluna " & COL_PATH & " (Caminho) está vazia." & vbCrLf & vbCrLf & _
                       "As colunas configuradas no VBA estão corretas?" & vbCrLf & _
                       "Deseja continuar mesmo assim?", vbYesNo + vbExclamation) = vbNo Then Exit Sub
        End If
        
        ' Lógica de Seleção: Aceita "YES", "TRUE", "SIM", "X", "1"
        If (fActive = "YES" Or fActive = "TRUE" Or fActive = "SIM" Or fActive = "X" Or fActive = "1") And fPath <> "" Then
            ' Sanitização básica de aspas para CSV
            fPath = Replace(fPath, ";", "_") 
            
            ' Adiciona linha ao manifesto: FILE;SELECTED;Caminho
            csvContent = csvContent & "FILE;SELECTED;" & fPath & vbCrLf
            totalFiles = totalFiles + 1
        End If
    Next i
    
    If totalFiles = 0 Then
        MsgBox "Nenhum arquivo encontrado para geração." & vbCrLf & vbCrLf & _
               "Verifique:" & vbCrLf & _
               "1. Se há 'X' ou 'Yes' na coluna " & COL_ACTIVE & "." & vbCrLf & _
               "2. Se os caminhos estão na coluna " & COL_PATH & "." & vbCrLf & _
               "3. Se a aba correta é '" & ws.Name & "'.", vbExclamation
        Exit Sub
    End If
    
    ' 4. Salvar CSV em UTF-8 (Sem BOM ou com BOM, C# entende ambos, mas ADODB é seguro)
    Call SaveTextToFile(csvContent, csvPath)
    
    ' 5. Disparar o Motor C#
    ' Shell executa de forma assíncrona. O usuário verá a janela do console.
    ' vbNormalFocus garante que a janela apareça.
    Dim pid As Double
    Dim cmd As String
    
    ' Aspas duplas para lidar com espaços nos caminhos
    cmd = """" & exePath & """ """ & csvPath & """"
    
    ' Executa
    pid = Shell(cmd, vbNormalFocus)
    
    If pid <> 0 Then
        ' Sucesso no disparo (não garante sucesso na execução)
        Application.StatusBar = "Gerador iniciado (PID: " & pid & ")... Verifique a janela do console."
    Else
        MsgBox "Falha ao iniciar o processo do gerador.", vbCritical
    End If

    Exit Sub

ErrorHandler:
    MsgBox "Erro no VBA: " & Err.Description, vbCritical
End Sub

'Função Auxiliar para obter Planilha por nome (seguro)
Private Function GetWorksheet(sheetName As String) As Worksheet
    On Error Resume Next
    Set GetWorksheet = ThisWorkbook.Sheets(sheetName)
    ' Se falhar pelo nome exato, tenta achar "Base de Dados" como fallback
    If GetWorksheet Is Nothing Then
        Set GetWorksheet = ThisWorkbook.Sheets("Base de Dados")
    End If
    On Error GoTo 0
End Function

'Função para Salvar UTF-8 sem BOM
Private Sub SaveTextToFile(content As String, filePath As String)
    Dim stream As Object
    Set stream = CreateObject("ADODB.Stream")
    
    With stream
        .Type = 2 ' adTypeText
        .Charset = "utf-8"
        .Open
        .WriteText content
        .SaveToFile filePath, 2 ' adSaveCreateOverWrite
        .Close
    End With
    Set stream = Nothing
End Sub