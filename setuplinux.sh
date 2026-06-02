#!/bin/bash

echo ""
echo "============================================"
echo "          GEOHOUSE — Setup Completo"
echo "============================================"
echo ""
echo " Como usar:"
echo " 1. Coloque este arquivo na pasta raiz do projeto"
echo " 2. No terminal execute: chmod +x setup.sh && ./setup.sh"
echo " 3. Se for a primeira vez, ele instala o Node.js"
echo "    automaticamente"
echo " 4. Instala todas as dependencias e sobe o projeto"
echo ""
echo "============================================"
echo ""

# ─────────────────────────────────────────────
#  PASSO 1 — Verificar e instalar o Node.js
# ─────────────────────────────────────────────
echo "[1/3] Verificando Node.js..."

if ! command -v node &> /dev/null; then
    echo "Node.js nao encontrado. Instalando..."
    echo ""

    # Detecta a distro Linux
    if command -v apt-get &> /dev/null; then
        # Ubuntu / Debian
        curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
        sudo apt-get install -y nodejs

    elif command -v dnf &> /dev/null; then
        # Fedora / RHEL
        curl -fsSL https://rpm.nodesource.com/setup_20.x | sudo bash -
        sudo dnf install -y nodejs

    elif command -v yum &> /dev/null; then
        # CentOS
        curl -fsSL https://rpm.nodesource.com/setup_20.x | sudo bash -
        sudo yum install -y nodejs

    elif command -v pacman &> /dev/null; then
        # Arch Linux
        sudo pacman -S --noconfirm nodejs npm

    else
        echo "❌ Distro nao suportada. Instale o Node.js manualmente:"
        echo "   https://nodejs.org"
        exit 1
    fi

    echo ""
    echo "✅ Node.js instalado com sucesso!"
else
    echo "✅ Node.js ja esta instalado."
fi

# ─────────────────────────────────────────────
#  PASSO 2 — Instalar dependencias do projeto
#  (vue, vue-router, vite, bootstrap, etc)
# ─────────────────────────────────────────────
echo ""
echo "[2/3] Instalando dependencias do projeto..."
echo "Isso pode demorar na primeira vez..."
echo ""

# Entra na pasta do projeto onde fica o package.json
cd "$(dirname "$0")/geohouse"

# Instala todas as dependencias listadas no package.json
# incluindo: vue, vue-router, vite, bootstrap e font-awesome
npm install

echo ""
echo "✅ Dependencias instaladas com sucesso!"

# ─────────────────────────────────────────────
#  PASSO 3 — Rodar o projeto
# ─────────────────────────────────────────────
echo ""
echo "[3/3] Iniciando o projeto..."
echo ""
echo " Acesse no navegador: http://localhost:5173"
echo " Para encerrar pressione CTRL+C"
echo ""

npm run dev
npm install
