# mod_UI_ZoneB

> Codigo VBA atual -- convertido automaticamente de `mod_UI_ZoneB.bas`

```vba
Attribute VB_Name = "mod_UI_ZoneB"
Option Explicit

' ==============================================================================
' RENDERIZADOR DA ZONA B (DETALHES & DOCUMENTOS)
' Vers�o: 1.3 (Skeleton Fallback & Type Safety)
' Depend�ncias: mod_Shared_Definitions, mod_UI_Core
' ==============================================================================

' Estrutura de Dados Interna
Private Type T_Doc_Item
    mapID As Long           ' ID �nico do mapeamento (0 se for Mock)
    Capitulo As String
    NomeArquivo As String
    PathCompleto As String
    Existe As Boolean
End Type

' Constantes Visuais
Private Const ICO_SIZE As Double = 16
Private Const CLR_BLOCKED As Long = 10526880 ' RGB(160,160,160) - Cinza

' ==============================================================================
' 1. MAIN ENTRY POINT
' ==============================================================================
Public Sub Render_ZoneB(selectedIHM As T_Card_Master)
    Dim ws As Worksheet
    Set ws = ActiveSheet
    
    Application.ScreenUpdating = False
    Clear_ZoneB ws
    Render_Hardware_Panel ws, selectedIHM
    Render_Doc_List ws, selectedIHM
    Application.ScreenUpdating = True
End Sub

Private Sub Clear_ZoneB(ws As Worksheet)
    Dim s As shape
    For Each s In ws.Shapes
        If s.name Like "zB_*" Then s.Delete
    Next s
    
    With ws.Range("G5:H30")
        .ClearContents
        .Interior.color = CLR_ZONE_BG
    End With
    ' Limpa J:L (�rea da Lista)
    With ws.Range("J5:L30")
        .ClearContents
        .Interior.color = CLR_ZONE_BG
    End With
End Sub

' ==============================================================================
' 2. PAINEL DE HARDWARE (ESQUERDA)
' ==============================================================================
Private Sub Render_Hardware_Panel(ws As Worksheet, data As T_Card_Master)
    Dim rngImg As Range
    Set rngImg = ws.Range("G5:H15")
    
    ' A. Imagem Ampliada (Din�mica)
    Dim imgPath As String
    Dim hasImg As Boolean
    
    If data.imgPath <> "" Then
        imgPath = ThisWorkbook.path & "\" & data.imgPath
        If Dir(imgPath) <> "" Then hasImg = True
    End If
    
    Dim shp As shape
    On Error Resume Next
    If hasImg Then
        Set shp = ws.Shapes.AddPicture(imgPath, msoFalse, msoTrue, _
                  rngImg.Left + 5, rngImg.top + 5, rngImg.Width - 10, rngImg.Height - 10)
    Else
        Set shp = ws.Shapes.AddShape(msoShapeRectangle, _
                  rngImg.Left + 5, rngImg.top + 5, rngImg.Width - 10, rngImg.Height - 10)
        shp.Fill.ForeColor.RGB = RGB(220, 220, 220)
    End If
    On Error GoTo 0
    
    If Not shp Is Nothing Then
        shp.name = "zB_BigThumb"
        shp.LockAspectRatio = msoTrue
        shp.Line.Visible = msoTrue
        shp.Line.ForeColor.RGB = CLR_TEXT_GREY
        shp.Line.Weight = 1
    End If
    
    ' B. Textos Descritivos
    With ws.Cells(16, 7)
        .Value = UCase(data.Modelo) & " (" & data.Engine & ")"
        .Font.name = "Segoe UI": .Font.Bold = True: .Font.Size = 11: .Font.color = CLR_TEXT_DARK
    End With
    
    With ws.Cells(17, 7)
        .Value = "Ref: " & data.Fabricante & " | Size: " & data.Tamanho
        .Font.name = "Segoe UI": .Font.Size = 9: .Font.color = CLR_TEXT_GREY
    End With
    
    With ws.Cells(18, 7)
        .Value = "Status: " & data.Status
        .Font.name = "Segoe UI": .Font.Bold = True: .Font.Size = 9
        If UCase(data.Status) = "ATIVO" Then .Font.color = CLR_STATUS_OK Else .Font.color = CLR_STATUS_ERR
    End With
    
    If data.Descricao <> "" Then
        With ws.Range("G20:H25")
            .Merge
            .Value = data.Descricao
            .VerticalAlignment = xlTop
            .WrapText = True
            .Font.name = "Segoe UI"
            .Font.Size = 8
            .Font.color = CLR_TEXT_GREY
        End With
    End If
End Sub

' ==============================================================================
' 3. PAINEL DE DOCUMENTOS (DIREITA)
' ==============================================================================
Private Sub Render_Doc_List(ws As Worksheet, ihmData As T_Card_Master)
    Dim docs() As T_Doc_Item
    Dim docCount As Integer
    Dim i As Integer, currRow As Integer
    
    ' 1. Tenta buscar do DB Real
    docCount = Fetch_Docs_From_DB(ihmData.id, docs)
    
    ' 2. Se falhar (DB vazio ou ID n�o mapeado), usa o Esqueleto Padr�o
    ' Isso garante que a UI NUNCA fique vazia ("Image 00024" look)
    If docCount = 0 Then
        docCount = Generate_Skeleton_Structure(ihmData, docs)
    End If
    
    ' 3. Renderiza
    currRow = 5
    For i = 1 To docCount
        Draw_Doc_Item ws, docs(i), currRow
        Draw_Separator_Line ws, currRow + 2
        currRow = currRow + 3
    Next i
End Sub

Private Sub Draw_Doc_Item(ws As Worksheet, item As T_Doc_Item, r As Integer)
    Dim shp As shape
    Dim cellIcon As Range
    Set cellIcon = ws.Cells(r, 11) ' Coluna K
    
    ' 1. Texto do Cap�tulo (Coluna J)
    With ws.Cells(r, 10)
        .Value = item.Capitulo
        .Font.name = "Segoe UI": .Font.Bold = True: .Font.Size = 9: .Font.color = CLR_TEXT_DARK
    End With
    
    ' 2. L�gica Visual (�cone + Tooltip)
    If item.Existe Then
        ' --- CEN�RIO: ARQUIVO EXISTE ---
        Dim iconPath As String
        iconPath = ThisWorkbook.path & "\assets\System\icon_word.png"
        
        On Error Resume Next
        If Dir(iconPath) <> "" Then
            Set shp = ws.Shapes.AddPicture(iconPath, msoFalse, msoTrue, _
                      cellIcon.Left + 5, cellIcon.top, ICO_SIZE, ICO_SIZE)
        Else
            Set shp = ws.Shapes.AddShape(msoShapeFlowchartDocument, _
                      cellIcon.Left + 5, cellIcon.top, ICO_SIZE, ICO_SIZE * 1.2)
            shp.Fill.ForeColor.RGB = RGB(42, 87, 154)
            shp.Line.Visible = msoFalse
        End If
        On Error GoTo 0
        
        With shp
            .name = "zB_BtnOpen_" & item.mapID
            .OnAction = "Doc_Open_Handler"
        End With
        
        ws.Hyperlinks.Add anchor:=shp, Address:="", SubAddress:="", ScreenTip:="Clique para abrir: " & item.NomeArquivo
        
        With ws.Cells(r + 1, 10)
            .Value = item.NomeArquivo
            .Font.name = "Consolas": .Font.Size = 8: .Font.color = CLR_TEXT_GREY
        End With
        
    Else
        ' --- CEN�RIO: ARQUIVO INEXISTENTE/BLOQUEADO ---
        Set shp = ws.Shapes.AddShape(msoShapeNoSymbol, _
                  cellIcon.Left + 5, cellIcon.top, ICO_SIZE, ICO_SIZE)
        
        With shp
            .name = "zB_Blocked_" & r ' ID irrelevante aqui
            .Fill.ForeColor.RGB = CLR_BLOCKED
            .Line.Visible = msoFalse
        End With
        
        ws.Hyperlinks.Add anchor:=shp, Address:="", SubAddress:="", _
            ScreenTip:="Para essa IHM n�o existe essa parte do Manual"
            
        ws.Cells(r + 1, 10).Value = ""
    End If
End Sub

Private Sub Draw_Separator_Line(ws As Worksheet, r As Integer)
    Dim lineShp As shape
    Dim xStart As Single, xEnd As Single, yPos As Single
    xStart = ws.Cells(r, 10).Left
    xEnd = ws.Cells(r, 12).Left + ws.Cells(r, 12).Width
    yPos = ws.Cells(r, 10).top
    
    Set lineShp = ws.Shapes.AddLine(xStart, yPos, xEnd, yPos)
    With lineShp
        .name = "zB_Sep_" & r
        .Line.ForeColor.RGB = RGB(200, 200, 200)
        .Line.Weight = 1
    End With
End Sub

' ==============================================================================
' 4. DATA FETCHING (DB_Mapping)
' ==============================================================================
Private Function Fetch_Docs_From_DB(ihmID As Long, ByRef arr() As T_Doc_Item) As Integer
    On Error GoTo ErrHandler
    
    Dim wsDB As Worksheet
    Set wsDB = ThisWorkbook.Worksheets("DB_Mapping")
    
    Dim lastRow As Long
    lastRow = wsDB.Cells(wsDB.Rows.count, 2).End(xlUp).Row
    
    If lastRow < 2 Then GoTo ErrHandler
    
    Dim data As Variant
    data = wsDB.Range("A2:F" & lastRow).Value
    
    Dim count As Integer
    count = 0
    
    Dim i As Long
    For i = 1 To UBound(data, 1)
        ' FIX CR�TICO: Val() garante que Texto "1" seja igual a N�mero 1
        If val(data(i, 2)) = val(ihmID) Then
            count = count + 1
            ReDim Preserve arr(1 To count)
            
            arr(count).mapID = data(i, 1)
            arr(count).Capitulo = data(i, 3)
            
            Dim rawPath As String
            rawPath = data(i, 4)
            
            If InStr(rawPath, "/") > 0 Then
                arr(count).NomeArquivo = Mid(rawPath, InStrRev(rawPath, "/") + 1)
                arr(count).PathCompleto = ThisWorkbook.path & "\" & Replace(rawPath, "/", "\")
            Else
                arr(count).NomeArquivo = rawPath
                arr(count).PathCompleto = ThisWorkbook.path & "\" & rawPath
            End If
            
            arr(count).Existe = (Dir(arr(count).PathCompleto) <> "")
        End If
    Next i
    
    Fetch_Docs_From_DB = count
    Exit Function

ErrHandler:
    Fetch_Docs_From_DB = 0
End Function

' ==============================================================================
' 5. FALLBACK SKELETON (Garante a UI preenchida)
' ==============================================================================
Private Function Generate_Skeleton_Structure(data As T_Card_Master, ByRef arr() As T_Doc_Item) As Integer
    ReDim arr(1 To 4)
    
    ' Define a estrutura padr�o esperada
    arr(1).Capitulo = "01. Interface"
    arr(2).Capitulo = "02. Modos"
    arr(3).Capitulo = "03. Opera��o"
    arr(4).Capitulo = "04. Falhas"
    
    ' Tenta adivinhar caminhos (apenas para ver se d� sorte)
    ' Se n�o der, ficar� como "Bloqueado", mas a lista aparecer�
    Dim i As Integer
    For i = 1 To 4
        arr(i).mapID = 0 ' Sem ID de mapa
        arr(i).NomeArquivo = "N/A"
        arr(i).Existe = False ' Default para bloqueado
    Next i
    
    Generate_Skeleton_Structure = 4
End Function

' ==============================================================================
' 6. HANDLER DE ABERTURA
' ==============================================================================
Public Sub Doc_Open_Handler()
    Dim btnName As String
    Dim mapID As Long
    
    btnName = Application.Caller
    On Error Resume Next
    mapID = CLng(Replace(btnName, "zB_BtnOpen_", ""))
    On Error GoTo 0
    
    If mapID = 0 Then Exit Sub
    
    Dim pathTarget As String
    pathTarget = Get_Path_By_MapID(mapID)
    
    If pathTarget <> "" And Dir(pathTarget) <> "" Then
        Documents.Open pathTarget
    Else
        MsgBox "Arquivo n�o encontrado:" & vbNewLine & pathTarget, vbExclamation
    End If
End Sub

Private Function Get_Path_By_MapID(targetID As Long) As String
    Dim wsDB As Worksheet
    Dim rngID As Range, cell As Range
    Set wsDB = ThisWorkbook.Worksheets("DB_Mapping")
    Set rngID = wsDB.Range("A:A")
    Set cell = rngID.Find(What:=targetID, LookIn:=xlValues, LookAt:=xlWhole)
    If Not cell Is Nothing Then
        Dim rawPath As String
        rawPath = cell.Offset(0, 3).Value
        Get_Path_By_MapID = ThisWorkbook.path & "\" & Replace(rawPath, "/", "\")
    Else
        Get_Path_By_MapID = ""
    End If
End Function


```
