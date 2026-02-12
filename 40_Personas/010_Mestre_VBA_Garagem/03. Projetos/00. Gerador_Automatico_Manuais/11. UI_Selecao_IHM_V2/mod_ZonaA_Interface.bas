Attribute VB_Name = "mod_ZonaA_Interface"
Option Explicit

' ==============================================================================
' MÓDULO: mod_ZonaA_Interface
' DESCRIÇÃO: Implementação da Zona A (Sidebar de Filtros + Lista de Cards).
'            Foco exclusivo na seleção de modelos de IHM.
' ==============================================================================

' --- CONFIGURAÇÕES DE LAYOUT ---
Private Const ROW_START As Integer = 5           ' Início do conteúdo após o cabeçalho
Private Const COL_FILTERS As Integer = 1         ' Coluna A
Private Const COL_CARDS As Integer = 2           ' Início em B (B:C)
Private Const CARD_WIDTH As Double = 230         ' Largura visual ocupando B e parte de C
Private Const CARD_HEIGHT As Double = 50
Private Const FILTER_SIZE As Double = 40         ' Tamanho do botão quadrado de filtro

' --- CORES ---
Private Const COL_KHS_ORANGE As Long = 49407     ' Laranja destaque
Private Const COL_BG_ACTIVE As Long = 14277081   ' Azulado/Cinza Ativo
Private Const COL_BG_INACTIVE As Long = 15921906 ' Cinza Desativado
Private Const COL_TEXT_DARK As Long = 4210752    ' Cinza Escuro

' ==============================================================================
' 1. SETUP INICIAL DA PLANILHA
' ==============================================================================
Public Sub Setup_ZonaA_Demo()
    Dim ws As Worksheet
    Set ws = ActiveSheet
    
    Application.ScreenUpdating = False
    
    ' Limpa Shapes existentes na Zona A
    Dim s As Shape
    For Each s In ws.Shapes
        If s.Left < ws.Columns("D").Left Then s.Delete
    Next s
    
    ' Configuração de Colunas
    ws.Columns("A").ColumnWidth = 8   ' Sidebar
    ws.Columns("B:C").ColumnWidth = 18 ' Espaço para os Cards
    ws.Columns("D").ColumnWidth = 2    ' Separador
    
    ' Cabeçalho Global (Linhas 1-3)
    With ws.Range("A1:C3")
        .Merge
        .Interior.Color = COL_TEXT_DARK
        .Value = " SELETOR IHM"
        .Font.Color = vbWhite
        .Font.Bold = True
        .Font.Size = 14
        .VerticalAlignment = xlCenter
    End With
    
    ' Linha 4 (Espaçador/Instrução)
    ws.Range("A4:C4").Value = "Filtros | Modelos"
    ws.Range("A4:C4").Font.Size = 8
    ws.Range("A4:C4").Font.Italic = True
    
    ' Renderização Inicial
    Render_Filters True, True, True
    Render_Cards True, True, True
    
    Application.ScreenUpdating = True
End Sub

' ==============================================================================
' 2. RENDERIZADOR DE FILTROS (ZONA A1)
' ==============================================================================
Private Sub Render_Filters(k As Boolean, s As Boolean, r As Boolean)
    Dim topPos As Double
    topPos = ActiveSheet.Cells(ROW_START, COL_FILTERS).Top
    
    ' Botão KHS
    Create_Filter_Toggle "btn_f_khs", "KHS", topPos, k
    
    ' Botão Siemens
    topPos = topPos + FILTER_SIZE + 10
    Create_Filter_Toggle "btn_f_sie", "SIE", topPos, s
    
    ' Botão Rockwell
    topPos = topPos + FILTER_SIZE + 10
    Create_Filter_Toggle "btn_f_roc", "ROC", topPos, r
End Sub

