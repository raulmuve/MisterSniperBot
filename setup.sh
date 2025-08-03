#!/bin/bash

set -e

echo "🔧 Actualizando sistema..."
sudo apt update && sudo apt upgrade -y

echo "📦 Instalando dependencias del sistema..."
sudo apt install -y \
    python3 python3-pip python3-venv \
    libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libxkbcommon0 \
    libgtk-3-0 libdrm2 libxcomposite1 libxdamage1 libxrandr2 \
    libgbm1 libasound2 libxshmfence1 libxss1 libx11-xcb1 \
    ca-certificates wget curl fonts-liberation xvfb

echo "🐍 Creando entorno virtual..."
python3 -m venv .venv
source .venv/bin/activate

echo "⬆️ Actualizando pip..."
pip install --upgrade pip

echo "📦 Instalando requirements.txt..."
pip install -r requirements.txt

echo "📥 Instalando navegadores de Playwright..."
playwright install

echo "✅ Todo listo. Para activar el entorno virtual, ejecuta:"
echo "source .venv/bin/activate"
