FROM python:3.10-slim

# Define workdir
WORKDIR /app

# Evita cache do pip e reduz tamanho
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instala dependências de sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia requirements e instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o projeto
COPY . .

# Porta usada pelo Fly
EXPOSE 8080

# Comando de produção com Gunicorn
CMD ["gunicorn", "app.wsgi:application", "--bind", "0.0.0.0:8080"]
