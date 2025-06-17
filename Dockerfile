# ---------- Base Image ----------
FROM python:3.11-slim AS base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Create non-root user
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl netcat \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ---------- Dependencies Layer ----------
FROM base AS builder

# Install pip dependencies early for caching
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# ---------- Final Image ----------
FROM base

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY ./app /app/app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Uvicorn CMD
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
