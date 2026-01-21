# Documentación de Arquitectura - TravesIA

Este directorio contiene toda la documentación arquitectónica del proyecto TravesIA, un sistema de gestión integral para agencias de turismo especializadas en circuitos por Sudamérica.

---

## 📚 Contenido

### 1. [Plan de Arquitectura](./architecture-plan.md)
Documento maestro que define:
- Bounded contexts y separación de responsabilidades
- Arquitectura de alto nivel (C4 diagrams)
- Modelo de datos detallado
- Especificaciones de APIs REST
- Decisiones técnicas y patrones de diseño
- Estrategias de seguridad, escalabilidad y performance
- Timeline y plan de implementación
- Handoffs a otros agentes (Database, Backend, Frontend, etc.)

**Status**: ✅ Completado
**Última actualización**: 2026-01-20

---

### 2. [Modelo de Datos](./data-model.md)
Documentación detallada del modelo de datos:
- Diagramas entidad-relación por bounded context
- Definición de todas las entidades y sus campos
- Índices críticos para performance
- Constraints y validaciones
- Volumen estimado de datos
- Estrategias de particionamiento

**Status**: ✅ Completado
**Última actualización**: 2026-01-20

---

### 3. [Architecture Decision Records (ADRs)](../adr/)
Decisiones arquitectónicas documentadas:
- [ADR-0001: Django REST Framework](../adr/0001-django-rest-framework.md)
- [ADR-0002: PostgreSQL Database](../adr/0002-postgresql-database.md)
- [ADR-0003: Monolito Modular](../adr/0003-monolith-modular-architecture.md)

**Ver índice completo**: [docs/adr/README.md](../adr/README.md)

---

## 🏗️ Stack Tecnológico

| Capa | Tecnología | Versión |
|------|------------|---------|
| **Frontend** | Vue 3 + Quasar 2 | Latest |
| **Backend** | Django + DRF | 5.0 |
| **Base de Datos** | PostgreSQL | 15+ |
| **Cache** | Redis | 7+ |
| **Storage** | AWS S3 | - |
| **API** | REST (OpenAPI) | v1 |
| **Auth** | JWT + MFA | - |
| **Deployment** | Docker Compose | - |

---

## 🎯 Bounded Contexts

El sistema se organiza en 6 contextos principales:

1. **Circuit Management**: Programas, grupos, pasajeros, itinerarios
2. **Operations**: Transporte, alojamiento, servicios especializados
3. **Supplier Management**: Proveedores, servicios, precios
4. **Financial**: Costos, ventas, facturación SUNAT, comisiones
5. **Document Management**: Repositorio digital de documentos
6. **Analytics & Reporting**: Liquidaciones, reportes, KPIs

---

## 📊 Diagramas de Arquitectura

### Arquitectura de Alto Nivel

```
┌─────────────┐
│   Usuarios  │
│   (Staff)   │
└──────┬──────┘
       │ HTTPS
       ▼
┌─────────────────────────────────────────┐
│         Vue 3 + Quasar 2                │
│         (Frontend SPA)                  │
└──────────────┬──────────────────────────┘
               │ REST API (JSON)
               │ JWT Auth
               ▼
┌─────────────────────────────────────────┐
│      Django + Django REST Framework     │
│                                         │
│  ┌────────┬────────┬────────┬────────┐ │
│  │Circuits│Operations│Suppliers│Financial│ │
│  └────────┴────────┴────────┴────────┘ │
│  ┌────────┬────────┐                   │
│  │Documents│Analytics│                  │
│  └────────┴────────┘                   │
└──────────┬──────────┬───────────────────┘
           │          │
           ▼          ▼
    ┌──────────┐  ┌────────┐
    │PostgreSQL│  │ Redis  │
    │   (DB)   │  │(Cache) │
    └──────────┘  └────────┘
           │
           ▼
    ┌──────────┐
    │  AWS S3  │
    │(Documents)│
    └──────────┘
```

---

## 🔗 Integraciones Externas

| Sistema | Propósito | Tipo |
|---------|-----------|------|
| **SUNAT** | Facturación electrónica (Perú) | SOAP/REST |
| **AWS S3** | Almacenamiento de documentos | SDK |
| **Email Service** | Notificaciones | SMTP/API |
| **SMS Provider** | MFA y alertas | API |

---

## 🔐 Seguridad

### Autenticación
- JWT (JSON Web Tokens) con refresh tokens
- MFA (Multi-Factor Authentication) con TOTP
- Roles: Admin, Operations Manager, Tour Conductor, Accountant, Viewer

### Encriptación
- Datos en tránsito: TLS 1.3
- Datos en reposo: AES-256 (campos sensibles)
- Passwords: bcrypt/argon2

