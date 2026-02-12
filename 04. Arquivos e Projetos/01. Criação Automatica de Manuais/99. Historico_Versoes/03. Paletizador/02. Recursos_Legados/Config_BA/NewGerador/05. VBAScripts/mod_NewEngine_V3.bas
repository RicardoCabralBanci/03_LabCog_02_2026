Attribute VB_Name = "mod_NewEngine"
Option Explicit

' ==========================================================================================
' MÓDULO: mod_NewEngine (V3 - UNIVERSAL)
' DESCRIÇÃO: Ponte inteligente entre Excel e Motor C#
' DIFERENCIAL: Localização dinâmica do Motor (mesma pasta ou subpasta NewGerador)
' AUTOR: Mestre em VBA (via Gemini CLI)
' DATA: 23/12/2025
' ==========================================================================================

' CONFIGURAÇÕES DE COLUNA (Ajuste se necessário)
Private Const TARGET_SHEET_NAME As String = "Dados Salvos"
Private Const COL_PATH As String = "G"
Private Const COL_ACTIVE As String = "B"
Private Const START_ROW As Integer = 5

Sub ExportarParaNovoGerador()
    Dim ws As Worksheet
    Dim lastRow As Long, i As Long
    Dim csvContent As String
    Dim fPath As String, fActive As String
    Dim csvPath As String, exePath As String
    Dim totalFiles As Integer
    Dim fso As Object
    
    On Error GoTo ErrorHandler
    Set fso = CreateObject("Scripting.FileSystemObject")
    
    ' 1. Localizar a Aba
    Set ws = GetWorksheet(TARGET_SHEET_NAME)
    If ws Is Nothing Then
        MsgBox "ERRO: Aba '" & TARGET_SHEET_NAME & "' não encontrada.", vbCritical
        Exit Sub
    End If
    
    ' 2. LÓGICA DE LOCALIZAÇÃO INTELIGENTE DO MOTOR
    ' Tenta encontrar o EXE em 3 lugares possíveis:
    Dim baseDir As String: baseDir = ThisWorkbook.Path
    
    If fso.FileExists(baseDir & "\NewGerador.exe") Then
        ' Caso A: Excel e EXE na mesma pasta
        exePath = baseDir & "\NewGerador.exe"
        csvPath = baseDir & "\input_manifest.csv"
    ElseIf fso.FileExists(baseDir & "\NewGerador\NewGerador.exe") Then
        ' Caso B: Excel fora, EXE dentro da pasta NewGerador
        exePath = baseDir & "\NewGerador\NewGerador.exe"
        csvPath = baseDir & "\NewGerador\input_manifest.csv"
    Else
        ' Caso C: Não encontrado
        MsgBox "ERRO: 'NewGerador.exe' não encontrado na pasta do Excel ou na subpasta \NewGerador." & vbCrLf & _
               "Caminho verificado: " & baseDir, vbCritical
        Exit Sub
    End If
    
    ' 3. Construir Manifesto
    csvContent = "CATEGORY;KEY;VALUE" & vbCrLf
    csvContent = csvContent & "META;EXPORT_DATE;" & Format(Now, "yyyy-mm-dd hh:mm:ss") & vbCrLf
    
    lastRow = ws.Cells(ws.Rows.Count, COL_PATH).End(xlUp).Row
    totalFiles = 0
    
    For i = START_ROW To lastRow
        fPath = Trim(ws.Range(COL_PATH & i).Value)
        fActive = UCase(Trim(ws.Range(COL_ACTIVE & i).Value))
        
        If (fActive = "YES" Or fActive = "TRUE" Or fActive = "SIM" Or fActive = "X" Or fActive = "1") And fPath <> "" Then
            csvContent = csvContent & "FILE;SELECTED;" & Replace(fPath, ";", "_") & vbCrLf
            totalFiles = totalFiles + 1
        End If
    Next i
    
    If totalFiles = 0 Then
        MsgBox "Nenhum arquivo selecionado.", vbExclamation
        Exit Sub
    End If
    
    ' 4. Salvar e Executar
    Call SaveTextToFile(csvContent, csvPath)
    
    Dim cmd As String
    cmd = """" & exePath & """ """ & csvPath & """"
    If Shell(cmd, vbNormalFocus) <> 0 Then
        Application.StatusBar = "Gerador V3 iniciado..."
    End If

    Exit Sub
ErrorHandler:
    MsgBox "Erro: " & Err.Description, vbCritical
End Sub

Private Function GetWorksheet(sheetName As String) As Worksheet
    On Error Resume Next
    Set GetWorksheet = ThisWorkbook.Sheets(sheetName)
    If GetWorksheet Is Nothing Then Set GetWorksheet = ThisWorkbook.Sheets("Base de Dados")
End Function

Private Sub SaveTextToFile(content As String, filePath As String)
    Dim stream As Object
    Set stream = CreateObject("ADODB.Stream")
    With stream
        .Type = 2: .Charset = "utf-8": .Open
        .WriteText content
        .SaveToFile filePath, 2
        .Close
    End With
End Sub
