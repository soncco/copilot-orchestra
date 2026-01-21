# 🚀 TravesIA - Overview del Proyecto

> Sistema completo de gestión turística para agencias de viaje - Desarrollado con Django + Quasar 2

## 📋 Descripción General

**TravesIA** es una plataforma SaaS diseñada para la gestión integral de agencias turísticas en Perú, especializada en:

- Gestión de circuitos turísticos y programas
- Administración de grupos de pasajeros
- Control de operaciones (hoteles, transporte, servicios)
- Facturación electrónica SUNAT (Perú)
- Gestión de proveedores y contratos
- Administración documental

## 🎯 Objetivos del Sistema

1. **Centralizar** toda la información operativa de la agencia
2. **Automatizar** procesos repetitivos (facturación, reportes)
3. **Integrar** con sistemas externos (SUNAT, proveedores)
4. **Optimizar** la gestión de recursos y costos
5. **Mejorar** la experiencia del cliente final

## 🏗️ Arquitectura Técnica

### Stack Completo

```
┌──────────────────────────────────────────────┐
│           FRONTEND (Quasar 2)                │
│    Vue 3 + TypeScript + Pinia + Vite         │
│         http://localhost:9000                │
└──────────────┬───────────────────────────────┘
               │ HTTP/REST + JWT
               │
┌──────────────▼───────────────────────────────┐
│          BACKEND (Django 5.0)                │
│   Django REST Framework + PostgreSQL         │
│         http://localhost:8000                │
└──────────────┬───────────────────────────────┘
               │
    ┌──────────┼──────────┐
    ▼          ▼          ▼
┌────────┐ ┌────────┐ ┌────────┐
│  Redis │ │Postgres│ │  AWS   │
│  Cache │ │   DB   │ │   S3   │
│ Celery │ │        │ │  Docs  │
└────────┘ └────────┘ └────────┘
```

### Tecnologías

**Backend**:

- Django 5.0 + DRF 3.14
- PostgreSQL 15
- Redis 7 (cache + Celery)
- Celery (tareas asíncronas)
- JWT Authentication + MFA

**Frontend**:

- Vue 3 (Composition API)
- Quasar 2 (Material Design)
- TypeScript
- Pinia (state management)
- Axios (HTTP client)
- Vite (build tool)

**Infraestructura**:

- Docker + Docker Compose
- AWS S3 (almacenamiento)
- Nginx (producción)

## 📊 Modelos de Datos

### Backend Django - 6 Apps

#### 1. **Authentication** (Autenticación)

- `User`: Usuarios del sistema
- `MFADevice`: Dispositivos de autenticación multifactor
- `AuditLog`: Registro de auditoría

#### 2. **Circuits** (Circuitos Turísticos)

- `Program`: Programas/Circuitos turísticos
- `Group`: Grupos de pasajeros
- `Passenger`: Pasajeros individuales
- `Itinerary`: Itinerarios por día
- `Flight`: Vuelos programados

#### 3. **Suppliers** (Proveedores)

- `Supplier`: Proveedores de servicios
- `SupplierService`: Servicios ofrecidos
- `SupplierPricing`: Tarifas y precios
- `ExchangeRate`: Tasas de cambio

#### 4. **Operations** (Operaciones)

- `Hotel`: Hoteles
- `Transportation`: Transporte
- `Staff`: Personal (guías, choferes)
- `OperationalService`: Servicios operativos

#### 5. **Financial** (Finanzas)

- `Invoice`: Facturas (SUNAT)
- `Cost`: Costos
- `Sale`: Ventas
- `Commission`: Comisiones
- `BankDeposit`: Depósitos bancarios

#### 6. **Documents** (Documentos)

- `Document`: Documentos (S3)

**Total**: 22 modelos implementados

## 🔐 Sistema de Autenticación

### Roles de Usuario