### Audit Trail
- Todos los cambios críticos registrados
- IP tracking
- Retention: 7 años

---

## ⚡ Performance

### Targets
- Response time: < 300ms (p95)
- Page load: < 2s
- Uptime: 99.5%

### Estrategias
- **Caching**: Redis (15min - 24h TTL según tipo de dato)
- **DB Optimization**: Índices estratégicos, query optimization
- **CDN**: CloudFront para assets estáticos
- **Connection Pooling**: pgBouncer para PostgreSQL

---

## 📈 Escalabilidad

### Fase Actual (Monolito Modular)
- Django instance única
- PostgreSQL single node
- Redis single instance
- Volumen: 50 grupos/año

### Futuro (si crece a 200+ grupos/año)
- Load balancer + múltiples Django instances
- PostgreSQL read replicas
- Redis cluster
- Celery workers distribuidos

---

## 🧪 Testing

### Cobertura Target
- **Unit Tests**: 80%+ coverage
- **Integration Tests**: Endpoints críticos
- **E2E Tests**: Flujos principales

### Herramientas
- **Backend**: pytest, pytest-django
- **Frontend**: Vitest, Cypress
- **API**: Postman/Newman

---

## 📦 Deployment

### Entornos
- **Development**: Local con Docker Compose
- **Staging**: AWS (ambiente de pruebas)
- **Production**: AWS (ambiente productivo)

### CI/CD
- **Plataforma**: GitHub Actions
- **Pipeline**: Test → Build → Deploy
- **Estrategia**: Blue/Green deployment

---

## 📅 Timeline de Implementación

| Fase | Duración | Descripción |
|------|----------|-------------|
| Setup | 1 semana | Infraestructura, Docker, repo |
| Circuit Management | 2 semanas | Programs, Groups, Passengers |
| Operations | 3 semanas | Transport, Hotels, Services |
| Suppliers | 1 semana | Supplier management |
| Financial | 2 semanas | Costs, Invoices, SUNAT |
| Documents | 1 semana | S3 integration |
| Analytics | 1 semana | Reports, KPIs |
| Testing & QA | 1 semana | Integration, E2E tests |
| Deployment | 1 semana | Production setup |
| **TOTAL** | **13 semanas** | ~3 meses |

---

## 👥 Handoffs

Este diseño arquitectónico está listo para ser implementado por los siguientes agentes:

### → Database Agent
- Crear esquema PostgreSQL
- Configurar Redis
- Implementar migraciones
- Documentar estrategia de backup

### → Backend Agent
- Implementar Django apps
- Crear API REST endpoints
- Integrar con SUNAT
- Configurar Celery

### → Frontend Agent
- Setup Quasar 2
- Implementar componentes
- State management (Pinia)
- Integración con API

### → DevOps Agent
- Docker Compose setup
- CI/CD pipeline
- AWS infrastructure
- Monitoreo y logging

### → Security Agent
- JWT + MFA implementation
- Encriptación de datos sensibles
- Audit trail
- Security testing

### → Testing Agent
- Unit tests
- Integration tests
- E2E tests
- Performance testing

---

## 📖 Referencias

- **Instrucciones Globales**: [.github/copilot-instructions.md](../../.github/copilot-instructions.md)
- **Contexto del Proyecto**: [project-context.md](../../project-context.md)
- **Requisitos**: [informacion.md](../../informacion.md)
- **ADRs**: [docs/adr/](../adr/)

---

**Versión**: 1.0
**Última Actualización**: 2026-01-20
**Mantenedor**: Architect Agent
**Status**: ✅ Ready for Implementation

## ¿Qué es un ADR?

Un ADR (Architecture Decision Record) documenta una decisión arquitectónica significativa junto con su contexto y consecuencias.

## Cuándo Crear un ADR

Crea un ADR cuando:

- Elijas entre múltiples alternativas técnicas significativas
- Tomes decisiones que afecten la estructura del sistema
- Selecciones tecnologías, frameworks o herramientas clave
- Cambies decisiones arquitectónicas previas

## Template ADR

Usa este template al crear nuevos ADRs:

```markdown
# ADR-XXX: [Título de la Decisión]

**Status**: [Proposed | Accepted | Deprecated | Superseded]
**Date**: YYYY-MM-DD
**Decision Makers**: [Nombres o roles]
**Supersedes**: [ADR-XXX] (si aplica)

## Context

[Describe el contexto y el problema que motivó la decisión.
¿Qué fuerzas están en juego? ¿Qué restricciones existen?]

## Decision

[Describe la decisión tomada. Sé específico y conciso.]

## Alternatives Considered

### Alternative 1: [Nombre]

**Pros**:

- [Pro 1]
- [Pro 2]

**Cons**:

- [Con 1]
- [Con 2]

### Alternative 2: [Nombre]

**Pros**:

- [Pro 1]

**Cons**:

- [Con 1]

## Consequences

### Positive

- [Consecuencia positiva 1]
- [Consecuencia positiva 2]

### Negative

- [Consecuencia negativa 1]
- [Consecuencia negativa 2]

### Neutral

- [Cambios necesarios, aprendizajes, etc.]

## Implementation Notes

[Detalles de implementación, consideraciones técnicas, pasos siguientes]

## Related Decisions

- [ADR-XXX: Título relacionado]
- [ADR-YYY: Otro título relacionado]

## References

- [Link a documentación]
- [Link a discusiones]
- [Link a benchmarks]
```

