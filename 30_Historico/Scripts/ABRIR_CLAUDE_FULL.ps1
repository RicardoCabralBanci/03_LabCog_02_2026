# LabCog KHS - Claude Interface (PowerShell Version)
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
Write-Host "========================================================" -ForegroundColor Yellow
Write-Host "  LABCOG KHS CLI - SISTEMA DE MEMORIA (CLAUDE)" -ForegroundColor Yellow
Write-Host "========================================================" -ForegroundColor Yellow
Write-Host ""

Write-Host "[1/3] Carregando memorias..." -ForegroundColor Gray
if (Test-Path $SyncScript) {
    python $SyncScript
}

Write-Host ""
Write-Host "[2/3] Iniciando Agente Claude..." -ForegroundColor Green
Write-Host "--------------------------------------------------------"
Write-Host ""

# Executa o Claude
claude

Write-Host ""
Write-Host "--------------------------------------------------------"
Write-Host "[3/3] Salvando novas memorias..." -ForegroundColor Gray

if (Test-Path $SyncScript) {
    python $SyncScript
}

Write-Host ""
Write-Host "========================================================" -ForegroundColor Yellow
Write-Host "  Sessao finalizada com sucesso." -ForegroundColor Yellow
Write-Host "========================================================" -ForegroundColor Yellow
Write-Host "Pressione Enter para fechar..."
Read-Host