Attribute VB_Name = "mod_Debug"
Option Explicit

Sub DiagnosticoDeColunas()
    Dim ws As Worksheet
    Dim msg As String
    Dim i As Integer
    Dim valB As String, valG As String, valA As String, valH As String
    
    ' Tenta pegar a aba Dados Salvos ou Base de Dados
    On Error Resume Next
    Set ws = ThisWorkbook.Sheets("Dados Salvos")
    If ws Is Nothing Then Set ws = ThisWorkbook.Sheets("Base de Dados")
    On Error GoTo 0
    
    If ws Is Nothing Then
        MsgBox "Aba 'Dados Salvos' não encontrada!", vbCritical
        Exit Sub
    End If
    
    msg = "Diagnóstico da Aba: " & ws.Name & vbCrLf & "--------------------------------" & vbCrLf
    
    ' Lê as linhas 5 a 10 para ver onde estão os dados
    For i = 5 To 10
        valA = Trim(ws.Range("A" & i).Value) ' Item?
        valB = Trim(ws.Range("B" & i).Value) ' Checkbox esperado
        valG = Trim(ws.Range("G" & i).Value) ' Caminho esperado
        
        ' Se G estiver vazio, tenta H ou F para ajudar a achar
        valH = Trim(ws.Range("H" & i).Value)
        
        msg = msg & "Linha " & i & ": Col A=[" & Left(valA, 10) & "] | Col B (Ativo)=[" & valB & "] | Col G (Path)=[" & Left(valG, 15) & "]" & vbCrLf
    Next i
    
    msg = msg & "--------------------------------" & vbCrLf & _
          "Se a Col B não tem 'X' ou 'Yes', ou a Col G não tem caminhos ('C:\...'), precisamos ajustar as constantes no script."
          
    MsgBox msg, vbInformation, "Raio-X da Planilha"
End Sub
