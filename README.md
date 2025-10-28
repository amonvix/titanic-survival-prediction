Titanic Survival Prediction 🧠⚙️



🚀 How We Ship – CI/CD Overview

This project follows a hybrid delivery strategy:

Continuous Integration (CI): Automatic
Continuous Deployment (CD): Manual (AWS ECS)

The goal is to ensure every commit is validated and packaged automatically,
while production releases remain under human control.

🧩 Workflow Summary
Stage	Trigger	Description
CI (Build & Test)	Every push / PR to main or develop	Runs Ruff linting, Pytest, builds the Docker image, and publishes it to GitHub Container Registry (GHCR).
CD (Deploy)	Manual (“Run workflow” in GitHub Actions)	Updates the running AWS ECS service to use a specific image version (tag).
Infra (Terraform)	Optional manual workflow	Applies or plans infrastructure changes with Terraform using OIDC authentication.
⚙️ CI Pipeline (.github/workflows/ci.yml)

Trigger:
Runs on every push or pull_request.

Steps:

Lint & format check with Ruff

Unit testing with Pytest

Build Docker image

Push image to GHCR using commit SHA as tag

Output image tag for later deployment

Resulting image:

ghcr.io/Amonvix/titanic-survival-prediction/titanic:<GIT_SHA>

🚀 CD Pipeline (.github/workflows/deploy-aws.yml)

Trigger:
Manual (GitHub Actions → “Deploy to AWS ECS (manual)” → “Run workflow”).

Inputs:

image_tag: SHA from the CI pipeline

environment: staging or production

Workflow Steps:

Authenticates with AWS using OIDC (no access keys needed)

Pulls the latest ECS task definition

Creates a new revision with the updated image

Updates ECS service and waits until it becomes stable

Production deployments can be gated with required approvals using GitHub Environments.

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

🧱 Infrastructure

Terraform defines all infrastructure resources (ECR, ECS, networking, IAM roles).
You can apply manually via a separate workflow:

Actions → Infra (Terraform)


or locally:

cd infra/terraform
terraform init
terraform plan
terraform apply

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

🔐 Required GitHub Secrets
Secret	Purpose
AWS_ROLE_TO_ASSUME	ARN of IAM Role trusted for GitHub OIDC
AWS_REGION	Region for ECS deployment
ECS_CLUSTER	ECS cluster name
ECS_SERVICE	ECS service name
ECS_TASK_FAMILY	Task definition family
ECS_CONTAINER_NAME	Container name in the ECS task
(optional) FLY_API_TOKEN	Kept for Fly.io testing or future lightweight deploys
🧭 Workflow Logic
flowchart LR
    subgraph CI["CI (Automatic)"]
        Lint[Ruff Lint]
        Test[Pytest]
        Build[Docker Build]
        Push[Push to GHCR]
    end

    subgraph CD["CD (Manual)"]
        Deploy[Deploy via ECS Update]
        Wait[Wait for Service Stability]
    end

    Lint --> Test --> Build --> Push --> Deploy --> Wait

🧩 Benefits

✅ Strong quality gate (every commit tested and linted)
✅ Immutable image versioning (tag = commit SHA)
✅ Secure AWS access via OIDC (no static keys)
✅ Manual approval before production deployment
✅ Simple rollback — redeploy previous SHA

🧠 TL;DR

We build automatically. We deploy deliberately.
This gives the team speed in development and confidence in production.

📦 Next Steps

Add coverage reporting

Automate rollback on failure

Integrate Prometheus/Grafana for metrics

Add Terraform remote backend (S3 + DynamoDB)

🧑‍💻 Author

Daniel Pedroso (Amonvix)
GitHub
 • LinkedIn

📜 License

Licensed under the MIT License.
Built with passion and precision 🧩