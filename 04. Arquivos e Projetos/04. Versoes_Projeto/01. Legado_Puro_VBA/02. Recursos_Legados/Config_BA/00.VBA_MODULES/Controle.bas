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
 Dim Shp As shape
 
 On Error Resume Next
 
 For Each Shp In ActiveSheet.Shapes
 
 If Not Application.Intersect(Shp.TopLeftCell, ActiveSheet.Range("B4:F50")) Is Nothing Then
 Shp.Select
 
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
Dim c As Cell


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




