# Use uma imagem base oficial do Python. A versão "slim" é mais leve.
FROM python:3.10-slim

# Defina o diretório de trabalho dentro do container
WORKDIR /app

# Copie todos os arquivos do seu projeto para dentro do container
# Isso inclui app.py, requirements.txt, model.pkl e preprocessor.pkl
COPY . .

# Instale as dependências listadas no requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# O Streamlit, por padrão, roda na porta 8501. Precisamos "expor" essa porta.
EXPOSE 8501

# Adicione um health check para a Fly.io saber se seu app está saudável.
# O Streamlit tem um endpoint de saúde interno que podemos usar.
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# O comando para iniciar a aplicação Streamlit quando o container iniciar.
CMD ["streamlit", "run", "app.py"]
