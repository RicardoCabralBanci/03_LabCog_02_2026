@echo off
title LabCog Claude Interface (PWSH 7)
set "PWSH_EXE=C:\Program Files\PowerShell\7\pwsh.exe"
set "SCRIPT_PATH=C:\LabCogKHS_CLI\30_Historico\Scripts\ABRIR_CLAUDE_FULL.ps1"

if exist "%PWSH_EXE%" (
    "%PWSH_EXE%" -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT_PATH%"
) else (
    echo [AVISO] PowerShell 7 nao encontrado. Usando Windows PowerShell padrao...
    powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT_PATH%"
)

if %ERRORLEVEL% neq 0 pause