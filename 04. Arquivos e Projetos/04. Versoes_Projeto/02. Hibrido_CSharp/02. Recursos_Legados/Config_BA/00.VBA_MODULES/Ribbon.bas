Attribute VB_Name = "Ribbon"
Sub limpeza(ByRef i As Integer, Optional byDummy As Byte)

Application.ScreenUpdating = False

With ThisWorkbook.Sheets(i)

Select Case i

Case 4, 7 To 10, 15 To 18, 29

.Unprotect vbNullString: .Range("B4:H100").ClearContents: .Protect vbNullString

Case 5, 6, 11, 13, 14, 19, 24, 28, 30, 33, 37, 41

.Unprotect vbNullString: .Range("D4:D100").ClearContents: .Protect vbNullString

Case 21, 22, 26, 31, 35, 38, 39

.Unprotect vbNullString: .Range("E4:E100").ClearContents: .Protect vbNullString

Case 23

.Unprotect vbNullString: .Range("C4:C6").ClearContents: .Protect vbNullString

Case 25

.Unprotect vbNullString: .Range("D4:E100").ClearContents: .Protect vbNullString

Case 27

.Unprotect vbNullString: .Range("C3").ClearContents: .Range("C7:C9").ClearContents
.Range("C13:C15").ClearContents: .Range("C19:C22").ClearContents: .Range("H3:H22").ClearContents: .Protect vbNullString

Case 32

.Unprotect vbNullString: .Range("C5:C7").ClearContents: .Range("C11:C12").ClearContents
.Range("C16:C20").ClearContents: .Range("H5:H20").ClearContents: .Protect vbNullString

Case 36

.Unprotect vbNullString: .Range("C5:C7").ClearContents: .Range("C11:C13").ClearContents
.Range("G11").ClearContents: .Range("H5:H7").ClearContents: .Protect vbNullString

Case 40

.Unprotect vbNullString: .Range("C5:C7").ClearContents: .Range("C11:C13").ClearContents
.Range("G5:G6").ClearContents: .Range("H10:H13").ClearContents: .Protect vbNullString

'Case 12, 20, 42

'.Unprotect vbNullString: .Range("C2").ClearContents: .Range("B5").MergeArea.ClearContents: .Range("B11").MergeArea.ClearContents
'.Range("B17").MergeArea.ClearContents: .Range("B23").MergeArea.ClearContents: .Range("B29").MergeArea.ClearContents: .Range("B35").MergeArea.ClearContents

'Application.EnableEvents = True: .Range("C2").ClearContents

End Select

End With

Planilha3.Unprotect

Application.EnableEvents = True: Application.ScreenUpdating = True

End Sub

Sub instruc(Optional byDummy As Byte)

Instruções.Show

End Sub

Sub z(control As IRibbonControl)

On Error GoTo exitsub

'Provavelmente levarei uma chamada se deixar isso, então...
Exit Sub

Dim rr As Integer

rr = Planilha2.Range("A150").Value

rr = rr + 1

Planilha2.Range("A150").Value = rr

'Ainda deixei limitado pra quem eu acho que segue o mesmo humor, mas né... melhor deixar de fora
If rr = 50 Then
If Planilha2.Range("A140").Value = "PillingerR" Or Planilha2.Range("A140").Value = "CeribeliK" Then

Dim WMP As Object
Set WMP = CreateObject("new:{6BF52A52-394A-11d3-B153-00C04F79FAA6}")
WMP.OpenPlayer "V:\Abteilungen\SaoPaulo\PQK-M\Extern\Config_BA\Substitute\..mp4"

Planilha2.Range("A150").Value = "0"

End If
End If

exitsub:

End Sub

'Callback for Salvar onAction
Sub GoSave(control As IRibbonControl)

On Error GoTo message

ThisWorkbook.Save
Exit Sub

message:
MsgBox "Ainda não foi salvo pela primeira vez, use a aba fixa 'Arquivo'", vbCritical, "Arquivo não existente ainda"

End Sub

'Callback for Inf0 onAction
Sub Inform(control As IRibbonControl)

Info.Show

End Sub

'Callback for Im0 onAction
Sub SImagem(control As IRibbonControl)

Dim an As Integer

With Planilha2

an = MsgBox("Deseja extrair as imagens de exemplo para conferência?" & vbNewLine & vbNewLine & _
"Está opção fará a execução ser consideravelmente mais lenta!", vbQuestion + vbYesNoCancel, "Extração de imagens")
If an = vbYes Then
.Range("G3").Value = "Exemplos"
ElseIf an = vbCancel Then
Exit Sub
Else: .Range("G3").Value = vbNullString: End If

.Range("G1").Value = "Imagem"

End With

Call Imagem.PopulateXL

End Sub

'Callback for Tab0 onAction
Sub STabela(control As IRibbonControl)

Dim an As Integer

With Planilha2

an = MsgBox("Deseja extrair as tabelas de exemplo para conferência? As mesmas podem ser encontradas na pasta de template." & vbNewLine _
& vbNewLine & "Está opção fará a execução ser consideravelmente mais lenta!", vbQuestion + vbYesNoCancel, "Extração de imagens")
If an = vbYes Then
.Range("G3").Value = "Exemplos"
ElseIf an = vbCancel Then
Exit Sub
Else: .Range("G3").Value = vbNullString: End If

