# Plan de Trabajo Arquitectónico - TravesIA

## 📋 Información del Proyecto

**Proyecto**: TravesIA
**Versión**: 1.0
**Tipo**: Sistema de Gestión de Agencia de Turismo (SaaS)
**Fecha**: 20 de enero de 2026
**Architect**: Architect Agent

---

## 🎯 Resumen Ejecutivo

TravesIA es un sistema integral de gestión para una agencia de turismo especializada en circuitos por Sudamérica (Perú, Bolivia, Chile, Ecuador, Galápagos). El sistema reemplazará procesos manuales con una solución digital que gestiona:

- **50+ grupos anuales** (40 jóvenes + 10 adultos)
- **4 circuitos principales** + circuitos personalizados
- **Operaciones complejas**: transporte, hoteles, servicios especializados
- **Multi-moneda**: USD y PEN (Soles Peruanos)
- **Gestión documental** centralizada
- **Integraciones**: SUNAT (facturación electrónica), sistemas de vuelos

### Stack Tecnológico Seleccionado

- **Frontend**: Vue 3 + Quasar 2
- **Backend**: Django (Python)
- **Base de Datos**: PostgreSQL + Redis (cache)
- **API**: REST (v1)
- **Autenticación**: JWT + MFA
- **Storage**: AWS S3
- **Deployment**: Docker + Docker Compose

---

## 🏗️ Análisis de Requisitos y Bounded Contexts

### Bounded Contexts Identificados

El sistema se dividirá en 6 contextos delimitados (Bounded Contexts) según DDD:

#### 1. **Circuit Management Context** (Gestión de Circuitos)

- Programas de viaje (Perbol Chil, Galer, Permap, Sudamérica)
- Itinerarios día a día
- Grupos y programación anual
- Pasajeros y datos de vuelos

#### 2. **Operations Context** (Operaciones - "La Biblia Digital")

- Transporte (buses, trenes, vuelos)
- Alojamiento (hoteles)
- Servicios especializados (entradas Machu Picchu, logística Salcantay)
- Personal operativo (guías, cocineros, arrieros)

#### 3. **Supplier Management Context** (Gestión de Proveedores)

- Registro de proveedores
- Catálogo de servicios
- Precios por períodos
- Contratos y acuerdos

#### 4. **Financial Context** (Gestión Financiera)

- Multi-moneda (USD, PEN)
- Costos por grupo
- Ingresos y depósitos bancarios
- Ventas adicionales
- Comisiones (Tour Conductor)
- Facturación electrónica SUNAT

#### 5. **Document Management Context** (Gestión Documental)

- Repositorio digital organizado por grupo
- Facturas, tickets, billetes
- Documentos de identidad
- Documentos confidenciales

#### 6. **Analytics & Reporting Context** (Reportes y Análisis)

- Liquidaciones por grupo
- Informes anuales comparativos
- Análisis de temporadas
- KPIs operacionales

### Requisitos No Funcionales

| Categoría          | Requisito                    | Target                  |
| ------------------ | ---------------------------- | ----------------------- |
| **Performance**    | Tiempo de respuesta promedio | < 300ms                 |
| **Performance**    | Carga de página inicial      | < 2s                    |
| **Disponibilidad** | Uptime                       | 99.5%                   |
| **Escalabilidad**  | Grupos concurrentes          | 50+                     |
| **Seguridad**      | Autenticación                | JWT + MFA               |
| **Seguridad**      | Datos sensibles              | Encriptación AES-256    |
| **Usabilidad**     | Soporte multi-dispositivo    | Desktop, Tablet, Mobile |
| **Compliance**     | Facturación electrónica      | SUNAT (Perú)            |

---

## 🏛️ Arquitectura de Alto Nivel

### Diagrama C4 - Nivel 1: Contexto del Sistema

```
┌─────────────────┐
│  Agencia Staff  │
│  (Usuarios)     │
└────────┬────────┘
         │
         │ Gestión de
         │ operaciones
         ▼
┌────────────────────────────────────────────┐
│                                            │
│         TravesIA System                    │
│  (Sistema de Gestión de Turismo)          │
│                                            │
└──┬──────┬──────┬──────┬──────┬──────┬────┘
   │      │      │      │      │      │
   ▼      ▼      ▼      ▼      ▼      ▼
┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐
│SUNAT │ │ AWS  │ │Email │ │SMS   │ │Payment│
│ API  │ │  S3  │ │Service│ │Provider│ │Gateway│
└──────┘ └──────┘ └──────┘ └──────┘ └──────┘
```

