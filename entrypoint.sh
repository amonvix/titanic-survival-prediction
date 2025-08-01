#!/bin/sh

# Sairá imediatamente se um comando falhar
set -e

# 1. Coleta os arquivos estáticos (CSS, JS, Imagens)
echo "Collecting static files..."
python manage.py collectstatic --noinput

# 2. Aplica as migrações do banco de dados
echo "Applying database migrations..."
python manage.py migrate

# 3. Carrega dados iniciais (opcional, mas mantido do seu script)
echo "Loading initial data..."
if ! python manage.py loaddata initial_data.json; then
    echo "Warning: Failed to load initial_data.json. Continuing without it." >&2
fi

# 4. Inicia o servidor Gunicorn com o worker Uvicorn (para ASGI)
echo "Starting Gunicorn server..."
exec gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:$PORT titanic_project.asgi:application