.Range("G1").Value = "Tabela"

End With

Call Tabela.PopulateXL

'Substitute.Show

End Sub

'Callback for Proteger onAction
Sub GoProtect(control As IRibbonControl)

Dim X As Boolean
    
    With ThisWorkbook.ActiveSheet
        X = .ProtectContents
        If X = False Then
            .Protect vbNullString
        Else: .Unprotect vbNullString: End If
    End With

End Sub

'Callback for Códigos onAction
Sub GoCode(control As IRibbonControl)

    Application.VBE.MainWindow.Visible = True

End Sub

'Callback for Restart onAction
Sub Restart(control As IRibbonControl)

Application.EnableEvents = False

Dim i As Integer

an = MsgBox("Todas páginas serão reiniciadas, deseja continuar?", vbExclamation + vbYesNo, "Atenção")
    If an = vbYes Then

For i = 4 To ThisWorkbook.Sheets.Count 'until last editable sheet, can be thisworkbook.sheets.count
Call limpeza(i)
Next

End If
Application.EnableEvents = True

End Sub

'Callback for Informações onAction
Sub GoInfo(control As IRibbonControl)

Dim an As Integer

    an = MsgBox("Este arquivo se destina a geração de manuais de operação dos modelos apresentados nas abas." & _
    vbNewLine & vbNewLine & "Deseja ir para página de instruções para mais informações?", vbInformation + vbYesNo, "Informação pertinente")
    If an = vbYes Then
    With Planilha1
        .Visible = xlSheetVisible
        .Activate
    End With
    End If
    
End Sub

'Callback for Ajuda onAction
Sub GoAjuda(control As IRibbonControl)

    MsgBox "Caso ocorra algum erro ou tenha dúvidas, favor entrar em contato com o responsável pela área de documentação!" & _
    vbNewLine & vbNewLine & "Antes de entrar em contato, favor verificar a página de instruções apertando o botão de 'Informações'." _
    , vbExclamation, "Ajuda"

End Sub

'Callback for Comp1 onAction
Sub Comp(control As IRibbonControl)

With Planilha4
.Visible = xlSheetVisible
.Activate
End With

End Sub

'Callback for Pr1 onAction
Sub Preenchimento(control As IRibbonControl)

Exemplos.Show

End Sub

'Callback for Limp1 onAction
Sub Limp(control As IRibbonControl)

Application.EnableEvents = False

Dim i As Integer

i = ThisWorkbook.ActiveSheet.Index

Call limpeza(i)

Application.EnableEvents = True

End Sub

'Callback for Mec1 onAction
Sub Mec1(control As IRibbonControl)

Planilha5.Activate

End Sub

'Callback for El1 onAction
Sub El1(control As IRibbonControl)

Planilha8.Activate

End Sub

'Callback for IHM1 onAction
Sub IHM1(control As IRibbonControl)

Planilha12.Activate

End Sub

'Callback for Ex1 onAction
Sub Ex1(control As IRibbonControl)

'Dim tr As String

'tr = Planilha2.Cells(20, 2).Value

Planilha2.Cells(20, 2).Value = Planilha2.Cells(20, 1).Value


Planilha2.Cells(20, 1).Value = "BTR"


Exceções.Show

'If tr <> planila2.Cells(20, 2).Value Then
'Exceções.UserForm_initialize
'End If

End Sub

'Callback for Ger1 onAction
Sub Ger1(control As IRibbonControl)

Planilha3.Range("B7").Value = "No"

Dim ans As Integer

Info.Show

Do Until Info.Visible = False
DoEvents
Loop

If Planilha5.Range("D4:D10").Cells.Count = WorksheetFunction.CountBlank(Planilha5.Range("D4:D10")) Then
an = MsgBox("Os dispositivos de proteção não foram selecionados, deseja conferir?" _
, vbYesNoCancel + vbExclamation, "Conteúdo ausente")
    If an = vbYes Then
        Planilha5.Activate
        Exit Sub
    End If
    If an = vbCancel Then
    Exit Sub
    End If
End If

If Planilha6.Range("D4:D28").Cells.Count = WorksheetFunction.CountBlank(Planilha6.Range("D4:D28")) Then
an = MsgBox("Os módulos do transportador não foram selecionados, deseja conferir?" _
, vbYesNoCancel + vbExclamation, "Conteúdo ausente")
    If an = vbYes Then
        Planilha6.Activate
        Exit Sub
    End If
    If an = vbCancel Then
    Exit Sub
    End If
End If

If Planilha7.Cells(4, 2).Value = vbNullString Then
an = MsgBox("Os tipos de recipientes não foram definidos, deseja conferir?" _
, vbYesNoCancel + vbExclamation, "Conteúdo ausente")
    If an = vbYes Then
        Planilha7.Activate
        Exit Sub
    End If
    If an = vbCancel Then
    Exit Sub
    End If
End If

If Planilha3.Range("E7") = vbNullString Then

If Planilha8.Cells(4, 2).Value = vbNullString Then
an = MsgBox("As áreas do sistema não foram definidas, deseja conferir?" _
, vbYesNoCancel + vbExclamation, "Conteúdo ausente")
    If an = vbYes Then
        Planilha8.Activate
        Exit Sub
    End If
    If an = vbCancel Then
    Exit Sub
    End If
