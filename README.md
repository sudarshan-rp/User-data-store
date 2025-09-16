# User Data Store - Kubernetes Application 

A User-data-store FastAPI application designed for deployment on Kubernetes (EKS) with PostgreSQL database backend. Automated deployment via GitHub Actions. With observability.

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
│   ├── pvc-k3.yaml            # PVC for K3s clusters
│   └── pvc-eks.yaml           # PVC for EKS clusters
├── .github/                   # GitHub workflows for automated deployment
├── Dockerfile                 # Multi-stage Docker build
├── docker-compose.yml         # Local development with Docker Compose
├── requirements.txt           # Python dependencies
├── run.py                     # Local development server
├── .dockerignore             # Docker build exclusions
└── .gitignore                # Git exclusions
```

## 🚀 Quick Start

### Prerequisites
- AWS EKS cluster (deployed via GitHub Actions)
  Use this repo for creating EKS cluster using IaC, automated with actions -- **https://github.com/sudarshan-rp/User-data-IaC.git**
- kubectl configured for EKS cluster
- GitHub repository with proper AWS credentials configured

### 1. Automated Deployment via GitHub Actions
The application is automatically deployed to EKS when changes are pushed to this branch.

### 2. Manual Deployment (if needed)
```bash
# Apply Kubernetes manifests to EKS
kubectl apply -f k8s/pvc-eks.yaml  # Use EKS-specific PVC
kubectl apply -f k8s/pg16.yaml
kubectl apply -f k8s/backend.yaml
```

### 3. Access the Application
```bash
# Port forward to access the backend
kubectl port-forward -n myapp service/backend-service 8008:8008

# Access the API documentation
open http://localhost:8008/docs
```

## 📋 File Details

### Core Application Files

#### `backend/main.py`
- **Purpose**: FastAPI application factory and configuration
- **Features**:
  - Application lifespan management
  - Database connection handling
  - Route registration
  - API documentation setup
- **Key Components**:
  - Creates FastAPI app with title "User Data Store API"
  - Includes health and user route modules
  - Manages database lifecycle (connect/disconnect)

#### `run.py`
- **Purpose**: Local development server launcher
- **Features**:
  - Automatically opens browser to API docs
  - Runs on `127.0.0.1:8083` with hot reload
  - Concurrent browser opening using threading

#### `requirements.txt`
- **Purpose**: Python dependency specification
- **Key Dependencies**:
  - `fastapi==0.115.13` - Web framework
  - `uvicorn==0.34.3` - ASGI server
  - `asyncpg==0.30.0` - Async PostgreSQL driver
  - `psycopg2-binary==2.9.10` - PostgreSQL adapter
  - `pydantic==1.10.22` - Data validation
  - `pytest==8.4.1` - Testing framework

### Docker Configuration

#### `Dockerfile`
- **Purpose**: Multi-stage Docker build for production
- **Stages**:
  1. **Builder**: Installs dependencies in virtual environment
  2. **Runtime**: Copies only necessary files for minimal image
- **Features**:
  - Python 3.12 slim base image
  - Virtual environment isolation
  - Build-time dependency caching
  - Exposes port 8008
  - Production-ready with uvicorn server

#### `docker-compose.yml`
- **Purpose**: Local development environment
- **Services**:
  - **backend**: FastAPI application (port 8008)
  - **db**: PostgreSQL 15 database
- **Features**:
  - Environment variable configuration
  - Persistent volume for database
  - Service dependency management

### Kubernetes Manifests

#### `k8s/pg16.yaml`
- **Purpose**: PostgreSQL 16 database deployment
- **Components**:
  - **Namespace**: `myapp` - Application namespace
  - **Deployment**: Single replica PostgreSQL 16
  - **Service**: ClusterIP service on port 5432
  - **Secret**: Database credentials (postgres/postgres/testdb)
  - **Volume**: Persistent storage with subPath for data isolation
- **Configuration**:
  - Uses secrets for secure credential management
  - Persistent volume claim for data persistence
  - SubPath mounting to avoid permission issues

#### `k8s/backend.yaml`
- **Purpose**: FastAPI backend deployment
- **Components**:
  - **Deployment**: Single replica backend service
  - **Service**: ClusterIP service on port 8008
- **Configuration**:
  - Uses public ECR image: `public.ecr.aws/a8e5a3z9/backend:latest`
  - Environment variables for database connection
  - Connects to PostgreSQL via `postgres-service`

#### `k8s/pvc.yaml`
- **Purpose**: Persistent Volume Claim for standard Kubernetes clusters
- **Specifications**:
  - **Storage**: 5Gi
  - **Access Mode**: ReadWriteOnce
  - **Storage Class**: `standard`

#### `k8s/pvc-eks.yaml`
- **Purpose**: Persistent Volume Claim optimized for EKS
- **Specifications**: EKS-specific storage class configuration

#### `k8s/pvc-k3.yaml`
- **Purpose**: Alternative PVC configuration for K3s clusters
- **Usage**: Lightweight Kubernetes distribution compatibility

## 🛠️ Development Workflow

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run locally with auto-reload
python run.py
```