### Diagrama C4 - Nivel 2: Contenedores

```
┌─────────────────────────────────────────────────────────────┐
│                     TravesIA System                          │
│                                                               │
│  ┌──────────────┐         ┌─────────────────┐               │
│  │   Vue 3 +    │ HTTP/   │  Django REST    │               │
│  │   Quasar 2   │ JSON    │     API         │               │
│  │  (Frontend)  │◄───────►│   (Backend)     │               │
│  │              │  JWT    │                 │               │
│  └──────────────┘         └────────┬────────┘               │
│                                    │                         │
│                                    │                         │
│                           ┌────────▼─────────┐               │
│                           │   PostgreSQL     │               │
│                           │   (Database)     │               │
│                           └──────────────────┘               │
│                                    ▲                         │
│                           ┌────────┴─────────┐               │
│                           │      Redis       │               │
│                           │     (Cache)      │               │
│                           └──────────────────┘               │
└───────────────────────────────────────────────────────────────┘
```

### Patrón Arquitectónico: Monolito Modular

**Justificación**:

- Equipo pequeño (Innovación)
- Desarrollo inicial rápido
- Complejidad de negocio alta pero volumen moderado (50 grupos/año)
- Posibilidad de migrar a microservicios en el futuro

**Estructura**:

```
travesia/
├── apps/
│   ├── circuits/          # Circuit Management Context
│   ├── operations/        # Operations Context
│   ├── suppliers/         # Supplier Management Context
│   ├── financial/         # Financial Context
│   ├── documents/         # Document Management Context
│   └── analytics/         # Analytics & Reporting Context
├── core/
│   ├── authentication/    # Auth & permissions
│   ├── common/           # Shared utilities
│   └── integrations/     # External services
├── config/
└── manage.py
```

---

## 🗄️ Modelo de Datos

### Entidades Principales

#### Circuit Management

```
Program
├── id: UUID
├── code: String (PERBOL_CHIL, GALER, etc.)
├── name: String
├── description: Text
├── duration_days: Integer
└── is_active: Boolean

Group
├── id: UUID
├── program_id: FK → Program
├── code: String (único por grupo)
├── year: Integer
├── departure_date: Date
├── return_date: Date
├── group_type: Enum (YOUNG, ADULT)
├── status: Enum (PLANNED, CONFIRMED, IN_PROGRESS, COMPLETED)
└── max_capacity: Integer

Passenger
├── id: UUID
├── group_id: FK → Group
├── first_name: String
├── last_name: String
├── passport_number: String
├── date_of_birth: Date
├── nationality: String
├── email: String
└── phone: String

Itinerary
├── id: UUID
├── program_id: FK → Program
├── day_number: Integer
├── location: String
├── activities: JSONB
└── description: Text

Flight
├── id: UUID
├── group_id: FK → Group
├── flight_number: String
├── airline: String
├── departure_airport: String
├── arrival_airport: String
├── departure_datetime: DateTime
└── arrival_datetime: DateTime
```

#### Operations Context

```
Transportation
├── id: UUID
├── type: Enum (BUS, TRAIN, FLIGHT, PRIVATE)
├── provider_id: FK → Supplier
├── route: String
├── departure_time: Time
├── arrival_time: Time
├── code: String (ej: SIFA, Cruz del Sur)
└── capacity: Integer

Accommodation
├── id: UUID
├── hotel_id: FK → Hotel
├── group_id: FK → Group
├── check_in_date: Date
├── check_out_date: Date
├── rooms_reserved: Integer
├── status: Enum
└── special_requests: Text

Hotel
├── id: UUID
├── name: String
├── city: String
├── address: Text
├── phone: String
├── email: String
├── capacity: Integer
└── amenities: JSONB

SpecialService
├── id: UUID
├── type: Enum (MACHU_PICCHU, SALCANTAY, GUIDE, etc.)
├── provider_id: FK → Supplier
├── group_id: FK → Group
├── service_date: Date
├── quantity: Integer
└── notes: Text

StaffAssignment
├── id: UUID
├── group_id: FK → Group
├── staff_id: FK → Staff
├── role: Enum (GUIDE, COOK, MULETEER, TOUR_CONDUCTOR)
├── from_date: Date
└── to_date: Date
```

