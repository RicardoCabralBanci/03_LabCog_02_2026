@echo off
chcp 65001 > nul

REM Define a raiz do projeto de forma absoluta para evitar erros de navegação
set "PROJECT_ROOT=C:\LabCogKHS_CLI"
REM O script agora está na mesma pasta que este .bat
set "SYNC_SCRIPT=%~dp0Sincronizar_Memorias_Universal.py"

REM 1. Navegar para a raiz do projeto para o Gemini trabalhar no contexto certo
cd /d "%PROJECT_ROOT%"

echo.
echo ========================================================
echo  LABCOG KHS CLI - AMBIENTE MONITORADO (UNIVERSAL)
echo ========================================================
echo.

REM 2. Sincronização Inicial
echo [1/3] Sincronizando todas as memórias...
python "%SYNC_SCRIPT%"

REM 3. Iniciar Gemini
echo.
echo [2/3] Iniciando Gemini CLI...
echo --------------------------------------------------------
call gemini
echo --------------------------------------------------------

REM 4. Sincronização Final
echo.
echo [3/3] Atualizando histórico com a sessão atual...
python "%SYNC_SCRIPT%"

echo.
echo Processo concluído. Memórias arquivadas em 30_Historico.
pause
