# TravesIA Backend

Backend API for TravesIA tourism management system built with Django and Django REST Framework.

## 🛠️ Tech Stack

- **Framework**: Django 5.0 + Django REST Framework
- **Database**: PostgreSQL 15
- **Cache**: Redis 7
- **Authentication**: JWT with MFA support (TOTP)
- **API Documentation**: drf-spectacular (OpenAPI/Swagger)
- **Storage**: AWS S3 for documents
- **Task Queue**: Celery with Redis broker

## 📋 Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- virtualenv or venv

## 🚀 Quick Start

### 1. Create Virtual Environment

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # For development
```

### 3. Environment Configuration

```bash
cp .env.example .env
# Edit .env with your configuration
```

Required environment variables:

- `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`
- `SECRET_KEY`
- `REDIS_URL`
- `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` (if using S3)

### 4. Initialize Database

First, make sure PostgreSQL is running and create the database:

```bash
# From the database/ directory
cd ../database
./scripts/init_database.sh
```

### 5. Create Django Migrations

```bash
cd ../backend
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

### 7. Run Development Server

```bash
python manage.py runserver
```

The API will be available at: `http://localhost:8000`

## 📚 API Documentation

Once the server is running, access the API documentation:

- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/
- **OpenAPI Schema**: http://localhost:8000/api/schema/

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication with optional MFA (Multi-Factor Authentication).

### Login

```bash
POST /api/v1/auth/login/
{
  "email": "user@example.com",
  "password": "your_password",
  "mfa_token": "123456"  # Optional, required if MFA is enabled
}
```

Response:

```json
{
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "admin"
  },
  "tokens": {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
}
```

### Using the Access Token

Include the access token in the Authorization header:

```bash
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

### Refresh Token

```bash
POST /api/v1/auth/refresh/
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

## 👥 User Roles

The system supports 5 user roles with different permissions:

1. **Admin**: Full system access
2. **Operations Manager**: Manage groups, circuits, suppliers, operations
3. **Tour Conductor**: View and update assigned groups
4. **Accountant**: Manage financial data, invoices, costs
5. **Viewer**: Read-only access

## 📁 Project Structure

```
backend/
├── apps/
│   ├── authentication/     # User authentication and authorization
│   ├── circuits/           # Programs, groups, passengers, itineraries
│   ├── suppliers/          # Suppliers, services, pricing
│   ├── operations/         # Hotels, transportation, accommodations
│   ├── financial/          # Costs, invoices, commissions
│   └── documents/          # Document management
├── config/
│   ├── settings/
│   │   ├── base.py        # Base settings
│   │   ├── development.py # Development settings
│   │   └── production.py  # Production settings
│   ├── urls.py            # Main URL configuration
│   ├── wsgi.py            # WSGI configuration
│   └── asgi.py            # ASGI configuration
├── core/
│   └── common/            # Shared utilities, models, permissions
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
└── .env.example          # Environment variables template
```

## 🧪 Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=apps --cov-report=html

# Run specific app tests
pytest apps/authentication/tests/
```

## 🔧 Development Tools

### Code Formatting

```bash
# Format code with black
black apps/ core/ config/

# Sort imports
isort apps/ core/ config/
```

### Linting

```bash
# Run flake8
flake8 apps/ core/ config/

# Type checking with mypy
mypy apps/ core/ config/
```

### Django Shell

```bash
# Interactive shell
python manage.py shell

# Shell with iPython
python manage.py shell_plus
```

## 🐳 Docker Support

Build and run with Docker:

```bash
# Build image
docker build -t travesia-backend .

# Run container
docker run -p 8000:8000 --env-file .env travesia-backend

# Or use Docker Compose
docker-compose up
```

## 📊 Database Management

### Create Migration

```bash
python manage.py makemigrations
python manage.py makemigrations <app_name>
```

### Apply Migrations

```bash
python manage.py migrate
python manage.py migrate <app_name>
```

### Rollback Migration

```bash
python manage.py migrate <app_name> <migration_number>
```

### Show Migrations

```bash
python manage.py showmigrations
```

## 🔄 Celery Tasks

Start Celery worker:

```bash
celery -A config worker -l info
```

Start Celery beat (scheduler):

```bash
celery -A config beat -l info
```

## 📝 API Endpoints

### Authentication

- `POST /api/v1/auth/login/` - User login
- `POST /api/v1/auth/logout/` - User logout
- `POST /api/v1/auth/refresh/` - Refresh access token
- `GET /api/v1/auth/me/` - Get current user
- `PATCH /api/v1/auth/update_profile/` - Update user profile
- `POST /api/v1/auth/change_password/` - Change password
- `POST /api/v1/auth/enable_mfa/` - Enable MFA
- `POST /api/v1/auth/disable_mfa/` - Disable MFA
- `POST /api/v1/auth/verify_mfa/` - Verify MFA token

### Users (Admin only)

- `GET /api/v1/auth/users/` - List users
- `POST /api/v1/auth/users/` - Create user
- `GET /api/v1/auth/users/{id}/` - Get user details
- `PATCH /api/v1/auth/users/{id}/` - Update user
- `DELETE /api/v1/auth/users/{id}/` - Deactivate user

### Audit Logs (Admin only)

- `GET /api/v1/auth/audit/` - List audit logs
- `GET /api/v1/auth/audit/{id}/` - Get audit log details

### Circuits (Coming Soon)

- Programs, Groups, Passengers, Itineraries, Flights

### Suppliers (Coming Soon)

- Suppliers, Services, Price Periods, Exchange Rates

### Operations (Coming Soon)

- Hotels, Transportation, Accommodations, Special Services, Staff

### Financial (Coming Soon)

- Group Costs, Additional Sales, Invoices, Commissions, Deposits

### Documents (Coming Soon)

- Document upload, download, management

## 🐛 Troubleshooting

### Database Connection Error

```bash
# Check PostgreSQL is running
pg_isready

# Check connection
psql -U postgres -h localhost -d travesia
```

### Redis Connection Error

```bash
# Check Redis is running
redis-cli ping
# Should return: PONG
```

### Migration Issues

```bash
# Reset migrations (WARNING: deletes all data)
python manage.py migrate <app_name> zero
python manage.py migrate
```

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Run tests and linting
4. Submit a pull request

## 📄 License

Proprietary - All rights reserved

## 📧 Support

For support, contact the development team.
