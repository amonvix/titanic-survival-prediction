# Base image com Python
FROM python:3.11-slim

# Diretório de trabalho
WORKDIR /app

# Copiar arquivos de dependências primeiro para cache de build
COPY requirements.txt .

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante do projeto
COPY . .

# Expor porta padrão do Django
EXPOSE 8000

# Comando de execução com Gunicorn
CMD ["gunicorn", "titanic_project.wsgi:application", "--bind", "0.0.0.0:8000"]

COPY entrypoint.sh .

ENTRYPOINT ["./entrypoint.sh"]