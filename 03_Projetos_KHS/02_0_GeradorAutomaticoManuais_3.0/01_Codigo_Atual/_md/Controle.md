# Controle

> Codigo VBA atual -- convertido automaticamente de `Controle.bas`

```vba
Attribute VB_Name = "Controle"
Private Sub volta()

Dim s As Worksheet

For Each s In ThisWorkbook.Sheets
s.Visible = xlSheetVisible
Next

'For Each s In ThisWorkbook.Sheets
's.Activate
'ActiveWindow.DisplayGridlines = False
'next

'Planilha2.Activate=se

Application.DisplayStatusBar = True
Application.DisplayFormulaBar = True
ActiveWindow.DisplayHeadings = True
ActiveWindow.DisplayHorizontalScrollBar = True
ActiveWindow.DisplayWorkbookTabs = True
ActiveWindow.DisplayVerticalScrollBar = True

End Sub

Sub picdelete(Optional byDummy As Byte)

Dim Sh As shape
With ActiveSheet
   For Each Sh In .Shapes
       If Not Application.Intersect(Sh.TopLeftCell, .Range("C4:F50")) Is Nothing Then
         If Sh.Type = msoPicture Then Sh.Delete
       End If
    Next Sh
End With

End Sub


Sub piccenter(Optional byDummy As Byte)
 Dim Row As Integer
 Dim shp As shape
 
 On Error Resume Next
 
 For Each shp In ActiveSheet.Shapes
 
 If Not Application.Intersect(shp.TopLeftCell, ActiveSheet.Range("B4:F50")) Is Nothing Then
 shp.Select
 
  Dim vSel As Variant
  Dim rngZ As Range
  Set vSel = Selection
  If VarType(vSel) = vbObject Then
    With vSel
      Set rngZ = .TopLeftCell
      .top = rngZ.top + (rngZ.Height - .Height) / 2
      .Left = rngZ.Left + (rngZ.Width - .Width) / 2
      .ShapeRange.LockAspectRatio = -1
      .Placement = xlMove
      .PrintObject = True
    End With
    rngZ.Select
  End If
  End If
Next
End Sub

Sub frez(Optional byDummy As Byte)

ActiveWindow.FreezePanes = True

End Sub

Sub ColCode(Optional byDummy As Byte)
MsgBox ActiveCell.Interior.ColorIndex
End Sub

Sub dd(Optional byDummy As Byte)

Dim olabel

Set olabel = ActiveSheet.OLEObjects.Add(ClassType:="Forms.Label.1", top:=5)

End Sub


Sub a(Optional byDummy As Byte)

Planilha26.Shapes("detail").Visible = msoCTrue

End Sub

Private Sub ssa() '(Optional byDummy As Byte)
Planilha2.Activate
Planilha2.Range("A150").Activate
'Application.EnableEvents = True
End Sub

Sub re(Optional byDummy As Byte)

Dim i As Long
Dim c As cell


i = WorksheetFunction.CountBlank(Planilha11.Range("D4:D20")) ' Planilha11.Range(("D4:D20" & Planilha11.Range("D" & Rows.Count).End(xlUp).Row)).Count

MsgBox i

End Sub

Private Sub dds() '(Optional byDummy As Byte)

'Dim erng As Range

'Set erng = Planilha40.Range("F8:I" & Planilha40.Range("H" & Rows.Count).End(xlUp).Row)
               ' erng.Copy
               
'               Planilha2.Range("A140").Value = Environ("Username")

'Application.Visible = True

Planilha3.Activate

End Sub
 Sub LibertarGeral()
     Dim ws As Worksheet
     For Each ws In ThisWorkbook.Worksheets
         ws.ScrollArea = "" ' Remove o limite de rolagem
         ws.EnableSelection = xlNoRestrictions ' Permite clicar em qualquer lugar
         ws.Visible = xlSheetVisible ' Mostra a aba
     Next ws

     ' Restaura a interface (o c�digo da "volta")
    Application.DisplayFormulaBar = True
    ActiveWindow.DisplayWorkbookTabs = True
    ActiveWindow.DisplayHeadings = True
    ActiveWindow.DisplayHorizontalScrollBar = True
    ActiveWindow.DisplayVerticalScrollBar = True
    Application.DisplayFormulaBar = True

    MsgBox "LIBERDADE! Scroll, Sele��o e Abas restaurados.", vbInformation
End Sub

Sub ListarBotoes()
    Dim shp As shape
    For Each shp In ActiveSheet.Shapes
        Debug.Print "Nome: " & shp.name & " | Macro Atual: " & shp.OnAction
    Next shp
End Sub
' =========================================================================================
' UTILIT�RIO: CORRETOR DE BOT�ES SMART V2 (COM REMO��O DE AUTO-REFER�NCIA)
' DESCRI��O:
' 1. Detecta sigla da m�quina (DPL, PCK...)
' 2. Detecta n�mero da p�gina atual por palavras-chave (Estrutura=1, T�cnicos=3...)
' 3. Corrige macros antigas.
' 4. REMOVE a macro se ela apontar para a pr�pria p�gina atual.
' =========================================================================================
Sub LiberarApenasImagens()
    Dim senha As String
    senha = "123" ' Coloque sua senha aqui se houver
    
    ' Primeiro desprotege para aplicar a nova regra
    On Error Resume Next
    ActiveSheet.Unprotect Password:=senha
    
    ' Reprotege, mas define DrawingObjects:=False (Isso libera as imagens)
    ActiveSheet.Protect Password:=senha, _
        DrawingObjects:=False, _
        Contents:=True, _
        Scenarios:=True
        
    If Err.Number = 0 Then
        MsgBox "C�lulas continuam protegidas, mas Imagens foram liberadas!", vbInformation
    Else
        MsgBox "Erro ao tentar alterar a prote��o.", vbCritical
    End If
    On Error GoTo 0
End Sub
Sub CorrigirBotoes_Smart_V2()
    Dim shp As shape
    Dim macroFull As String, macroNome As String
    Dim siglaNova As String, novaMacro As String
    Dim padroesAntigos As Variant
    Dim i As Integer, contador As Integer, removidos As Integer
    Dim numeroPaginaMacro As String
    Dim numeroPaginaAtual As String
    
    ' 1. Detectar Sigla Nova (3 primeiras letras)
    siglaNova = UCase(Left(ActiveSheet.name, 3))
    
    ' 2. Detectar P�gina Atual (L�gica Simplificada para PLT/DPL/PCK/DPK)
    ' Ajuste conforme seus nomes de aba reais
    If InStr(ActiveSheet.name, "Estrutura") > 0 Then numeroPaginaAtual = "1"
    If InStr(ActiveSheet.name, "Gerais") > 0 Then numeroPaginaAtual = "2"
    If InStr(ActiveSheet.name, "T�cnicos") > 0 Then numeroPaginaAtual = "3"
    If InStr(ActiveSheet.name, "El�tricos") > 0 Then numeroPaginaAtual = "4"
    If InStr(ActiveSheet.name, "IHM") > 0 Then numeroPaginaAtual = "5"
    
    padroesAntigos = Array("PCK", "PLT", "DPL", "DPK", "BTR", "GTR", "DVD", "PET", "CIP", "CMX", "CCMX")
    
    If MsgBox("Configura��o Detectada:" & vbNewLine & _
              "Sigla: " & siglaNova & vbNewLine & _
              "P�gina Atual (Identificada): PG" & numeroPaginaAtual & vbNewLine & vbNewLine & _
              "Vou corrigir as siglas e REMOVER macros que apontem para PG" & numeroPaginaAtual & "." & vbNewLine & _
              "Confirmar?", vbQuestion + vbYesNo, "Corretor Smart V2") = vbNo Then Exit Sub
    
    contador = 0
    removidos = 0
    
    For Each shp In ActiveSheet.Shapes
        macroFull = shp.OnAction
        
        If macroFull <> "" Then
            ' Limpa nome do arquivo
            If InStr(macroFull, "!") > 0 Then macroNome = Split(macroFull, "!")(1) Else macroNome = macroFull
            
            ' Verifica se � macro de navega��o (PG + Numero)
            If InStr(macroNome, "PG") > 0 And IsNumeric(Right(macroNome, 1)) Then
                
                For i = LBound(padroesAntigos) To UBound(padroesAntigos)
                    If InStr(1, macroNome, padroesAntigos(i), vbTextCompare) = 1 Then
                        ' Achou padr�o antigo
                        numeroPaginaMacro = Right(macroNome, Len(macroNome) - Len(padroesAntigos(i))) ' Pega "1", "3", etc. (Assumindo PG1, PG3...)
                        ' Ajuste fino: Se a macro for ex: PCKPG1, removemos PCK (3 chars) -> sobra PG1.
                        ' Se a macro for PCKPG1, numeroPaginaMacro tem que pegar o numero.
                        ' Corre��o da l�gica de extra��o:
                        numeroPaginaMacro = Right(macroNome, 1) ' Pega s� o �ltimo d�gito (assume 1-9)
                        
                        ' Verifica Auto-Refer�ncia
                        If numeroPaginaMacro = numeroPaginaAtual Then
                            shp.OnAction = "" ' Remove a macro!
                            removidos = removidos + 1
                            Debug.Print "Removido (Auto-Ref): " & shp.name & " | Era: " & macroNome
                        Else
                            ' Corrige a macro
                            novaMacro = siglaNova & "PG" & numeroPaginaMacro
                            If novaMacro <> macroNome Then
                                shp.OnAction = novaMacro
                                contador = contador + 1
                                Debug.Print "Corrigido: " & shp.name & " | " & macroNome & " -> " & novaMacro
                            End If
                        End If
                        Exit For
                    End If
                Next i
            End If
        End If
    Next shp
    
    MsgBox "Conclu�do!" & vbNewLine & _
           "Redirecionados: " & contador & vbNewLine & _
           "Removidos (Mesma P�gina): " & removidos, vbInformation
End Sub

```
