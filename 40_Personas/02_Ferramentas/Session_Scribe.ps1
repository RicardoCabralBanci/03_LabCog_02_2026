$ErrorActionPreference = "Continue" # Permite ver erros sem abortar imediatamente para logar
$DataAtual = Get-Date -Format "yyyy-MM-dd_HH-mm"
$PastaLogs = "C:\LabCogKHS_CLI\04. Arquivos e Projetos\Criação Automatica de Manuais\33. Histórico\33.1 Histórico Bruto Personas"

Clear-Host
Write-Host "--- DIAGNOSTICO DO ESCRIBA ---" -ForegroundColor Yellow

# 1. Verificar/Criar Diretório
try {
    if (-not (Test-Path -LiteralPath $PastaLogs)) {
        Write-Host "Diretório não encontrado. Criando: $PastaLogs"
        New-Item -ItemType Directory -Path $PastaLogs -Force | Out-Null
    } else {
        Write-Host "Diretório de logs verificado: OK" -ForegroundColor Green
    }
}
catch {
    Write-Host "ERRO ao acessar diretório complexo: $_" -ForegroundColor Red
}

$CaminhoLog = Join-Path $PastaLogs "Sessao_$DataAtual.md"

# 2. Iniciar Transcrição
Write-Host "Tentando iniciar gravação em: $CaminhoLog"
try {
    Start-Transcript -Path $CaminhoLog -Append -ErrorAction Stop
}
catch {
    Write-Host "FALHA ao gravar no caminho original. Tentando caminho simplificado..." -ForegroundColor Red
    $PastaLogsSimples = "C:\LabCogKHS_CLI\logs_backup"
    New-Item -ItemType Directory -Path $PastaLogsSimples -Force | Out-Null
    $CaminhoLog = Join-Path $PastaLogsSimples "Sessao_$DataAtual.md"
    Write-Host "Novo caminho: $CaminhoLog" -ForegroundColor Yellow
    Start-Transcript -Path $CaminhoLog -Append
}

# 3. Executar Gemini
Write-Host "----------------------------------------------------------"
Write-Host "Iniciando Gemini..."
try {
    # Tenta invocar o comando. Se 'gemini' for um script .cmd/.bat, o PowerShell precisa saber.
    # Usamos o operador '&' para executar o comando encontrado no PATH.
    & gemini
}
catch {
    Write-Host "ERRO CRÍTICO: Não foi possível iniciar o 'gemini'. Verifique se está no PATH." -ForegroundColor Red
    Write-Host "Detalhe do erro: $_" -ForegroundColor Red
}
finally {
    Stop-Transcript
    Write-Host "`n--- FIM DA SESSÃO ---" -ForegroundColor Cyan
    Write-Host "Pressione ENTER para fechar esta janela..."
    Read-Host
}