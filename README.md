# Titanic Survival Prediction

[![Status](https://img.shields.io/badge/status-live-brightgreen)](#)  
[![License](https://img.shields.io/github/license/Amonvix/titanic-survival-prediction)](#)  
[![Python](https://img.shields.io/badge/python-3.10-blue)](#)  
[![FastAPI](https://img.shields.io/badge/fastapi-0.95-brightgreen)](#)  
[![TensorFlow](https://img.shields.io/badge/tensorflow-2.x-orange)](#)  

## Overview

This project is a **machine learning-driven API** built with **FastAPI** to predict the survival probability of Titanic passengers. The model is trained with features like age, class, sex, fare, family relations, and port of embarkation.  
Deployed at **Fly.io**, the endpoint `/predict/` accepts JSON payload and returns survival predictions.

## Demo / Live

Access the live app here:  
🔗 https://titanic-survival-prediction.fly.dev/

Example request:

```bash
curl -X POST https://titanic-survival-prediction.fly.dev/predict/ \
  -H "Content-Type: application/json" \
  -d '{
        "age": 28,
        "sex": "male",
        "pclass": 3,
        "sibsp": 0,
        "parch": 0,
        "fare": 7.25,
        "embarked": "Southampton",
        "deck": "Unknown"
      }'

{
  "survived_probability": 0.237,
  "survived": false
}
| Component                | Technology                |
| ------------------------ | ------------------------- |
| API                      | FastAPI                   |
| Model                    | TensorFlow / scikit-learn |
| Data Processing          | pandas, NumPy             |
| Containerization         | Docker                    |
| DevOps / Hosting         | Fly.io                    |
| CI/CD (planned)          | GitHub Actions            |
| Infrastructure (planned) | Terraform                 |

[ Client / UI ] → HTTP JSON → [ FastAPI + Prediction ] → [ ML model loaded ] → Response

flowchart LR
    subgraph Dev["Dev Laptop"]
        C[Code: FastAPI + TensorFlow]
        T[Unit/API Tests]
    end

    C -->|git push| R[(GitHub Repo)]

    subgraph CI["GitHub Actions (CI/CD)"]
        A1[Lint & Type Check\nruff/mypy]
        A2[Tests\npytest + coverage]
        A3[Security Scan\npip-audit/trivy]
        A4[Build Docker Image]
        A5[Tag & Push Image\nGHCR]
        A6[Deploy to Fly.io\nflyctl]
        A7[AWS Check (Opcional)\nOIDC -> IAM Role\nPush Image p/ ECR ou Artefato p/ S3]
    end

    R -->|on: push / PR / tag| A1 --> A2 --> A3 --> A4 --> A5 --> A6
    A5 -->|image: ghcr.io/amonvix/titanic-api:sha| RT[(Runtime: Fly.io)]
    A4 --> A7

    subgraph Cloud["Runtime"]
        RT --> Svc[FastAPI /predict]
        Svc --> Model[(ML Model\nTensorFlow/Keras)]
        Svc --> Logs[(App Logs)]
        Svc --> Metrics[(Future: Prom/Grafana)]
    end

    subgraph AWS["AWS (somente para checagem)"]
        OIDC[GitHub OIDC Provider] --> IAM[IAM Role c/ Trust OIDC]
        IAM --> ECR[(ECR Repo)]
        IAM --> S3[(S3 Artifacts - opcional)]
    end

    A7 -->|assume-role| IAM
    A7 --> ECR
    A7 --> S3



Getting Started (Local)
Clone this repo:

git clone https://github.com/Amonvix/titanic-survival-prediction.git
cd titanic-survival-prediction

(Optional) Create and activate a virtual environment:
python3 -m venv venv
source venv/bin/activate

Install dependencies:
pip install -r requirements.txt

Run the app:
uvicorn main:app --reload

Test with curl (same block as above) or open localhost:8000/docs to inspect endpoints.


Docker

Build and run with Docker:
docker build -t titanic-api .
docker run -d -p 8000:8000 titanic-api
Then test with curl at http://localhost:8000/predict/.

Model Details

Trained on the classic Titanic dataset (train + test split, cross-validation).

Preprocessing includes handling missing values, encoding categorical features (sex, embarked, deck).

Model outputs both a survival probability and a binary decision (threshold 0.5).

Performance metrics (accuracy, ROC-AUC, etc.) can be added here.


Future Improvements

Add CI/CD pipelines (GitHub Actions) for testing, linting, and deployment.

Define Terraform modules to provision infra (Fly, DNS, SSL).

Add unit tests, end-to-end tests, and model drift monitoring.

Add metrics & logging (Prometheus, Grafana).

Expand dataset and explore ensemble models.


Contributing

Feel free to open issues or send pull requests.
Please follow the style guidelines and include tests for new features.

License & Credits

Licensed under the MIT License.
Built by Amon.
Thanks to open-source libraries and maintainers.















