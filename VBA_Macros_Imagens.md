# Macros VBA para Manipulação de Imagens Bloqueadas

Este documento contém as rotinas VBA para lidar com imagens que não podem ser selecionadas manualmente no Excel devido a proteções, controles ActiveX ou Ribbons personalizados.

## 1. Macro: Destravar e Listar Objetos (Com Log na Verificação Imediata)
Esta macro tenta desproteger a planilha e lista todos os objetos encontrados diretamente na janela de **Verificação Imediata** (`Ctrl + G`), permitindo que você copie a lista facilmente.

```vba
Sub Destravar_e_Listar()
    Dim shp As Shape
    Dim contador As Integer
    
    ' 1. Tenta Desproteger a Planilha (força bruta sem senha)
    On Error Resume Next
    ActiveSheet.Unprotect
    If Err.Number <> 0 Then
        Debug.Print "AVISO: A planilha tem senha. Alguns objetos podem continuar bloqueados."
        Err.Clear
    Else
        Debug.Print "SUCESSO: Planilha desprotegida (ou não tinha senha)."
    End If
    On Error GoTo 0
    
    ' 2. Lista os objetos na Verificação Imediata
    Debug.Print "--------------------------------------------------"
    Debug.Print "LISTAGEM DE OBJETOS NA ABA: " & ActiveSheet.Name
    Debug.Print "--------------------------------------------------"
    
    contador = 0
    For Each shp In ActiveSheet.Shapes
        contador = contador + 1
        
        ' Tenta pegar o Texto Alternativo sem dar erro se não existir
        Dim altText As String
        altText = ""
        On Error Resume Next
        altText = shp.AlternativeText
        On Error GoTo 0
        
        ' Imprime os detalhes para copiar
        Debug.Print "Objeto #" & contador
        Debug.Print "   Nome (ID): " & shp.Name
        Debug.Print "   Tipo: " & TypeName(shp.OLEFormat.Object)
        Debug.Print "   Texto Alternativo: " & altText
        Debug.Print "   Posição: Top=" & shp.Top & " Left=" & shp.Left
        Debug.Print "--------------------------------------------------"
        
        ' Força o desbloqueio do objeto individualmente
        shp.Locked = False
    Next shp
    
    Debug.Print "FIM DA LISTAGEM. Total de objetos: " & contador
    
    MsgBox "Verificação concluída! Pressione Ctrl + G para ver a lista completa.", vbInformation
End Sub
```

## 2. Macro: Substituir Imagem na Seleção
Esta macro identifica a imagem sobre as células selecionadas, apaga-a e insere uma nova imagem no mesmo lugar, preservando o **Nome** e o **Texto Alternativo** (essencial para que outros scripts não quebrem).

