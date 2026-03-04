#!/bin/bash
# =============================================================
# Production Deployment Script for Library Management System
# Student ID: 00016042
# =============================================================

set -e  # Exit on any error

echo "======================================"
echo " Library Management System Deployment"
echo "======================================"

# Navigate to project directory
cd /opt/library-management-django

# Pull latest images from Docker Hub
echo "[1/6] Pulling latest Docker images..."
docker compose pull

# Stop old containers
echo "[2/6] Stopping old containers..."
docker compose down --remove-orphans

# Start new containers in detached mode
echo "[3/6] Starting new containers..."
docker compose up -d

# Wait for PostgreSQL to be ready
echo "[4/6] Waiting for database to be ready..."
for i in {1..30}; do
    if docker compose exec -T db pg_isready -U "${DB_USER}" -d "${DB_NAME}" > /dev/null 2>&1; then
        echo "Database is ready!"
        break
    fi
    echo "Waiting... ($i/30)"
    sleep 2
done

# Run database migrations
echo "[5/6] Running database migrations..."
docker compose exec -T web python manage.py migrate --noinput

# Collect static files
echo "[6/6] Collecting static files..."
docker compose exec -T web python manage.py collectstatic --noinput

echo ""
echo "======================================"
echo " Deployment completed successfully!"
echo "======================================"
docker compose ps
