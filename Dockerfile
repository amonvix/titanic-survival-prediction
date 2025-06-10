# Base image com Python
FROM python:3.11-slim

# Diretório de trabalho
WORKDIR /app

# Copiar arquivos de dependências primeiro para cache de build
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante do projeto
COPY . .

# Copiar o script de inicialização antes do ENTRYPOINT
COPY entrypoint.sh ./entrypoint.sh
RUN chmod +x ./entrypoint.sh

# Expor porta padrão do Django
EXPOSE 8000

# Definir o entrypoint e o comando padrão
ENTRYPOINT ["./entrypoint.sh"]
CMD ["gunicorn", "titanic_project.wsgi:application", "--bind", "0.0.0.0:8000"]

