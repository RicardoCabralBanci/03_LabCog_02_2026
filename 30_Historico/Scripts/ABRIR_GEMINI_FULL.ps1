# LabCog KHS - Gemini Interface (PowerShell Version)
$ErrorActionPreference = "Stop"

$ProjectRoot = "C:\LabCogKHS_CLI"
$SyncScript  = "$ProjectRoot\30_Historico\Scripts\Sincronizar_Memorias_Universal.py"

if (Test-Path $ProjectRoot) {
    Set-Location $ProjectRoot
} else {
    Write-Error "Projeto nao encontrado em: $ProjectRoot"
    exit 1
}

Clear-Host
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "  LABCOG KHS CLI - SISTEMA DE MEMORIA (PWSH)" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "[1/3] Carregando memorias..." -ForegroundColor Gray
if (Test-Path $SyncScript) {
    python $SyncScript
}

Write-Host ""
Write-Host "[2/3] Iniciando Agente Gemini..." -ForegroundColor Green
Write-Host "--------------------------------------------------------"
Write-Host ""

# Executa o Gemini
gemini

Write-Host ""
Write-Host "--------------------------------------------------------"
Write-Host "[3/3] Salvando novas memorias..." -ForegroundColor Gray

if (Test-Path $SyncScript) {
    python $SyncScript
}

Write-Host ""
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "  Sessao finalizada com sucesso." -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "Pressione Enter para fechar..."
Read-Host