# 🧪 User Data Store – Local Development

This branch provides a local development environment for the **User Data Store** application using **Docker Compose** and **FastAPI**. It's ideal for testing and building features without needing Kubernetes.

---

## 📦 What This Branch Does

- Runs the **FastAPI backend** and **PostgreSQL** database locally using Docker Compose.
- Enables auto-reload and hot-restart for rapid backend development.
- Provides access to interactive API documentation via Swagger UI.
- Mirrors the same backend logic and API structure used in production.

---

## 🛠️ Tools & Technologies Used

- **FastAPI** – Backend web framework
- **PostgreSQL** – Local database
- **Docker Compose** – Container orchestration
- **Uvicorn** – ASGI server
- **Pydantic** – Data validation
- **pytest** – Testing

---
## 🧱 Architecture Diagram (Local)
---
## ⚡ Quick Start

### Option 1: Run via Docker Compose

```bash
# Start backend and PostgreSQL
docker-compose up --build
```

### Option 2: Run Locally (without Docker)

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run with hot reload
python run.py
```

---

## ✅ Prerequisites

* Docker
* Docker Compose
* Python 3.12+ (for non-Docker option)
* Local port 8008 and 5432 free

---

## 🚀 Accessing the Application

After running either option above:
```
Swagger UI: http://localhost:8008/docs

Health Check: http://localhost:8008/api/health
```

---

## ⚙️ Environment Variables

Defined in `docker-compose.yml` or `.env` (if using Python locally):
```
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=testdb
```

---

## 📚 Additional Documentation

[Backend Architecture](https://github.com/sudarshan-rp/User-data-store/wiki/Backend-Architecture)

[Best-Practices](https://github.com/sudarshan-rp/User-data-store/wiki/%F0%9F%8F%86-Best-Practices)  

[Troubleshooting](https://github.com/sudarshan-rp/User-data-store/wiki/%F0%9F%94%A7-Troubleshooting)

[Additional References](https://github.com/sudarshan-rp/User-data-store/wiki/%F0%9F%93%9A-Additional-References)

[Contributing Guide](https://github.com/sudarshan-rp/User-data-store/wiki/%F0%9F%A4%9D-Contributing-Guide)
