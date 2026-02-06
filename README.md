# Titanic Survival Prediction – ML API with FastAPI, Docker, CI/CD and Terraform

This project is a production-like Machine Learning application that predicts the probability of survival of Titanic passengers.

It includes:
- a trained ML model
- a REST API built with FastAPI
- Dockerized application
- CI/CD pipeline with GitHub Actions
- Infrastructure as Code with Terraform

> 🇧🇷 Contexto em português:  
> Este projeto não é apenas um notebook de ciência de dados. Ele demonstra o ciclo completo de um produto de ML: treino do modelo, exposição via API, empacotamento com Docker, pipeline de CI/CD e infraestrutura como código.

---

## Architecture Flow

Data -> ML Training -> Model Artifact  
Model Artifact -> FastAPI API -> Docker -> CI/CD -> Terraform (Cloud)

`[ Data ] -> [ ML Training ] -> [ Model Artifact ]`
`|`
`v`
`[ FastAPI API ]`
`|`
`v`
`[ Docker ]`
`|`
`v`
`[ CI/CD ]`
`|`
`v`
`[ Terraform ]`

> 🇧🇷 Arquitetura em PT:  
> O fluxo é de ponta a ponta: dados → treinamento do modelo → API de predição → container → pipeline → infraestrutura.

---

## Features

- Survival prediction using ML  
- REST API endpoint (/predict)  
- Input validation  
- Docker support  
- CI/CD with GitHub Actions  
- Terraform templates for cloud infrastructure  

> 🇧🇷 O que isso demonstra tecnicamente:  
> - Integração de ML com backend  
> - Deploy preparado para produção  
> - Automação de build e entrega  
> - Infraestrutura como código (IaC)

---

## Example Request

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "pclass": 3,
    "sex": "male",
    "age": 22,
    "sibsp": 1,
    "parch": 0,
    "fare": 7.25,
    "embarked": "S"
  }'
```

## Running Locally

```bash
docker build -t titanic-api .
docker run -p 8000:8000 titanic-api
```
Open in your browser:
[Swagger](http://localhost:8000/docs)

Execução local em PT:
A API é exposta via FastAPI com documentação interativa (Swagger).

## CI/CD Strategy

The CI/CD pipeline automates:

- container build  
- basic validation checks  
- packaging for deployment  

This ensures every change is validated and reproducible, reducing configuration drift and manual errors.

---

## Infrastructure as Code (Terraform)

The infrastructure layer is fully described using Terraform, enabling:

- reproducible environments  
- consistent deployments  
- cloud-agnostic design principles  

This approach reflects production-grade practices commonly used in real-world cloud architectures.

---

## Why This Project Matters (For Recruiters)

This project demonstrates the candidate’s ability to:

- Design cloud-ready architectures for ML systems  
- Bridge Data Science and Backend Engineering  
- Implement DevOps automation and Infrastructure as Code  
- Think in terms of production systems, not isolated experiments  
- Apply software engineering and architectural principles to ML workloads  

It reflects practical experience with:

- API design  
- containerization  
- CI/CD pipelines  
- cloud infrastructure modeling  
- end-to-end solution delivery  

---

## Project Status

- Functional ML model  
- API available for inference  
- Dockerized application  
- CI/CD pipelines configured  
- Terraform templates included  
- Study / portfolio project (not a commercial product)