End If

If Planilha9.Cells(4, 2).Value = vbNullString Then
an = MsgBox("A tabela de dispositivos de comando não foi especificada, deseja conferir?" _
, vbYesNoCancel + vbExclamation, "Conteúdo ausente")
    If an = vbYes Then
        Planilha9.Activate
        Exit Sub
    End If
    If an = vbCancel Then
    Exit Sub
    End If
End If

If Planilha10.Cells(4, 2).Value = vbNullString Then
an = MsgBox("A tabela de dispositivos de aviso não foi especificada, deseja conferir?" _
, vbYesNoCancel + vbExclamation, "Conteúdo ausente")
    If an = vbYes Then
        Planilha10.Activate
        Exit Sub
    End If
    If an = vbCancel Then
    Exit Sub
    End If
End If

If Planilha11.Range("D4:D20").Cells.Count = WorksheetFunction.CountBlank(Planilha11.Range("D4:D20")) Then
an = MsgBox("Os componentes elétricos não foram selecionados, deseja conferir?" _
, vbYesNoCancel + vbExclamation, "Conteúdo ausente")
    If an = vbYes Then
        Planilha11.Activate
        Exit Sub
    End If
    If an = vbCancel Then
    Exit Sub
    End If
End If

If Planilha12.Cells(2, 4).Value = "Não escolhido" Then
an = MsgBox("O modelo de IHM não foi selecionado, deseja conferir?" _
, vbYesNoCancel + vbExclamation, "Conteúdo ausente")
    If an = vbYes Then
        Planilha12.Activate
        Exit Sub
    End If
    If an = vbCancel Then
    Exit Sub
    End If
End If

End If

Call btr.Manual

End Sub

'Callback for GIHM1 onAction
Sub GIMH1(control As IRibbonControl)

Dim ans As Integer

Info.Show

Do Until Info.Visible = False
DoEvents
Loop

Dim an As Integer

If Planilha11.Range("D4:D20").Cells.Count = WorksheetFunction.CountBlank(Planilha11.Range("D4:D20")) Then
an = MsgBox("O manual de atualização de IHM apresenta o capítulo de operação por completo, assim é necessário o preenchimento dos componentes elétricos" _
& vbNewLine & vbNewLine & "Deseja preencher agora?", vbYesNoCancel + vbExclamation, "Conteúdo ausente")
    If an = vbYes Then
        Planilha11.Activate
        Exit Sub
    End If
    If an = vbCancel Then
    Exit Sub
    End If
End If


Planilha3.Range("B7").Value = "Yes"


Call btr.Manual

End Sub

'Callback for Mec2 onAction
Sub Mec2(control As IRibbonControl)

Planilha13.Activate

End Sub

'Callback for El2 onAction
Sub El2(control As IRibbonControl)

Planilha16.Activate

End Sub

'Callback for IHM2 onAction
Sub IHM2(control As IRibbonControl)

Planilha20.Activate

End Sub

'Callback for Ex2 onAction
Sub Ex2(control As IRibbonControl)

'Dim tr As String

'tr = Planilha2.Cells(20, 2).Value

Planilha2.Cells(20, 2).Value = Planilha2.Cells(20, 1).Value


Planilha2.Cells(20, 1).Value = "BTR" 'GTR could be used, but since both share exact same list, BTR was used instead


Exceções.Show

'If tr <> planila2.Cells(20, 2).Value Then
'Exceções.UserForm_initialize
'End If

End Sub

'Callback for Ger2 onAction
Sub Ger2(control As IRibbonControl)

Planilha3.Range("B144").Value = "No"

Dim ans As Integer

Info.Show

Do Until Info.Visible = False
DoEvents
Loop

If Planilha13.Range("D4:D10").Cells.Count = WorksheetFunction.CountBlank(Planilha13.Range("D4:D10")) Then
an = MsgBox("Os dispositivos de proteção não foram selecionados, deseja conferir?" _
, vbYesNoCancel + vbExclamation, "Conteúdo ausente")
    If an = vbYes Then
        Planilha13.Activate
        Exit Sub
    End If
    If an = vbCancel Then
    Exit Sub
    End If
End If

If Planilha14.Range("D4:D26").Cells.Count = WorksheetFunction.CountBlank(Planilha14.Range("D4:D26")) Then
an = MsgBox("Os módulos do transportador não foram selecionados, deseja conferir?" _
, vbYesNoCancel + vbExclamation, "Conteúdo ausente")
    If an = vbYes Then
        Planilha14.Activate
        Exit Sub
    End If
    If an = vbCancel Then
    Exit Sub
    End If
End If

If Planilha15.Cells(4, 2).Value = vbNullString Then
an = MsgBox("Os tipos de recipientes não foram definidos, deseja conferir?" _
, vbYesNoCancel + vbExclamation, "Conteúdo ausente")
    If an = vbYes Then
        Planilha15.Activate
        Exit Sub
    End If
    If an = vbCancel Then
    Exit Sub
    End If
End If

If Planilha3.Range("E7") = vbNullString Then

If Planilha16.Cells(4, 2).Value = vbNullString Then
an = MsgBox("As áreas do sistema não foram definidas, deseja conferir?" _
, vbYesNoCancel + vbExclamation, "Conteúdo ausente")
    If an = vbYes Then
        Planilha16.Activate
        Exit Sub
    End If
    If an = vbCancel Then
    Exit Sub
    End If