1. **ADMIN**: Acceso total al sistema
2. **MANAGER**: Gestión operativa completa
3. **SALES**: Ventas, pasajeros, reportes comerciales
4. **GUIDE**: Consulta de itinerarios y grupos asignados
5. **OPERATIONS**: Operaciones, hoteles, transporte

### Seguridad

- JWT tokens (access + refresh)
- MFA opcional (TOTP - Google Authenticator)
- Permisos basados en roles
- Audit logging completo
- Token auto-refresh en frontend

## 🌐 API REST

### Endpoints Principales (50+)

```
POST   /api/v1/auth/login              # Login
POST   /api/v1/auth/logout             # Logout
POST   /api/v1/auth/refresh            # Refresh token
POST   /api/v1/auth/mfa/enable         # Activar MFA

GET    /api/v1/circuits/programs       # Listar programas
POST   /api/v1/circuits/programs       # Crear programa
GET    /api/v1/circuits/groups         # Listar grupos
GET    /api/v1/circuits/passengers     # Listar pasajeros

GET    /api/v1/suppliers/              # Listar proveedores
GET    /api/v1/operations/hotels       # Listar hoteles
GET    /api/v1/financial/invoices      # Listar facturas
GET    /api/v1/documents/              # Listar documentos

... y 40+ endpoints más
```

**Documentación API**:

- Swagger UI: `http://localhost:8000/api/docs`
- ReDoc: `http://localhost:8000/api/redoc`

## 💼 Funcionalidades Principales

### ✅ Completadas (Backend)

1. **Gestión de Programas**
   - CRUD completo de circuitos turísticos
   - Itinerarios detallados por día
   - Gestión de vuelos

2. **Gestión de Grupos**
   - Organización de grupos de pasajeros
   - Asignación de programas
   - Tracking de estado

3. **Gestión de Pasajeros**
   - Datos personales completos
   - Documentos asociados
   - Pagos y saldos

4. **Proveedores**
   - Catálogo de proveedores
   - Servicios y tarifas
   - Integración con operaciones

5. **Operaciones**
   - Gestión de hoteles
   - Transporte
   - Personal (guías, choferes)
   - Servicios operativos

6. **Finanzas**
   - Facturación electrónica (preparado para SUNAT)
   - Costos y ventas
   - Comisiones
   - Depósitos bancarios

7. **Documentos**
   - Upload a AWS S3
   - Organización por categorías
   - Asociación con pasajeros/grupos

### ✅ Completadas (Frontend)

1. **Autenticación**
   - Login con email/password
   - Soporte MFA (TOTP)
   - Auto-refresh de tokens
   - Route guards

2. **Dashboard**
   - Vista general de estadísticas
   - Grupos recientes
   - Quick actions

3. **Layout**
   - Sidebar con navegación
   - Header con user menu
   - Responsive design

### ⏳ Pendientes (Frontend)

1. **Páginas CRUD** (11 páginas)
   - Programs, Groups, Passengers
   - Suppliers
   - Hotels, Transportation, Staff
   - Invoices, Costs, Sales
   - Documents

2. **Componentes Reutilizables**
   - DataTable con paginación
   - Form modals
   - Confirm dialogs
   - File upload

3. **Features Avanzadas**
   - Calendar view
   - Reports con filtros
   - Analytics dashboard
   - Export PDF/Excel

## 📁 Estructura del Proyecto

