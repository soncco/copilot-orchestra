# Project Context - Variables de Configuración

> Este archivo define las variables de configuración que se utilizan en todo el sistema de orquestación multi-agente. Actualiza estos valores según el proyecto específico.

---

## 🎯 Información del Proyecto

### Identificación

- **Nombre del Proyecto**: `{{PROJECT_NAME}}`
- **Versión**: `{{PROJECT_VERSION}}`
- **Tipo**: SaaS Application
- **Fecha de Inicio**: `{{START_DATE}}`
- **Equipo**: `{{TEAM_NAME}}`

---

## 🏗️ Stack Tecnológico

### Frontend

```yaml
FRAMEWORK: "{{FRAMEWORK}}"
# Opciones: React, Vue, Angular, Svelte, Next.js, Nuxt, SolidJS, Qwik

UI_LIBRARY: "{{UI_LIBRARY}}"
# Opciones: Material-UI, Ant Design, Chakra UI, Tailwind CSS, Bootstrap, Shadcn/UI

STATE_MANAGEMENT: "{{STATE_MANAGEMENT}}"
# Opciones: Redux, Zustand, MobX, Recoil, Jotai, Context API, Pinia (Vue)

STYLING_APPROACH: "{{STYLING_APPROACH}}"
# Opciones: CSS Modules, Styled Components, Emotion, Tailwind, SASS, CSS-in-JS

BUILD_TOOL: "{{BUILD_TOOL}}"
# Opciones: Vite, Webpack, Turbopack, esbuild, Parcel, Rollup
```

### Backend

```yaml
BACKEND_STACK: "{{BACKEND_STACK}}"
# Opciones: Node.js, Python, Java, Go, Rust, PHP, Ruby, C#/.NET

BACKEND_FRAMEWORK: "{{BACKEND_FRAMEWORK}}"
# Node: Express, Fastify, NestJS, Koa, Hono
# Python: FastAPI, Django, Flask, Starlette
# Java: Spring Boot, Quarkus, Micronaut
# Go: Gin, Echo, Fiber, Chi

API_PATTERN: "{{API_PATTERN}}"
# Opciones: REST, GraphQL, gRPC, tRPC, WebSocket

API_VERSION: "{{API_VERSION}}"
# Ejemplo: v1, v2, etc.
```

### Base de Datos

```yaml
DATABASE: "{{DATABASE}}"
# Opciones: PostgreSQL, MySQL, MongoDB, Redis, CockroachDB, Cassandra

DATABASE_ORM: "{{DATABASE_ORM}}"
# Opciones: Prisma, TypeORM, Sequelize, Drizzle, SQLAlchemy, GORM, Hibernate

CACHE_LAYER: "{{CACHE_LAYER}}"
# Opciones: Redis, Memcached, DynamoDB, in-memory

SEARCH_ENGINE: "{{SEARCH_ENGINE}}"
# Opciones: Elasticsearch, Algolia, MeiliSearch, Typesense, none
```

---

## ☁️ Infraestructura y DevOps

### Cloud Provider

```yaml
CLOUD_PROVIDER: "{{CLOUD_PROVIDER}}"
# Opciones: AWS, GCP, Azure, DigitalOcean, Vercel, Netlify, Railway, Fly.io

REGION: "{{REGION}}"
# Ejemplo: us-east-1, eu-west-1, etc.

CDN: "{{CDN}}"
# Opciones: CloudFront, Cloudflare, Fastly, Akamai, none
```

### Deployment

```yaml
DEPLOYMENT_STRATEGY: "{{DEPLOYMENT_STRATEGY}}"
# Opciones: Docker, Kubernetes, Serverless, VM-based, Platform-as-Service

CONTAINER_REGISTRY: "{{CONTAINER_REGISTRY}}"
# Opciones: Docker Hub, ECR, GCR, ACR, GitHub Container Registry

ORCHESTRATION: "{{ORCHESTRATION}}"
# Opciones: Kubernetes, Docker Swarm, ECS, Cloud Run, none

CI_CD_PLATFORM: "{{CI_CD_PLATFORM}}"
# Opciones: GitHub Actions, GitLab CI, CircleCI, Jenkins, Travis CI, Bitbucket Pipelines
```

