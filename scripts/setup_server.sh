#!/bin/bash
# =============================================================
# Server Setup Script for Eskiz Cloud Server
# Run this once on the server to set up the environment
# Student ID: 00016042
# =============================================================

set -e

echo "Setting up Library Management System on server..."

# Update system packages
sudo apt-get update && sudo apt-get upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose plugin
sudo apt-get install -y docker-compose-plugin

# Configure UFW Firewall
sudo ufw allow 22/tcp   # SSH
sudo ufw allow 80/tcp   # HTTP
sudo ufw allow 443/tcp  # HTTPS
sudo ufw --force enable

# Create project directory
sudo mkdir -p /opt/library-management-django
sudo chown $USER:$USER /opt/library-management-django
cd /opt/library-management-django

# Clone the repository
git clone https://github.com/00016042/library-management-django.git .

# Create .env file (fill in with real values)
cat > .env << 'EOF'
SECRET_KEY=your-production-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.uz,www.yourdomain.uz
DB_NAME=library_db
DB_USER=library_user
DB_PASSWORD=your-strong-db-password
DB_HOST=db
DB_PORT=5432
EOF

echo "Server setup complete!"
echo "Next steps:"
echo "1. Edit /opt/library-management-django/.env with real values"
echo "2. Install SSL certificate with: sudo certbot certonly --webroot"
echo "3. Run: docker compose up -d"