```
ericxpeditions/
├── .github/
│   ├── agents/                    # Definiciones de agentes
│   │   ├── architect-agent.md
│   │   ├── backend-agent.md
│   │   ├── frontend-agent.md
│   │   └── ... (9 agentes)
│   └── copilot-instructions.md    # Instrucciones globales
├── backend/                       # Django Backend
│   ├── apps/
│   │   ├── authentication/        # App: Auth + Users
│   │   ├── circuits/              # App: Programs + Groups
│   │   ├── suppliers/             # App: Suppliers
│   │   ├── operations/            # App: Hotels + Transport
│   │   ├── financial/             # App: Invoices + Finance
│   │   └── documents/             # App: Documents
│   ├── config/                    # Django settings
│   │   ├── settings/
│   │   │   ├── base.py
│   │   │   ├── development.py
│   │   │   └── production.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── core/                      # Utilities
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── manage.py
│   ├── requirements.txt
│   ├── README.md
│   └── STATUS.md
├── frontend/                      # Quasar Frontend
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   ├── layouts/
│   │   │   └── MainLayout.vue
│   │   ├── pages/
│   │   │   ├── LoginPage.vue
│   │   │   └── DashboardPage.vue
│   │   ├── router/
│   │   │   ├── index.ts
│   │   │   └── routes.ts
│   │   ├── services/
│   │   │   ├── api.ts
│   │   │   └── auth.service.ts
│   │   ├── stores/
│   │   │   ├── index.ts
│   │   │   └── auth.ts
│   │   ├── types/
│   │   │   └── index.ts
│   │   ├── App.vue
│   │   └── main.ts
│   ├── public/
│   ├── .env
│   ├── .env.example
│   ├── quasar.config.js
│   ├── package.json
│   ├── tsconfig.json
│   └── README.md
├── docs/                          # Documentación
│   ├── api/
│   │   └── README.md
│   └── architecture/
│       └── README.md
├── examples/
│   ├── authentication-feature.md
│   └── monolith-to-spa-migration.md
├── agents-config.json             # Config de agentes
├── project-context.md             # Variables del proyecto
├── PROJECT-SUMMARY.md             # Resumen técnico
├── PROJECT-OVERVIEW.md            # Este archivo
├── README.md                      # README del sistema
├── CONTRIBUTING.md
├── CHANGELOG.md
└── LICENSE
```

## 🚀 Setup y Ejecución

### Prerequisitos

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Redis 7+
- Docker + Docker Compose (opcional)

### Opción 1: Docker (Recomendado)

```bash
# 1. Backend
cd backend
cp .env.example .env
# Editar .env

docker-compose up --build -d

# Migraciones
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate

# Superusuario
docker-compose exec web python manage.py createsuperuser

# 2. Frontend
cd ../frontend
cp .env.example .env
npm install
npm run dev
```

### Opción 2: Local Development

**Backend**:

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Configurar DATABASE_URL, REDIS_URL, etc.
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

**Frontend**:

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

### URLs de Acceso

- **Frontend**: http://localhost:9000
- **Backend API**: http://localhost:8000/api/v1
- **Django Admin**: http://localhost:8000/admin
- **Swagger Docs**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

## 🧪 Testing

### Backend

```bash
cd backend
python manage.py test
```

### Frontend

```bash
cd frontend
npm run test
```

## 📈 Estado del Proyecto

### Completado ✅

| Componente        | Progreso | Estado               |
| ----------------- | -------- | -------------------- |
| Backend API       | 100%     | ✅ Completo          |
| Modelos de Datos  | 100%     | ✅ 22 modelos        |
| Autenticación     | 100%     | ✅ JWT + MFA         |
| Frontend Base     | 100%     | ✅ Login + Dashboard |
| Docker Setup      | 100%     | ✅ Funcionando       |
| Documentación API | 100%     | ✅ Swagger           |

### En Desarrollo 🚧

| Componente     | Progreso | Próximo       |
| -------------- | -------- | ------------- |
| CRUD Pages     | 15%      | Programs Page |
| Componentes UI | 10%      | DataTable     |
| Integración    | 50%      | Testing E2E   |
| Reports        | 0%       | Diseño        |

### Pendiente ⏳

- Integración SUNAT real
- Sistema de notificaciones
- Exportación PDF/Excel
- Mobile app (Capacitor)
- Analytics dashboard
- Real-time updates (WebSocket)

## 🗺️ Roadmap

### Fase 1: Foundation (✅ Completada)

- Backend API completo
- Frontend base con auth
- Docker environment
- Documentación básica

