#!/bin/bash

# Parar execução se algum comando falhar
set -e

# Aplicar migrations
echo "⏳ Applying database migrations..."
python manage.py migrate --noinput

# Coletar arquivos estáticos (se estiver usando)
echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

# Iniciar servidor Gunicorn
echo "🚀 Starting server..."
exec gunicorn titanic_project.wsgi:application --bind 0.0.0.0:8000
