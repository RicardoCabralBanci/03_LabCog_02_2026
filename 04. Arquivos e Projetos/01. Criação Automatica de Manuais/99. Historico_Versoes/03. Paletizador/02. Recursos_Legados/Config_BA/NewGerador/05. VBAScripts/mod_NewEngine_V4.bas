Attribute VB_Name = "mod_NewEngine"
Option Explicit

' ==========================================================================================
' MÓDULO: mod_NewEngine (V4 - BASEADO NO SCRIPT EXPORTAÇÃO)
' DESCRIÇÃO: Ponte inteligente entre Excel e Motor C#
' COLUNAS: Baseadas no arquivo Script_Exportacao_VBA.md (Ativo=B, Path=C)
' ABA: Base de Dados
' AUTOR: Mestre em VBA (via Gemini CLI)
' DATA: 23/12/2025
' ==========================================================================================

' CONFIGURAÇÕES DE COLUNA (Baseado na análise forense)
Private Const TARGET_SHEET_NAME As String = "Base de Dados" ' Mudança crítica: Base de Dados
Private Const COL_PATH As String = "C"                      ' Mudança crítica: Coluna C
Private Const COL_ACTIVE As String = "B"                    ' Mantido: Coluna B
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
    ' Tenta "Base de Dados", se falhar tenta "Dados Salvos"
    On Error Resume Next
    Set ws = ThisWorkbook.Sheets(TARGET_SHEET_NAME)
    If ws Is Nothing Then
        Set ws = ThisWorkbook.Sheets("Dados Salvos")
        If Not ws Is Nothing Then
            MsgBox "Aviso: Aba 'Base de Dados' não encontrada. Usando 'Dados Salvos'.", vbInformation
        End If
    End If
    On Error GoTo ErrorHandler
    
    If ws Is Nothing Then
        MsgBox "ERRO CRÍTICO: Nenhuma aba de dados encontrada (Base de Dados/Dados Salvos).", vbCritical
        Exit Sub
    End If
    
    ' ATIVA A ABA PARA O USUÁRIO VER
    ws.Activate
    
    ' 2. LÓGICA DE LOCALIZAÇÃO INTELIGENTE DO MOTOR
    Dim baseDir As String: baseDir = ThisWorkbook.Path
    
    If fso.FileExists(baseDir & "\NewGerador.exe") Then
        exePath = baseDir & "\NewGerador.exe"
        csvPath = baseDir & "\input_manifest.csv"
    ElseIf fso.FileExists(baseDir & "\NewGerador\NewGerador.exe") Then
        exePath = baseDir & "\NewGerador\NewGerador.exe"
        csvPath = baseDir & "\NewGerador\input_manifest.csv"
    Else
        MsgBox "ERRO: 'NewGerador.exe' não encontrado.", vbCritical
        Exit Sub
    End If
    
    ' 3. Construir Manifesto
    csvContent = "CATEGORY;KEY;VALUE" & vbCrLf
    csvContent = csvContent & "META;EXPORT_DATE;" & Format(Now, "yyyy-mm-dd hh:mm:ss") & vbCrLf
    
    lastRow = ws.Cells(ws.Rows.Count, COL_PATH).End(xlUp).Row
    
    ' Proteção contra planilha vazia
    If lastRow < START_ROW Then lastRow = START_ROW
    
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
        MsgBox "Nenhum arquivo selecionado na aba '" & ws.Name & "'." & vbCrLf & _
               "Verifique as colunas B (Ativo) e C (Caminho).", vbExclamation
        Exit Sub
    End If
    
    ' 4. Salvar e Executar
    Call SaveTextToFile(csvContent, csvPath)
    
    Dim cmd As String
    cmd = """" & exePath & """ """ & csvPath & """"
    If Shell(cmd, vbNormalFocus) <> 0 Then
        Application.StatusBar = "Gerador V4 iniciado com " & totalFiles & " arquivos..."
    End If

    Exit Sub
ErrorHandler:
    MsgBox "Erro: " & Err.Description, vbCritical
End Sub

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
