#!/bin/bash

# Script para ejecutar el bot de Discord

echo "🤖 Iniciando Bot de Discord..."

# Verificar si existe el entorno virtual
if [ ! -d ".venv" ]; then
    echo "❌ Entorno virtual no encontrado"
    echo "🔧 Ejecuta primero: ./setup.sh"
    exit 1
fi

# Verificar si existe .env
if [ ! -f ".env" ]; then
    echo "❌ Archivo .env no encontrado"
    echo "📄 Copia .env.example a .env y configura tu token"
    exit 1
fi

# Activar entorno virtual
source .venv/bin/activate

# Verificar que las dependencias estén instaladas
if ! python -c "import discord" 2>/dev/null; then
    echo "📦 Instalando dependencias faltantes..."
    pip install -r requirements.txt
fi

# Ejecutar el bot
echo "🚀 Iniciando bot..."
python botdiscord.py