### Monitoring y Observability

```yaml
LOGGING: "{{LOGGING}}"
# Opciones: CloudWatch, Stackdriver, ELK Stack, Loki, Datadog

MONITORING: "{{MONITORING}}"
# Opciones: Prometheus + Grafana, Datadog, New Relic, Dynatrace, AppDynamics

APM: "{{APM}}"
# Opciones: Sentry, Bugsnag, Rollbar, New Relic, DataDog APM

TRACING: "{{TRACING}}"
# Opciones: Jaeger, Zipkin, OpenTelemetry, AWS X-Ray
```

---

## 🔐 Seguridad y Autenticación

### Autenticación

```yaml
AUTH_METHOD: "{{AUTH_METHOD}}"
# Opciones: JWT, OAuth2, Session-based, Auth0, Clerk, Supabase Auth, Firebase Auth

AUTH_PROVIDER: "{{AUTH_PROVIDER}}"
# Opciones: Custom, Auth0, Clerk, Supabase, Firebase, Okta, AWS Cognito

SESSION_STORAGE: "{{SESSION_STORAGE}}"
# Opciones: Redis, Database, Memory, JWT (stateless)

MFA_ENABLED: "{{MFA_ENABLED}}"
# Opciones: true, false
```

### Security Tools

```yaml
SECRETS_MANAGEMENT: "{{SECRETS_MANAGEMENT}}"
# Opciones: AWS Secrets Manager, GCP Secret Manager, HashiCorp Vault, Doppler

SSL_PROVIDER: "{{SSL_PROVIDER}}"
# Opciones: Let's Encrypt, AWS ACM, Cloudflare, DigiCert

WAF: "{{WAF}}"
# Opciones: AWS WAF, Cloudflare WAF, Imperva, none
```

---

## 📧 Servicios Externos e Integraciones

### Comunicaciones

```yaml
EMAIL_SERVICE: "{{EMAIL_SERVICE}}"
# Opciones: SendGrid, AWS SES, Mailgun, Postmark, Resend, SMTP

SMS_SERVICE: "{{SMS_SERVICE}}"
# Opciones: Twilio, AWS SNS, Vonage, MessageBird, none

NOTIFICATION_SERVICE: "{{NOTIFICATION_SERVICE}}"
# Opciones: Firebase Cloud Messaging, OneSignal, Pusher, Socket.io
```

### Pagos y Facturación

```yaml
PAYMENT_PROVIDER: "{{PAYMENT_PROVIDER}}"
# Opciones: Stripe, PayPal, Square, Braintree, Adyen, none

SUBSCRIPTION_MANAGEMENT: "{{SUBSCRIPTION_MANAGEMENT}}"
# Opciones: Stripe Billing, Chargebee, Recurly, Paddle
```

### Storage

```yaml
FILE_STORAGE: "{{FILE_STORAGE}}"
# Opciones: S3, GCS, Azure Blob Storage, Cloudinary, DigitalOcean Spaces

MEDIA_PROCESSING: "{{MEDIA_PROCESSING}}"
# Opciones: Cloudinary, Imgix, ImageKit, AWS MediaConvert, none
```

---

## 🧪 Testing y Calidad

### Testing Framework

```yaml
UNIT_TEST_FRAMEWORK: "{{UNIT_TEST_FRAMEWORK}}"
# Opciones: Jest, Vitest, Mocha, Pytest, JUnit, Go Test

E2E_TEST_FRAMEWORK: "{{E2E_TEST_FRAMEWORK}}"
# Opciones: Playwright, Cypress, Selenium, Puppeteer, TestCafe

API_TEST_FRAMEWORK: "{{API_TEST_FRAMEWORK}}"
# Opciones: Supertest, Postman, REST Assured, Insomnia

COVERAGE_TOOL: "{{COVERAGE_TOOL}}"
# Opciones: Istanbul, c8, Coverage.py, JaCoCo
```

### Code Quality

