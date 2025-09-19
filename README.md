# User Data Store - Kubernetes Application (EKS Deployment)

The User Data Store is a FastAPI-based microservice that exposes a RESTful API for managing user data, connected to a PostgreSQL backend. It is deployed on Amazon Elastic Kubernetes Service (EKS) with infrastructure provisioned using IaC (Infrastructure as Code) and automated deployment pipelines via GitHub Actions.

This is the **production-ready deployment** of the **User Data Store** application using **Amazon EKS**, **FastAPI**, **PostgreSQL**, and **GitHub Actions** for automated CI/CD.
This branch is optimized for **cloud-native scalability, reliability, and observability** using Kubernetes best practices.

---

## 🚧 Under Active Development 🚧
![Status](https://img.shields.io/badge/status-active--development-orange?style=for-the-badge&logo=github)
> **This repository is a work in progress. Expect frequent updates, breaking changes, and evolving features.**  

---

## 📐 Architecture Diagram (EKS)
<img width="1262" height="893" alt="diagram-export-9-18-2025-7_14_40-PM" src="https://github.com/user-attachments/assets/75f76652-c248-43d4-92fa-9a8151697ad7" />


---

## ⚙️ Technologies Used

[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/) 
[![Amazon EKS](https://img.shields.io/badge/Amazon_EKS-232F3E?style=for-the-badge&logo=amazon-eks&logoColor=white)](https://aws.amazon.com/eks/)
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)](https://github.com/features/actions)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)](https://kubernetes.io/)
[![kubectl](https://img.shields.io/badge/kubectl-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)](https://kubernetes.io/docs/reference/kubectl/)
[![AWS CloudWatch](https://img.shields.io/badge/AWS_CloudWatch-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white)](https://aws.amazon.com/cloudwatch/)
[![IaC – User‑data‑IaC](https://img.shields.io/badge/Infrastructure‑as‑Code-5A29E4?style=for-the-badge&logo=terraform&logoColor=white)](https://github.com/your-org/User-data-IaC)
* IaC – EKS infrastructure created using GitHub repo: ➡️ [User-data-IaC](https://github.com/sudarshan-rp/User-data-IaC)

---

## ⚡ Quick Start

### 1. ✅ Prerequisites

* AWS account with EKS permissions
* EKS cluster created using the IaC repo
* `kubectl` configured to point to the correct cluster
* GitHub Actions secrets configured:
  * `AWS_ACCESS_KEY_ID`
  * `AWS_SECRET_ACCESS_KEY`
  * `AWS_REGION`
  * `EKS_CLUSTER_NAME`
  * `ECR_REGISTRY_URI`

### 2. 🚀 Automated Deployment (via GitHub Actions)

Pushing to this branch triggers a GitHub Actions workflow that:
1. Builds Docker image for backend
2. Pushes it to Amazon ECR
3. Applies Kubernetes manifests (/k8s/*.yaml)
4. Verifies successful deployment
Monitor progress under the "Actions" tab in GitHub.

---

### 3. 🚀 Manual Deployment (if needed)

```bash
# Set KUBECONFIG to EKS cluster
aws eks update-kubeconfig --region <region> --name <cluster-name>

# Apply manifests in order
kubectl apply -f k8s/pvc-eks.yaml
kubectl apply -f k8s/pg16.yaml
kubectl apply -f k8s/backend.yaml
```

### 4. 🔎 Access the App

```bash
# Forward port from service to localhost
kubectl port-forward -n myapp service/backend-service 8008:8008

# Access API documentation
http://localhost:8008/docs
```

---

## 📁 Project Structure

```
├── backend/                    # FastAPI application backend
│   ├── __init__.py
│   ├── main.py                # Application entry point and FastAPI app creation
│   ├── api/                   # API layer
│   │   └── routes/            # API route definitions
│   │       ├── health_routes.py    # Health check endpoints
│   │       └── user_routes.py      # User management endpoints
│   ├── db/                    # Database layer
│   ├── models/                # Data models
│   └── services/              # Business logic layer
├── k8s/                       # Kubernetes manifests
│   ├── backend.yaml           # Backend deployment and service
│   ├── pg16.yaml              # PostgreSQL 16 deployment, service, and secrets
│   ├── pvc.yaml               # Persistent Volume Claim for standard storage
│   └── pvc-eks.yaml           # PVC for EKS clusters
├── .github/                   # GitHub workflows for automated deployment
├── Dockerfile                 # Multi-stage Docker build
├── requirements.txt           # Python dependencies
├── .dockerignore             # Docker build exclusions
└── .gitignore                # Git exclusions
```

---

## ⚙️ Environment Variables

```env
POSTGRES_HOST=postgres-service
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=testdb
DATABASE_URL=postgresql://postgres:postgres@postgres-service:5432/testdb
```
These are injected into the container via Kubernetes ConfigMaps or directly in the manifest.

---

## 🔍 Monitoring, Logs, Debugging

```bash
# Check pod status
kubectl get pods -n myapp

# Get logs from backend
kubectl logs -n myapp deployment/backend

# Get logs from DB
kubectl logs -n myapp deployment/postgres-db
```
For more debugging tools and techniques, refer to the Wiki

---

## 📚 Additional Documentation

[Backend Architecture](https://github.com/sudarshan-rp/User-data-store/wiki/Backend-Architecture)

[Best-Practices](https://github.com/sudarshan-rp/User-data-store/wiki/%F0%9F%8F%86-Best-Practices)  

[Troubleshooting](https://github.com/sudarshan-rp/User-data-store/wiki/%F0%9F%94%A7-Troubleshooting)

[Additional References](https://github.com/sudarshan-rp/User-data-store/wiki/%F0%9F%93%9A-Additional-References)

[Contributing Guide](https://github.com/sudarshan-rp/User-data-store/wiki/%F0%9F%A4%9D-Contributing-Guide)
