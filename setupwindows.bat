@echo off
chcp 65001 >nul
echo.
echo ============================================
echo           GEOHOUSE — Setup Completo
echo ============================================
echo.
echo  Como usar:
echo  1. Coloque este arquivo na pasta raiz do projeto
echo  2. De dois cliques neste arquivo
echo  3. Se for a primeira vez, ele instala o Node.js
echo     e pede para fechar e abrir o terminal
echo  4. Na segunda execucao, instala tudo e sobe
echo     o projeto automaticamente
echo.
echo ============================================
echo.

REM ─────────────────────────────────────────────
REM  PASSO 1 — Verificar e instalar o Node.js
REM ─────────────────────────────────────────────
echo [1/3] Verificando Node.js...
node --version >nul 2>&1

IF %ERRORLEVEL% NEQ 0 (
    echo Node.js nao encontrado. Iniciando download...
    echo Isso pode demorar alguns minutos...
    echo.

    REM Baixa o instalador do Node.js v20 LTS direto do site oficial
    curl -o node_installer.msi https://nodejs.org/dist/v20.11.0/node-v20.11.0-x64.msi

    echo Instalando Node.js silenciosamente...
    msiexec /i node_installer.msi /quiet /norestart

    REM Remove o instalador apos instalar
    del node_installer.msi

    echo.
    echo ✅ Node.js instalado com sucesso!
    echo.
    echo ⚠️  IMPORTANTE:
    echo     Feche este terminal e execute este arquivo novamente
    echo     para continuar com a instalacao do projeto.
    echo.
    pause
    exit
)

echo ✅ Node.js ja esta instalado.

REM ─────────────────────────────────────────────
REM  PASSO 2 — Instalar dependencias do projeto
REM  (vue, vue-router, vite, bootstrap, etc)
REM ─────────────────────────────────────────────
echo.
echo [2/3] Instalando dependencias do projeto...
echo Isso pode demorar na primeira vez...
echo.

REM Entra na pasta do projeto onde fica o package.json
cd /d "%~dp0geohouse"

REM Instala todas as dependencias listadas no package.json
REM incluindo: vue, vue-router, vite, bootstrap e font-awesome
npm install

echo.
echo ✅ Dependencias instaladas com sucesso!

REM ─────────────────────────────────────────────
REM  PASSO 3 — Rodar o projeto
REM ─────────────────────────────────────────────
echo.
echo [3/3] Iniciando o projeto...
echo.
echo  Acesse no navegador: http://localhost:5173
echo  Para encerrar pressione CTRL+C
echo.

npm run dev

pause
