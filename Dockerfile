# Dockerfile

FROM python:3.12.3
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libffi-dev \
    libssl-dev \
    libblas-dev \
    liblapack-dev \
    gfortran \
    && apt-get clean

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt || cat /app/requirements.txt


COPY . .

CMD ["gunicorn", "titanic_project.wsgi:application", "--bind", "0.0.0.0:8080"]