```yaml
LINTER: "{{LINTER}}"
# Opciones: ESLint, Pylint, Flake8, Golangci-lint, RuboCop

FORMATTER: "{{FORMATTER}}"
# Opciones: Prettier, Black, gofmt, rustfmt, StandardJS

TYPE_CHECKER: "{{TYPE_CHECKER}}"
# Opciones: TypeScript, Flow, MyPy, none

CODE_REVIEW_TOOL: "{{CODE_REVIEW_TOOL}}"
# Opciones: SonarQube, CodeClimate, Codacy, DeepSource
```

---

## 🌐 Configuración de Entornos

### Entornos Disponibles

```yaml
ENVIRONMENTS:
  - development
  - staging
  - production
  - testing (opcional)

BRANCH_STRATEGY: "{{BRANCH_STRATEGY}}"
# Opciones: Git Flow, GitHub Flow, Trunk-based, GitLab Flow
```

### URLs Base

```yaml
DEVELOPMENT_URL: "http://localhost:{{DEV_PORT}}"
STAGING_URL: "{{STAGING_URL}}"
PRODUCTION_URL: "{{PRODUCTION_URL}}"
API_BASE_URL: "{{API_BASE_URL}}"
```

---

## 📊 Analytics y Business Intelligence

```yaml
ANALYTICS: "{{ANALYTICS}}"
# Opciones: Google Analytics, Mixpanel, Amplitude, Plausible, PostHog

PRODUCT_ANALYTICS: "{{PRODUCT_ANALYTICS}}"
# Opciones: Mixpanel, Amplitude, PostHog, Heap

ERROR_TRACKING: "{{ERROR_TRACKING}}"
# Opciones: Sentry, Bugsnag, Rollbar, LogRocket
```

---

## 🔧 Herramientas de Desarrollo

### Package Managers

```yaml
PACKAGE_MANAGER: "{{PACKAGE_MANAGER}}"
# Opciones: npm, yarn, pnpm, bun (Node); pip, poetry (Python); maven, gradle (Java)

MONO_REPO_TOOL: "{{MONO_REPO_TOOL}}"
# Opciones: Turborepo, Nx, Lerna, Rush, none
```

### Development Tools

```yaml
API_DOCUMENTATION: "{{API_DOCUMENTATION}}"
# Opciones: Swagger/OpenAPI, Postman, Stoplight, Redoc

DATABASE_GUI: "{{DATABASE_GUI}}"
# Opciones: pgAdmin, MongoDB Compass, DBeaver, TablePlus, Prisma Studio

LOCAL_DEV_ENVIRONMENT: "{{LOCAL_DEV_ENVIRONMENT}}"
# Opciones: Docker Compose, Kubernetes (kind/minikube), Native, Devcontainers
```

---

## 🎨 Convenciones del Proyecto

### Naming Conventions

```yaml
FILE_NAMING: "{{FILE_NAMING}}"
# Opciones: kebab-case, camelCase, PascalCase, snake_case

COMPONENT_NAMING: "PascalCase"
FUNCTION_NAMING: "camelCase"
CONSTANT_NAMING: "UPPER_SNAKE_CASE"
```

### Commit Convention

```yaml
COMMIT_STANDARD: "Conventional Commits"
# feat:, fix:, docs:, style:, refactor:, test:, chore:

CHANGELOG_GENERATOR: "{{CHANGELOG_GENERATOR}}"
# Opciones: standard-version, semantic-release, conventional-changelog
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

AUTO_DEPLOY_ENABLED: "{{AUTO_DEPLOY_ENABLED}}"
# Opciones: true, false

REVIEW_REQUIRED: "{{REVIEW_REQUIRED}}"
# Opciones: true, false
```

---

## 🔄 Sincronización y Versionado

```yaml
VERSION_CONTROL: "Git"
REPOSITORY_HOST: "{{REPOSITORY_HOST}}"
# Opciones: GitHub, GitLab, Bitbucket, Azure DevOps

MAIN_BRANCH: "{{MAIN_BRANCH}}"
# Opciones: main, master, production

DEVELOPMENT_BRANCH: "{{DEVELOPMENT_BRANCH}}"
# Opciones: develop, dev, development
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
