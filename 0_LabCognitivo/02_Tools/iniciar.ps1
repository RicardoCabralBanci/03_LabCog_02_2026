# iniciar.ps1 - Launcher do Laboratorio Cognitivo
# Uso: .\0_LabCognitivo\02_Tools\iniciar.ps1
# Requer: PowerShell 7+, Python no PATH, Claude Code CLI instalado

$ErrorActionPreference = "Continue"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent (Split-Path -Parent $ScriptDir)

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Laboratorio Cognitivo - Inicializacao" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 1. Ativar venv se existir
$VenvActivate = Join-Path $ProjectRoot "venv\Scripts\Activate.ps1"
if (Test-Path $VenvActivate) {
    Write-Host "[Launcher] Ativando virtual environment..." -ForegroundColor Yellow
    & $VenvActivate
}

# 2. Rodar transcricao de sessoes
$TranscriptScript = Join-Path $ScriptDir "transcrever_sessoes.py"
if (Test-Path $TranscriptScript) {
    Write-Host "[Launcher] Transcrevendo sessoes anteriores..." -ForegroundColor Yellow
    python $TranscriptScript
    Write-Host ""
}

# 3. Abrir Claude Code CLI
Write-Host "[Launcher] Abrindo Claude Code..." -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Set-Location $ProjectRoot
claude
