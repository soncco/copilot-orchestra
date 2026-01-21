# 📚 Índice de Documentación - TravesIA

> Guía completa de toda la documentación del proyecto

---

## 🎯 Documentos Principales

### General

1. **[README.md](../README.md)**
   - Sistema Multi-Agent Orchestration
   - Arquitectura del sistema de agentes
   - Quick start general

2. **[PROJECT-OVERVIEW.md](../PROJECT-OVERVIEW.md)** ⭐
   - Descripción completa del proyecto TravesIA
   - Stack tecnológico
   - Estructura del proyecto
   - Estado actual y roadmap

3. **[project-context.md](../project-context.md)**
   - Variables de configuración del proyecto
   - Tecnologías seleccionadas
   - Convenciones y estándares

4. **[PROJECT-SUMMARY.md](../PROJECT-SUMMARY.md)**
   - Resumen técnico del proyecto
   - Decisiones de arquitectura

5. **[PROJECT_STATUS.sh](../PROJECT_STATUS.sh)** 🚀
   - Script visual de estado del proyecto
   - Verificación de servicios
   - Comandos útiles
   - **Ejecutar**: `chmod +x PROJECT_STATUS.sh && ./PROJECT_STATUS.sh`

---

## 🔧 Backend (Django)

### Documentación General

1. **[backend/README.md](../backend/README.md)**
   - Setup y configuración del backend
   - Instalación con Docker
   - Variables de entorno
   - Comandos útiles

2. **[backend/STATUS.md](../backend/STATUS.md)** ⭐
   - Estado completo del backend
   - 6 apps implementadas
   - 22 modelos documentados
   - API endpoints listados
   - Próximos pasos

### Apps Django

Cada app tiene su propia documentación:

#### 1. Authentication

- **Path**: `backend/apps/authentication/`
- **Modelos**: User, MFADevice, AuditLog
- **Features**: JWT, MFA (TOTP), Audit logging
- **Roles**: ADMIN, MANAGER, SALES, GUIDE, OPERATIONS

#### 2. Circuits

- **Path**: `backend/apps/circuits/`
- **Modelos**: Program, Group, Passenger, Itinerary, Flight
- **Features**: Gestión de circuitos turísticos, grupos, pasajeros

#### 3. Suppliers

- **Path**: `backend/apps/suppliers/`
- **Modelos**: Supplier, SupplierService, SupplierPricing, ExchangeRate
- **Features**: Catálogo de proveedores, tarifas, multi-moneda

#### 4. Operations

- **Path**: `backend/apps/operations/`
- **Modelos**: Hotel, Transportation, Staff, OperationalService
- **Features**: Gestión operativa de servicios turísticos

#### 5. Financial

- **Path**: `backend/apps/financial/`
- **Modelos**: Invoice, Cost, Sale, Commission, BankDeposit
- **Features**: Facturación SUNAT, costos, ventas, comisiones

#### 6. Documents

- **Path**: `backend/apps/documents/`
- **Modelos**: Document
- **Features**: Gestión de documentos con AWS S3

### API Documentation

1. **[docs/api/README.md](./api/README.md)**
   - Guía de la API REST
   - OpenAPI/Swagger specification
   - Endpoints documentados

2. **Swagger UI (Live)**
   - URL: http://localhost:8000/api/docs
   - Documentación interactiva
   - Try-it-out directo

3. **ReDoc (Live)**
   - URL: http://localhost:8000/api/redoc
   - Documentación estática elegante

---

## 🎨 Frontend (Quasar 2)

### Documentación General

1. **[frontend/README.md](../frontend/README.md)**
   - Setup del frontend Quasar 2
   - Instalación y configuración
   - Desarrollo y build
   - Estructura de carpetas

2. **[FRONTEND_COMPLETE.md](../FRONTEND_COMPLETE.md)** ⭐
   - Documentación completa de lo implementado
   - 14 archivos creados detallados
   - API client, services, stores, pages
   - TypeScript types (19 interfaces)
   - Próximos pasos con estimaciones

### Arquitectura Frontend

**Tecnologías**:

- Vue 3 (Composition API)
- Quasar 2 (Material Design)
- TypeScript (strict mode)
- Pinia (state management)
- Axios (HTTP client)
- Vite (build tool)

**Estructura**:

