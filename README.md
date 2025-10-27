Titanic Survival Prediction 🧠⚙️














🚀 Overview

Titanic Survival Prediction is a machine learning–powered API that predicts whether a passenger would have survived the Titanic disaster based on demographic and ticket data.
Built with FastAPI and trained on the Kaggle Titanic dataset, this project serves as a foundation for a full MLOps workflow — including model training, API serving, Docker containerization, CI/CD automation, and future deployment via Fly.io and AWS ECS using Terraform.

🧩 Current Status
Component	Status	Technology
Data Processing	✅ Complete	pandas, NumPy
Model Training	✅ Functional	scikit-learn, TensorFlow
API	✅ Functional	FastAPI
Docker	✅ Ready	Dockerfile
CI/CD	🚧 In Progress	GitHub Actions
Infrastructure as Code	🚧 In Progress	Terraform (AWS ECS planned)
Deployment	🚧 Upcoming	Fly.io / AWS
Frontend	❌ Not yet implemented	
🧠 Architecture
Current Pipeline
flowchart LR
    D[Raw Titanic Data] --> P[Preprocessing & Feature Encoding]
    P --> M[Model Training - Scikit-learn / TensorFlow]
    M --> F[Model Saved as pipeline.pkl]
    F --> A[FastAPI /predict Endpoint]
    A --> R[JSON Response with Probability + Prediction]

Planned Full MLOps Flow
flowchart LR
    subgraph Dev["Local Dev"]
        Code[FastAPI + ML Training]
        Tests[Pytest / Ruff / Mypy]
    end

    Code -->|git push| Repo[(GitHub Repo)]

    subgraph CI["GitHub Actions"]
        CI1[Lint & Type Check]
        CI2[Run Tests]
        CI3[Build Docker Image]
        CI4[Push Image to GHCR/ECR]
        CI5[Deploy to Fly.io or AWS ECS]
    end

    Repo --> CI1 --> CI2 --> CI3 --> CI4 --> CI5

    subgraph Cloud["Cloud Runtime"]
        API[FastAPI App Container]
        Model[Loaded Model.pkl]
        Logs[Structured Logs]
        Metrics[Monitoring (Prometheus/Grafana - Planned)]
    end

    CI5 --> API --> Model --> Logs

📂 Project Structure
titanic-survival-prediction/
├── app/
│   ├── core/config.py
│   ├── models/
│   │   ├── predict.py
│   │   └── schemas.py
│   └── routers/main.py
│
├── data/
│   ├── titanic.csv
│   └── titanic_clean.csv
│
├── infra/
│   └── terraform/
│       ├── main.tf
│       ├── outputs.tf
│       └── provider.tf
│
├── models/pipeline.pkl
├── scripts/
│   ├── create_pipeline.py
│   ├── save_sklearn_model.py
│   └── train_model.py
│
├── aws-oidc-setup/
│   ├── policy-ecr.json
│   └── trust-policy.json
│
├── Dockerfile
├── requirements.txt
├── requirements-dev.txt
├── mypy.ini
├── pytest.ini
└── .github/workflows/ci.yml

🧪 Running Locally

Clone the repository and set up your environment:

git clone https://github.com/Amonvix/titanic-survival-prediction.git
cd titanic-survival-prediction
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt


Run the API locally:

uvicorn app.routers.main:app --reload


Then open your browser at http://localhost:8000/docs
 to access Swagger UI.

🧾 Example Request
curl -X POST http://localhost:8000/predict/ \
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


Response:

{
  "survived_probability": 0.237,
  "survived": false
}

🧱 Docker

Build and run the container:

docker build -t titanic-api .
docker run -d -p 8000:8000 titanic-api


Then test via:

curl http://localhost:8000/predict/

🧮 Model Training

The model is trained on the Kaggle Titanic dataset with preprocessing, encoding, and normalization handled by a Scikit-learn pipeline.
Trained models are serialized to models/pipeline.pkl.

Key scripts:

train_model.py — trains the model

create_pipeline.py — builds preprocessing & inference pipeline

save_sklearn_model.py — saves the model for API use

Future integration with TensorFlow will allow hybrid or ensemble training.

🧰 CI/CD & Infrastructure

CI/CD: GitHub Actions (.github/workflows/ci.yml) handles linting, testing, and build automation.

Docker Build: Prepares production-ready container image for deployment.

Terraform: Declarative IaC setup under infra/terraform for AWS ECS / ECR resources.

OIDC Setup: aws-oidc-setup/ enables secure GitHub → AWS role assumption for deployments.

Planned next steps:

✅ Add automated tests and coverage reports

✅ Push Docker image to GHCR / ECR

🚀 Deploy on Fly.io / AWS ECS via Terraform

🧭 Roadmap

 Model training and serialization

 API for prediction

 Dockerized application

 CI/CD pipeline via GitHub Actions

 Infrastructure provisioning via Terraform

 Deploy to Fly.io / AWS ECS

 Add Prometheus/Grafana metrics

 Unit & integration tests

🧑‍💻 Author

Daniel Pedroso (Amonvix)
GitHub
 • LinkedIn

📜 License

Licensed under the MIT License.
Built with passion and precision 🧩