#### Supplier Management

```
Supplier
├── id: UUID
├── name: String
├── type: Enum (TRANSPORT, HOTEL, SERVICE, etc.)
├── contact_name: String
├── address: Text
├── phone: String
├── email: String
├── tax_id: String
├── bank_account: String
└── is_active: Boolean

SupplierService
├── id: UUID
├── supplier_id: FK → Supplier
├── service_type: String
├── description: Text
└── details: JSONB

PricePeriod
├── id: UUID
├── supplier_service_id: FK → SupplierService
├── valid_from: Date
├── valid_to: Date
├── price: Decimal
├── currency: Enum (USD, PEN)
└── notes: Text
```

#### Financial Context

```
GroupCost
├── id: UUID
├── group_id: FK → Group
├── category: Enum (TRANSPORT, ACCOMMODATION, SERVICE, etc.)
├── description: String
├── amount: Decimal
├── currency: Enum (USD, PEN)
├── payment_date: Date
└── supplier_id: FK → Supplier

AdditionalSale
├── id: UUID
├── group_id: FK → Group
├── passenger_id: FK → Passenger (opcional)
├── description: String (ej: Sobrevuelo Nazca)
├── amount: Decimal
├── currency: Enum (USD, PEN)
└── sale_date: Date

Commission
├── id: UUID
├── group_id: FK → Group
├── staff_id: FK → Staff
├── type: Enum (TOUR_CONDUCTOR, GUIDE, etc.)
├── amount: Decimal
├── currency: Enum (USD, PEN)
└── payment_status: Enum

Invoice
├── id: UUID
├── group_id: FK → Group
├── invoice_number: String
├── sunat_cdr: String (Constancia SUNAT)
├── issue_date: Date
├── amount: Decimal
├── currency: Enum
├── status: Enum (DRAFT, SENT, PAID)
└── xml_file: String (ruta S3)

BankDeposit
├── id: UUID
├── invoice_id: FK → Invoice
├── bank: String
├── account_number: String
├── deposit_date: Date
├── amount: Decimal
└── reference: String
```

#### Document Management

```
Document
├── id: UUID
├── group_id: FK → Group (opcional)
├── category: Enum (INVOICE, TICKET, ID, CONTRACT, etc.)
├── name: String
├── file_path: String (S3)
├── file_type: String
├── file_size: Integer
├── is_confidential: Boolean
├── uploaded_by: FK → User
├── uploaded_at: DateTime
└── metadata: JSONB
```

### Relaciones Críticas

```
Program 1──────* Group
Group 1────────* Passenger
Group 1────────* Itinerary
Group 1────────* Transportation
Group 1────────* Accommodation
Group 1────────* SpecialService
Group 1────────* GroupCost
Group 1────────* AdditionalSale
Group 1────────* Invoice
Group 1────────* Document
Supplier 1─────* SupplierService
SupplierService 1──* PricePeriod
```

### Índices Críticos

```sql
-- Búsquedas frecuentes
CREATE INDEX idx_group_program_year ON groups(program_id, year);
CREATE INDEX idx_passenger_group ON passengers(group_id);
CREATE INDEX idx_group_dates ON groups(departure_date, return_date);
CREATE INDEX idx_supplier_type ON suppliers(type, is_active);
CREATE INDEX idx_document_group_category ON documents(group_id, category);
CREATE INDEX idx_invoice_status ON invoices(status, issue_date);

-- Full-text search
CREATE INDEX idx_supplier_search ON suppliers USING gin(to_tsvector('spanish', name || ' ' || contact_name));
```

---

## 🔌 Especificación de APIs

### Convenciones Generales

- **Base URL**: `/api/v1/`
- **Autenticación**: Bearer Token (JWT)
- **Content-Type**: `application/json`
- **Paginación**: Offset-based (`?offset=0&limit=20`)
- **Filtrado**: Query params (`?status=CONFIRMED&year=2026`)
- **Ordenamiento**: `?ordering=-departure_date`

### Endpoints Principales

#### Circuit Management

