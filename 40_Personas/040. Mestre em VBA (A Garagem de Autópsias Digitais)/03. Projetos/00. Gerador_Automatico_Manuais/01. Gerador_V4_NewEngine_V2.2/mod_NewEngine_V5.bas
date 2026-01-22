Attribute VB_Name = "mod_NewEngine"
Option Explicit

' ==========================================================================================
' MÓDULO: mod_NewEngine (V5 - HYBRID ARCHITECTURE)
' DESCRIÇÃO: Motor Híbrido com suporte a MachineType e RowIndex
' ATUALIZAÇÃO: 13/01/2026 - Adicionado suporte a PLT/PCK e Indexação Espacial
' AUTOR: Mestre em VBA
' ==========================================================================================

Private Const TARGET_SHEET_NAME As String = "Base de Dados"
Private Const COL_PATH As String = "C"
Private Const COL_ACTIVE As String = "B"
Private Const START_ROW As Integer = 5

' Ponto Único de Entrada
' MachineType: "CCMX", "PLT", "PCK", etc.
Sub ExportarParaNovoGerador(Optional MachineType As String = "CCMX")
    Dim ws As Worksheet
    Dim lastRow As Long, i As Long
    Dim csvContent As String
    Dim fPath As String, fActive As String
    Dim csvPath As String, exePath As String
    Dim totalFiles As Integer
    Dim fso As Object
    
    On Error GoTo ErrorHandler
    Set fso = CreateObject("Scripting.FileSystemObject")
    
    ' 1. Localizar Aba
    Set ws = LocateDatabaseSheet()
    If ws Is Nothing Then Exit Sub
    
    ' 2. Localizar Engine
    If Not LocateEngine(fso, exePath, csvPath) Then Exit Sub
    
    ' 3. Construir Manifesto (V5 Standard)
    ' HEADER: CATEGORY;KEY;VALUE
    csvContent = "CATEGORY;KEY;VALUE" & vbCrLf
    csvContent = csvContent & "META;EXPORT_DATE;" & Format(Now, "yyyy-mm-dd hh:mm:ss") & vbCrLf
    csvContent = csvContent & "META;MACHINE_TYPE;" & MachineType & vbCrLf
    
    lastRow = ws.Cells(ws.Rows.Count, COL_PATH).End(xlUp).Row
    If lastRow < START_ROW Then lastRow = START_ROW
    
    totalFiles = 0
    
    ' Varredura com Indexação Espacial
    For i = START_ROW To lastRow
        fPath = Trim(ws.Range(COL_PATH & i).Value)
        fActive = UCase(Trim(ws.Range(COL_ACTIVE & i).Value))
        
        ' Verifica Ativação (Compatibilidade com X, YES, TRUE, 1)
        If IsActive(fActive) And fPath <> "" Then
            ' V5 CRITICAL CHANGE: 
            ' Passamos o ÍNDICE DA LINHA (i) como Key.
            ' O C# usará este índice para mapear onde o arquivo se encaixa na estrutura do Word
            ' baseando-se nas "Zonas" (ex: Linhas 50-100 = Seção Hidráulica do PLT).
            csvContent = csvContent & "FILE;" & i & ";" & Replace(fPath, ";", "_") & vbCrLf
            totalFiles = totalFiles + 1
        End If
    Next i
    
    If totalFiles = 0 Then
        MsgBox "Nenhum arquivo selecionado para a máquina: " & MachineType & vbCrLf & _
               "Verifique se marcou os 'X' na aba correta e se a Base de Dados foi atualizada.", vbExclamation
        Exit Sub
    End If
    
    ' 4. Disparar
    Call SaveTextToFile(csvContent, csvPath)
    Call LaunchEngine(exePath, csvPath, totalFiles, MachineType)

    Exit Sub
ErrorHandler:
    MsgBox "Erro Fatal no Modulo V5: " & Err.Description, vbCritical
End Sub

' --- HELPER FUNCTIONS ---

Private Function LocateDatabaseSheet() As Worksheet
    On Error Resume Next
    Set LocateDatabaseSheet = ThisWorkbook.Sheets(TARGET_SHEET_NAME)
    If LocateDatabaseSheet Is Nothing Then
        Set LocateDatabaseSheet = ThisWorkbook.Sheets("Dados Salvos")
        If Not LocateDatabaseSheet Is Nothing Then
            ' Silencioso, apenas usa o fallback
        Else
            MsgBox "CRÍTICO: Aba '" & TARGET_SHEET_NAME & "' não encontrada.", vbCritical
        End If
    End If
End Function

Private Function LocateEngine(fso As Object, ByRef exePath As String, ByRef csvPath As String) As Boolean
    Dim baseDir As String: baseDir = ThisWorkbook.Path
    
    ' Prioridade: Subpasta NewGerador (Mais organizado)
    If fso.FileExists(baseDir & "\NewGerador\NewGerador.exe") Then
        exePath = baseDir & "\NewGerador\NewGerador.exe"
        csvPath = baseDir & "\NewGerador\input_manifest.csv"
        LocateEngine = True
        Exit Function
    End If
    
    ' Fallback: Mesma pasta
    If fso.FileExists(baseDir & "\NewGerador.exe") Then
        exePath = baseDir & "\NewGerador.exe"
        csvPath = baseDir & "\input_manifest.csv"
        LocateEngine = True
        Exit Function
    End If
    
    MsgBox "ERRO: Engine 'NewGerador.exe' não encontrada em:" & vbCrLf & baseDir & vbCrLf & "ou subpasta \NewGerador", vbCritical
    LocateEngine = False
End Function

Private Function IsActive(val As String) As Boolean
    IsActive = (val = "YES" Or val = "TRUE" Or val = "SIM" Or val = "X" Or val = "1")
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

Private Sub LaunchEngine(exePath As String, csvPath As String, count As Integer, mType As String)
    Dim cmd As String
    ' Aspas duplas para caminhos com espaço
    cmd = """" & exePath & """ """ & csvPath & """"
    
    If Shell(cmd, vbNormalFocus) <> 0 Then
        Application.StatusBar = "Gerando Manual (" & mType & ") - Processando " & count & " arquivos..."
    End If
End Sub