End If

If Planilha17.Cells(4, 2).Value = vbNullString Then
an = MsgBox("A tabela de dispositivos de comando não foi especificada, deseja conferir?" _
, vbYesNoCancel + vbExclamation, "Conteúdo ausente")
    If an = vbYes Then
        Planilha17.Activate
        Exit Sub
    End If
    If an = vbCancel Then
    Exit Sub
    End If
End If

If Planilha18.Cells(4, 2).Value = vbNullString Then
an = MsgBox("A tabela de dispositivos de aviso não foi especificada, deseja conferir?" _
, vbYesNoCancel + vbExclamation, "Conteúdo ausente")
    If an = vbYes Then
        Planilha18.Activate
        Exit Sub
    End If
    If an = vbCancel Then
    Exit Sub
    End If
End If

If Planilha19.Range("D4:D20").Cells.Count = WorksheetFunction.CountBlank(Planilha19.Range("D4:D20")) Then
an = MsgBox("Os componentes elétricos não foram selecionados, deseja conferir?" _
, vbYesNoCancel + vbExclamation, "Conteúdo ausente")
    If an = vbYes Then
        Planilha19.Activate
        Exit Sub
    End If
    If an = vbCancel Then
    Exit Sub
    End If
End If

If Planilha20.Cells(2, 4).Value = "Não escolhido" Then
an = MsgBox("O modelo de IHM não foi selecionado, deseja conferir?" _
, vbYesNoCancel + vbExclamation, "Conteúdo ausente")
    If an = vbYes Then
        Planilha20.Activate
        Exit Sub
    End If
    If an = vbCancel Then
    Exit Sub
    End If
End If

End If

Call gtr.Manual

End Sub

'Callback for GIHM1 onAction
Sub GIMH2(control As IRibbonControl)

Dim ans As Integer

Info.Show

Do Until Info.Visible = False
DoEvents
Loop

Dim an As Integer

If Planilha19.Range("D4:D20").Cells.Count = WorksheetFunction.CountBlank(Planilha19.Range("D4:D20")) Then
an = MsgBox("O manual de atualização de IHM apresenta o capítulo de operação por completo, assim é necessário o preenchimento dos componentes elétricos" _
& vbNewLine & vbNewLine & "Deseja preencher agora?", vbYesNoCancel + vbExclamation, "Conteúdo ausente")
    If an = vbYes Then
        Planilha19.Activate
        Exit Sub
    End If
    If an = vbCancel Then
    Exit Sub
    End If
End If


Planilha3.Range("B144").Value = "Yes"


Call gtr.Manual 'the calling must be to standard module 'GTR.manual

End Sub

'Callback for Mec3 onAction
Sub Mec3(control As IRibbonControl)

Planilha21.Activate

End Sub

'Callback for El3 onAction
Sub El3(control As IRibbonControl)

Planilha24.Activate

End Sub

'Callback for IHM3 onAction
Sub IHM3(control As IRibbonControl)

MsgBox "No momento apenas Clearline está registrada no banco de dados." & vbNewLine & _
"Caso outra IHM seja utilizada, favor entrar em contato com o responsável pela área de documentação.", _
vbOKOnly + vbExclamation, "Seleção não possível"

End Sub

'Callback for Ex3 onAction
Sub Ex3(control As IRibbonControl)

'Dim tr As String

'tr = Planilha2.Cells(20, 1).Value
Planilha2.Cells(20, 2).Value = Planilha2.Cells(20, 1).Value


Planilha2.Cells(20, 1).Value = "DVD"


Exceções.Show

'If tr <> planilha2.Cells(20, 1).Value Then
'Exceções.UserForm_initialize
'End If

End Sub

'Callback for Ger3 onAction
Sub Ger3(control As IRibbonControl)

Planilha3.Range("B279").Value = "No"

Dim ans As Integer

Info.Show

Do Until Info.Visible = False
DoEvents
Loop

If Planilha21.Range("E4:E23").Cells.Count = WorksheetFunction.CountBlank(Planilha21.Range("E4:E23")) Then
an = MsgBox("Os componentes estruturais da máquina não foram selecionados, deseja conferir?" _
, vbYesNoCancel + vbExclamation, "Conteúdo ausente")
    If an = vbYes Then
        Planilha21.Activate
        Exit Sub
    End If
    If an = vbCancel Then
    Exit Sub
    End If
End If

If Planilha22.Range("E4:E13").Cells.Count = WorksheetFunction.CountBlank(Planilha22.Range("E4:E13")) Then
an = MsgBox("Os componentes do manifold não foram selecionados, deseja conferir?" _
, vbYesNoCancel + vbExclamation, "Conteúdo ausente")
    If an = vbYes Then
        Planilha22.Activate
        Exit Sub
    End If
    If an = vbCancel Then
    Exit Sub
    End If
End If

If Planilha23.Cells(4, 3).Value = vbNullString Then
an = MsgBox("Os dados da enchedora não foram definidos, deseja conferir?" _
, vbYesNoCancel + vbExclamation, "Conteúdo ausente")
    If an = vbYes Then
        Planilha23.Activate
        Exit Sub
    End If
    If an = vbCancel Then
    Exit Sub
    End If
