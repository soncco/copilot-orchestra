# Project Context - Variables de Configuración

> Este archivo define las variables de configuración que se utilizan en todo el sistema de orquestación multi-agente. Actualiza estos valores según el proyecto específico.

---

## 🎯 Información del Proyecto

El archivo informacion.md contiene en grandes rasgos los requisitos del sistema.

### Identificación

- **Nombre del Proyecto**: TravesIA
- **Versión**: 1.0
- **Tipo**: SaaS Application
- **Fecha de Inicio**: 20/01/2026
- **Equipo**: Innovación

---

## 🏗️ Stack Tecnológico

### Frontend

```yaml
FRAMEWORK: Vue 3 + Quasar 2
# Opciones: React, Vue, Angular, Svelte, Next.js, Nuxt, SolidJS, Qwik
```

### Backend

```yaml
BACKEND_STACK: Python
# Opciones: Node.js, Python, Java, Go, Rust, PHP, Ruby, C#/.NET

BACKEND_FRAMEWORK: Django
# Node: Express, Fastify, NestJS, Koa, Hono
# Python: FastAPI, Django, Flask, Starlette
# Java: Spring Boot, Quarkus, Micronaut
# Go: Gin, Echo, Fiber, Chi

API_PATTERN: REST
# Opciones: REST, GraphQL, gRPC, tRPC, WebSocket

API_VERSION: v1
# Ejemplo: v1, v2, etc.
```

### Base de Datos

```yaml
DATABASE: PostgreSQL
# Opciones: PostgreSQL, MySQL, MongoDB, Redis, CockroachDB, Cassandra

DATABASE_ORM: Django ORM
# Opciones: Prisma, TypeORM, Sequelize, Drizzle, SQLAlchemy, GORM, Hibernate

CACHE_LAYER: Redis
# Opciones: Redis, Memcached, DynamoDB, in-memory
```

---

## ☁️ Infraestructura y DevOps

### Deployment

```yaml
DEPLOYMENT_STRATEGY: Docker
# Opciones: Docker, Kubernetes, Serverless, VM-based, Platform-as-Service

CONTAINER_REGISTRY: Docker
# Opciones: Docker Hub, ECR, GCR, ACR, GitHub Container Registry
```

### Monitoring y Observability

```yaml
LOGGING: Django Logging
# Opciones: CloudWatch, Stackdriver, ELK Stack, Loki, Datadog
```

---

## 🔐 Seguridad y Autenticación

### Autenticación

```yaml
AUTH_METHOD: JWT
# Opciones: JWT, OAuth2, Session-based, Auth0, Clerk, Supabase Auth, Firebase Auth

MFA_ENABLED: true
# Opciones: true, false
```

### Storage

```yaml
FILE_STORAGE: S3
# Opciones: S3, GCS, Azure Blob Storage, Cloudinary, DigitalOcean Spaces
```

---

## 🌐 Configuración de Entornos

### Entornos Disponibles

```yaml

```

### URLs Base

```yaml
DEVELOPMENT_BACKEND_URL: "http://localhost:8000"
DEVELOPMENT_FRONTEND_URL: "http://localhost:3000"
```

---

### Development Tools

```yaml
API_DOCUMENTATION: Swagger/OpenAPI
# Opciones: Swagger/OpenAPI, Postman, Stoplight, Redoc

DATABASE_GUI: pgAdmin
# Opciones: pgAdmin, DBeaver, TablePlus, DataGrip
# pgAdmin disponible en: http://localhost:5050

LOCAL_DEV_ENVIRONMENT: Docker Compose
# Opciones: Docker Compose, Kubernetes (kind/minikube), Native, Devcontainers
```

### Commit Convention

```yaml
COMMIT_STANDARD: "Conventional Commits"
# feat:, fix:, docs:, style:, refactor:, test:, chore:
```

---

## 📝 Configuración de Agentes

### Agentes Activos

Lista de agentes habilitados para este proyecto:

- [x] Architect Agent
- [x] Backend Agent
- [x] Frontend Agent
- [x] DevOps Agent
- [x] Security Agent
- [x] Testing Agent
- [x] Documentation Agent
- [x] Code Review Agent
- [x] Database Agent
- [x] Integration Agent

### Workflow Predeterminado

```yaml
DEFAULT_WORKFLOW: "feature_development"
# Opciones: feature_development, bug_fix, refactor, deployment
```

---

## 🔄 Sincronización y Versionado

```yaml
VERSION_CONTROL: "Git"
REPOSITORY_HOST: "{{REPOSITORY_HOST}}"
# Opciones: GitHub, GitLab, Bitbucket, Azure DevOps

MAIN_BRANCH: main
# Opciones: main, master, production
```

---

## 📌 Notas Importantes

### Instrucciones de Uso

1. **Inicialización**: Reemplaza todas las variables `{{VARIABLE}}` con los valores reales del proyecto
2. **Validación**: Ejecuta `./scripts/validate-config.sh` para verificar la configuración
3. **Sincronización**: Este archivo debe estar sincronizado con `agents-config.json`
4. **Actualización**: Mantén este archivo actualizado cuando cambies tecnologías

### Variables Requeridas

Las siguientes variables son **obligatorias** para el funcionamiento del sistema:

- `PROJECT_NAME`
- `FRAMEWORK`
- `BACKEND_STACK`
- `DATABASE`
- `CLOUD_PROVIDER`
- `AUTH_METHOD`
- `DEPLOYMENT_STRATEGY`

### Ejemplo de Configuración Completa

```yaml
# Proyecto Next.js + FastAPI + PostgreSQL + AWS
PROJECT_NAME: "MyAwesomeSaaS"
FRAMEWORK: "Next.js"
BACKEND_STACK: "Python"
BACKEND_FRAMEWORK: "FastAPI"
DATABASE: "PostgreSQL"
DATABASE_ORM: "Prisma"
CLOUD_PROVIDER: "AWS"
AUTH_METHOD: "JWT"
DEPLOYMENT_STRATEGY: "Docker"
CI_CD_PLATFORM: "GitHub Actions"
```

---

**Última actualización**: `{{LAST_UPDATE_DATE}}`
**Versión del contexto**: `1.0.0`
**Responsable**: `{{TECH_LEAD_NAME}}`