```
frontend/src/
├── layouts/       MainLayout (sidebar, header)
├── pages/         Login, Dashboard, CRUD pages
├── services/      API client, Auth service
├── stores/        Pinia stores (auth)
├── types/         TypeScript interfaces
├── router/        Vue Router + guards
└── components/    Componentes reutilizables
```

### Páginas Implementadas

1. **LoginPage** ✅
   - Autenticación JWT
   - Soporte MFA (TOTP)
   - Validación de formulario
   - Error handling

2. **DashboardPage** ✅
   - Stats cards
   - Recent groups
   - Quick actions
   - Welcome message

3. **MainLayout** ✅
   - Sidebar con 13 menu items
   - User menu
   - Responsive design

---

## 🏗️ Arquitectura

### Diagramas

1. **[docs/architecture/README.md](./architecture/README.md)**
   - Arquitectura general del sistema
   - Diagramas de componentes
   - Flujos de datos

### Patrones y Decisiones

**Backend**:

- Repository Pattern
- Service Layer
- Django REST Framework ViewSets
- JWT Authentication con MFA
- Celery para tareas asíncronas

**Frontend**:

- Composition API (Vue 3)
- Singleton para API client
- Pinia stores para state
- Route guards para auth
- Auto-refresh de tokens

---

## 🔐 Seguridad

### Autenticación y Autorización

**JWT Tokens**:

- Access token: 24 horas
- Refresh token: 7 días
- Auto-refresh en interceptor
- Storage: localStorage (frontend)

**MFA (Multi-Factor Auth)**:

- TOTP (Time-based One-Time Password)
- Compatible con Google Authenticator, Authy
- QR code para setup
- Backup codes (futuro)

**Roles y Permisos**:

- ADMIN: Full access
- MANAGER: Gestión completa
- SALES: Ventas y pasajeros
- GUIDE: Consulta de itinerarios
- OPERATIONS: Operaciones

### Buenas Prácticas Implementadas

- ✅ CORS configurado
- ✅ SQL Injection protection (Django ORM)
- ✅ XSS protection (DRF serializers)
- ✅ CSRF tokens
- ✅ Rate limiting (futuro)
- ✅ Audit logging completo
- ✅ Password hashing (Django default)

---

## 🐳 DevOps y Deployment

### Docker

**Archivos**:

- `backend/Dockerfile` - Backend container
- `backend/docker-compose.yml` - Servicios completos

**Servicios**:

- `web`: Django app
- `db`: PostgreSQL 15
- `redis`: Redis 7 (cache + Celery)
- `celery`: Celery worker
- `celery-beat`: Celery scheduler

**Comandos**:

```bash
docker-compose up -d              # Iniciar
docker-compose logs -f web        # Ver logs
docker-compose exec web bash      # Shell
docker-compose down               # Detener
```

### Environment Variables

**Backend** (.env):

```env
DEBUG=True
DATABASE_URL=postgresql://user:pass@db:5432/travesia
REDIS_URL=redis://redis:6379/0
SECRET_KEY=your-secret-key
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
AWS_STORAGE_BUCKET_NAME=travesia-files
```

**Frontend** (.env):

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_API_TIMEOUT=10000
VITE_JWT_ACCESS_TOKEN_KEY=travesia_access_token
VITE_JWT_REFRESH_TOKEN_KEY=travesia_refresh_token
```

---

## 🧪 Testing

### Backend Tests

**Pendiente**: 0% coverage

**Próximo**:

- Unit tests para modelos
- Integration tests para APIs
- Tests para autenticación y permisos

**Comandos**:

```bash
cd backend
python manage.py test
python manage.py test apps.authentication
coverage run --source='.' manage.py test
coverage report
```

### Frontend Tests

**Pendiente**: 0% coverage

**Próximo**:

- Unit tests con Vitest
- Component tests con Testing Library
- E2E tests con Playwright

**Comandos**:

```bash
cd frontend
npm run test
npm run test:coverage
npm run test:e2e
```

---

## 📖 Ejemplos y Tutoriales

### Use Cases

1. **[examples/authentication-feature.md](../examples/authentication-feature.md)**
   - Ejemplo de implementación de feature de autenticación
   - Workflow multi-agente

2. **[examples/monolith-to-spa-migration.md](../examples/monolith-to-spa-migration.md)**
   - Migración de monolito a SPA
   - Estrategia y pasos

### Snippets Útiles

**Backend - Crear un nuevo endpoint**:

```python
# views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

