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