```http
# Programs
GET    /api/v1/programs/
POST   /api/v1/programs/
GET    /api/v1/programs/{id}/
PUT    /api/v1/programs/{id}/
DELETE /api/v1/programs/{id}/

# Groups
GET    /api/v1/groups/
POST   /api/v1/groups/
GET    /api/v1/groups/{id}/
PUT    /api/v1/groups/{id}/
PATCH  /api/v1/groups/{id}/status/
GET    /api/v1/groups/{id}/passengers/
POST   /api/v1/groups/{id}/passengers/import/  # Import from Excel

# Passengers
GET    /api/v1/passengers/
POST   /api/v1/passengers/
GET    /api/v1/passengers/{id}/
PUT    /api/v1/passengers/{id}/
DELETE /api/v1/passengers/{id}/

# Itineraries
GET    /api/v1/itineraries/
POST   /api/v1/itineraries/
GET    /api/v1/itineraries/{id}/
PUT    /api/v1/itineraries/{id}/
GET    /api/v1/programs/{program_id}/itinerary/
```

#### Operations

```http
# Transportation
GET    /api/v1/transportation/
POST   /api/v1/transportation/
GET    /api/v1/transportation/{id}/
PUT    /api/v1/transportation/{id}/
GET    /api/v1/groups/{group_id}/transportation/

# Accommodations
GET    /api/v1/accommodations/
POST   /api/v1/accommodations/
GET    /api/v1/accommodations/{id}/
PUT    /api/v1/accommodations/{id}/
GET    /api/v1/hotels/
GET    /api/v1/hotels/{id}/availability/?from=2026-06-01&to=2026-06-05

# Special Services
GET    /api/v1/special-services/
POST   /api/v1/special-services/
GET    /api/v1/special-services/{id}/
PUT    /api/v1/special-services/{id}/

# Staff Assignments
GET    /api/v1/staff-assignments/
POST   /api/v1/staff-assignments/
GET    /api/v1/groups/{group_id}/staff/
```

#### Suppliers

```http
GET    /api/v1/suppliers/
POST   /api/v1/suppliers/
GET    /api/v1/suppliers/{id}/
PUT    /api/v1/suppliers/{id}/
GET    /api/v1/suppliers/{id}/services/
POST   /api/v1/suppliers/{id}/services/
GET    /api/v1/supplier-services/{id}/prices/
POST   /api/v1/supplier-services/{id}/prices/
```

#### Financial

```http
# Group Costs
GET    /api/v1/group-costs/
POST   /api/v1/group-costs/
GET    /api/v1/groups/{group_id}/costs/
GET    /api/v1/groups/{group_id}/costs/summary/  # Total por categoría

# Additional Sales
GET    /api/v1/additional-sales/
POST   /api/v1/additional-sales/
GET    /api/v1/groups/{group_id}/additional-sales/

# Commissions
GET    /api/v1/commissions/
POST   /api/v1/commissions/
POST   /api/v1/commissions/calculate/  # Auto-cálculo

# Invoices (SUNAT Integration)
GET    /api/v1/invoices/
POST   /api/v1/invoices/
GET    /api/v1/invoices/{id}/
POST   /api/v1/invoices/{id}/send-to-sunat/
GET    /api/v1/invoices/{id}/download-xml/
GET    /api/v1/invoices/{id}/download-pdf/

# Bank Deposits
GET    /api/v1/bank-deposits/
POST   /api/v1/bank-deposits/
GET    /api/v1/invoices/{invoice_id}/deposits/
```

#### Documents

```http
GET    /api/v1/documents/
POST   /api/v1/documents/upload/
GET    /api/v1/documents/{id}/
DELETE /api/v1/documents/{id}/
GET    /api/v1/documents/{id}/download/
GET    /api/v1/groups/{group_id}/documents/
```

#### Analytics

```http
GET    /api/v1/analytics/group-liquidation/{group_id}/
GET    /api/v1/analytics/annual-report/?year=2026
GET    /api/v1/analytics/seasonal-analysis/
GET    /api/v1/analytics/kpis/
```

### Ejemplo de Request/Response

```http
POST /api/v1/groups/
Authorization: Bearer {jwt_token}
Content-Type: application/json

{
  "program_id": "uuid-here",
  "code": "PERBOL-2026-05",
  "year": 2026,
  "departure_date": "2026-06-15",
  "return_date": "2026-07-05",
  "group_type": "YOUNG",
  "max_capacity": 30,
  "status": "PLANNED"
}

Response: 201 Created
{
  "id": "new-uuid",
  "program_id": "uuid-here",
  "program": {
    "code": "PERBOL_CHIL",
    "name": "Perú, Bolivia y Chile"
  },
  "code": "PERBOL-2026-05",
  "year": 2026,
  "departure_date": "2026-06-15",
  "return_date": "2026-07-05",
  "group_type": "YOUNG",
  "max_capacity": 30,
  "status": "PLANNED",
  "created_at": "2026-01-20T10:30:00Z",
  "updated_at": "2026-01-20T10:30:00Z"
}
```

