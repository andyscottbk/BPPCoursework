# Use slim base image to minimise attack surface - critical for MNPI security
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Create non-root user for security - containers should not run as root
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

# Copy and install dependencies first (layer caching)
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY app/ .

# Set ownership to non-root user
RUN chown -R appuser:appgroup /app
USER appuser

# Inform orchestrator of listening port
EXPOSE 80

# Health check for container orchestration
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:80/health')" || exit 1

# Use gunicorn for production - not Flask dev server
CMD ["gunicorn", "--bind", "0.0.0.0:80", "--workers", "2", "--timeout", "60", "app:app"]
