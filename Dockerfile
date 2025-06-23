FROM python:3.11-slim

# Diretório de trabalho
WORKDIR /app

# Instala dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copia requirements e instala as libs Python
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia todo o projeto
COPY . .

# Permissão para script de entrada
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

# Porta exposta (padrão Gunicorn)
EXPOSE 8001

# Comando de inicialização
ENTRYPOINT ["./entrypoint.sh"]