---

## 🎨 Patrones de Diseño y Decisiones Técnicas

### ADR-001: Django REST Framework para API

**Status**: Accepted

**Context**: Necesitamos un framework robusto para construir la API REST con autenticación JWT, serialización, validación y documentación automática.

**Decision**: Usar Django REST Framework (DRF)

**Rationale**:

- Integración nativa con Django
- Autenticación JWT out-of-the-box
- Serializers potentes con validación
- Browsable API para desarrollo
- Generación automática de OpenAPI/Swagger

**Consequences**:

- ✅ Desarrollo más rápido
- ✅ Documentación automática
- ✅ Ecosystem maduro
- ⚠️ Curva de aprendizaje moderada

---

### ADR-002: Repository Pattern para Acceso a Datos

**Status**: Accepted

**Context**: Necesitamos abstraer el acceso a datos para facilitar testing y futura migración.

**Decision**: Implementar Repository Pattern

**Estructura**:

```python
# repositories/group_repository.py
class GroupRepository:
    def find_by_id(self, group_id: UUID) -> Optional[Group]:
        pass

    def find_by_year(self, year: int) -> List[Group]:
        pass

    def save(self, group: Group) -> Group:
        pass

    def delete(self, group_id: UUID) -> None:
        pass

# services/group_service.py
class GroupService:
    def __init__(self, group_repo: GroupRepository):
        self.group_repo = group_repo

    def create_group(self, data: CreateGroupDTO) -> Group:
        # Lógica de negocio
        group = Group(**data)
        return self.group_repo.save(group)
```

**Rationale**:

- Separación de concerns
- Facilita unit testing (mocking)
- Abstrae Django ORM (futuro cambio)

---

### ADR-003: Multi-Moneda con Modelo Flexible

**Status**: Accepted

**Context**: El sistema maneja USD y PEN (Soles), con posibilidad de agregar más monedas.

**Decision**: Campo `currency` en todas las entidades financieras + tabla de tipos de cambio

**Modelo**:

```python
class ExchangeRate(models.Model):
    from_currency = models.CharField(max_length=3)  # USD
    to_currency = models.CharField(max_length=3)    # PEN
    rate = models.DecimalField(max_digits=10, decimal_places=4)
    effective_date = models.DateField()

    class Meta:
        unique_together = ['from_currency', 'to_currency', 'effective_date']

# Uso en servicios
class FinancialService:
    def convert_currency(self, amount, from_curr, to_curr, date):
        rate = ExchangeRate.objects.get(
            from_currency=from_curr,
            to_currency=to_curr,
            effective_date__lte=date
        ).order_by('-effective_date').first()
        return amount * rate.rate
```

---

### ADR-004: AWS S3 para Almacenamiento de Documentos

**Status**: Accepted

**Context**: Necesitamos almacenar facturas, tickets, documentos de identidad, etc.

**Decision**: AWS S3 con organización por grupo

**Estructura de Buckets**:

```
travesia-documents/
├── groups/
│   ├── PERBOL-2026-01/
│   │   ├── invoices/
│   │   ├── tickets/
│   │   ├── passports/
│   │   └── contracts/
│   └── GALER-2026-03/
├── suppliers/
│   ├── contracts/
│   └── price-lists/
└── confidential/
    └── hotel-pricing/
```

**Seguridad**:

- Pre-signed URLs con expiración (15 min)
- Encriptación S3 Server-Side (SSE)
- IAM roles restrictivos
- Versionado habilitado

---

### ADR-005: SUNAT Integration Strategy

**Status**: Proposed

**Context**: Integración con sistema de facturación electrónica SUNAT (Perú)

**Decision**: Servicio dedicado para integración SUNAT con queue de procesamiento

**Arquitectura**:

```python
class SUNATService:
    def generate_xml(self, invoice: Invoice) -> str:
        # Generar XML según estándar SUNAT
        pass

    def sign_xml(self, xml: str) -> str:
        # Firmar digitalmente con certificado
        pass

    def send_to_sunat(self, signed_xml: str) -> SUNATResponse:
        # Enviar a webservice SUNAT
        pass

    def process_cdr(self, cdr: str) -> bool:
        # Procesar Constancia de Recepción
        pass
```