End If


If Planilha24.Range("D4:D13").Cells.Count = WorksheetFunction.CountBlank(Planilha24.Range("D4:D13")) Then
an = MsgBox("Os componentes elétricos não foram selecionados, deseja conferir?" _
, vbYesNoCancel + vbExclamation, "Conteúdo ausente")
    If an = vbYes Then
        Planilha24.Activate
        Exit Sub
    End If
    If an = vbCancel Then
    Exit Sub
    End If
End If

If Planilha25.Range("D4:E32").Cells.Count = WorksheetFunction.CountBlank(Planilha25.Range("D4:E32")) Then
an = MsgBox("Nenhuma botoeira foi selecionada, deseja conferir?" _
, vbYesNoCancel + vbExclamation, "Conteúdo ausente")
    If an = vbYes Then
        Planilha25.Activate
        Exit Sub
    End If
    If an = vbCancel Then
    Exit Sub
    End If
End If


Call dvd.Manual

End Sub

'Callback for GIHM1 onAction
Sub GIMH3(control As IRibbonControl)

Dim ans As Integer

Info.Show

Do Until Info.Visible = False
DoEvents
Loop

Dim an As Integer

If Planilha24.Range("D4:D13").Cells.Count = WorksheetFunction.CountBlank(Planilha24.Range("D4:D13")) Then
an = MsgBox("O manual de atualização de IHM apresenta o capítulo de operação por completo, assim é necessário o preenchimento dos componentes elétricos" _
& vbNewLine & vbNewLine & "Deseja preencher agora?", vbYesNoCancel + vbExclamation, "Conteúdo ausente")
    If an = vbYes Then
        Planilha24.Activate
        Exit Sub
    End If
    If an = vbCancel Then
    Exit Sub
    End If
End If


Planilha3.Range("B279").Value = "Yes"


Call dvd.Manual

End Sub

'Callback for Mec4 onAction
Sub Mec4(control As IRibbonControl)

Planilha26.Activate

End Sub

'Callback for El4 onAction
Sub El4(control As IRibbonControl)

Planilha28.Activate

End Sub

'Callback for IHM4 onAction
Sub IHM4(control As IRibbonControl)

MsgBox "No momento apenas Clearline está registrada no banco de dados." & vbNewLine & _
"Caso outra IHM seja utilizada, favor entrar em contato com o responsável pela área de documentação.", _
vbOKOnly + vbExclamation, "Seleção não possível"

End Sub

'Callback for Ex4 onAction
Sub Ex4(control As IRibbonControl)

Planilha2.Cells(20, 2).Value = Planilha2.Cells(20, 1).Value


Planilha2.Cells(20, 1).Value = "PET"


Exceções.Show

End Sub

'Callback for Ger4 onAction
Sub Ger4(control As IRibbonControl)

Planilha3.Range("B442").Value = "No"

Dim ans As Integer

Info.Show

Do Until Info.Visible = False
DoEvents
Loop

If Planilha26.Range("E4:E14").Cells.Count = WorksheetFunction.CountBlank(Planilha26.Range("E4:E14")) Then
an = MsgBox("Os componentes estruturais do sistema não foram selecionados, deseja conferir?" _
, vbYesNoCancel + vbExclamation, "Conteúdo ausente")
    If an = vbYes Then
        Planilha26.Activate
        Exit Sub
    End If
    If an = vbCancel Then
    Exit Sub
    End If
End If

If Planilha27.Cells(3, 3).Value = vbNullString Then
an = MsgBox("O comando das válvulas não foi especificado, deseja conferir?" _
, vbYesNoCancel + vbExclamation, "Conteúdo ausente")
    If an = vbYes Then
        Planilha27.Activate
        Exit Sub
    End If
    If an = vbCancel Then
    Exit Sub
    End If
End If

If Planilha27.Cells(7, 3).Value = vbNullString Then
an = MsgBox("Os dados da enchedora não foram fornecidos, deseja conferir?" _
, vbYesNoCancel + vbExclamation, "Conteúdo ausente")
    If an = vbYes Then
        Planilha27.Activate
        Exit Sub
    End If
    If an = vbCancel Then
    Exit Sub
    End If
End If

If Planilha27.Cells(13, 3).Value = vbNullString Then
an = MsgBox("Os dados do rinser não foram fornecidos, deseja conferir?" _
, vbYesNoCancel + vbExclamation, "Conteúdo ausente")
    If an = vbYes Then
        Planilha27.Activate
        Exit Sub
    End If
    If an = vbCancel Then
    Exit Sub
    End If
End If

If Planilha27.Cells(19, 3).Value = vbNullString Then
an = MsgBox("Os dados do lacrador não foram fornecidos, deseja conferir?" _
, vbYesNoCancel + vbExclamation, "Conteúdo ausente")
    If an = vbYes Then
        Planilha27.Activate
        Exit Sub
    End If
    If an = vbCancel Then
    Exit Sub
    End If
End If

If Planilha28.Range("D4:D16").Cells.Count = WorksheetFunction.CountBlank(Planilha28.Range("D4:D16")) Then
an = MsgBox("Os componentes elétricos não foram selecionados, deseja conferir?" _
, vbYesNoCancel + vbExclamation, "Conteúdo ausente")
    If an = vbYes Then
        Planilha28.Activate
        Exit Sub
    End If
    If an = vbCancel Then
    Exit Sub
    End If