### Docker Development
```bash
# Build and run with Docker Compose
docker-compose up --build
```

### EKS Deployment via GitHub Actions
1. Push changes to the repository
2. GitHub Actions automatically builds and deploys to EKS
3. Monitor deployment status in GitHub Actions tab

### Manual EKS Deployment
```bash
# Configure kubectl for EKS
aws eks update-kubeconfig --region <region> --name <cluster-name>

# Apply manifests
kubectl apply -f k8s/pvc-eks.yaml  # Use EKS-specific storage class
kubectl apply -f k8s/pg16.yaml
kubectl apply -f k8s/backend.yaml
```

## 🔧 Configuration

### Environment Variables
- `DATABASE_URL`: PostgreSQL connection string
- `POSTGRES_HOST`: Database host (default: postgres-service)
- `POSTGRES_PORT`: Database port (default: 5432)
- `POSTGRES_USER`: Database username
- `POSTGRES_PASSWORD`: Database password
- `POSTGRES_DB`: Database name

### Database Configuration
- **Default Credentials**: postgres/postgres/testdb
- **Port**: 5432
- **Storage**: 5Gi persistent volume
- **Version**: PostgreSQL 16

## 📊 API Endpoints

### Health Routes (`/api`)
- Health check endpoints for monitoring application status

### User Routes (`/users`)
- User management functionality
- CRUD operations for user data

### API Documentation
- **Swagger UI**: `http://localhost:8008/docs`
- **ReDoc**: `http://localhost:8008/redoc`

## 🔍 Monitoring & Debugging

### Check Pod Status
```bash
kubectl get pods -n myapp
kubectl logs -n myapp deployment/backend
kubectl logs -n myapp deployment/postgres-db
```

### Database Access
```bash
kubectl exec -it -n myapp deployment/postgres-db -- psql -U postgres -d testdb
```

### Service Testing
```bash
kubectl port-forward -n myapp service/backend-service 8008:8008
curl http://localhost:8008/api/health
```

## 🚀 Production Considerations

1. **Security**: Update default database credentials in production
2. **Scaling**: Configure Horizontal Pod Autoscaler (HPA) for backend services
3. **Storage**: Use EKS-optimized storage classes (gp3, io1, etc.)
4. **Monitoring**: Implement CloudWatch monitoring and logging
5. **Secrets**: Use AWS Secrets Manager or Kubernetes secrets
6. **Ingress**: Configure ALB Ingress Controller for external access
7. **High Availability**: Deploy across multiple AZs
8. **Backup**: Configure automated database backups

## 📝 Notes

- This application is designed for EKS deployment via GitHub Actions
- Uses EKS-optimized storage classes for production workloads
- Includes multiple PVC options for different Kubernetes distributions
- Database uses subPath mounting to avoid common permission issues
- Application follows user-data-store architecture pattern (API, Business Logic, Data)
- Automated CI/CD pipeline handles building and deployment to EKS

## 🔧 Troubleshooting

### Common Issues

#### Pod Startup Issues
```bash
# Check pod status and events
kubectl get pods -n myapp
kubectl describe pod <pod-name> -n myapp
kubectl logs <pod-name> -n myapp

# Check resource constraints
kubectl top pods -n myapp
kubectl describe nodes
```

#### Database Connection Issues
```bash
# Test database connectivity
kubectl exec -it -n myapp deployment/postgres-db -- pg_isready -U postgres

# Check database logs
kubectl logs -n myapp deployment/postgres-db

# Verify service endpoints
kubectl get endpoints -n myapp
```

