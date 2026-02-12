Attribute VB_Name = "mod_Teleporte"
Option Explicit
' ==============================================================================
' MÓDULO: mod_Teleporte (Navegação Rápida)
' AUTOR: Mestre em VBA
' DESCRIÇÃO: Busca abas por índice ou nome parcial (CodeName ou Name)
' USO: Atribua a um atalho (Ex: Ctrl+Shift+F)
' ==============================================================================

Public Sub Teleportar()
    Dim termo As String
    Dim ws As Worksheet
    Dim listaEncontradas As String
    Dim contador As Integer
    Dim matchExato As Worksheet
    Dim indicesEncontrados As String
    
    ' 1. Solicita o destino
    termo = InputBox("Digite o NÚMERO (Index) ou PARTE DO NOME da aba:", "Teleporte Quântico")
    If Trim(termo) = "" Then Exit Sub
    
    ' 2. Tentativa Direta Numérica (Índice Absoluto)
    If IsNumeric(termo) Then
        If Val(termo) > 0 And Val(termo) <= ActiveWorkbook.Sheets.Count Then
            ActiveWorkbook.Sheets(Val(termo)).Activate
            Exit Sub
        End If
    End If
    
    ' 3. Busca Textual (Fuzzy Search)
    termo = UCase(Trim(termo))
    contador = 0
    listaEncontradas = "Encontrei estas opções:" & vbNewLine & vbNewLine
    
    For Each ws In ActiveWorkbook.Sheets
        ' Verifica Nome Visível OU CodeName (Ex: Planilha1)
        If InStr(1, UCase(ws.Name), termo) > 0 Or InStr(1, UCase(ws.CodeName), termo) > 0 Then
            contador = contador + 1
            If contador = 1 Then Set matchExato = ws
            
            ' Monta lista para desambiguação
            listaEncontradas = listaEncontradas & "[" & ws.Index & "] " & ws.Name & " (" & ws.CodeName & ")" & vbNewLine
            
            ' Se achar match exato de nome, prioriza
            If UCase(ws.Name) = termo Then
                ws.Activate
                Exit Sub
            End If
        End If
    Next ws
    
    ' 4. Decisão do Destino
    If contador = 0 Then
        MsgBox "Nada encontrado no setor '" & termo & "'. A nave está à deriva.", vbExclamation
    ElseIf contador = 1 Then
        ' Apenas um resultado? Vá direto.
        matchExato.Activate
    Else
        ' Múltiplos resultados? Pergunte.
        Dim escolha As String
        escolha = InputBox(listaEncontradas & vbNewLine & "Digite o NÚMERO da opção desejada:", "Ambiguidade Detectada")
        
        If IsNumeric(escolha) Then
            If Val(escolha) > 0 And Val(escolha) <= ActiveWorkbook.Sheets.Count Then
                ActiveWorkbook.Sheets(Val(escolha)).Activate
            End If
        End If
    End If
End Sub
