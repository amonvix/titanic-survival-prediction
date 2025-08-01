# Etapa 1: Build de dependências (evita imagem gigante)
FROM python:3.10-slim AS builder

# Diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema necessárias para compilar pacotes Python
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar apenas requirements primeiro (melhora cache do Docker)
COPY requirements.txt .

# Criar venv para instalação isolada (reduz tamanho final)
RUN python -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-cache-dir --upgrade pip \
    && /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# Etapa 2: Imagem final enxuta
FROM python:3.10-slim

# Adicionar venv ao PATH
ENV PATH="/opt/venv/bin:$PATH"

# Diretório de trabalho
WORKDIR /app

# Copiar venv da etapa anterior
COPY --from=builder /opt/venv /opt/venv

# Copiar o projeto
COPY . .

# Variáveis Fly.io
EXPOSE 8000
ENV PORT 8000

# Coletar arquivos estáticos (caso use admin)
RUN python manage.py collectstatic --noinput || true

# Comando para iniciar Gunicorn com UvicornWorker
CMD ["gunicorn", "app.asgi:application", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