class MyModelViewSet(viewsets.ModelViewSet):
    queryset = MyModel.objects.all()
    serializer_class = MyModelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(
            user=self.request.user
        )
```

**Frontend - Llamar a API**:

```typescript
// pages/MyPage.vue
import { apiClient } from "@/services/api";

const fetchData = async () => {
  try {
    const data = await apiClient.get("/myendpoint");
    console.log(data);
  } catch (error) {
    console.error(error);
  }
};
```

---

## 🗺️ Roadmap y Planning

### Q1 2026 (En Curso)

- ✅ Backend API completa
- ✅ Frontend foundation (auth, dashboard)
- 🚧 Frontend CRUD pages (15%)
- ⏳ Testing básico
- ⏳ Integración SUNAT

### Q2 2026

- ⏳ Dashboard con analytics
- ⏳ Sistema de reportes
- ⏳ Calendar view
- ⏳ Email notifications
- ⏳ File management avanzado

### Q3 2026

- ⏳ Real-time notifications (WebSocket)
- ⏳ WhatsApp integration
- ⏳ Payment gateway integration
- ⏳ Mobile app (Capacitor)

### Q4 2026

- ⏳ AI features (recommendations)
- ⏳ Multi-idioma (i18n)
- ⏳ Multi-moneda avanzado
- ⏳ Public API para partners

---

## 👥 Equipo y Agentes

### Sistema Multi-Agente

Este proyecto usa un **sistema de orquestación multi-agente** con 9 agentes especializados:

1. **[Architect Agent](./.github/agents/architect-agent.md)**
   - Decisiones de arquitectura
   - Diseño de sistemas
   - Patrones y best practices

2. **[Backend Agent](./.github/agents/backend-agent.md)**
   - Desarrollo Django/API
   - Lógica de negocio
   - Database integration

3. **[Database Agent](./.github/agents/database-agent.md)**
   - Diseño de modelos
   - Optimización de queries
   - Migraciones

4. **[Frontend Agent](./.github/agents/frontend-agent.md)**
   - Desarrollo Quasar/Vue
   - UI/UX implementation
   - State management

5. **[Testing Agent](./.github/agents/testing-agent.md)**
   - Tests automatizados
   - Quality assurance
   - Test coverage

6. **[Security Agent](./.github/agents/security-agent.md)**
   - Auditoría de seguridad
   - Vulnerability scanning
   - Best practices enforcement

7. **[Code Review Agent](./.github/agents/code-review-agent.md)**
   - Revisión de código
   - Code quality
   - Refactoring suggestions

8. **[Documentation Agent](./.github/agents/documentation-agent.md)**
   - Documentación técnica
   - API docs
   - User guides

9. **[DevOps Agent](./.github/agents/devops-agent.md)**
   - Deployment
   - CI/CD pipelines
   - Infrastructure

### Configuración

**[agents-config.json](../.github/agents-config.json)**:

- Configuración de todos los agentes
- Workflows definidos
- Protocolos de handoff

**[copilot-instructions.md](../.github/copilot-instructions.md)**:

- Instrucciones globales
- Principios fundamentales
- Estándares de código

---

## 🔄 Workflows

### Feature Development

1. **Architect Agent** → Diseña la feature
2. **Backend Agent** → Implementa API
3. **Frontend Agent** → Implementa UI
4. **Testing Agent** → Crea tests
5. **Security Agent** → Audita
6. **Code Review Agent** → Revisa
7. **Documentation Agent** → Documenta
8. **DevOps Agent** → Despliega

### Bug Fix

1. **Testing Agent** → Reproduce bug
2. **Agente responsable** → Corrige
3. **Testing Agent** → Verifica fix
4. **Code Review Agent** → Revisa
5. **DevOps Agent** → Despliega (si crítico)

---

## 📞 Recursos y Soporte

### Links Útiles

**Backend**:

- Django: https://docs.djangoproject.com/
- DRF: https://www.django-rest-framework.org/
- PostgreSQL: https://www.postgresql.org/docs/
- Celery: https://docs.celeryproject.org/

**Frontend**:

- Vue 3: https://vuejs.org/
- Quasar: https://quasar.dev/
- Pinia: https://pinia.vuejs.org/
- TypeScript: https://www.typescriptlang.org/

**DevOps**:

- Docker: https://docs.docker.com/
- AWS: https://docs.aws.amazon.com/

### Contacto

- **Issues**: GitHub Issues
- **Email**: support@travesia.com
- **Wiki**: (futuro)

---

## 📝 Convenciones

### Git Commits

Formato Conventional Commits:

```
<type>(<scope>): <message>