End If

Call pet.Manual

End Sub

'Callback for GIHM1 onAction
Sub GIMH4(control As IRibbonControl)

Dim ans As Integer

Info.Show

Do Until Info.Visible = False
DoEvents
Loop

Dim an As Integer

If Planilha28.Range("D4:D16").Cells.Count = WorksheetFunction.CountBlank(Planilha28.Range("D4:D16")) Then
an = MsgBox("O manual de atualização de IHM apresenta o capítulo de operação por completo, assim é necessário o preenchimento dos componentes elétricos" _
& vbNewLine & vbNewLine & "Deseja preencher agora?", vbYesNoCancel + vbExclamation, "Conteúdo ausente")
    If an = vbYes Then
        Planilha28.Activate
        Exit Sub
    End If
    If an = vbCancel Then
    Exit Sub
    End If
End If


Planilha3.Range("B442").Value = "Yes"


Call pet.Manual

End Sub

'Callback for Mec5 onAction
Sub Mec5(control As IRibbonControl)

Planilha29.Activate

End Sub

'Callback for El5 onAction
Sub El5(control As IRibbonControl)

Planilha33.Activate

End Sub

'Callback for IHM5 onAction
Sub IHM5(control As IRibbonControl)

MsgBox "No momento apenas Clearline está registrada no banco de dados." & vbNewLine & _
"Caso outra IHM seja utilizada, favor entrar em contato com o responsável pela área de documentação.", _
vbOKOnly + vbExclamation, "Seleção não possível"

End Sub

'Callback for Ex5 onAction
Sub Ex5(control As IRibbonControl)

Planilha2.Cells(20, 2).Value = Planilha2.Cells(20, 1).Value


Planilha2.Cells(20, 1).Value = "CIP"


Exceções.Show

End Sub

'Callback for Ger5 onAction
Sub Ger5(control As IRibbonControl)

Planilha3.Range("B534").Value = "No"

Dim ans As Integer

Info.Show

Do Until Info.Visible = False
DoEvents
Loop

If Planilha29.Cells(4, 2).Value = vbNullString Then
an = MsgBox("Os químicos do sistema não foram especificados, deseja conferir?" _
, vbYesNoCancel + vbExclamation, "Conteúdo ausente")
    If an = vbYes Then
        Planilha29.Activate
        Exit Sub
    End If
    If an = vbCancel Then
    Exit Sub
    End If
End If

If Planilha30.Range("D4:D8").Cells.Count = WorksheetFunction.CountBlank(Planilha30.Range("D4:D8")) Then
an = MsgBox("A estrutura do sistema não foi especificada, deseja conferir?" _
, vbYesNoCancel + vbExclamation, "Conteúdo ausente")
    If an = vbYes Then
        Planilha30.Activate
        Exit Sub
    End If
    If an = vbCancel Then
    Exit Sub
    End If
End If

If Planilha31.Range("E4:E21").Cells.Count = WorksheetFunction.CountBlank(Planilha31.Range("E4:E21")) Then
an = MsgBox("Os componentes gerais do sistema não foram especificados, deseja conferir?" _
, vbYesNoCancel + vbExclamation, "Conteúdo ausente")
    If an = vbYes Then
        Planilha31.Activate
        Exit Sub
    End If
    If an = vbCancel Then
    Exit Sub
    End If
End If

If Planilha32.Range("C5").Value = vbNullString Then
an = MsgBox("As dimensões do sistema não foram especificadas, deseja conferir?" _
, vbYesNoCancel + vbExclamation, "Conteúdo ausente")
    If an = vbYes Then
        Planilha32.Activate
        Exit Sub
    End If
    If an = vbCancel Then
    Exit Sub
    End If
End If
    
If Planilha32.Range("C11").Value = vbNullString Then
an = MsgBox("Os pesos aproximados do sistema não foram especificados, deseja conferir?" _
, vbYesNoCancel + vbExclamation, "Conteúdo ausente")
    If an = vbYes Then
        Planilha32.Activate
        Exit Sub
    End If
    If an = vbCancel Then
    Exit Sub
    End If
End If
    
If Planilha32.Range("C16").Value = vbNullString Then
an = MsgBox("As capacidades do sistema não foram especificadas, deseja conferir?" _
, vbYesNoCancel + vbExclamation, "Conteúdo ausente")
    If an = vbYes Then
        Planilha32.Activate
        Exit Sub
    End If
    If an = vbCancel Then
    Exit Sub
    End If
End If
    
If Planilha32.Range("H5").Value = vbNullString Then
an = MsgBox("Os volumes dos tanques não foram especificados, deseja conferir?" _
, vbYesNoCancel + vbExclamation, "Conteúdo ausente")
    If an = vbYes Then
        Planilha32.Activate
        Exit Sub
    End If
    If an = vbCancel Then
    Exit Sub
    End If
End If

If Planilha3.Range("B566").Value = "Yes" Then
an = MsgBox("A disposição de tanques fornecida não foi cadastrada, um template será adicionado e deve ser modificado manualmente." & _
vbNewLine & "Caso deseja revisar o preenchimento aperte 'Cancelar'.", vbOKCancel + vbExclamation, "Disposição não cadastrada")
    If an = vbCancel Then
        Planilha29.Activate
        Exit Sub
    End If
