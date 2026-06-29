# BPP Coursework - BPM Frontend Application

A containerised Python Flask web application deployed via a secure CI/CD pipeline to AWS ECS, built for a regulated financial services environment handling MNPI data.

## Architecture

```
GitHub Push
    │
    ▼
GitHub Actions Pipeline
    ├── Unit Tests (pytest)
    ├── Security Scan (pip-audit)
    ├── Static Analysis (CodeQL)
    ├── Docker Build & Push (ECR)
    ├── Infrastructure Deploy (CloudFormation)
    └── ECS Deploy (Fargate)
```

## Repository Structure

```
├── app/
│   ├── app.py                  # Flask application
│   ├── requirements.txt        # Python dependencies
│   └── tests/
│       ├── test_unit.py        # Unit tests
│       └── test_api.py         # API integration tests
├── Dockerfile                  # Hardened container definition
├── infrastructure/
│   └── cloudformation.yml      # IaC - ECS task & service definition
└── .github/
    └── workflows/
        └── cicd.yml            # GitHub Actions pipeline
```

## Pipeline Jobs

| Job | Trigger | Purpose |
|---|---|---|
| Unit Tests | Every push/PR | Validates app logic and security behaviour |
| Security Scan | Every push/PR | CVE scanning with pip-audit |
| Static Analysis | Every push/PR | SAST with GitHub CodeQL |
| Build & Push | Push to main only | Builds Docker image, pushes to ECR |
| Deploy Infrastructure | Push to main only | CloudFormation IaC deployment |
| Deploy to ECS | Push to main only | Forces new Fargate deployment |

## Required GitHub Secrets

Set these in **Settings → Secrets and variables → Actions**:

| Secret | Description |
|---|---|
| `AWS_ACCESS_KEY_ID` | AWS IAM access key |
| `AWS_SECRET_ACCESS_KEY` | AWS IAM secret key |

## Local Development

```bash
# Install dependencies
pip install -r app/requirements.txt

# Run tests
pytest app/tests/test_unit.py -v

# Run application locally
python app/app.py

# Build Docker image
docker build -t bpm-frontend .
docker run -p 80:80 bpm-frontend
```

## Security Considerations

- Slim base image (`python:3.11-slim`) minimises attack surface
- Non-root container user
- ECS tasks deployed in private subnets only
- All secrets managed via AWS Secrets Manager / GitHub Actions secrets
- Pipeline blocks deployment on CVE findings
- CloudFormation provides immutable audit trail of infrastructure changes
