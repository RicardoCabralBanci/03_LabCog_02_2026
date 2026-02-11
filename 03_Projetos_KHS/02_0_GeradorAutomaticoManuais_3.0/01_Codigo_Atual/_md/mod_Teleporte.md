# mod_Teleporte

> Codigo VBA atual -- convertido automaticamente de `mod_Teleporte.bas`

```vba
Attribute VB_Name = "mod_Teleporte"
Public Sub Teleportar()
Attribute Teleportar.VB_ProcData.VB_Invoke_Func = "F\n14"
    Dim termo As String
    Dim ws As Worksheet
    Dim listaEncontradas As String
    Dim contador As Integer
    Dim matchExato As Worksheet
    Dim escolha As String
    
    ' 1. Interface de Entrada
    termo = InputBox("Destino? (N�mero ou Parte do Nome):", "Teleporte Qu�ntico")
    If Trim(termo) = "" Then Exit Sub
    
    termo = UCase(Trim(termo))
    contador = 0
    listaEncontradas = "M�ltiplos destinos encontrados:" & vbNewLine & vbNewLine
    
    ' ---------------------------------------------------------
    ' REMOVIDO: A verifica��o de �ndice num�rico imediata (Se��o 2 antiga)
    ' Agora o c�digo busca pelo texto, mesmo que seja um n�mero.
    ' ---------------------------------------------------------
    
    ' 2. Busca Fuzzy (Nome ou CodeName)
    For Each ws In ActiveWorkbook.Sheets
        ' Busca no Nome da Aba (Name) e no Nome do Objeto (CodeName)
        ' Verifica tamb�m se o CodeName termina com o n�mero digitado (ex: Planilha47 e termo 47)
        If InStr(1, UCase(ws.name), termo) > 0 Or _
           InStr(1, UCase(ws.CodeName), termo) > 0 Then
           
            contador = contador + 1
            If contador = 1 Then Set matchExato = ws
            
            listaEncontradas = listaEncontradas & "[" & ws.Index & "] " & ws.name & " (" & ws.CodeName & ")" & vbNewLine
            
            ' Se o CodeName for EXATAMENTE "Planilha" + o n�mero, prioriza
            If UCase(ws.CodeName) = "PLANILHA" & termo Then
                ws.Activate
                Exit Sub
            End If
        End If
    Next ws
    
    ' 3. Resolu��o de Conflitos
    If contador = 0 Then
        ' Se n�o achou pelo NOME, tenta pelo �NDICE (posi��o) como �ltima op��o
        If IsNumeric(termo) Then
            If val(termo) > 0 And val(termo) <= ActiveWorkbook.Sheets.count Then
                ActiveWorkbook.Sheets(val(termo)).Activate
                Exit Sub
            End If
        End If
        MsgBox "Setor '" & termo & "' n�o encontrado.", vbExclamation
        
    ElseIf contador = 1 Then
        matchExato.Activate
    Else
        ' Desambigua��o
        escolha = InputBox(listaEncontradas & vbNewLine & "Digite o N�MERO DA POSI��O (Index) para ir:", "Ambiguidade Detectada")
        
        If IsNumeric(escolha) Then
            If val(escolha) > 0 And val(escolha) <= ActiveWorkbook.Sheets.count Then
                ActiveWorkbook.Sheets(val(escolha)).Activate
            End If
        End If
    End If
End Sub


```
