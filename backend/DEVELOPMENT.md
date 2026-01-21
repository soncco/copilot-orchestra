# Backend API - Guía de Desarrollo

## 📖 Índice

1. [Estructura del Proyecto](#estructura-del-proyecto)
2. [Modelos de Datos](#modelos-de-datos)
3. [Endpoints de API](#endpoints-de-api)
4. [Autenticación y Autorización](#autenticación-y-autorización)
5. [Workflows Comunes](#workflows-comunes)
6. [Testing](#testing)
7. [Deployment](#deployment)

## Estructura del Proyecto

El backend sigue una arquitectura **Monolito Modular** organizada por bounded contexts:

```
backend/
├── apps/                       # Django applications
│   ├── authentication/        # Autenticación y usuarios
│   │   ├── models.py         # User, UserSession, AuditLog
│   │   ├── serializers.py    # UserSerializer, LoginSerializer, etc.
│   │   ├── views.py          # AuthViewSet, UserViewSet
│   │   └── urls.py
│   ├── circuits/             # Gestión de circuitos
│   │   ├── models.py         # Program, Group, Passenger, Itinerary, Flight
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── suppliers/            # Proveedores (TODO)
│   ├── operations/           # Operaciones (TODO)
│   ├── financial/            # Financiero (TODO)
│   └── documents/            # Documentos (TODO)
├── config/                    # Configuración Django
│   ├── settings/
│   │   ├── base.py           # Configuración base
│   │   ├── development.py    # Desarrollo
│   │   └── production.py     # Producción
│   ├── urls.py               # URLs principales
│   └── wsgi.py
├── core/                      # Código compartido
│   └── common/
│       ├── models.py         # TimeStampedModel, SoftDeleteModel
│       ├── exceptions.py     # Excepciones personalizadas
│       ├── permissions.py    # Permisos basados en roles
│       ├── pagination.py     # Clases de paginación
│       └── utils.py          # Utilidades
└── manage.py
```

## Modelos de Datos

### Authentication App

#### User

```python
- id: UUID (PK)
- email: EmailField (unique)
- first_name, last_name: CharField
- role: ['admin', 'operations_manager', 'tour_conductor', 'accountant', 'viewer']
- mfa_enabled: Boolean
- mfa_secret: CharField
```

#### UserSession

```python
- id: UUID (PK)
- user: FK(User)
- token: CharField
- ip_address: GenericIPAddressField
- expires_at: DateTimeField
```

#### AuditLog

```python
- id: UUID (PK)
- user: FK(User)
- action: ['login', 'logout', 'create', 'update', 'delete', ...]
- resource_type: CharField
- resource_id: CharField
- metadata: JSONField
```

### Circuits App

#### Program

```python
- id: UUID (PK)
- code: CharField (unique)
- name: CharField
- duration_days: Integer
- base_price: Decimal
- status: ['draft', 'active', 'archived']
```

#### Group

```python
- id: UUID (PK)
- code: CharField (unique)
- program: FK(Program)
- start_date, end_date: DateField
- tour_conductor: FK(User, null=True)
- status: ['planning', 'confirmed', 'in_progress', 'completed', 'cancelled']
- current_passengers: Integer
- max_passengers: Integer
```

#### Passenger

```python
- id: UUID (PK)
- group: FK(Group)
- first_name, last_name: CharField
- document_type: ['dni', 'passport', 'ruc', 'other']
- document_number: CharField
- status: ['reserved', 'confirmed', 'cancelled', 'no_show']
- base_price, total_price: Decimal
```

#### Itinerary

```python
- id: UUID (PK)
- group: FK(Group)
- day_number: Integer
- date: DateField
- title, description, location: CharField/TextField
- breakfast_included, lunch_included, dinner_included: Boolean
```

#### Flight

```python
- id: UUID (PK)
- group: FK(Group)
- flight_type: ['outbound', 'return', 'domestic']
- airline, flight_number: CharField
- departure/arrival_airport, city, country: CharField
- departure/arrival_datetime: DateTimeField
```

## Endpoints de API

### Documentación Interactiva

- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/
- **OpenAPI Schema**: http://localhost:8000/api/schema/

### Authentication (`/api/v1/auth/`)

```
POST   /login/                  # Login
POST   /logout/                 # Logout
POST   /refresh/                # Refresh token
GET    /me/                     # Get current user
PATCH  /update_profile/         # Update profile
POST   /change_password/        # Change password
POST   /enable_mfa/             # Enable MFA
POST   /verify_mfa/             # Verify MFA token
POST   /disable_mfa/            # Disable MFA
```

### Users (`/api/v1/auth/users/`)

```
GET    /                        # List users (admin only)
POST   /                        # Create user (admin only)
GET    /{id}/                   # Get user (admin only)
PATCH  /{id}/                   # Update user (admin only)
DELETE /{id}/                   # Deactivate user (admin only)
```

### Programs (`/api/v1/circuits/programs/`)

```
GET    /                        # List programs
POST   /                        # Create program
GET    /{id}/                   # Get program
PATCH  /{id}/                   # Update program
DELETE /{id}/                   # Delete program
GET    /{id}/groups/            # Get groups for program
```

### Groups (`/api/v1/circuits/groups/`)

```
GET    /                        # List groups
POST   /                        # Create group
GET    /{id}/                   # Get group (with passengers, flights, itinerary)
PATCH  /{id}/                   # Update group
DELETE /{id}/                   # Delete group
GET    /{id}/passengers/        # Get passengers for group
GET    /{id}/itinerary/         # Get itinerary for group
GET    /{id}/flights/           # Get flights for group
PATCH  /{id}/update_status/     # Update group status
```

### Passengers (`/api/v1/circuits/passengers/`)

```
GET    /                        # List passengers
POST   /                        # Create passenger
GET    /{id}/                   # Get passenger
PATCH  /{id}/                   # Update passenger
DELETE /{id}/                   # Delete passenger
POST   /import_passengers/      # Import from CSV/Excel (TODO)
GET    /export_passengers/      # Export to CSV (TODO)
```

### Itinerary (`/api/v1/circuits/itinerary/`)

```
GET    /                        # List itinerary items
POST   /                        # Create itinerary item
GET    /{id}/                   # Get itinerary item
PATCH  /{id}/                   # Update itinerary item
DELETE /{id}/                   # Delete itinerary item
```

### Flights (`/api/v1/circuits/flights/`)

```
GET    /                        # List flights
POST   /                        # Create flight
GET    /{id}/                   # Get flight
PATCH  /{id}/                   # Update flight
DELETE /{id}/                   # Delete flight
```

## Autenticación y Autorización

### JWT Authentication

Todos los endpoints (excepto login) requieren un token JWT en el header:

```
Authorization: Bearer <access_token>
```

### Roles y Permisos

| Role                   | Permisos                               |
| ---------------------- | -------------------------------------- |
| **admin**              | Full access to all resources           |
| **operations_manager** | Manage circuits, suppliers, operations |
| **tour_conductor**     | View and update assigned groups        |
| **accountant**         | Manage financial data                  |
| **viewer**             | Read-only access                       |

### Custom Permissions

```python
from core.common.permissions import IsAdmin, IsOperationsManager

class MyViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOperationsManager]
```

## Workflows Comunes

### 1. Crear un Nuevo Grupo

```python
# 1. Crear programa (si no existe)
POST /api/v1/circuits/programs/
{
  "code": "PERU-15D",
  "name": "Peru Mágico 15 días",
  "duration_days": 15,
  "base_price": "2500.00",
  "currency": "USD",
  "status": "active",
  "max_passengers": 30,
  "min_passengers": 15
}

# 2. Crear grupo
POST /api/v1/circuits/groups/
{
  "code": "GRP-2024-001",
  "name": "Grupo Enero 2024",
  "program_id": "<program_uuid>",
  "start_date": "2024-01-15",
  "end_date": "2024-01-30",
  "max_passengers": 25,
  "status": "planning"
}

# 3. Agregar pasajeros
POST /api/v1/circuits/passengers/
{
  "group": "<group_uuid>",
  "first_name": "Juan",
  "last_name": "Pérez",
  "document_type": "dni",
  "document_number": "12345678",
  "nationality": "PER",
  "date_of_birth": "1980-05-15",
  "gender": "M",
  "email": "juan@example.com",
  "phone": "+51 987654321",
  "status": "confirmed",
  "base_price": "2500.00"
}

# 4. Crear itinerario
POST /api/v1/circuits/itinerary/
{
  "group": "<group_uuid>",
  "day_number": 1,
  "date": "2024-01-15",
  "title": "Llegada a Lima",
  "description": "Recepción en aeropuerto y traslado al hotel",
  "location": "Lima",
  "breakfast_included": false,
  "lunch_included": false,
  "dinner_included": true
}

# 5. Agregar vuelos
POST /api/v1/circuits/flights/
{
  "group": "<group_uuid>",
  "flight_type": "outbound",
  "airline": "LATAM",
  "flight_number": "LA2315",
  "departure_airport": "MAD",
  "departure_city": "Madrid",
  "departure_country": "ESP",
  "arrival_airport": "LIM",
  "arrival_city": "Lima",
  "arrival_country": "PER",
  "departure_datetime": "2024-01-14T22:30:00Z",
  "arrival_datetime": "2024-01-15T08:45:00Z"
}
```

### 2. Autenticación con MFA

```python
# 1. Login normal
POST /api/v1/auth/login/
{
  "email": "admin@example.com",
  "password": "password123"
}

# 2. Habilitar MFA
POST /api/v1/auth/enable_mfa/
{
  "password": "password123"
}
# Response: { "mfa_uri": "otpauth://...", "secret": "..." }

# 3. Escanear QR o ingresar secret en app autenticadora (Google Authenticator, Authy)

# 4. Login con MFA
POST /api/v1/auth/login/
{
  "email": "admin@example.com",
  "password": "password123",
  "mfa_token": "123456"
}
```

## Testing

### Run Tests

```bash
# All tests
pytest

# Specific app
pytest apps/circuits/tests/

# With coverage
pytest --cov=apps --cov-report=html
```

### Escribir Tests

```python
# apps/circuits/tests/test_groups.py
import pytest
from rest_framework.test import APIClient
from apps.circuits.models import Group, Program
from apps.authentication.models import User

@pytest.mark.django_db
class TestGroupAPI:
    def test_create_group(self):
        client = APIClient()
        user = User.objects.create_user(
            email='test@example.com',
            password='test123',
            role='operations_manager'
        )
        client.force_authenticate(user=user)

        program = Program.objects.create(
            code='TEST-01',
            name='Test Program',
            duration_days=7,
            base_price=1000
        )

        response = client.post('/api/v1/circuits/groups/', {
            'code': 'GRP-001',
            'name': 'Test Group',
            'program_id': str(program.id),
            'start_date': '2024-06-01',
            'end_date': '2024-06-08',
            'max_passengers': 20
        })

        assert response.status_code == 201
        assert Group.objects.count() == 1
```

## Deployment

### Docker Production

```bash
# Build image
docker build -t travesia-backend:latest .

# Run with docker-compose
docker-compose -f docker-compose.prod.yml up -d
```

### Manual Production

```bash
# Install dependencies
pip install -r requirements.txt -r requirements-prod.txt

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Start with gunicorn
gunicorn --bind 0.0.0.0:8000 --workers 3 config.wsgi:application
```

### Environment Variables (Production)

```bash
DEBUG=False
SECRET_KEY=<random-secret-key>
ALLOWED_HOSTS=api.travesia.com
DB_HOST=db.example.com
USE_S3=True
AWS_STORAGE_BUCKET_NAME=travesia-prod
CELERY_BROKER_URL=redis://redis.example.com:6379/0
```

## Próximos Pasos (TODO)

- [ ] Implementar apps restantes (Suppliers, Operations, Financial, Documents)
- [ ] Agregar import/export CSV para passengers
- [ ] Implementar notificaciones por email
- [ ] Agregar webhooks para SUNAT
- [ ] Tests de integración completos
- [ ] Performance optimization (caching, query optimization)
- [ ] CI/CD pipeline

## Soporte

Para preguntas o issues, contacta al equipo de desarrollo.