Types:
- feat: Nueva feature
- fix: Bug fix
- docs: Documentación
- style: Formato
- refactor: Refactoring
- test: Tests
- chore: Mantenimiento

Examples:
feat(circuits): add program CRUD endpoints
fix(auth): resolve token refresh issue
docs(readme): update installation steps
```

### Code Style

**Python (Backend)**:

- PEP 8
- Black formatter
- isort para imports
- Type hints

**TypeScript (Frontend)**:

- ESLint + Prettier
- Vue 3 Style Guide
- Composition API
- Strict mode

### Naming

**Variables**: camelCase (TS), snake_case (Python)
**Functions**: verbos descriptivos
**Classes**: PascalCase
**Constants**: UPPER_SNAKE_CASE
**Files**: kebab-case.vue, snake_case.py

---

## ✅ Checklist de Setup

### Primer Setup

- [ ] Clonar repositorio
- [ ] Leer PROJECT-OVERVIEW.md
- [ ] Instalar Docker + Docker Compose
- [ ] Instalar Node.js 18+
- [ ] Instalar Python 3.11+

### Backend Setup

- [ ] `cd backend`
- [ ] `cp .env.example .env`
- [ ] Editar .env con credenciales
- [ ] `docker-compose up -d`
- [ ] `docker-compose exec web python manage.py migrate`
- [ ] `docker-compose exec web python manage.py createsuperuser`
- [ ] Probar: http://localhost:8000/api/docs

### Frontend Setup

- [ ] `cd frontend`
- [ ] `npm install`
- [ ] `cp .env.example .env`
- [ ] Editar .env (VITE_API_BASE_URL)
- [ ] `npm run dev`
- [ ] Probar: http://localhost:9000

### Verificación

- [ ] Login funciona
- [ ] Dashboard carga
- [ ] Tokens se refrescan
- [ ] Logout funciona
- [ ] Backend responde en /api/v1/
- [ ] Swagger docs accessible

---

## 🎯 Quick Reference

### URLs Importantes

| Servicio     | URL                             | Descripción          |
| ------------ | ------------------------------- | -------------------- |
| Frontend     | http://localhost:9000           | Quasar app           |
| Backend API  | http://localhost:8000/api/v1    | REST API             |
| Django Admin | http://localhost:8000/admin     | Admin panel          |
| Swagger      | http://localhost:8000/api/docs  | API docs interactiva |
| ReDoc        | http://localhost:8000/api/redoc | API docs estática    |

### Comandos Rápidos

```bash
# Backend
cd backend && docker-compose up -d
docker-compose logs -f web
docker-compose exec web python manage.py shell

# Frontend
cd frontend && npm run dev
npm run build

# Ver estado
./PROJECT_STATUS.sh

# Tests
cd backend && python manage.py test
cd frontend && npm run test
```

### Estructura de Archivos

```
ericxpeditions/
├── backend/          ✅ Completo (100%)
├── frontend/         🚧 En desarrollo (30%)
├── docs/            📚 Documentación
│   ├── api/         API specs
│   └── architecture/ Diagramas
├── .github/         🤖 Agentes
└── examples/        📖 Ejemplos
```

---

## 📌 Próximos Pasos Inmediatos

1. **Test de Integración** (30 min)
   - Verificar login end-to-end
   - Probar dashboard
   - Validar token refresh

2. **Programs CRUD Page** (3-4 horas)
   - ProgramsListPage.vue
   - ProgramFormPage.vue
   - programs.service.ts

3. **Componentes Reutilizables** (2-3 horas)
   - DataTable.vue
   - FormDialog.vue
   - ConfirmDialog.vue

4. **Groups CRUD Page** (3-4 horas)
   - GroupsListPage.vue
   - GroupFormPage.vue
   - groups.service.ts

---

**Última actualización**: 22 Enero 2026  
**Versión**: 1.0.0  
**Mantenedor**: Equipo de Innovación

---

**💡 Tip**: Ejecuta `./PROJECT_STATUS.sh` para ver el estado visual del proyecto