#### Storage Issues
```bash
# Check PVC status
kubectl get pvc -n myapp
kubectl describe pvc postgres-pvc -n myapp

# Check storage class
kubectl get storageclass
```

#### Network Issues
```bash
# Test service connectivity
kubectl exec -it -n myapp deployment/backend -- curl http://postgres-service:5432

# Check service configuration
kubectl get svc -n myapp
kubectl describe svc backend-service -n myapp
```

### Performance Issues
```bash
# Monitor resource usage
kubectl top pods -n myapp
kubectl top nodes

# Check application metrics
kubectl port-forward -n myapp service/backend-service 8008:8008
curl http://localhost:8008/api/health
```

## 📚 Additional References

### FastAPI Documentation
- [FastAPI Official Docs](https://fastapi.tiangolo.com/)
- [FastAPI Best Practices](https://github.com/zhanymkanov/fastapi-best-practices)
- [Async Programming with FastAPI](https://fastapi.tiangolo.com/async/)

### Kubernetes Resources
- [Kubernetes Official Documentation](https://kubernetes.io/docs/)
- [EKS User Guide](https://docs.aws.amazon.com/eks/latest/userguide/)
- [Kubernetes Best Practices](https://kubernetes.io/docs/concepts/configuration/overview/)

### PostgreSQL Resources
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [PostgreSQL on Kubernetes](https://kubernetes.io/docs/tutorials/stateful-application/postgresql/)
- [Database Performance Tuning](https://wiki.postgresql.org/wiki/Performance_Optimization)

### Docker & Containerization
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Multi-stage Builds](https://docs.docker.com/develop/dev-best-practices/#use-multi-stage-builds)
- [Container Security](https://kubernetes.io/docs/concepts/security/)

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Set up local development environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

### Code Standards
- Follow PEP 8 style guidelines
- Use type hints for all function parameters and return values
- Write docstrings for all public functions and classes
- Maintain test coverage above 80%

### Testing
```bash
# Run tests locally
pytest

# Run with coverage
pytest --cov=backend --cov-report=html

# Run specific test file
pytest tests/test_user_routes.py
```

### Pull Request Process
1. Ensure all tests pass
2. Update documentation if needed
3. Add/update tests for new functionality
4. Submit PR with clear description of changes
5. Ensure CI/CD pipeline passes

### Commit Message Format
```
type(scope): brief description

Detailed explanation of changes (if needed)

Fixes #issue-number
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

## 🏆 Best Practices

### Application Development
- **Separation of Concerns**: Keep API routes, business logic, and data access separate
- **Environment Configuration**: Use environment variables for all configuration
- **Error Handling**: Implement comprehensive error handling and logging
- **Input Validation**: Validate all input data using Pydantic models
- **API Versioning**: Version your APIs for backward compatibility

### Database Management
- **Connection Pooling**: Use connection pooling for better performance
- **Migrations**: Implement database migration strategy
- **Backup Strategy**: Regular automated backups
- **Indexing**: Proper database indexing for query performance
- **Security**: Use least privilege principle for database access

### Kubernetes Deployment
- **Resource Limits**: Always set resource requests and limits
- **Health Checks**: Implement liveness and readiness probes
- **Secrets Management**: Never store secrets in plain text
- **Namespace Isolation**: Use namespaces for environment separation
- **Rolling Updates**: Configure rolling update strategy

### Security Best Practices
- **Image Scanning**: Scan container images for vulnerabilities
- **Network Policies**: Implement Kubernetes network policies
- **RBAC**: Use Role-Based Access Control
- **TLS Encryption**: Enable TLS for all communications
- **Regular Updates**: Keep dependencies and base images updated

### Monitoring & Observability
- **Structured Logging**: Use structured JSON logging
- **Metrics Collection**: Implement application metrics
- **Distributed Tracing**: Add tracing for request flows
- **Alerting**: Set up proactive alerting
- **Dashboard**: Create monitoring dashboards

### CI/CD Best Practices
- **Automated Testing**: Run tests on every commit
- **Security Scanning**: Include security scans in pipeline
- **Environment Parity**: Keep dev/staging/prod environments similar
- **Rollback Strategy**: Implement automated rollback capabilities
- **Blue-Green Deployment**: Consider blue-green deployment strategy