Private Sub Create_Filter_Toggle(id As String, label As String, topPos As Double, isActive As Boolean)
    Dim s As Shape
    Set s = ActiveSheet.Shapes.AddShape(msoShapeRoundedRectangle, 5, topPos, 45, FILTER_SIZE)
    With s
        .Name = id
        .TextFrame.Characters.Text = label
        .TextFrame.Characters.Font.Size = 8
        .TextFrame.Characters.Font.Bold = True
        .TextFrame.Characters.Font.Color = IIf(isActive, vbWhite, COL_TEXT_DARK)
        .OnAction = "'Toggle_Filter """ & id & """'"
        
        If isActive Then
            .Fill.ForeColor.RGB = COL_KHS_ORANGE
            .Line.Weight = 2
        Else
            .Fill.ForeColor.RGB = COL_BG_INACTIVE
            .Line.Weight = 1
            .Fill.Transparency = 0.3
        End If
    End With
End Sub

' ==============================================================================
' 3. RENDERIZADOR DE CARDS (ZONA A2)
' ==============================================================================
Private Sub Render_Cards(ShowKHS As Boolean, ShowSiemens As Boolean, ShowRockwell As Boolean)
    Dim ws As Worksheet
    Dim topPos As Double
    Dim s As Shape
    
    Set ws = ActiveSheet
    topPos = ws.Cells(ROW_START, COL_CARDS).Top
    
    ' Limpa apenas Cards e Títulos de Grupo
    For Each s In ws.Shapes
        If s.Name Like "card_*" Or s.Name Like "grp_*" Then s.Delete
    Next s
    
    ' --- LISTAGEM DINÂMICA ---
    
    ' Seção KHS
    If ShowKHS Then
        topPos = Add_Group_Title("KHS CLEARLINE", topPos)
        topPos = Add_IHM_Card("khs_30", "Clearline 3.0", "21.5'' Panel", topPos)
        topPos = Add_IHM_Card("khs_20", "Clearline 2.0", "21.5'' Panel", topPos)
        topPos = Add_IHM_Card("khs_10", "Clearline 1.0", "15'' Panel", topPos)
    End If
    
    ' Seção Siemens
    If ShowSiemens Then
        topPos = Add_Group_Title("SIEMENS", topPos + 5)
        topPos = Add_IHM_Card("sie_tp", "TP Comfort", "High Performance", topPos)
        topPos = Add_IHM_Card("sie_mp", "MP 377", "Legacy Multi", topPos)
    End If
    
    ' Seção Rockwell
    If ShowRockwell Then
        topPos = Add_Group_Title("ROCKWELL / AB", topPos + 5)
        topPos = Add_IHM_Card("roc_pv", "PV 1500", "PanelView Plus", topPos)
    End If
    
End Sub

Private Function Add_IHM_Card(id As String, title As String, info As String, topPos As Double) As Double
    Dim ws As Worksheet: Set ws = ActiveSheet
    Dim shp As Shape
    Dim leftPos As Double: leftPos = ws.Cells(1, COL_CARDS).Left
    
    ' Shape do Card
    Set shp = ws.Shapes.AddShape(msoShapeRectangle, leftPos, topPos, CARD_WIDTH, CARD_HEIGHT)
    With shp
        .Name = "card_bg_" & id
        .Fill.ForeColor.RGB = vbWhite
        .Line.ForeColor.RGB = 12632256
        .TextFrame.Characters.Text = title & vbNewLine & info
        .TextFrame.Characters.Font.Color = COL_TEXT_DARK
        .TextFrame.Characters.Font.Size = 10
        .TextFrame.MarginLeft = 10
        .OnAction = "'On_Card_Select """ & id & """'"
    End With
    
    Add_IHM_Card = topPos + CARD_HEIGHT + 5
End Function

Private Function Add_Group_Title(txt As String, topPos As Double) As Double
    Dim s As Shape
    Set s = ActiveSheet.Shapes.AddTextbox(msoTextOrientationHorizontal, ActiveSheet.Cells(1, COL_CARDS).Left, topPos, CARD_WIDTH, 15)
    With s
        .Name = "grp_lbl_" & Replace(txt, " ", "_")
        .TextFrame.Characters.Text = txt
        .TextFrame.Characters.Font.Size = 7
        .TextFrame.Characters.Font.Bold = True
        .TextFrame.Characters.Font.Color.RGB = 8421504
        .Fill.Transparency = 1
        .Line.Visible = msoFalse
    End With
    Add_Group_Title = topPos + 15
End Function

' ==============================================================================
' 4. LÓGICA DE EVENTOS
' ==============================================================================

Public Sub Toggle_Filter(btnID As String)
    Dim ws As Worksheet: Set ws = ActiveSheet
    Dim s As Shape: Set s = ws.Shapes(btnID)
    
    ' Inverte estado visual (Simplificado: checa cor)
    If s.Fill.ForeColor.RGB = COL_KHS_ORANGE Then
        s.Fill.ForeColor.RGB = COL_BG_INACTIVE
        s.TextFrame.Characters.Font.Color = COL_TEXT_DARK
    Else
        s.Fill.ForeColor.RGB = COL_KHS_ORANGE
        s.TextFrame.Characters.Font.Color = vbWhite
    End If
    
    ' Lê todos os estados e atualiza a lista
    Dim k As Boolean, si As Boolean, r As Boolean
    k = (ws.Shapes("btn_f_khs").Fill.ForeColor.RGB = COL_KHS_ORANGE)
    si = (ws.Shapes("btn_f_sie").Fill.ForeColor.RGB = COL_KHS_ORANGE)
    r = (ws.Shapes("btn_f_roc").Fill.ForeColor.RGB = COL_KHS_ORANGE)
    
    Render_Cards k, si, r
End Sub

Public Sub On_Card_Select(id As String)
    ' Feedback simples
    Dim s As Shape
    For Each s In ActiveSheet.Shapes
        If s.Name Like "card_bg_*" Then s.Line.ForeColor.RGB = 12632256: s.Line.Weight = 1
    Next s
    
    With ActiveSheet.Shapes("card_bg_" & id)
        .Line.ForeColor.RGB = COL_KHS_ORANGE
        .Line.Weight = 3
    End With
End Sub