## Ejemplo: ADR-001

Ver ejemplo completo en `examples/authentication-feature.md`

## Numeración

- ADR-001, ADR-002, etc.
- Secuencial, nunca reutilizar números
- Usar 3 dígitos con padding: 001, 002, etc.

## Status Lifecycle

```
Proposed → Accepted → [Deprecated | Superseded]
           ↓
       Rejected
```

- **Proposed**: Propuesta en discusión
- **Accepted**: Decisión aceptada e implementada
- **Deprecated**: Ya no se recomienda pero aún en uso
- **Superseded**: Reemplazada por otra decisión (especifica cuál)
- **Rejected**: Propuesta rechazada (documentar por qué)

## Comandos Útiles

### Crear Nuevo ADR

```bash
# Listar ADRs existentes
ls -l docs/architecture/decisions/

# Crear nuevo (obtener próximo número)
NEXT_NUM=$(printf "%03d" $(($(ls docs/architecture/decisions/ | grep -oP '^\d+' | sort -n | tail -1) + 1)))

# Copiar template
cp docs/architecture/ADR-TEMPLATE.md docs/architecture/decisions/ADR-${NEXT_NUM}-mi-decision.md
```

### Buscar ADRs

```bash
# Buscar por keyword
grep -r "database" docs/architecture/decisions/

# Listar solo aceptados
grep -l "Status: Accepted" docs/architecture/decisions/*.md
```

## Best Practices

### 1. Sé Conciso

- ADRs no son specs completas
- Enfócate en la decisión y su justificación
- Enlaces a docs detalladas si es necesario

### 2. Documenta el Contexto

- ¿Por qué era necesario decidir?
- ¿Qué restricciones había?
- ¿Qué alternativas se consideraron?

### 3. Explica las Consecuencias

- No solo las positivas
- Documenta trade-offs
- Incluye consecuencias a largo plazo

### 4. Actualiza Status

- Marca como Deprecated cuando cambies
- Crea ADR nuevo que superseda (no edites el viejo)
- Mantén historia de decisiones

### 5. Vincular Decisiones Relacionadas

- Referencias a ADRs relacionados
- Cadenas de decisiones
- Evolución del pensamiento

## Ejemplo ADR Completo

```markdown
# ADR-001: Use PostgreSQL as Primary Database

**Status**: Accepted
**Date**: 2026-01-10
**Decision Makers**: Architect Agent, Backend Team

## Context

We need a relational database for our SaaS application that handles:

- User authentication and authorization
- Transactional data (orders, payments)
- Complex queries with joins
- ACID guarantees
- Scalability to 100k+ users

## Decision

We will use PostgreSQL as our primary database.

## Alternatives Considered

### Alternative 1: MySQL

**Pros**:

- Wide adoption
- Good performance
- Many hosting options

**Cons**:

- Less advanced JSON support
- Weaker full-text search
- License concerns (Oracle)

### Alternative 2: MongoDB

**Pros**:

- Flexible schema
- Horizontal scaling
- Good for rapid prototyping

**Cons**:

- No ACID transactions (initially)
- Eventual consistency challenges
- Not ideal for complex joins

## Consequences

### Positive

- Excellent ACID compliance
- Advanced JSON support (JSONB)
- Powerful full-text search
- Rich extension ecosystem (PostGIS, etc.)
- Strong community and tooling

### Negative

- Vertical scaling primary approach
- More complex clustering than MongoDB
- Requires careful index management

### Neutral

- Team needs to learn PostgreSQL-specific features
- Will use Prisma ORM for abstraction
- Hosting costs similar to alternatives

## Implementation Notes

- Use PostgreSQL 15+
- Enable JSONB for flexible fields
- Set up proper indexes from start
- Use connection pooling (PgBouncer)
- Backups via automated snapshots

## Related Decisions

- ADR-002: Use Prisma as ORM
- ADR-005: Database migration strategy

## References

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Why Postgres](https://www.craigkerstiens.com/2017/04/30/why-postgres-five-years-later/)
```

---

**Mantén tus ADRs actualizados y documenta todas las decisiones importantes!**
