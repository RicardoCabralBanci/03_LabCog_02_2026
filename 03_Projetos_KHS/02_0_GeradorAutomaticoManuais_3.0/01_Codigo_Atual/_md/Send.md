# Send

> Codigo VBA atual -- convertido automaticamente de `Send.bas`

```vba
Attribute VB_Name = "Send"
Sub check(Optional byDummy As Byte)

Dim i As Integer
Dim em As Outlook.MailItem
Dim out As Outlook.Application
Dim mec As String
Dim ele As String
Dim ok As String

'Create objects
Set out = GetObject(, "Outlook.Application")
If out Is Nothing Then
    Set out = CreateObject("Outlook.Application")
End If

Set em = out.CreateItem(olMailItem)

Call destiny(em)

'Fill control

    'BTR/DTR
    If Planilha3.Range("F25").Value = "Essa" Then
    
        If Planilha2.Range("E2").Value <> "" Then
            em.Body = "Mensagem autom�tica - Configurador de manuais" & vbLf & vbLf & _
            "Manual gerado com sucesso, assim finalizamos o procedimento para a posi��o K-" & Info.Projeto & vbLf & vbLf & Planilha2.Range("E2").Value
        GoTo loc: End If
        
        Call btr(em)
    End If
        
    'GTR
    If Planilha3.Range("F161").Value = "Essa" Then
    
        If Planilha2.Range("E2").Value <> "" Then
            em.Body = "Mensagem autom�tica - Configurador de manuais" & vbLf & vbLf & _
            "Manual gerado com sucesso, assim finalizamos o procedimento para a posi��o K-" & Info.Projeto & vbLf & vbLf & Planilha2.Range("E2").Value
        GoTo loc: End If
    
    Call gtr(em)
    End If
            
    'DVD - Precisa ter um check de se foi alterado as tabelas e imagens, ou refor�ar para revisar o arquivo (da� inclui o pedido de revis�o em todos)
    If Planilha3.Range("F294").Value = "Essa" Then
    
        If Planilha2.Range("E2").Value <> "" Then
            em.Body = "Mensagem autom�tica - Configurador de manuais" & vbLf & vbLf & _
            "Manual gerado com sucesso! Alguns conte�dos, para a posi��o K-" & Info.Projeto & _
            ", devem ser revisados ou alterados manualmente. Assim que o procedimento for finalizado, informe o t�rmino respondendo a esse email." & _
            vbLf & vbLf & Planilha2.Range("E2").Value
        GoTo loc: End If
    
    Call dvd(em)
    End If
    
    'PET
    If Planilha3.Range("F459").Value = "Essa" Then
    
        If Planilha2.Range("E2").Value <> "" Then
            em.Body = "Mensagem autom�tica - Configurador de manuais" & vbLf & vbLf & _
            "Manual gerado com sucesso! Alguns conte�dos, para a posi��o K-" & Info.Projeto & _
            ", devem ser revisados ou alterados manualmente. Assim que o procedimento for finalizado, informe o t�rmino respondendo a esse email." & _
            vbLf & vbLf & Planilha2.Range("E2").Value
        GoTo loc: End If
    
    Call pet(em)
    End If
    
    'CIP
    If Planilha3.Range("F550").Value = "Essa" Then
    
        If Planilha2.Range("E2").Value <> "" Then
            em.Body = "Mensagem autom�tica - Configurador de manuais" & vbLf & vbLf & _
            "Manual gerado com sucesso! Alguns conte�dos, para a posi��o K-" & Info.Projeto & _
            ", devem ser revisados ou alterados manualmente. Assim que o procedimento for finalizado, informe o t�rmino respondendo a esse email." & _
            vbLf & vbLf & Planilha2.Range("E2").Value
        GoTo loc: End If
    
    Call cip(em)
    End If
    
    'CMX
    If Planilha3.Range("F660").Value = "Essa" Then
    
        If Planilha2.Range("E2").Value <> "" Then
            em.Body = "Mensagem autom�tica - Configurador de manuais" & vbLf & vbLf & _
            "Manual gerado com sucesso! Alguns conte�dos, para a posi��o K-" & Info.Projeto & _
            ", devem ser revisados ou alterados manualmente. Assim que o procedimento for finalizado, informe o t�rmino respondendo a esse email." & _
            vbLf & vbLf & Planilha2.Range("E2").Value
        GoTo loc: End If
    
    Call cmx(em)
    End If
    
    'CCMX
    If Planilha3.Range("F741").Value = "Essa" Then
    
        If Planilha2.Range("E2").Value <> "" Then
            em.Body = "Mensagem autom�tica - Configurador de manuais" & vbLf & vbLf & _
            "Manual gerado com sucesso! Alguns conte�dos, para a posi��o K-" & Info.Projeto & _
            ", devem ser revisados ou alterados manualmente. Assim que o procedimento for finalizado, informe o t�rmino respondendo a esse email." & _
            vbLf & vbLf & Planilha2.Range("E2").Value
        GoTo loc: End If
    
    Call ccmx(em)
    End If
    
loc:

If Planilha3.Range("N1").Value = "Display" Then
    em.Display: End If
    
If Planilha3.Range("N1").Value = "Send" Then
    em.Send: End If

End Sub

Private Sub destiny(ByRef em As Outlook.MailItem)

With em
    .Subject = "Preenchimento - Configurador BA"

    'Define users and recipients (while user defined task)
    If Environ("username") = "krystalasm" Then                                                  'test
        .To = "Thiago.Alves@khs.com; Ronald.Pillinger@khs.com"
    ElseIf Environ("username") = "martinelliv" Then                                             'Transp. el.
        .To = "Matheus.Krystalas@khs.com; Ronald.Pillinger@khs.com"
    ElseIf Environ("username") = "pillingerr" Then                                              'Transp. mec.
        .To = "Matheus.Krystalas@khs.com; Victor.Martinelli@khs.com"
    ElseIf Environ("username") = "pennar" Or Environ("username") = "bischoffp" Then             'Ench. e proc. mec.
        .To = "Matheus.Krystalas@khs.com; Luis.Rossanez@khs.com"
    ElseIf Environ("username") = "rossanezl" And Planilha3.Range("F294").Value = "Essa" Then    'Ench. el.
        .To = "Matheus.Krystalas@khs.com; paula.bischoff@khs.com"
    ElseIf Environ("username") = "rossanezl" And Planilha3.Range("F294").Value = "Outra" Then   'Proc. el.
        .To = "Matheus.Krystalas@khs.com; rena.penna@khs.com"
    Else: .To = "Matheus.Krystalas@khs.com": End If                                             'Out data

End With

End Sub

Private Sub btr(ByRef em As Outlook.MailItem)

With Planilha3
    .Range("N17").Value = "Mec�nica - Abas preenchidas: ": .Range("N18").Value = "Mec�nica - Abas n�o preenchidas: "
    .Range("N20").Value = "El�trica - Abas preenchidas: ": .Range("N21").Value = "El�trica - Abas n�o preenchidas: "

    If .Range("G17").Value = "" Then
        For i = 17 To 19
            If .Cells(i, 5).Value = "preenchida" Then
            .Range("N17").Value = .Range("N17").Value & .Cells(i, 6).Value & "; "
            Else: .Range("N18").Value = .Range("N18").Value & .Cells(i, 6).Value & "; ": End If
        Next: mec = .Range("N17").Value & vbLf & .Range("N18").Value
    Else: mec = .Range("G17").Value: End If
    
    If .Range("G20").Value = "" Then
        For i = 20 To 24
            If .Cells(i, 5).Value = "preenchida" Then
            .Range("N20").Value = .Range("N20").Value & .Cells(i, 6).Value & "; "
            Else: .Range("N21").Value = .Range("N21").Value & .Cells(i, 6).Value & "; ": End If
        Next: ele = .Range("N20").Value & vbLf & .Range("N21").Value
    Else: ele = .Range("G20").Value: End If

    If .Range("F26").Value = "N�o" Then
        ok = "Manual n�o pode ser gerado."
    Else: ok = "Manual pode ser gerado.": End If

    em.Body = "Mensagem autom�tica - Configurador de manuais" & vbLf & vbLf & mec & vbLf & vbLf & ele & vbLf & vbLf & ok & vbLf & vbLf & ThisWorkbook.path
    
End With
    
End Sub

Private Sub gtr(ByRef em As Outlook.MailItem)

With Planilha3
    .Range("N153").Value = "Mec�nica - Abas preenchidas: ": .Range("N154").Value = "Mec�nica - Abas n�o preenchidas: "
    .Range("N156").Value = "El�trica - Abas preenchidas: ": .Range("N157").Value = "El�trica - Abas n�o preenchidas: "

    If .Range("G153").Value = "" Then
        For i = 153 To 155
            If .Cells(i, 5).Value = "preenchida" Then
            .Range("N153").Value = .Range("N153").Value & .Cells(i, 6).Value & "; "
            Else: .Range("N154").Value = .Range("N154").Value & .Cells(i, 6).Value & "; ": End If
        Next: mec = .Range("N153").Value & vbLf & .Range("N154").Value
    Else: mec = .Range("G153").Value: End If
    
    If .Range("G156").Value = "" Then
        For i = 156 To 160
            If .Cells(i, 5).Value = "preenchida" Then
            .Range("N156").Value = .Range("N156").Value & .Cells(i, 6).Value & "; "
            Else: .Range("N157").Value = .Range("N157").Value & .Cells(i, 6).Value & "; ": End If
        Next: ele = .Range("N156").Value & vbLf & .Range("N157").Value
    Else: ele = .Range("G156").Value: End If

    If .Range("F162").Value = "N�o" Then
        ok = "Manual n�o pode ser gerado."
    Else: ok = "Manual pode ser gerado.": End If

    em.Body = "Mensagem autom�tica - Configurador de manuais" & vbLf & vbLf & mec & vbLf & vbLf & ele & vbLf & vbLf & ok & vbLf & vbLf & ThisWorkbook.path

End With
    
End Sub

Private Sub dvd(ByRef em As Outlook.MailItem)

With Planilha3
    .Range("N289").Value = "Mec�nica - Abas preenchidas: ": .Range("N290").Value = "Mec�nica - Abas n�o preenchidas: "
    .Range("N292").Value = "El�trica - Abas preenchidas: ": .Range("N293").Value = "El�trica - Abas n�o preenchidas: "

    If .Range("G289").Value = "" Then
        For i = 289 To 291
            If .Cells(i, 5).Value = "preenchida" Then
            .Range("N289").Value = .Range("N289").Value & .Cells(i, 6).Value & "; "
            Else: .Range("N290").Value = .Range("N290").Value & .Cells(i, 6).Value & "; ": End If
        Next: mec = .Range("N289").Value & vbLf & .Range("N290").Value
    Else: mec = .Range("G289").Value: End If
    
    If .Range("G292").Value = "" Then
        For i = 292 To 293
            If .Cells(i, 5).Value = "preenchida" Then
            .Range("N292").Value = .Range("N292").Value & .Cells(i, 6).Value & "; "
            Else: .Range("N293").Value = .Range("N293").Value & .Cells(i, 6).Value & "; ": End If
        Next: ele = .Range("N292").Value & vbLf & .Range("N293").Value
    Else: ele = .Range("G292").Value: End If

    If .Range("F295").Value = "N�o" Then
        ok = "Manual n�o pode ser gerado."
    Else: ok = "Manual pode ser gerado.": End If

    em.Body = "Mensagem autom�tica - Configurador de manuais" & vbLf & vbLf & mec & vbLf & vbLf & ele & vbLf & vbLf & ok & vbLf & vbLf & ThisWorkbook.path
    
End With
    
End Sub

Private Sub pet(ByRef em As Outlook.MailItem)

With Planilha3
    .Range("N455").Value = "Mec�nica - Abas preenchidas: ": .Range("N456").Value = "Mec�nica - Abas n�o preenchidas: "

    If .Range("G455").Value = "" Then
        For i = 455 To 456
            If .Cells(i, 5).Value = "preenchida" Then
            .Range("N455").Value = .Range("N455").Value & .Cells(i, 6).Value & "; "
            Else: .Range("N456").Value = .Range("N456").Value & .Cells(i, 6).Value & "; ": End If
        Next: mec = .Range("N455").Value & vbLf & .Range("N456").Value
    Else: mec = .Range("G455").Value: End If
    
    ele = .Range("G457").Value: End If

    If .Range("F460").Value = "N�o" Then
        ok = "Manual n�o pode ser gerado."
    Else: ok = "Manual pode ser gerado.": End If

    em.Body = "Mensagem autom�tica - Configurador de manuais" & vbLf & vbLf & mec & vbLf & vbLf & ele & vbLf & vbLf & ok & vbLf & vbLf & ThisWorkbook.path
    
End With
    
End Sub

Private Sub cip(ByRef em As Outlook.MailItem)

With Planilha3
    .Range("N545").Value = "Mec�nica - Abas preenchidas: ": .Range("N546").Value = "Mec�nica - Abas n�o preenchidas: "

    If .Range("G545").Value = "" Then
        For i = 545 To 548
            If .Cells(i, 5).Value = "preenchida" Then
            .Range("N545").Value = .Range("N545").Value & .Cells(i, 6).Value & "; "
            Else: .Range("N546").Value = .Range("N546").Value & .Cells(i, 6).Value & "; ": End If
        Next: mec = .Range("N545").Value & vbLf & .Range("N546").Value
    Else: mec = .Range("G545").Value: End If
    
    ele = .Range("G549").Value: End If

    If .Range("F551").Value = "N�o" Then
        ok = "Manual n�o pode ser gerado."
    Else: ok = "Manual pode ser gerado.": End If

    em.Body = "Mensagem autom�tica - Configurador de manuais" & vbLf & vbLf & mec & vbLf & vbLf & ele & vbLf & vbLf & ok & vbLf & vbLf & ThisWorkbook.path
    
End With
    
End Sub

Private Sub cmx(ByRef em As Outlook.MailItem)

With Planilha3
    .Range("N657").Value = "Mec�nica - Abas preenchidas: ": .Range("N658").Value = "Mec�nica - Abas n�o preenchidas: "

    If .Range("G657").Value = "" Then
        For i = 657 To 658
            If .Cells(i, 5).Value = "preenchida" Then
            .Range("N657").Value = .Range("N657").Value & .Cells(i, 6).Value & "; "
            Else: .Range("N658").Value = .Range("N658").Value & .Cells(i, 6).Value & "; ": End If
        Next: mec = .Range("N657").Value & vbLf & .Range("N658").Value
    Else: mec = .Range("G657").Value: End If
    
    ele = .Range("G659").Value: End If

    If .Range("F661").Value = "N�o" Then
        ok = "Manual n�o pode ser gerado."
    Else: ok = "Manual pode ser gerado.": End If

    em.Body = "Mensagem autom�tica - Configurador de manuais" & vbLf & vbLf & mec & vbLf & vbLf & ele & vbLf & vbLf & ok & vbLf & vbLf & ThisWorkbook.path
    
End With
    
End Sub

Private Sub ccmx(ByRef em As Outlook.MailItem)

With Planilha3
    .Range("N736").Value = "Mec�nica - Abas preenchidas: ": .Range("N737").Value = "Mec�nica - Abas n�o preenchidas: "
    .Range("N739").Value = "El�trica - Abas preenchidas: ": .Range("N740").Value = "El�trica - Abas n�o preenchidas: "

    If .Range("G736").Value = "" Then
        For i = 736 To 738
            If .Cells(i, 5).Value = "preenchida" Then
            .Range("N736").Value = .Range("N736").Value & .Cells(i, 6).Value & "; "
            Else: .Range("N737").Value = .Range("N737").Value & .Cells(i, 6).Value & "; ": End If
        Next: mec = .Range("N736").Value & vbLf & .Range("N737").Value
    Else: mec = .Range("G736").Value: End If
    
    If .Range("G739").Value = "" Then
        For i = 739 To 740
            If .Cells(i, 5).Value = "preenchida" Then
            .Range("N739").Value = .Range("N739").Value & .Cells(i, 6).Value & "; "
            Else: .Range("N740").Value = .Range("N740").Value & .Cells(i, 6).Value & "; ": End If
        Next: ele = .Range("N739").Value & vbLf & .Range("N740").Value
    Else: ele = .Range("G739").Value: End If

    If .Range("F742").Value = "N�o" Then
        ok = "Manual n�o pode ser gerado."
    Else: ok = "Manual pode ser gerado.": End If

    em.Body = "Mensagem autom�tica - Configurador de manuais" & vbLf & vbLf & mec & vbLf & vbLf & ele & vbLf & vbLf & ok & vbLf & vbLf & ThisWorkbook.path
    
End With
    
End Sub

```
