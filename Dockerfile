# ---------- 1) Builder stage: install deps into a portable venv ----------
FROM python:3.12-slim AS builder

# All file ops happen under /app inside the image
WORKDIR /app

# Quality-of-life envs: faster startup, no .pyc files
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# System packages only needed to build some wheels (e.g., psycopg/uvloop)
# If your deps are pure-Python/prebuilt wheels, you can remove this to slim further.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc \
  && rm -rf /var/lib/apt/lists/*

# Copy only the dependency manifest first to maximize Docker layer caching
COPY requirements.txt .

# Create a virtualenv and install Python deps into it
RUN python -m venv /venv \
 && /venv/bin/pip install --upgrade pip \
 && /venv/bin/pip install --no-cache-dir -r requirements.txt


# ---------- 2) Runtime stage: copy only what's needed to run ----------
FROM gcr.io/distroless/python3-debian12:nonroot AS runtime

# Same working directory
WORKDIR /app

RUN groupadd -r bkgroup && useradd -r -g bkgroup bkuser

# Make the builder venv the default Python on PATH
ENV PATH="/venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Bring in the virtualenv from the builder image (contains all deps)
COPY --from=builder /venv /venv

# Copy your application code (match your current structure)
COPY --chown=bkuser:bkgroup ./backend ./backend

# (Optional) if you run via a helper script; not required for uvicorn CMD below
# COPY ./run.py ./run.py

# Tell Docker (and humans) which port the app listens on inside the container
EXPOSE 8008

USER bkuser

# Start FastAPI with Uvicorn; binds to all interfaces inside the container
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8008"]
