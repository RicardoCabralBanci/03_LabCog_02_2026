Attribute VB_Name = "mod_Ribbon_V5"
Option Explicit

' ==========================================================================================
' MÓDULO: mod_Ribbon_V5
' DESCRIÇÃO: Centralizador de Callbacks do Ribbon (Híbrido)
' ATUALIZAÇÃO: 13/01/2026 - Inclusão de PLT (ID 8) e PCK (ID 9)
' AUTOR: Mestre em VBA
' ==========================================================================================

' --- CALLBACKS DE NAVEGAÇÃO E SISTEMA (GENÉRICOS) ---

Sub GoSave(control As IRibbonControl)
    On Error Resume Next
    ThisWorkbook.Save
    If Err.Number <> 0 Then MsgBox "Erro ao salvar o arquivo.", vbCritical
End Sub

Sub Inform(control As IRibbonControl)
    On Error Resume Next
    Info.Show ' Chama o UserForm Legado
End Sub

Sub SImagem(control As IRibbonControl)
    ' Chama a lógica legada de imagem se o módulo Imagem existir
    On Error Resume Next
    Call Imagem.PopulateXL
End Sub

Sub STabela(control As IRibbonControl)
    On Error Resume Next
    Call Tabela.PopulateXL
End Sub

Sub Preenchimento(control As IRibbonControl)
    On Error Resume Next
    Exemplos.Show
End Sub

Sub Limp(control As IRibbonControl)
    ' Limpa a aba ativa usando a lógica legada de limpeza
    Application.EnableEvents = False
    Call limpeza(ThisWorkbook.ActiveSheet.Index)
    Application.EnableEvents = True
End Sub

' --- MÁQUINA 7: CCMX (LEGADO/REFERÊNCIA) ---

Sub Mec7(control As IRibbonControl)
    Planilha38.Activate
End Sub

Sub El7(control As IRibbonControl)
    Planilha41.Activate
End Sub

Sub IHM7(control As IRibbonControl)
    Planilha42.Activate
End Sub

Sub Ger7(control As IRibbonControl)
    ' Wrapper para a Engine Híbrida
    Call mod_NewEngine.ExportarParaNovoGerador("CCMX")
End Sub


' --- MÁQUINA 8: PALETIZADOR (NOVO) ---

Sub Mec_PLT(control As IRibbonControl)
    ' Planilha 43 (Clonada do CCMX)
    On Error Resume Next
    Planilha43.Activate
    If Err.Number <> 0 Then MsgBox "Aba PLT Estrutura (Planilha43) não encontrada.", vbExclamation
End Sub

Sub Dados_PLT(control As IRibbonControl)
    On Error Resume Next
    Planilha44.Activate
End Sub

Sub El_PLT(control As IRibbonControl)
    On Error Resume Next
    Planilha45.Activate
End Sub

Sub IHM_PLT(control As IRibbonControl)
    On Error Resume Next
    Planilha46.Activate
End Sub

Sub Gerar_PLT_Click(control As IRibbonControl)
    ' Dispara a Engine Híbrida para PLT
    If MsgBox("Deseja gerar o manual do Paletizador (PLT)?", vbQuestion + vbYesNo) = vbYes Then
        Call mod_NewEngine.ExportarParaNovoGerador("PLT")
    End If
End Sub


' --- MÁQUINA 9: ENCAIXOTADORA (NOVO) ---

Sub Mec_PCK(control As IRibbonControl)
    On Error Resume Next
    Planilha47.Activate
End Sub

Sub Dados_PCK(control As IRibbonControl)
    On Error Resume Next
    Planilha48.Activate
End Sub

Sub El_PCK(control As IRibbonControl)
    On Error Resume Next
    Planilha49.Activate
End Sub

Sub IHM_PCK(control As IRibbonControl)
    On Error Resume Next
    Planilha50.Activate
End Sub

Sub Gerar_PCK_Click(control As IRibbonControl)
    If MsgBox("Deseja gerar o manual da Encaixotadora (PCK)?", vbQuestion + vbYesNo) = vbYes Then
        Call mod_NewEngine.ExportarParaNovoGerador("PCK")
    End If
End Sub


' --- ADAPTAÇÃO DA SUB LIMPEZA (LEGADO) ---
' Cole este bloco dentro do módulo legado ou substitua se necessário

Sub limpeza(ByRef i As Integer, Optional byDummy As Byte)
    Application.ScreenUpdating = False
    On Error Resume Next
    With ThisWorkbook.Sheets(i)
        .Unprotect vbNullString
        Select Case i
            ' Casos Legados (Preservados)
            Case 4, 7 To 10, 15 To 18, 29
                .Range("B4:H100").ClearContents
            Case 5, 6, 11, 13, 14, 19, 24, 28, 30, 33, 37, 41
                .Range("D4:D100").ClearContents
            
            ' CASO NOVO: CCMX, PLT e PCK (Slots 38 a 52)
            ' Seguindo o padrão do CCMX (Coluna E para seleções)
            Case 38, 39, 43, 44, 47, 48
                 .Range("E4:E100").ClearContents
            
            ' IHM e Elétrica (Coluna D)
            Case 41, 42, 45, 46, 49, 50
                 .Range("D4:D100").ClearContents
        End Select
        .Protect vbNullString
    End With
    Application.EnableEvents = True: Application.ScreenUpdating = True
End Sub
