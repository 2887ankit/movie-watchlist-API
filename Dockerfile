# ─────────────────────────────────────────────
# Stage 1 – install dependencies as (deps)
# ─────────────────────────────────────────────
FROM python:3.12-slim AS deps
WORKDIR /app

# Avoid .pyc(cache files) files and enable immediate logging by forcing unbuffered stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Installs minimal OS packages then cleans up
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
  && rm -rf /var/lib/apt/lists/*

# It maximize Docker layer caching for app dependencies
COPY requirements.txt .

# Create a virtual environment inside the image to install the Python dependencies into it
RUN python -m venv /opt/venv \
 && . /opt/venv/bin/activate \
 && pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# ─────────────────────────────────────────────
# Stage 2 – runtime
# ─────────────────────────────────────────────
FROM python:3.12-slim
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH" \
    DATABASE_URL="sqlite:///./movies.db"

# Create a non-root user for better security
RUN useradd -m -u 10001 appuser

# Copy venv from dependencies stage
COPY --from=deps /opt/venv /opt/venv

# Copy source code after dependencies to maximize cache hits
COPY src ./src

# Make sure app files are owned by the non-root user
RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 8080
CMD ["uvicorn", "app.main:app", "--app-dir", "src", "--host", "0.0.0.0", "--port", "8080"]
