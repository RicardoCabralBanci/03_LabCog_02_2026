# Páginas

> Codigo VBA atual -- convertido automaticamente de `Páginas.bas`

```vba
Attribute VB_Name = "P�ginas"
' =========================================================================================
' M�DULO: Navega��o de P�ginas (REVISADO)
' DESCRI��O: Macros de salto entre abas. Sincronizado com Imagem 00019.
' =========================================================================================

Sub top(Optional byDummy As Byte)
    Dim i As Long
    i = ActiveCell.Column
    ThisWorkbook.ActiveSheet.Cells(4, i).Select
End Sub

' --- BTR (8 P�ginas) ---
Sub BTRPG1(Optional byDummy As Byte): Planilha5.Activate: End Sub   ' Prote��o
Sub BTRPG2(Optional byDummy As Byte): Planilha6.Activate: End Sub   ' Transportadores
Sub BTRPG3(Optional byDummy As Byte): Planilha7.Activate: End Sub   ' Recipientes
Sub BTRPG4(Optional byDummy As Byte): Planilha8.Activate: End Sub   ' �reas
Sub BTRPG5(Optional byDummy As Byte): Planilha9.Activate: End Sub   ' Comando
Sub BTRPG6(Optional byDummy As Byte): Planilha10.Activate: End Sub  ' Aviso
Sub BTRPG7(Optional byDummy As Byte): Planilha11.Activate: End Sub  ' El�trica
Sub BTRPG8(Optional byDummy As Byte): Planilha12.Activate: End Sub  ' IHM

' --- GTR (7 P�ginas) ---
Sub GTRPG1(Optional byDummy As Byte): Planilha13.Activate: End Sub
Sub GTRPG2(Optional byDummy As Byte): Planilha14.Activate: End Sub
Sub GTRPG3(Optional byDummy As Byte): Planilha15.Activate: End Sub
Sub GTRPG4(Optional byDummy As Byte): Planilha16.Activate: End Sub
Sub GTRPG5(Optional byDummy As Byte): Planilha17.Activate: End Sub
Sub GTRPG6(Optional byDummy As Byte): Planilha18.Activate: End Sub
Sub GTRPG7(Optional byDummy As Byte): Planilha19.Activate: End Sub
Sub GTRPG8(Optional byDummy As Byte): Planilha20.Activate: End Sub ' IHM

' --- DVD (5 P�ginas) ---
Sub DVDPG1(Optional byDummy As Byte): Planilha21.Activate: End Sub
Sub DVDPG2(Optional byDummy As Byte): Planilha22.Activate: End Sub
Sub DVDPG3(Optional byDummy As Byte): Planilha23.Activate: End Sub
Sub DVDPG4(Optional byDummy As Byte): Planilha24.Activate: End Sub
Sub DVDPG5(Optional byDummy As Byte): Planilha251.Activate: End Sub

' --- PET (3 P�ginas) ---
Sub PETPG1(Optional byDummy As Byte): Planilha26.Activate: End Sub
Sub PETPG2(Optional byDummy As Byte): Planilha27.Activate: End Sub
Sub PETPG3(Optional byDummy As Byte): Planilha28.Activate: End Sub ' El�trica

' --- CIP (5 P�ginas) ---
Sub CIPPG1(Optional byDummy As Byte): Planilha291.Activate: End Sub ' Qu�micos
Sub CIPPG2(Optional byDummy As Byte): Planilha30.Activate: End Sub  ' Estrutura
Sub CIPPG3(Optional byDummy As Byte): Planilha31.Activate: End Sub  ' Gerais
Sub CIPPG4(Optional byDummy As Byte): Planilha321.Activate: End Sub ' T�cnicos
Sub CIPPG5(Optional byDummy As Byte): Planilha33.Activate: End Sub  ' El�trica
Sub CIPPG6(Optional byDummy As Byte): Planilha34.Activate: End Sub  ' IHM

' --- CMX (3 P�ginas) ---
Sub CMXPG1(Optional byDummy As Byte): Planilha35.Activate: End Sub
Sub CMXPG2(Optional byDummy As Byte): Planilha36.Activate: End Sub
Sub CMXPG3(Optional byDummy As Byte): Planilha37.Activate: End Sub ' El�trica

' --- CCMX (5 P�ginas) ---
Sub CCMXPG1(Optional byDummy As Byte): Planilha38.Activate: End Sub ' Estrutura
Sub CCMXPG2(Optional byDummy As Byte): Planilha39.Activate: End Sub ' Gerais
Sub CCMXPG3(Optional byDummy As Byte): Planilha401.Activate: End Sub ' T�cnicos
Sub CCMXPG4(Optional byDummy As Byte): Planilha41.Activate: End Sub ' El�trica
Sub CCMXPG5(Optional byDummy As Byte): Planilha42.Activate: End Sub ' IHM

' --- PALETIZADOR (PLT) ---
Sub PLTPG1(Optional byDummy As Byte): Planilha43.Activate: End Sub  ' Estrutura
Sub PLTPG2(Optional byDummy As Byte): Planilha44.Activate: End Sub  ' Gerais
Sub PLTPG3(Optional byDummy As Byte): Planilha451.Activate: End Sub ' T�cnicos
Sub PLTPG4(Optional byDummy As Byte): Planilha46.Activate: End Sub  ' El�trica
Sub PLTPG5(Optional byDummy As Byte): Planilha53.Activate: End Sub  ' IHM Nova

' --- DESPALETIZADOR (DPL) ---
Sub DPLPG1(Optional byDummy As Byte): Planilha48.Activate: End Sub  ' Estrutura
Sub DPLPG2(Optional byDummy As Byte): Planilha49.Activate: End Sub  ' Gerais
Sub DPLPG3(Optional byDummy As Byte): Planilha501.Activate: End Sub ' T�cnicos
Sub DPLPG4(Optional byDummy As Byte): Planilha51.Activate: End Sub  ' El�trica
Sub DPLPG5(Optional byDummy As Byte): Planilha54.Activate: End Sub  ' IHM Nova

' --- ENCAIXOTADORA (PCK) ---
Sub PCKPG1(Optional byDummy As Byte): Planilha52.Activate: End Sub  ' Estrutura
Sub PCKPG2(Optional byDummy As Byte): Planilha57.Activate: End Sub  ' Gerais
Sub PCKPG3(Optional byDummy As Byte): Planilha502.Activate: End Sub ' T�cnicos
Sub PCKPG4(Optional byDummy As Byte): Planilha58.Activate: End Sub  ' El�trica
Sub PCKPG5(Optional byDummy As Byte): Planilha55.Activate: End Sub  ' IHM Nova

' --- DESENCAIXOTADORA (DPK) ---
Sub DPKPG1(Optional byDummy As Byte): Planilha59.Activate: End Sub  ' Estrutura
Sub DPKPG2(Optional byDummy As Byte): Planilha60.Activate: End Sub  ' Gerais
Sub DPKPG3(Optional byDummy As Byte): Planilha503.Activate: End Sub ' T�cnicos
Sub DPKPG4(Optional byDummy As Byte): Planilha61.Activate: End Sub  ' El�trica
Sub DPKPG5(Optional byDummy As Byte): Planilha56.Activate: End Sub  ' IHM Nova

```