### Fase 2: CRUD Implementation (En Curso)

- **Enero 2026**
  - ⏳ Programs CRUD page
  - ⏳ Groups CRUD page
  - ⏳ Passengers CRUD page
  - ⏳ Componentes reutilizables

### Fase 3: Advanced Features

- **Febrero 2026**
  - ⏳ Calendar view
  - ⏳ Reports system
  - ⏳ Analytics dashboard
  - ⏳ Export functionality

### Fase 4: Integration & Polish

- **Marzo 2026**
  - ⏳ SUNAT integration
  - ⏳ Email notifications
  - ⏳ File management improvements
  - ⏳ Performance optimization

### Fase 5: Production Ready

- **Abril 2026**
  - ⏳ Testing completo
  - ⏳ Security audit
  - ⏳ Deployment automation
  - ⏳ User documentation

## 👥 Equipo y Agentes

Este proyecto utiliza el sistema de **Multi-Agent Orchestration** con 9 agentes especializados:

1. **Architect Agent** - Decisiones de arquitectura
2. **Backend Agent** - Django/API development
3. **Database Agent** - Diseño de modelos
4. **Frontend Agent** - Quasar/Vue development
5. **Testing Agent** - Tests automatizados
6. **Security Agent** - Auditoría de seguridad
7. **Code Review Agent** - Revisión de código
8. **Documentation Agent** - Documentación
9. **DevOps Agent** - Deployment y CI/CD

## 📝 Convenciones

### Git Commits

Formato: `<type>(<scope>): <message>`

```bash
feat(circuits): add program CRUD endpoints
fix(auth): resolve token refresh issue
docs(readme): update installation steps
test(financial): add invoice service tests
refactor(suppliers): improve query performance
```

### Code Style

**Backend (Python)**:

- PEP 8
- Black formatter
- isort para imports
- Type hints donde sea posible

**Frontend (TypeScript)**:

- ESLint + Prettier
- Vue 3 Composition API
- Functional components
- TypeScript strict mode

## 🔒 Seguridad

- JWT con refresh tokens
- MFA opcional (TOTP)
- CORS configurado
- SQL injection protection (Django ORM)
- XSS protection (DRF serializers)
- CSRF protection
- Rate limiting
- Audit logging completo

## 📚 Recursos

### Documentación Técnica

- [Backend README](./backend/README.md)
- [Backend STATUS](./backend/STATUS.md)
- [Frontend README](./frontend/README.md)
- [API Docs](http://localhost:8000/api/docs)

### Guías

- [Contributing Guide](./CONTRIBUTING.md)
- [Changelog](./CHANGELOG.md)
- [Architecture Docs](./docs/architecture/)

### Ejemplos

- [Authentication Feature](./examples/authentication-feature.md)
- [Monolith to SPA Migration](./examples/monolith-to-spa-migration.md)

## 🐛 Troubleshooting

### Backend no inicia

1. Verificar PostgreSQL: `docker-compose ps`
2. Ver logs: `docker-compose logs web`
3. Verificar .env: `DATABASE_URL`, `REDIS_URL`

### Frontend no conecta

1. Verificar backend corriendo: `curl http://localhost:8000/api/v1/`
2. Verificar CORS en backend settings
3. Verificar `.env` frontend: `VITE_API_BASE_URL`

### Errores de MFA

1. Sincronizar reloj del sistema (NTP)
2. Regenerar QR code
3. Verificar app authenticator (Google Auth, Authy)

## 📞 Contacto y Soporte

- **Issues**: GitHub Issues
- **Documentación**: Ver carpeta `/docs`
- **Email**: support@travesia.com

## 📄 Licencia

Propietario - TravesIA © 2026. Todos los derechos reservados.

---

**Última Actualización**: 22 Enero 2026  
**Versión**: 1.0.0  
**Status**: En Desarrollo Activo 🚧

---

**Desarrollado con ❤️ por el equipo de Innovación usando Django + Quasar**
