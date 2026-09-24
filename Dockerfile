# ==============================================================================
# Linux Command Simulator & RHCSA 9 Hub - Production Dockerfile
# ==============================================================================

FROM python:3.11-slim

# Prevent Python from writing .pyc files and enable live stdout logging
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5050

WORKDIR /app

# Install curl for container healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies first (leveraging Docker layer cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create a secure non-root user
RUN groupadd -g 1001 appuser && \
    useradd -u 1001 -g appuser -s /bin/bash -m appuser

# Copy application source code
COPY . .

# Set permissions for non-root user
RUN chown -R appuser:appuser /app

# Switch to non-root execution
USER appuser

# Expose web application port
EXPOSE 5050

# Container Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5050/api/stats || exit 1

# Start Flask web server
CMD ["python", "app.py"]
