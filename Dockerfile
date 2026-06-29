# =============================================================
# STAGE 1: Build the React frontend
# =============================================================
FROM node:20-slim AS react-build

WORKDIR /frontend

# Copy package files first for layer caching
COPY frontend/package*.json ./
RUN npm ci --silent

# Copy source and build
COPY frontend/ ./
RUN npm run build

# =============================================================
# STAGE 2: Production image - Nginx + Flask API
# Uses a minimal base to reduce attack surface (MNPI security)
# =============================================================
FROM python:3.11-slim

# Install Nginx and supervisor to manage both processes
RUN apt-get update && apt-get install -y --no-install-recommends \
    nginx \
    supervisor \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root app user
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

# Install Python dependencies
WORKDIR /app
COPY app/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy Flask API
COPY app/ ./

# Copy built React app to Nginx web root
COPY --from=react-build /frontend/dist /var/www/html

# Nginx config
COPY nginx.conf /etc/nginx/nginx.conf

# Supervisor config to manage Nginx + Gunicorn
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Set ownership
RUN chown -R appuser:appgroup /app \
    && chown -R appuser:appgroup /var/www/html \
    && chown -R appuser:appgroup /var/log/nginx \
    && chown -R appuser:appgroup /var/lib/nginx \
    && touch /run/nginx.pid && chown appuser:appgroup /run/nginx.pid

USER appuser

EXPOSE 80

# Health check via Nginx -> Flask /health proxy
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:80/health || exit 1

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