End If

Call cip.Manual

End Sub

'Callback for GIHM1 onAction
Sub GIMH5(control As IRibbonControl)

Dim ans As Integer

Info.Show

Do Until Info.Visible = False
DoEvents
Loop

Dim an As Integer

If Planilha33.Range("D4:D9").Cells.Count = WorksheetFunction.CountBlank(Planilha33.Range("D4:D9")) Then
an = MsgBox("O manual de atualização de IHM apresenta o capítulo de operação por completo, assim é necessário o preenchimento dos componentes elétricos" _
& vbNewLine & vbNewLine & "Deseja preencher agora?", vbYesNoCancel + vbExclamation, "Conteúdo ausente")
    If an = vbYes Then
        Planilha33.Activate
        Exit Sub
    End If
    If an = vbCancel Then
    Exit Sub
    End If
End If


Planilha3.Range("534").Value = "Yes"


Call cip.Manual

End Sub

'Callback for Mec6 onAction
Sub Mec6(control As IRibbonControl)

Planilha35.Activate

End Sub

'Callback for El6 onAction
Sub El6(control As IRibbonControl)

Planilha37.Activate

End Sub

'Callback for IHM6 onAction
Sub IHM6(control As IRibbonControl)

MsgBox "No momento apenas Clearline está registrada no banco de dados." & vbNewLine & _
"Caso outra IHM seja utilizada, favor entrar em contato com o responsável pela área de documentação.", _
vbOKOnly + vbExclamation, "Seleção não possível"

End Sub

'Callback for Ex6 onAction
Sub Ex6(control As IRibbonControl)

Planilha2.Cells(20, 2).Value = Planilha2.Cells(20, 1).Value


Planilha2.Cells(20, 1).Value = "CIP" 'Could be CMX, but both share exact same list


Exceções.Show

End Sub

'Callback for Ger6 onAction
Sub Ger6(control As IRibbonControl)

Planilha3.Range("B650").Value = "No"

Dim ans As Integer

Info.Show

Do Until Info.Visible = False
DoEvents
Loop

If Planilha35.Range("E4:E22").Cells.Count = WorksheetFunction.CountBlank(Planilha35.Range("E4:E22")) Then
an = MsgBox("A estrutura do sistema não foi especificada, deseja conferir?" _
, vbYesNoCancel + vbExclamation, "Conteúdo ausente")
    If an = vbYes Then
        Planilha35.Activate
        Exit Sub
    End If
    If an = vbCancel Then
    Exit Sub
    End If
End If

If Planilha36.Range("C5").Value = vbNullString Then
an = MsgBox("As dimensões do sistema não foram especificadas, deseja conferir?" _
, vbYesNoCancel + vbExclamation, "Conteúdo ausente")
    If an = vbYes Then
        Planilha36.Activate
        Exit Sub
    End If
    If an = vbCancel Then
    Exit Sub
    End If
End If
    
If Planilha36.Range("G11").Value = vbNullString Then
an = MsgBox("O peso aproximado não foi especificado, deseja conferir?" _
, vbYesNoCancel + vbExclamation, "Conteúdo ausente")
    If an = vbYes Then
        Planilha36.Activate
        Exit Sub
    End If
    If an = vbCancel Then
    Exit Sub
    End If
End If
    
If Planilha36.Range("C11").Value = vbNullString Then
an = MsgBox("As capacidades do sistema não foram especificadas, deseja conferir?" _
, vbYesNoCancel + vbExclamation, "Conteúdo ausente")
    If an = vbYes Then
        Planilha36.Activate
        Exit Sub
    End If
    If an = vbCancel Then
    Exit Sub
    End If
End If
    
If Planilha36.Range("H5").Value = vbNullString Then
an = MsgBox("Os volumes dos tanques não foram especificados, deseja conferir?" _
, vbYesNoCancel + vbExclamation, "Conteúdo ausente")
    If an = vbYes Then
        Planilha36.Activate
        Exit Sub
    End If
    If an = vbCancel Then
    Exit Sub
    End If
End If

If Planilha37.Range("D4:D9").Cells.Count = WorksheetFunction.CountBlank(Planilha37.Range("D4:D9")) Then
an = MsgBox("Os componentes elétricos não foram selecionados, deseja conferir?" _
, vbYesNoCancel + vbExclamation, "Conteúdo ausente")
    If an = vbYes Then
        Planilha37.Activate
        Exit Sub
    End If
    If an = vbCancel Then
    Exit Sub
    End If
End If

Call cmx.Manual

End Sub

'Callback for GIHM1 onAction
Sub GIMH6(control As IRibbonControl)

Dim ans As Integer

Info.Show

Do Until Info.Visible = False
DoEvents
Loop

Dim an As Integer

If Planilha37.Range("D4:D9").Cells.Count = WorksheetFunction.CountBlank(Planilha37.Range("D4:D9")) Then
an = MsgBox("O manual de atualização de IHM apresenta o capítulo de operação por completo, assim é necessário o preenchimento dos componentes elétricos" _
& vbNewLine & vbNewLine & "Deseja preencher agora?", vbYesNoCancel + vbExclamation, "Conteúdo ausente")
    If an = vbYes Then
        Planilha37.Activate
        Exit Sub
    End If
    If an = vbCancel Then
    Exit Sub
    End If
