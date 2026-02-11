# mod_UI_ZoneA

> Codigo VBA atual -- convertido automaticamente de `mod_UI_ZoneA.bas`

```vba
Attribute VB_Name = "mod_UI_ZoneA"
Option Explicit

' ==============================================================================
' ARQUITETURA DE UI - ZONA A (GALERIA & NAVEGA��O)
' Vers�o: 4.1 (Est�vel - Assets Reais)
' Depend�ncias: mod_Shared_Definitions, mod_UI_ZoneB
' ==============================================================================

' --- GEOMETRIA ---
Private Const COL_SIDEBAR As String = "A"
Private Const ROW_START_UI As Integer = 5
Private Const BTN_HEIGHT_CELLS As Integer = 2
Private Const CARD_HEIGHT_CELLS As Integer = 4

' --- DADOS LOCAIS ---
Private Catalog() As T_Card_Master
Private CatalogCount As Integer
Private IsCatalogLoaded As Boolean

' --- ESTADO DOS FILTROS ---
Public Filter_Clearline As Boolean
Public Filter_Siemens As Boolean
Public Filter_Rockwell As Boolean

' ==============================================================================
' 1. MAIN SETUP
' ==============================================================================
Public Sub Init_UI()
    Dim ws As Worksheet
    Set ws = ActiveSheet
    
    Application.ScreenUpdating = False
    
    Load_Catalog_From_DB
    
    On Error Resume Next
    ws.DrawingObjects.Delete
    On Error GoTo 0
    
    With ws.Cells
        .Interior.color = xlNone
        .ClearContents
        .Borders.LineStyle = xlNone
    End With
    ws.Rows.RowHeight = 15
    
    ' --- CONFIGURA��O DE COLUNAS ---
    ws.Columns("A").ColumnWidth = 25
    ws.Columns("B").ColumnWidth = 2
    ws.Columns("C:E").ColumnWidth = 22
    ws.Columns("F").ColumnWidth = 2
    ws.Columns("G:H").ColumnWidth = 15
    ws.Columns("I").ColumnWidth = 2
    ws.Columns("J:L").ColumnWidth = 15
    ws.Columns("M").ColumnWidth = 2
    ws.Columns("N:P").ColumnWidth = 15
    
    ' --- PINTURA DA ESTRUTURA ---
    Dim lastRowVisible As Long
    lastRowVisible = 100
    
    ws.Range("A5:A" & lastRowVisible).Interior.color = CLR_SIDEBAR_BG
    ws.Range("B4:B" & lastRowVisible).Interior.color = CLR_HEADER_BG
    ws.Range("F4:F" & lastRowVisible).Interior.color = CLR_HEADER_BG
    ws.Range("I4:I" & lastRowVisible).Interior.color = CLR_HEADER_BG
    ws.Range("M4:M" & lastRowVisible).Interior.color = CLR_HEADER_BG
    
    ws.Range("C5:E" & lastRowVisible).Interior.color = CLR_ZONE_BG
    ws.Range("G5:H" & lastRowVisible).Interior.color = CLR_ZONE_BG
    ws.Range("J5:L" & lastRowVisible).Interior.color = CLR_ZONE_BG
    ws.Range("N5:P" & lastRowVisible).Interior.color = CLR_ZONE_BG
    
    With ws.Range("A4:P4")
        .Interior.color = CLR_HEADER_BG
        .Font.color = CLR_TEXT_WHITE
        .Font.Bold = True
        .Font.name = "Segoe UI"
        .Font.Size = 9
        .VerticalAlignment = xlCenter
    End With
    
    ' --- T�TULOS ---
    ws.Cells(4, 1).Value = "FILTROS"
    ws.Cells(4, 1).HorizontalAlignment = xlCenter
    
    With ws.Range("C4:E4")
        .HorizontalAlignment = xlCenterAcrossSelection
        ws.Cells(4, 3).Value = "CAT�LOGO DE MODELOS"
    End With
    
    With ws.Range("G4:H4")
        .HorizontalAlignment = xlCenterAcrossSelection
        ws.Cells(4, 7).Value = "DETALHES"
    End With
    
    With ws.Range("J4:L4")
        .HorizontalAlignment = xlCenterAcrossSelection
        ws.Cells(4, 10).Value = "ESTRUTURA"
    End With
    
    With ws.Range("N4:P4")
        .HorizontalAlignment = xlCenterAcrossSelection
        ws.Cells(4, 14).Value = "INPUT & A��O"
    End With
    
    ' --- INITIALIZE ---
    If Not Filter_Clearline And Not Filter_Siemens And Not Filter_Rockwell Then
        Filter_Clearline = True: Filter_Siemens = True: Filter_Rockwell = True
    End If
    
    Render_Sidebar
    Render_Gallery_Matrix
    
    ws.Range("A1").Select
    Application.ScreenUpdating = True
End Sub

' ==============================================================================
' 2. DATA LOADER
' ==============================================================================
Private Sub Load_Catalog_From_DB()
    Dim wsDB As Worksheet, lastRow As Long, i As Long
    On Error Resume Next
    Set wsDB = Planilha66
    If wsDB Is Nothing Then Set wsDB = ThisWorkbook.Sheets("ihm_models")
    On Error GoTo 0
    
    If wsDB Is Nothing Then
        CatalogCount = 3
        ReDim Catalog(1 To 3)
        With Catalog(1)
            .id = 1: .Fabricante = "Clearline": .Modelo = "CL 3.0"
            .Status = "Ativo": .Engine = "Zenon": .Descricao = "Interface padr�o KHS."
            .imgPath = "assets\thumbs\cl30.png"
        End With
        With Catalog(2)
            .id = 2: .Fabricante = "Siemens": .Modelo = "TP Comfort"
            .Status = "Ativo": .Engine = "WinCC TIA": .Descricao = "Pain�is Siemens TIA Portal."
            .imgPath = "assets\thumbs\sie_tp.png"
        End With
        With Catalog(3)
            .id = 3: .Fabricante = "Rockwell": .Modelo = "PV Plus"
            .Status = "Legado": .Engine = "FTView": .Descricao = "Pain�is Allen-Bradley antigos."
            .imgPath = "assets\thumbs\roc_pv.png"
        End With
        IsCatalogLoaded = True
        Exit Sub
    End If
    
    lastRow = wsDB.Cells(wsDB.Rows.count, 1).End(xlUp).Row
    If lastRow < 2 Then Exit Sub
    
    CatalogCount = lastRow - 1
    ReDim Catalog(1 To CatalogCount)
    
    For i = 2 To lastRow
        With Catalog(i - 1)
            .id = wsDB.Cells(i, 1).Value
            .Fabricante = wsDB.Cells(i, 3).Value
            .Modelo = wsDB.Cells(i, 4).Value
            .Tamanho = wsDB.Cells(i, 5).Value
            .Engine = wsDB.Cells(i, 6).Value
            .Status = wsDB.Cells(i, 7).Value
            .imgPath = wsDB.Cells(i, 8).Value
            .Descricao = wsDB.Cells(i, 9).Value
        End With
    Next i
    IsCatalogLoaded = True
End Sub

' ==============================================================================
' 3. SIDEBAR RENDERER
' ==============================================================================
Private Sub Render_Sidebar()
    Dim ws As Worksheet: Set ws = ActiveSheet
    Dim currRow As Integer
    Dim s As shape
    
    For Each s In ws.Shapes
        If s.name Like "btn_filter_*" Then
            s.Delete
        End If
    Next s
    
    currRow = ROW_START_UI
    
    Draw_Flat_Btn "btn_filter_khs", "CLEARLINE", currRow, Filter_Clearline
    currRow = currRow + BTN_HEIGHT_CELLS
    
    Draw_Flat_Btn "btn_filter_sie", "SIEMENS", currRow, Filter_Siemens
    currRow = currRow + BTN_HEIGHT_CELLS
    
    Draw_Flat_Btn "btn_filter_roc", "ROCKWELL", currRow, Filter_Rockwell
End Sub

Private Sub Draw_Flat_Btn(id As String, label As String, startRow As Integer, isOn As Boolean)
    Dim ws As Worksheet: Set ws = ActiveSheet
    Dim rng As Range, btn As shape
    
    Set rng = ws.Range(ws.Cells(startRow, 1), ws.Cells(startRow + BTN_HEIGHT_CELLS - 1, 1))
    
    Set btn = ws.Shapes.AddShape(msoShapeRoundedRectangle, _
        rng.Left + 2, rng.top + 2, rng.Width - 4, rng.Height - 4)
        
    With btn
        .name = id
        .TextFrame.Characters.Text = label
        .TextFrame.Characters.Font.Bold = True
        .TextFrame.Characters.Font.Size = 9
        .TextFrame.Characters.Font.name = "Segoe UI"
        .Line.Visible = msoFalse
        .OnAction = "Toggle_Filter_Handler"
        .ThreeD.BevelTopType = msoBevelNone
        .Shadow.Visible = msoFalse
        
        With .Fill
            .Solid
            If isOn Then
                .ForeColor.RGB = CLR_BTN_ACTIVE
            Else
                .ForeColor.RGB = CLR_BTN_INACTIVE
            End If
        End With
        
        If isOn Then
            .TextFrame.Characters.Font.color = CLR_TEXT_WHITE
            .Shadow.Type = msoShadow25
            .Shadow.Blur = 3
            .Shadow.Visible = msoTrue
        Else
            .TextFrame.Characters.Font.color = CLR_TEXT_DARK
        End If
    End With
End Sub

' ==============================================================================
' 4. GALLERY RENDERER
' ==============================================================================
Public Sub Render_Gallery_Matrix()
    Dim ws As Worksheet: Set ws = ActiveSheet
    Dim i As Integer, counter As Integer
    Dim targetCol As Integer, targetRow As Integer, showItem As Boolean
    Dim s As shape
    
    If Not IsCatalogLoaded Then Load_Catalog_From_DB
    
    For Each s In ws.Shapes
        If s.name Like "grp_card_*" Then
            s.Delete
        End If
    Next s
    
    counter = 0
    targetRow = ROW_START_UI
    
    For i = 1 To CatalogCount
        showItem = False
        Select Case UCase(Catalog(i).Fabricante)
            Case "CLEARLINE": If Filter_Clearline Then showItem = True
            Case "SIEMENS":   If Filter_Siemens Then showItem = True
            Case "ROCKWELL":  If Filter_Rockwell Then showItem = True
        End Select
        
        If showItem Then
            targetCol = 3 + (counter Mod 3)
            If counter > 0 And (counter Mod 3) = 0 Then
                targetRow = targetRow + CARD_HEIGHT_CELLS
            End If
            
            Draw_Card_Matrix Catalog(i), targetRow, targetCol
            counter = counter + 1
        End If
    Next i
End Sub

Private Sub Draw_Card_Matrix(data As T_Card_Master, rowIdx As Integer, colIdx As Integer)
    Dim ws As Worksheet: Set ws = ActiveSheet
    Dim rng As Range, bg As shape, img As shape, txt As shape
    Dim shpNames() As String: Dim shpCount As Integer: shpCount = 0
    Dim margin As Double: margin = 4
    
    Set rng = ws.Range(ws.Cells(rowIdx, colIdx), ws.Cells(rowIdx + CARD_HEIGHT_CELLS - 1, colIdx))
    
    ' Fundo Card
    Set bg = ws.Shapes.AddShape(msoShapeRoundedRectangle, _
        rng.Left + margin, rng.top + margin, rng.Width - (margin * 2), rng.Height - (margin * 2))
    bg.name = "tmp_bg_" & data.id
    bg.Fill.Solid
    bg.Fill.ForeColor.RGB = CLR_CARD_BG
    bg.Line.Visible = msoFalse
    bg.ThreeD.BevelTopType = msoBevelNone
    bg.Shadow.Type = msoShadow25
    bg.Shadow.Blur = 4
    bg.Shadow.Transparency = 0.7
    AddShapeToArray bg.name, shpNames, shpCount
    
    ' --- IMAGEM DA IHM (Din�mica Real) ---
    Dim imgPath As String
    Dim hasImg As Boolean
    
    If data.imgPath <> "" Then
        imgPath = ThisWorkbook.path & "\" & data.imgPath
        If Dir(imgPath) <> "" Then hasImg = True
    End If
    
    On Error Resume Next
    If hasImg Then
        Set img = ws.Shapes.AddPicture(imgPath, msoFalse, msoTrue, bg.Left + 5, bg.top + 5, 40, 40)
    Else
        Set img = ws.Shapes.AddShape(msoShapeRectangle, bg.Left + 5, bg.top + 5, 40, 40)
        img.Fill.ForeColor.RGB = RGB(220, 220, 220)
        img.Line.ForeColor.RGB = RGB(180, 180, 180)
    End If
    On Error GoTo 0
    
    img.name = "tmp_img_" & data.id
    img.LockAspectRatio = msoTrue
    AddShapeToArray img.name, shpNames, shpCount
    
    ' T�tulo
    Set txt = ws.Shapes.AddTextbox(msoTextOrientationHorizontal, bg.Left + 50, bg.top + 2, bg.Width - 52, 32)
    With txt.TextFrame
        .Characters.Text = data.Modelo
        .Characters.Font.Bold = True
        .Characters.Font.Size = 9
        .Characters.Font.name = "Segoe UI"
        .Characters.Font.color = CLR_TEXT_DARK
        .MarginLeft = 0: .MarginRight = 0: .MarginTop = 0: .MarginBottom = 0
    End With
    txt.Fill.Visible = msoFalse: txt.Line.Visible = msoFalse
    txt.name = "tmp_txt_" & data.id
    AddShapeToArray txt.name, shpNames, shpCount
    
    ' Badge
    Dim bColor As Long
    Select Case UCase(data.Fabricante)
        Case "SIEMENS": bColor = CLR_BRAND_SIE
        Case "CLEARLINE": bColor = CLR_BRAND_KHS
        Case "ROCKWELL": bColor = CLR_BRAND_ROC
        Case Else: bColor = CLR_TEXT_GREY
    End Select
    
    Dim b1 As shape
    Set b1 = ws.Shapes.AddShape(msoShapeRoundedRectangle, bg.Left + 50, bg.top + 35, 60, 15)
    With b1
        .name = "tmp_b1_" & data.id
        .Fill.Solid
        .Fill.ForeColor.RGB = bColor
        .Line.Visible = msoFalse
        .ThreeD.BevelTopType = msoBevelNone
        .TextFrame.Characters.Text = data.Engine
        .TextFrame.Characters.Font.Size = 7
        .TextFrame.Characters.Font.color = vbWhite
    End With
    AddShapeToArray b1.name, shpNames, shpCount

    ' Agrupar
    Dim grp As shape
    Set grp = ws.Shapes.Range(shpNames).Group
    grp.name = "grp_card_" & data.id
    grp.OnAction = "Card_Click_Handler"
End Sub

' ==============================================================================
' 5. HANDLERS E INTEGRA��O
' ==============================================================================
Public Sub Toggle_Filter_Handler()
    Dim id As String: id = Application.Caller
    Application.ScreenUpdating = False
    
    If id = "btn_filter_khs" Then Filter_Clearline = Not Filter_Clearline
    If id = "btn_filter_sie" Then Filter_Siemens = Not Filter_Siemens
    If id = "btn_filter_roc" Then Filter_Rockwell = Not Filter_Rockwell
    
    Render_Sidebar
    Render_Gallery_Matrix
    Application.ScreenUpdating = True
End Sub

Public Sub Card_Click_Handler()
    Dim cardID As Long
    Dim i As Integer
    Dim selectedData As T_Card_Master
    Dim found As Boolean
    Dim shpName As String
    Dim strID As String
    Dim nameParts() As String
    
    On Error GoTo ErrorHandler
    shpName = Application.Caller
    nameParts = Split(shpName, "_")
    strID = nameParts(UBound(nameParts))
    
    If Not IsNumeric(strID) Then
        MsgBox "Erro Fatal: ID n�o num�rico detectado." & vbCrLf & "Elemento: " & shpName, vbCritical
        Exit Sub
    End If
    
    cardID = CLng(strID)
    If Not IsCatalogLoaded Then Load_Catalog_From_DB
    
    For i = 1 To CatalogCount
        If Catalog(i).id = cardID Then
            selectedData = Catalog(i)
            found = True
            Exit For
        End If
    Next i
    
    If found Then mod_UI_ZoneB.Render_ZoneB selectedData
    Exit Sub

ErrorHandler:
    MsgBox "Erro no Clique: " & Err.Description, vbCritical
End Sub

Private Sub AddShapeToArray(name As String, arr() As String, ByRef count As Integer)
    count = count + 1
    ReDim Preserve arr(1 To count)
    arr(count) = name
End Sub



```
