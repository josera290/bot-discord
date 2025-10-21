#!/bin/bash

# Script para configurar el entorno de desarrollo

echo "🚀 Configurando entorno de desarrollo para Bot de Discord..."

# Crear entorno virtual si no existe
if [ ! -d ".venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv .venv
fi

# Activar entorno virtual
echo "⚡ Activando entorno virtual..."
source .venv/bin/activate

# Instalar dependencias
echo "📋 Instalando dependencias..."
pip install -r requirements.txt

# Verificar si existe .env
if [ ! -f ".env" ]; then
    echo "⚠️  Archivo .env no encontrado"
    echo "📄 Copiando .env.example a .env..."
    cp .env.example .env
    echo "✏️  Por favor, edita el archivo .env y agrega tu token de Discord"
    echo "🔗 Obten tu token en: https://discord.com/developers/applications"
else
    echo "✅ Archivo .env encontrado"
fi

echo ""
echo "🎉 ¡Setup completado!"
echo ""
echo "📝 Próximos pasos:"
echo "1. Edita el archivo .env con tu token de Discord"
echo "2. Ejecuta: ./run.sh para iniciar el bot"
echo "   O ejecuta: source .venv/bin/activate && python botdiscord.py"
