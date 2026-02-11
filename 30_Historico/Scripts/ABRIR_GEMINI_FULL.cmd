@echo off
title LabCog Gemini Interface
cd /d "C:\LabCogKHS_CLI"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "C:\LabCogKHS_CLI\30_Historico\Scripts\ABRIR_GEMINI_FULL.ps1"
if %ERRORLEVEL% neq 0 pause