End If


Planilha3.Range("650").Value = "Yes"


Call cmx.Manual

End Sub

'Callback for Mec7 onAction
Sub Mec7(control As IRibbonControl)

Planilha38.Activate

End Sub

'Callback for El7 onAction
Sub El7(control As IRibbonControl)

Planilha41.Activate

End Sub

'Callback for IHM7 onAction
Sub IHM7(control As IRibbonControl)

Planilha42.Activate

End Sub

'Callback for Ex7 onAction
Sub Ex7(control As IRibbonControl)

Planilha2.Cells(20, 2).Value = Planilha2.Cells(20, 1).Value


Planilha2.Cells(20, 1).Value = "CIP" 'Could be CMX, but both share exact same list


Exceções.Show

End Sub

'Callback for Ger7 onAction
Sub Ger7(control As IRibbonControl)

Planilha3.Range("B730").Value = "No"

Dim ans As Integer

Info.Show

Do Until Info.Visible = False
DoEvents
Loop

If Planilha38.Range("E4:E11").Cells.Count = WorksheetFunction.CountBlank(Planilha38.Range("E4:E11")) Then
an = MsgBox("A estrutura do sistema não foi especificada, deseja conferir?" _
, vbYesNoCancel + vbExclamation, "Conteúdo ausente")
    If an = vbYes Then
        Planilha38.Activate
        Exit Sub
    End If
    If an = vbCancel Then
    Exit Sub
    End If
End If

If Planilha39.Range("E4:E21").Cells.Count = WorksheetFunction.CountBlank(Planilha39.Range("E4:E21")) Then
an = MsgBox("A estrutura do sistema não foi especificada, deseja conferir?" _
, vbYesNoCancel + vbExclamation, "Conteúdo ausente")
    If an = vbYes Then
        Planilha39.Activate
        Exit Sub
    End If
    If an = vbCancel Then
    Exit Sub
    End If
End If

If Planilha40.Range("C5").Value = vbNullString Then
an = MsgBox("As dimensões do sistema não foram especificadas, deseja conferir?" _
, vbYesNoCancel + vbExclamation, "Conteúdo ausente")
    If an = vbYes Then
        Planilha40.Activate
        Exit Sub
    End If
    If an = vbCancel Then
    Exit Sub
    End If
End If
    
If Planilha40.Range("G5").Value = vbNullString Then
an = MsgBox("Os pesos aproximado não foram especificados, deseja conferir?" _
, vbYesNoCancel + vbExclamation, "Conteúdo ausente")
    If an = vbYes Then
        Planilha40.Activate
        Exit Sub
    End If
    If an = vbCancel Then
    Exit Sub
    End If
End If
    
If Planilha40.Range("C11").Value = vbNullString Then
an = MsgBox("As capacidades do sistema não foram especificadas, deseja conferir?" _
, vbYesNoCancel + vbExclamation, "Conteúdo ausente")
    If an = vbYes Then
        Planilha40.Activate
        Exit Sub
    End If
    If an = vbCancel Then
    Exit Sub
    End If
End If
    
If Planilha40.Range("H10").Value = vbNullString Then
an = MsgBox("Os volumes dos tanques não foram especificados, deseja conferir?" _
, vbYesNoCancel + vbExclamation, "Conteúdo ausente")
    If an = vbYes Then
        Planilha40.Activate
        Exit Sub
    End If
    If an = vbCancel Then
    Exit Sub
    End If
End If

If Planilha41.Range("D4:D10").Cells.Count = WorksheetFunction.CountBlank(Planilha41.Range("D4:D10")) Then
an = MsgBox("Os componentes elétricos não foram selecionados, deseja conferir?" _
, vbYesNoCancel + vbExclamation, "Conteúdo ausente")
    If an = vbYes Then
        Planilha41.Activate
        Exit Sub
    End If
    If an = vbCancel Then
    Exit Sub
    End If
End If

If Planilha42.Range("D2").Value = "Não escolhido" Then
an = MsgBox("A IHM não foi selecionado, deseja conferir?" _
, vbYesNoCancel + vbExclamation, "Conteúdo ausente")
    If an = vbYes Then
        Planilha42.Activate
        Exit Sub
    End If
    If an = vbCancel Then
    Exit Sub
    End If
End If

Call ccmx.Manual

End Sub

'Callback for GIHM1 onAction
Sub GIMH7(control As IRibbonControl)

Dim ans As Integer

Info.Show

Do Until Info.Visible = False
DoEvents
Loop

Dim an As Integer

If Planilha41.Range("D4:D10").Cells.Count = WorksheetFunction.CountBlank(Planilha41.Range("D4:D10")) Then
an = MsgBox("O manual de atualização de IHM apresenta o capítulo de operação por completo, assim é necessário o preenchimento dos componentes elétricos" _
& vbNewLine & vbNewLine & "Deseja preencher agora?", vbYesNoCancel + vbExclamation, "Conteúdo ausente")
    If an = vbYes Then
        Planilha41.Activate
        Exit Sub
    End If
    If an = vbCancel Then
    Exit Sub
    End If
End If

Planilha3.Range("730").Value = "Yes"


Call ccmx.Manual

End Sub
