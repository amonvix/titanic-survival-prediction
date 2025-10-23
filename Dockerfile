# 📍 Caminho: Dockerfile

FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Instala gcc para dependências que precisam compilar
RUN apt-get update && apt-get install -y --no-install-recommends gcc \
    && rm -rf /var/lib/apt/lists/*

# Instala as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copia o restante do projeto
COPY . .

# Expõe a porta 8000
EXPOSE 8000

# Comando para rodar o Django (modo desenvolvimento por enquanto)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
