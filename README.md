# Truck In-N-Out Backend

A backend API for the Truck In-N-Out application, built with Django and Django REST Framework, providing endpoints for ordering, menu management, and user authentication.

---

## Tech Stack

- **Language & Framework**: Python 3.10+, Django 4.x, Django REST Framework
- **Database**: PostgreSQL (default)
- **Authentication**: JWT (using djangorestframework-simplejwt)
- **Email**: Django’s built-in email backends (SMTP, console)
- **Containerization**: Docker & Docker Compose
- **Testing**: pytest, pytest-django
- **Linting & Formatting**: flake8, isort, black

---

## Prerequisites

- **Python** ≥ 3.10
- uv
- **Docker Desktop** (https://www.docker.com/)
- **Git**

---

## Getting Started

### Clone the Repo

```bash
git clone https://github.com/<your-org>/truck-in-n-out-backend.git
cd truck-in-n-out-backend
```

### Environment Variables

Create a `.env` file first then add the environment variables:

```bash
SECRET_KEY=Secret key used by Django for cryptographic signing
DEBUG=Enables or disables Django's debug mode (`True` or
DATABASE_URL=URL for connecting to the PostgreSQL database
AWS_ACCESS_KEY=AWS access key ID for authenticating AWS services
AWS_SECRET_ACCESS_KEY=AWS secret access key for authenticating AWS servic
AWS_STORAGE_BUCKET_NAME=Name of the S3 bucket used for storing static/media
AWS_S3_SIGNATURE_VERSION=S3 signature version used for requests (e.g., `s3v4
AWS_QUERYSTRING_EXPIRE=Duration (in seconds) before S3 URL query strings e
AWS_S3_REGION_NAME=AWS region where the S3 bucket is located
DEFAULT_FILE_STORAGE=Django setting to specify default file storage back
AWS_S3_CUSTOM_DOMAIN=Custom domain for accessing S3-hosted files
RESEND_API_KEY=API key for sending emails using Resend
RESEND_HOST=Host endpoint for the Resend API
FRONTEND_DOMAIN=Domain of the frontend application
```

### Virtual Environment & Dependencies

#### Install uv first

Unix Based:

```bash
curl -LsSf https://astral.sh/uv/install.sh
```

Windows:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Run the following after installing and adding uv to path:

```bash
uv sync
```

---

## Running Docker

Ensure Docker Desktop is running, then:

```bash
docker-compose up --build
```

This will start two services:

- **web**: Django application on port 8000
- **db**: PostgreSQL database

To stop and remove containers:

```bash
docker-compose down
```

---
