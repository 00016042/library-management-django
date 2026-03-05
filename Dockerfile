# Stage 1: Builder - install dependencies
FROM python:3.11-slim AS builder

WORKDIR /app

# Install system dependencies for building Python packages
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install into a virtual environment
COPY app/requirements.txt .
RUN pip install --upgrade pip && \
    pip install --prefix=/install --no-cache-dir -r requirements.txt

# Stage 2: Production - minimal runtime image

FROM python:3.11-slim AS production

WORKDIR /app

# Install only runtime system dependencies (no build tools)
RUN apt-get update && apt-get install -y \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder stage
COPY --from=builder /install /usr/local

# Create non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser -d /app -s /sbin/nologin appuser

# Copy application code
COPY app/ .

# Create necessary directories and set permissions
RUN mkdir -p /app/staticfiles /app/media && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Collect static files and start Gunicorn
CMD ["sh", "-c", "python manage.py collectstatic --noinput && \
     python manage.py migrate --noinput && \
     gunicorn library.wsgi:application \
     --bind 0.0.0.0:8000 \
     --workers 3 \
     --timeout 120 \
     --access-logfile - \
     --error-logfile -"]