```vba
Sub Substituir_Imagem_Na_Selecao()
    Dim shp As Shape
    Dim targetShp As Shape
    Dim fd As FileDialog
    Dim newPicPath As String
    Dim oldLeft As Double, oldTop As Double
    Dim oldWidth As Double, oldHeight As Double
    Dim oldName As String
    Dim oldAltText As String
    Dim ws As Worksheet
    
    Set ws = ActiveSheet
    
    ' 1. Procura uma imagem que cruze com as células que você selecionou
    For Each shp In ws.Shapes
        ' Verifica se a imagem intersecta com a seleção atual
        If Not Intersect(shp.TopLeftCell, Selection) Is Nothing Or _
           Not Intersect(shp.BottomRightCell, Selection) Is Nothing Then
            Set targetShp = shp
            Exit For ' Pega a primeira que achar
        End If
    Next shp
    
    If targetShp Is Nothing Then
        MsgBox "Nenhuma imagem encontrada sobre as células selecionadas." & vbNewLine & _
               "Selecione as células atrás da imagem e tente de novo.", vbExclamation
        Exit Sub
    End If
    
    ' 2. Confirmação
    If MsgBox("Encontrei a imagem: '" & targetShp.Name & "'." & vbNewLine & _
              "Deseja substituí-la?", vbYesNo + vbQuestion) = vbNo Then Exit Sub
    
    ' 3. Pede a nova imagem
    Set fd = Application.FileDialog(msoFileDialogFilePicker)
    With fd
        .Title = "Selecione a nova imagem"
        .Filters.Clear
        .Filters.Add "Imagens", "*.jpg, *.jpeg, *.png, *.bmp"
        If .Show = -1 Then
            newPicPath = .SelectedItems(1)
        Else
            Exit Sub
        End If
    End With
    
    ' 4. Guarda as coordenadas e metadados da antiga
    With targetShp
        oldLeft = .Left
        oldTop = .Top
        oldWidth = .Width
        oldHeight = .Height
        oldName = .Name
        On Error Resume Next
        oldAltText = .AlternativeText
        On Error GoTo 0
        .Delete
    End With
    
    ' 5. Insere a nova
    Dim newShp As Shape
    Set newShp = ws.Shapes.AddPicture(Filename:=newPicPath, _
                                      LinkToFile:=msoFalse, _
                                      SaveWithDocument:=msoTrue, _
                                      Left:=oldLeft, _
                                      Top:=oldTop, _
                                      Width:=oldWidth, _
                                      Height:=oldHeight)
                                      
    ' 6. Restaura o nome para o código antigo não quebrar
    newShp.Name = oldName
    On Error Resume Next
    newShp.AlternativeText = oldAltText
    On Error GoTo 0
    
    MsgBox "Imagem substituída e renomeada para: " & oldName
End Sub

## 3. Macro: Centralizar Imagens nas Células
Estas rotinas alinham as imagens perfeitamente no centro (horizontal e vertical) da célula onde elas estão posicionadas.

### Centralizar apenas a SELECIONADA
```vba
Sub Centralizar_Imagem_Selecionada()
    Dim shp As Shape
    Dim targetCell As Range
    
    On Error Resume Next
    Set shp = Selection.ShapeRange(1)
    On Error GoTo 0
    
    If shp Is Nothing Then
        MsgBox "Por favor, selecione uma imagem primeiro.", vbExclamation
        Exit Sub
    End If
    
    ' Pega a área da célula (considera células mescladas)
    Set targetCell = shp.TopLeftCell.MergeArea
    
    ' Cálculo do Centro
    shp.Left = targetCell.Left + (targetCell.Width - shp.Width) / 2
    shp.Top = targetCell.Top + (targetCell.Height - shp.Height) / 2
End Sub
```

### Centralizar TODAS da Planilha (Limpeza Geral)
```vba
Sub Centralizar_TODAS_as_Imagens()
    Dim shp As Shape
    Dim targetCell As Range
    Dim contador As Integer
    
    contador = 0
    For Each shp In ActiveSheet.Shapes
        ' Ignora botões e comentários, foca em imagens e formas
        If shp.Type <> msoFormControl And shp.Type <> msoComment Then
            
            Set targetCell = shp.TopLeftCell.MergeArea
            
            ' Alinhamento Horizontal
            shp.Left = targetCell.Left + (targetCell.Width - shp.Width) / 2
            
            ' Alinhamento Vertical
            shp.Top = targetCell.Top + (targetCell.Height - shp.Height) / 2
            
            contador = contador + 1
        End If
    Next shp
    
    MsgBox contador & " objetos foram centralizados!", vbInformation
End Sub
```

```

## Como Usar
1. Abra o Excel e pressione `Alt + F11`.
2. Vá em **Exibir > Verificação Imediata** (ou pressione `Ctrl + G`) para abrir a janela de logs.
3. Cole os códigos acima em um Módulo.
4. Rode a macro `Destravar_e_Listar`.
5. Os nomes e detalhes aparecerão na janela imediata para você copiar.