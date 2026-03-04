# Library Management System

A fully-featured Django web application for managing library books, authors, members, and book borrowing operations. Deployed with Docker, Nginx, and PostgreSQL using a complete CI/CD pipeline via GitHub Actions.

**Student ID:** 00016042 | **Module:** Distributed Systems and Cloud Computing

---

## Features

- **User Authentication** – Register, login, logout with session management
- **Book Management** – Full CRUD: add, view, edit, delete books with cover images
- **Author Management** – Author profiles with biographical information
- **Category System** – Books organized by categories (many-to-many)
- **Borrowing System** – Borrow and return books with due dates and status tracking
- **Member Profiles** – Auto-generated member IDs and profile management
- **Admin Panel** – Django admin interface for superuser management
- **Search & Filter** – Search books by title, author, ISBN, or category
- **Pagination** – Paginated book listings
- **Responsive UI** – Bootstrap 5 responsive design

---

## Technologies Used

| Category | Technology |
|----------|-----------|
| Backend | Django 4.2, Python 3.11 |
| Database | PostgreSQL 15 |
| Web Server | Nginx 1.25 |
| Application Server | Gunicorn |
| Containerization | Docker, Docker Compose |
| CI/CD | GitHub Actions |
| Registry | Docker Hub |
| Cloud | Eskiz Server (Ubuntu 22.04) |
| SSL | Let's Encrypt (Certbot) |
| Frontend | Bootstrap 5, Font Awesome |

---

## Database Schema

```
User (Django built-in)
  └── Member (OneToOne)
        └── BorrowRecord (Many) ─── Book (Many-to-One) ─── Author
                                                     └── Category (Many-to-Many)
```

### Models
- **Author** – `first_name`, `last_name`, `bio`, `birth_date`, `photo`
- **Category** – `name`, `slug`, `description`
- **Book** – `title`, `isbn`, `description`, `published_date`, `author` (FK), `categories` (M2M), `available_copies`, `cover_image`
- **Member** – `user` (OneToOne), `phone`, `address`, `member_id`, `membership_date`
- **BorrowRecord** – `book` (FK), `member` (FK), `borrow_date`, `due_date`, `return_date`, `status`

---

## Local Setup Instructions

### Prerequisites
- Docker Desktop installed and running
- Git

### Quick Start

```bash
# Clone the repository
git clone https://github.com/00016042/library-management-django.git
cd library-management-django

# Copy environment file
cp .env.example .env
# Edit .env with your values (see Environment Variables section)

# Build and start all services
docker compose up --build -d

# The application will be running at http://localhost
```

### Create Superuser (Admin)

```bash
docker compose exec web python manage.py createsuperuser
```

### Access
- **Application:** http://localhost
- **Admin Panel:** http://localhost/admin/

---

## Deployment Instructions

### Server Requirements
- Ubuntu 22.04 LTS
- Minimum 1GB RAM, 20GB storage
- Public IP address

### Step 1: Server Setup
```bash
# SSH into your server
ssh user@your-server-ip

# Download and run setup script
wget https://raw.githubusercontent.com/00016042/library-management-django/main/scripts/setup_server.sh
chmod +x setup_server.sh
./setup_server.sh
```

### Step 2: Configure Environment
```bash
# Edit the .env file on server
nano /opt/library-management-django/.env
```

### Step 3: SSL Certificate
```bash
# Install Certbot
sudo apt install certbot -y

# Get SSL certificate
sudo certbot certonly --standalone -d yourdomain.uz

# Update nginx.conf with your domain
```

### Step 4: Start Services
```bash
cd /opt/library-management-django
docker compose up -d
```

---

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | `django-insecure-...` |
| `DEBUG` | Debug mode (False in prod) | `False` |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts | `yourdomain.uz,www.yourdomain.uz` |
| `DB_NAME` | PostgreSQL database name | `library_db` |
| `DB_USER` | PostgreSQL username | `library_user` |
| `DB_PASSWORD` | PostgreSQL password | `strongpassword` |
| `DB_HOST` | Database host (use `db` for Docker) | `db` |
| `DB_PORT` | PostgreSQL port | `5432` |

### GitHub Secrets (for CI/CD)
| Secret | Description |
|--------|-------------|
| `DOCKERHUB_USERNAME` | Docker Hub username |
| `DOCKERHUB_TOKEN` | Docker Hub access token |
| `SSH_PRIVATE_KEY` | SSH private key for server access |
| `SSH_HOST` | Server IP address |
| `SSH_USERNAME` | Server SSH username |

---

## CI/CD Pipeline

The GitHub Actions pipeline (`.github/workflows/deploy.yml`) runs on every push to `main`:

1. **Lint** – flake8 code quality check
2. **Test** – pytest-django runs all tests against PostgreSQL
3. **Build** – Docker image built with multi-stage build
4. **Push** – Image tagged (`latest` + commit SHA) and pushed to Docker Hub
5. **Deploy** – SSH into server, pull new images, restart services, run migrations

---

## Project Structure

```
library-management-django/
├── .github/workflows/deploy.yml   # CI/CD pipeline
├── app/
│   ├── library/                   # Django project settings & URLs
│   ├── books/                     # Books, Authors, Members, Borrowing
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── forms.py
│   │   ├── admin.py
│   │   └── tests.py
│   ├── accounts/                  # User authentication
│   ├── templates/                 # HTML templates
│   ├── static/                    # CSS, JS, Images
│   ├── requirements.txt
│   ├── manage.py
│   └── pytest.ini
├── nginx/nginx.conf               # Nginx configuration
├── scripts/                       # Deployment scripts
├── Dockerfile                     # Multi-stage Docker build
├── docker-compose.yml             # Production compose
├── docker-compose.dev.yml         # Development compose
├── .env.example                   # Environment variables template
├── .dockerignore
├── .gitignore
└── README.md
```

---

## Running Tests

```bash
# Run tests inside Docker
docker compose exec web pytest books/tests.py -v

# Run tests locally (requires virtual environment)
cd app
pip install -r requirements.txt
pytest books/tests.py -v
```

---

## Test Credentials

| Role | Username | Password |
|------|----------|----------|
| Admin | admin | admin123 |
| Test User | testmember | member123 |

---

## Screenshots

*(Screenshots of running application are included in the technical report)*

---

## Live Access

- **Application URL:** https://yourdomain.uz
- **GitHub Repository:** https://github.com/00016042/library-management-django
- **Docker Hub:** https://hub.docker.com/r/kozimbek/library-management-django
