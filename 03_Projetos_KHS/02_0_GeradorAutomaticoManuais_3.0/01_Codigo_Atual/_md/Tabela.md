# Tabela

> Codigo VBA atual -- convertido automaticamente de `Tabela.bas`

```vba
Attribute VB_Name = "Tabela"
Option Explicit

Private Const FILE_ROW = 1
Private Const HEADER_ROW = 3
Private Const START_ROW = 4
Private Const ALT_COL = 4
Private Const PATH_COL = 5

Sub PopulateXL(Optional byDummy As Byte)

'On Error GoTo CloseWord
On Error GoTo 0

    Dim objword As Word.Application
    Dim objDoc As Word.Document
    Dim objWS As Worksheet
    Dim path As String
    
    path = ActiveWorkbook.path & "\"
    
    Set objword = New Word.Application
    objword.Visible = False
    If Planilha2.Range("E2").Value = "" Then
    Set objDoc = selectWordFile(objword, path)
    Else
    Set objDoc = objword.Documents.Open(Planilha2.Range("E2").Value, , True, , , , , , , , , False)
    End If
    If objDoc Is Nothing Then GoTo CloseWord
    
    Planilha2.Range(("D4:G" & Planilha2.Range("D" & Rows.count).End(xlUp).Row)).ClearContents
    
    Set objWS = Planilha2
    objWS.Cells(FILE_ROW, ALT_COL).Value = "Local do Arquivo"
    objWS.Cells(FILE_ROW, PATH_COL).Value = objDoc.FullName
    objWS.Cells(HEADER_ROW, ALT_COL).Value = "T�tulo"
    objWS.Cells(HEADER_ROW, PATH_COL).Value = "Local da Tabela"
    
    getTablesTitle objDoc, objWS, objword
    
    objDoc.Close (False)
    
    'new UserForm
    Substitute.Show
    
    'Unload Tabelas
    'Planilha2.Visible = True
    'Planilha2.Activate
    'Planilha2.Cells(4, 2).Select
    
CloseWord:
    objword.Quit
    On Error GoTo 0
End Sub

Sub substituteTables(Optional byDummy As Byte)

Dim objWS As Excel.Worksheet
Dim objword As Word.Application
Dim objDoc As Word.Document
Dim Row As Long
Dim altText As String
Dim docPath As String
Dim tablePath As String
    
    
    Set objWS = Planilha2
    
    Row = START_ROW
    altText = objWS.Cells(Row, ALT_COL)
    tablePath = objWS.Cells(Row, PATH_COL)
    docPath = objWS.Cells(FILE_ROW, PATH_COL)
    
    If Dir(docPath) = "" Then ' FILE NOT FOUND
        MsgBox "Word File not found"
        Exit Sub
    End If
    
    Set objword = New Word.Application
    Set objDoc = objword.Documents.Open(docPath, , True, , , , , , , , , False)
    
    While altText <> ""
        Dim table As Word.table
        Set table = Nothing
        
        If tablePath <> "" And Dir(tablePath) <> "" Then ' Check if file exists
            Set table = findTableByTitle(objDoc, altText)
            If Not table Is Nothing Then
                Call substituteTable(table, tablePath)
            End If
        Else
'            Set table = findTableByTitle(objDoc, altText)
'            If Not table Is Nothing Then
'                table.Title = ""
'            End If
        End If
        
        ' Update loop variables
        Row = Row + 1
        altText = objWS.Cells(Row, ALT_COL)
        tablePath = objWS.Cells(Row, PATH_COL)
    Wend
    
    'Unload Tabelas
    'Planilha1.Activate
    'Planilha2.Visible = False
    
    objword.Visible = True
    
    
End Sub

Private Sub substituteTable(ByRef table As Word.table, ByRef newPath As String)
    On Error GoTo FinishWord
    Dim objword As Word.Application
    Dim objDoc As Word.Document
    Dim newTable As Word.table
    
    Set objword = New Word.Application
    objword.Visible = False
    
    If Dir(newPath) = "" Then ' FILE NOT FOUND
        MsgBox "Table File not found"
        GoTo FinishWord
    End If
    
    Set objDoc = objword.Documents.Open(newPath, , True, , , , , , , , , False)
    
    Dim rng As Word.Range
    Set rng = table.Range
    objDoc.Tables(1).Range.Copy
    table.Delete
    rng.Paste
    
FinishWord:
    If Not objDoc Is Nothing Then objDoc.Close
    If Not objword Is Nothing Then objword.Quit
    On Error GoTo 0
End Sub

Private Function selectWordFile(objword As Word.Application, Optional ByVal path As String) As Word.Document
Dim dlgSelectFile As FileDialog
Dim objDoc As Word.Document

Set dlgSelectFile = Application.FileDialog(msoFileDialogFilePicker)

    With dlgSelectFile
        .AllowMultiSelect = False
        .title = "Select Word File"
        .InitialFileName = path
        .Filters.Clear
        .Filters.Add "Word Files", "*.docx, *.doc, *.docm"
        .FilterIndex = 1
    End With
    
    If Not dlgSelectFile.Show Then
        objword.Quit
        Set objDoc = Nothing
        Exit Function
    End If

    Set objDoc = objword.Documents.Open(dlgSelectFile.SelectedItems(1), , True, , , , , , , , , False)
    
    Set selectWordFile = objDoc
End Function


Sub getTablesTitle(ByRef objDoc As Word.Document, ByRef objWS As Worksheet, ByRef objword As Word.Application)
Dim Row As Long
Dim oTable As Word.table
Dim oRng As Word.Range
Dim cht As ChartObject
Dim str As String

    Row = START_ROW
    'loop through inline shapes
    For Each oTable In objDoc.Tables
        'check if the current shape is a valid inlineShape
        If isValid(oTable) Then
            oTable.Select   ' This selection is needed, otherwise raises error "80004005 - AlternativeMethod has failed" on some files
            If oTable.title <> "" Then
                objWS.Cells(Row, 4).Value = oTable.title
                
                If Planilha2.Range("G3").Value = "Exemplos" Then
                    
                    'empty file handler 1
                    objword.Visible = True
                    '
                    Set oRng = oTable.Range
                    'orng.Select
                    'Stop
                    'orng.Expand wdSentence
                    oRng.CopyAsPicture
                    
                    Planilha2.Activate
                    
                    Planilha2.Range("A20").PasteSpecial xlPasteAll
                                        
                    'empty file handler 2
                    Application.ScreenUpdating = True
                    '
                    Set cht = Planilha2.ChartObjects.Add(Left:=Planilha2.Range("A20").Left, _
                    Width:=Planilha2.Shapes(1).Width, top:=Planilha2.Range("A20").top, Height:=Planilha2.Shapes(1).Height)
                    
                    str = "V:\Abteilungen\SaoPaulo\PQK-M\Extern\Config_BA\Substitute\"
                    
                    Wait (1)
                    
                    Planilha2.Shapes(1).Cut
                    
                    cht.Activate
                    cht.Chart.Paste
                    cht.Chart.Export Filename:=str & Row & ".bmp"
                    cht.Delete
                    Application.ScreenUpdating = False
                
                End If
                
                Row = Row + 1
            End If
        End If
    Next
    If Planilha2.Range("D4").Value = "" Then
        MsgBox "O arquivo n�o apresenta tabelas marcadas para substituir.", vbOKOnly + vbInformation, "Substitui��o n�o necess�ria!"
        End
    End If

    
End Sub

Private Function findTableByTitle(objDoc As Word.Document, altText As String) As Word.table
Dim oTable As Word.table
    
    Set findTableByTitle = Nothing
    
    For Each oTable In objDoc.Tables
        'check if the current shape is a valid inlineShape
        If isValid(oTable) Then
            oTable.Select
            If oTable.title = altText Then
                Set findTableByTitle = oTable
                Exit Function
            End If
        End If
    Next
    
End Function

Private Function isValid(ByRef table As Word.table) As Boolean
    isValid = True
    'Select Case (table.)   ' This selection is needed, otherwise raises error "80004005 - AlternativeMethod has failed" on some files
    '    Case wdTable:
    '        isValid = True
    'End Select
End Function

Function Wait(ByVal Seconds As Single)
    Dim CurrentTimer As Variant
    CurrentTimer = Timer
    Do While Timer < CurrentTimer + Seconds
    Loop
End Function

```