**Consideraciones**:

- Certificado digital requerido
- Retry logic (3 intentos)
- Queue para procesamiento asíncrono (Celery)
- Almacenar XML y CDR en S3

---

### ADR-006: Caching Strategy

**Status**: Accepted

**Decision**: Redis para caché de consultas frecuentes

**Estrategia**:

```python
# Cache para catálogos estáticos
CACHE_CONFIG = {
    'programs': {'ttl': 3600},          # 1 hora
    'suppliers': {'ttl': 1800},         # 30 min
    'hotels': {'ttl': 1800},            # 30 min
    'exchange_rates': {'ttl': 86400},   # 24 horas
}

# Invalidación
def invalidate_cache_on_update(sender, instance, **kwargs):
    cache_key = f"{sender.__name__}:{instance.id}"
    cache.delete(cache_key)
```

---

### ADR-007: Quasar Framework para Frontend

**Status**: Accepted

**Context**: Necesitamos UI responsiva con soporte desktop, tablet y móvil.

**Decision**: Quasar 2 con Vue 3 Composition API

**Rationale**:

- Material Design components out-of-the-box
- Responsive layout automático
- Build para múltiples plataformas
- TypeScript support
- Vite build system (rápido)

**Estructura de Componentes**:

```
src/
├── pages/
│   ├── Groups/
│   │   ├── GroupList.vue
│   │   ├── GroupDetail.vue
│   │   └── GroupForm.vue
│   ├── Operations/
│   ├── Financial/
│   └── Analytics/
├── components/
│   ├── common/
│   ├── forms/
│   └── tables/
├── composables/
│   ├── useGroups.ts
│   ├── useAuth.ts
│   └── useFinancial.ts
├── stores/
│   ├── auth.ts
│   ├── groups.ts
│   └── notifications.ts
└── router/
```

---

## 🔐 Seguridad y Autenticación

### Estrategia de Autenticación

**JWT (JSON Web Tokens)**:

```python
# Configuración Django
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'ALGORITHM': 'HS256',
}

# Endpoints
POST /api/v1/auth/login/         # → access + refresh token
POST /api/v1/auth/refresh/       # → nuevo access token
POST /api/v1/auth/logout/        # → blacklist refresh token
POST /api/v1/auth/register/      # → registro (solo admin)
POST /api/v1/auth/change-password/
```

**Multi-Factor Authentication (MFA)**:

```python
# TOTP (Time-based One-Time Password)
POST /api/v1/auth/mfa/enable/
POST /api/v1/auth/mfa/verify/
POST /api/v1/auth/mfa/disable/

# Biblioteca: pyotp
```

### Roles y Permisos (RBAC)

```python
ROLES = {
    'ADMIN': {
        'permissions': ['*'],  # Todos los permisos
    },
    'OPERATIONS_MANAGER': {
        'permissions': [
            'view_groups', 'manage_groups',
            'view_operations', 'manage_operations',
            'view_suppliers', 'manage_suppliers',
            'view_financial', 'manage_financial',
        ],
    },
    'TOUR_CONDUCTOR': {
        'permissions': [
            'view_groups', 'view_itineraries',
            'view_passengers', 'update_passengers',
            'create_additional_sales',
            'view_operations',
        ],
    },
    'ACCOUNTANT': {
        'permissions': [
            'view_financial', 'manage_invoices',
            'view_costs', 'create_costs',
            'generate_reports',
        ],
    },
    'VIEWER': {
        'permissions': [
            'view_groups', 'view_operations',
            'view_financial', 'view_reports',
        ],
    },
}
```

### Encriptación de Datos Sensibles

```python
# django-cryptography para campos sensibles
from django_cryptography.fields import encrypt

class Passenger(models.Model):
    passport_number = encrypt(models.CharField(max_length=20))
    # Encriptado en DB, decriptado automáticamente en app
```

### Audit Trail

```python
class AuditLog(models.Model):
    user = models.ForeignKey(User)
    action = models.CharField()  # CREATE, UPDATE, DELETE, VIEW
    model = models.CharField()
    object_id = models.UUIDField()
    changes = models.JSONField()  # Diff de cambios
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)
```

---

## ⚡ Performance y Escalabilidad

### Optimización de Queries

**N+1 Problem Prevention**:

```python
# MAL
groups = Group.objects.all()
for group in groups:
    print(group.program.name)  # Query por cada group

# BIEN
groups = Group.objects.select_related('program').all()
for group in groups:
    print(group.program.name)  # 1 solo query con JOIN
```

**Paginación Eficiente**:

```python
class GroupViewSet(viewsets.ModelViewSet):
    pagination_class = PageNumberPagination
    page_size = 20
    max_page_size = 100
```

### Caching Layers

```
┌─────────────┐
│   Browser   │ ← Cache de assets estáticos (1 año)
└──────┬──────┘
       │
┌──────▼──────┐
│ CloudFront  │ ← CDN para static files
└──────┬──────┘
       │
┌──────▼──────┐
│  Django API │
└──────┬──────┘
       │
┌──────▼──────┐
│    Redis    │ ← Cache de queries (15min - 24h)
└──────┬──────┘
       │
┌──────▼──────┐
│ PostgreSQL  │
└─────────────┘
```

### Estrategia de Escalado

**Actual (Fase 1)**:

- Single Django instance
- PostgreSQL single node
- Redis single node
- S3 para archivos

**Futuro (Fase 2 - si se necesita)**:

- Multiple Django instances con load balancer
- PostgreSQL con read replicas
- Redis Cluster
- Celery workers para tareas asíncronas

### Background Jobs

```python
# Celery para tareas asíncronas
CELERY_TASKS = {
    'send_email': {'priority': 'high'},
    'generate_report': {'priority': 'medium'},
    'cleanup_old_files': {'priority': 'low'},
    'sync_sunat': {'priority': 'high'},
}

# Ejemplo
@shared_task
def generate_annual_report(year):
    report = AnalyticsService().generate_annual_report(year)
    send_email_with_attachment(report)
```

---

## 📊 Monitoreo y Observability

### Logging Estructurado

```python
import structlog

logger = structlog.get_logger()

logger.info(
    "group_created",
    group_id=str(group.id),
    code=group.code,
    user_id=str(request.user.id),
    ip=request.META.get('REMOTE_ADDR')
)
```

### Métricas Clave (KPIs)

```python
METRICS_TO_TRACK = {
    # Performance
    'api_response_time_p50': 'latencia mediana',
    'api_response_time_p95': 'latencia p95',
    'api_error_rate': 'tasa de errores',

    # Negocio
    'groups_created_per_month': 'grupos creados',
    'revenue_per_group': 'revenue promedio',
    'supplier_payment_delays': 'pagos retrasados',

    # Sistema
    'database_connections': 'conexiones DB',
    'cache_hit_ratio': 'ratio de cache hits',
    'storage_usage': 'uso de S3',
}
```

### Health Checks

```python
# /api/v1/health/
{
  "status": "healthy",
  "timestamp": "2026-01-20T10:30:00Z",
  "services": {
    "database": {
      "status": "up",
      "latency_ms": 12
    },
    "redis": {
      "status": "up",
      "latency_ms": 3
    },
    "s3": {
      "status": "up",
      "latency_ms": 45
    },
    "sunat": {
      "status": "degraded",
      "latency_ms": 2300,
      "message": "Alta latencia detectada"
    }
  }
}
```

---

## 🚀 Plan de Deployment

### Entornos

```
Development  → Staging → Production
(local)        (AWS)     (AWS)
```

### Docker Compose Setup

```yaml
# docker-compose.yml
version: "3.8"

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: travesia
      POSTGRES_USER: travesia_user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  backend:
    build: ./backend
    command: gunicorn config.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - ./backend:/app
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis
    environment:
      - DATABASE_URL=postgresql://travesia_user:${DB_PASSWORD}@db:5432/travesia
      - REDIS_URL=redis://redis:6379/0
      - AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
      - AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}

  frontend:
    build: ./frontend
    command: quasar dev
    volumes:
      - ./frontend:/app
    ports:
      - "3000:3000"
    depends_on:
      - backend

  celery_worker:
    build: ./backend
    command: celery -A config worker -l info
    depends_on:
      - db
      - redis

  celery_beat:
    build: ./backend
    command: celery -A config beat -l info
    depends_on:
      - db
      - redis

volumes:
  postgres_data:
```

### CI/CD Pipeline (GitHub Actions)

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: |
          docker-compose -f docker-compose.test.yml up --abort-on-container-exit

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to production
        run: |
          # Deploy logic here
```

---

## 📅 Timeline Estimado

| Fase                           | Duración       | Descripción                               |
| ------------------------------ | -------------- | ----------------------------------------- |
| **Fase 1: Setup**              | 1 semana       | Infraestructura inicial, Docker, repo     |
| **Fase 2: Circuit Management** | 2 semanas      | Programs, Groups, Passengers, Itineraries |
| **Fase 3: Operations**         | 3 semanas      | Transportation, Hotels, Special Services  |
| **Fase 4: Suppliers**          | 1 semana       | Supplier management, pricing              |
| **Fase 5: Financial**          | 2 semanas      | Costs, Sales, Invoices, SUNAT             |
| **Fase 6: Documents**          | 1 semana       | S3 integration, upload/download           |
| **Fase 7: Analytics**          | 1 semana       | Reports, KPIs                             |
| **Fase 8: Testing & QA**       | 1 semana       | Integration tests, E2E                    |
| **Fase 9: Deployment**         | 1 semana       | Production setup, migration               |
| **Total**                      | **13 semanas** | (~3 meses)                                |

---

## ✅ Checkpoints de Validación

Antes de proceder con la implementación, validar:

- [x] Todos los bounded contexts identificados
- [x] Modelo de datos completo con relaciones
- [x] Especificaciones de APIs definidas
- [x] Decisiones técnicas documentadas (ADRs)
- [x] Patrones de diseño seleccionados
- [x] Estrategia de seguridad definida
- [x] Plan de escalabilidad establecido
- [x] Monitoreo y observability planificados
- [x] Timeline y fases claras

---

## 🤝 Handoffs a Otros Agentes

### → Database Agent

**Tareas**:

1. Crear esquema PostgreSQL basado en modelo de datos
2. Crear migraciones Django iniciales
3. Diseñar índices según patrones de acceso
4. Configurar Redis para caching
5. Documentar estrategia de backup

**Archivos de Referencia**:

- [docs/architecture/data-model.md](./data-model.md)
- [docs/architecture/architecture-plan.md](./architecture-plan.md)

---

### → Backend Agent

**Tareas**:

1. Implementar Django apps según bounded contexts
2. Crear models según especificación
3. Implementar Django REST Framework endpoints
4. Desarrollar repositories y services
5. Integrar con SUNAT
6. Configurar Celery para tareas asíncronas

**Archivos de Referencia**:

- [docs/api/openapi.yaml](../api/) (por crear)
- [docs/architecture/architecture-plan.md](./architecture-plan.md)

---

### → Frontend Agent

**Tareas**:

1. Setup Quasar 2 project
2. Crear estructura de componentes
3. Implementar state management (Pinia)
4. Integrar con API REST
5. Diseño responsive (desktop, tablet, mobile)

**Archivos de Referencia**:

- [docs/architecture/architecture-plan.md](./architecture-plan.md)
- Figma designs (si existen)

---

### → DevOps Agent

**Tareas**:

1. Configurar Docker Compose para desarrollo
2. Setup CI/CD con GitHub Actions
3. Configurar AWS resources (S3, RDS, etc.)
4. Implementar monitoreo y logging
5. Documentar proceso de deployment

**Archivos de Referencia**:

- [docs/architecture/architecture-plan.md](./architecture-plan.md)

---

### → Security Agent

**Tareas**:

1. Revisar estrategia de autenticación JWT
2. Implementar MFA
3. Configurar encriptación de datos sensibles
4. Implementar audit trail
5. Security testing y penetration testing

---

### → Testing Agent

**Tareas**:

1. Crear suite de tests unitarios (target: 80% coverage)
2. Implementar integration tests para APIs críticas
3. Desarrollar E2E tests para flujos principales
4. Performance testing (load testing)

---

## 📚 Referencias

- **Django Documentation**: https://docs.djangoproject.com/
- **Django REST Framework**: https://www.django-rest-framework.org/
- **Vue 3 Documentation**: https://vuejs.org/
- **Quasar Framework**: https://quasar.dev/
- **PostgreSQL Best Practices**: https://www.postgresql.org/docs/
- **SUNAT Documentation**: https://www.sunat.gob.pe/
- **AWS S3 Documentation**: https://docs.aws.amazon.com/s3/

---

**Versión**: 1.0
**Última Actualización**: 20 de enero de 2026
**Responsable**: Architect Agent
**Status**: Ready for Implementation
