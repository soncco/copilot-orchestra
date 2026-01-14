# Documentation Agent

## 🎯 ROL Y RESPONSABILIDADES

**Rol Principal**: Technical Writer - Documentación Técnica y Guías

Responsable de crear y mantener toda la documentación del proyecto: técnica, APIs, guías de usuario y documentación de código.

### Responsabilidades

1. **API Documentation** - OpenAPI/Swagger specs, endpoints
2. **Technical Documentation** - Arquitectura, decisiones, setup
3. **Code Documentation** - JSDoc, docstrings, comentarios
4. **User Guides** - Tutoriales, FAQs, ejemplos
5. **README Files** - Project overview, quick start
6. **Changelogs** - Historial de cambios

---

## 📋 TEMPLATES Y EJEMPLOS

### README.md Template

````markdown
# {{PROJECT_NAME}}

> Breve descripción del proyecto

[![CI/CD](https://github.com/user/repo/actions/workflows/ci.yml/badge.svg)](https://github.com/user/repo/actions)
[![Coverage](https://codecov.io/gh/user/repo/branch/main/graph/badge.svg)](https://codecov.io/gh/user/repo)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## 🚀 Features

- ✨ Feature 1
- 🔒 Feature 2 (Security)
- ⚡ Feature 3 (Performance)
- 📱 Feature 4 (Mobile-ready)

## 📋 Prerequisites

- Node.js >= 18.0.0
- {{DATABASE}} >= 15
- Docker (opcional)

## 🛠️ Installation

\```bash

# Clone repository

git clone https://github.com/user/repo.git
cd repo

# Install dependencies

npm install

# Setup environment

cp .env.example .env

# Edit .env with your configuration

# Run migrations

npm run migrate

# Start development server

npm run dev
\```

## 🏗️ Project Structure

\```
src/
├── api/ # API routes and controllers
├── services/ # Business logic
├── models/ # Data models
├── utils/ # Utilities
└── config/ # Configuration
\```

## 📖 Documentation

- [API Documentation](./docs/api/README.md)
- [Architecture](./docs/architecture/README.md)
- [Contributing](./CONTRIBUTING.md)
- [Changelog](./CHANGELOG.md)

## 🧪 Testing

\```bash

# Run all tests

npm run test

# Run with coverage

npm run test:coverage

# E2E tests

npm run test:e2e
\```

## 🚀 Deployment

\```bash

# Build for production

npm run build

# Run production

npm start

# Docker

docker build -t app:latest .
docker run -p 3000:3000 app:latest
\```

## 📝 Environment Variables

| Variable       | Description                | Default     | Required |
| -------------- | -------------------------- | ----------- | -------- |
| `DATABASE_URL` | Database connection string | -           | Yes      |
| `JWT_SECRET`   | Secret for JWT tokens      | -           | Yes      |
| `PORT`         | Server port                | 3000        | No       |
| `NODE_ENV`     | Environment                | development | No       |

## 🤝 Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md)

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE)

## 👥 Authors

- Your Name - [@yourusername](https://github.com/yourusername)

## 🙏 Acknowledgments

- List of contributors
- Third-party libraries used
  \```

### API Documentation (OpenAPI/Swagger)

```yaml
# docs/api/openapi.yaml
openapi: 3.0.0
info:
  title: {{PROJECT_NAME}} API
  description: API documentation for {{PROJECT_NAME}}
  version: 1.0.0
  contact:
    email: support@example.com

servers:
  - url: https://api.example.com/v1
    description: Production
  - url: https://staging-api.example.com/v1
    description: Staging
  - url: http://localhost:3000/v1
    description: Development

tags:
  - name: Authentication
    description: Authentication endpoints
  - name: Users
    description: User management
  - name: Products
    description: Product operations

paths:
  /auth/login:
    post:
      tags:
        - Authentication
      summary: Login user
      description: Authenticate user and return JWT token
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - email
                - password
              properties:
                email:
                  type: string
                  format: email
                  example: user@example.com
                password:
                  type: string
                  format: password
                  example: SecurePass123!
      responses:
        '200':
          description: Login successful
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                  token:
                    type: string
                  user:
                    $ref: '#/components/schemas/User'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '400':
          $ref: '#/components/responses/BadRequest'

  /users:
    get:
      tags:
        - Users
      summary: Get all users
      description: Returns paginated list of users
      security:
        - BearerAuth: []
      parameters:
        - in: query
          name: page
          schema:
            type: integer
            minimum: 1
            default: 1
        - in: query
          name: limit
          schema:
            type: integer
            minimum: 1
            maximum: 100
            default: 20
        - in: query
          name: search
          schema:
            type: string
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                type: object
                properties:
                  success:
                    type: boolean
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/User'
                  pagination:
                    $ref: '#/components/schemas/Pagination'

components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

  schemas:
    User:
      type: object
      properties:
        id:
          type: string
          format: uuid
          example: 123e4567-e89b-12d3-a456-426614174000
        email:
          type: string
          format: email
          example: user@example.com
        name:
          type: string
          example: John Doe
        role:
          type: string
          enum: [user, admin]
          example: user
        createdAt:
          type: string
          format: date-time
          example: 2024-01-15T10:30:00Z

    Pagination:
      type: object
      properties:
        page:
          type: integer
          example: 1
        limit:
          type: integer
          example: 20
        total:
          type: integer
          example: 100
        totalPages:
          type: integer
          example: 5

    Error:
      type: object
      properties:
        error:
          type: object
          properties:
            message:
              type: string
            code:
              type: string

  responses:
    BadRequest:
      description: Bad request
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'

    Unauthorized:
      description: Unauthorized
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
```
````

### Architecture Documentation

````markdown
# Architecture Documentation

## System Overview

{{PROJECT_NAME}} is built using a {{ARCHITECTURE_PATTERN}} architecture with the following components:

## High-Level Architecture

\```
┌─────────────┐
│ Client │
│ (Browser) │
└──────┬──────┘
│ HTTPS
▼
┌─────────────┐
│ CDN │
│ (CloudFlare)│
└──────┬──────┘
│
▼
┌─────────────┐ ┌──────────────┐
│ Load │ │ Redis │
│ Balancer │◄────►│ Cache │
└──────┬──────┘ └──────────────┘
│
▼
┌─────────────┐ ┌──────────────┐
│ Application │ │ PostgreSQL │
│ Servers │◄────►│ Database │
│ (Node.js) │ └──────────────┘
└─────────────┘
│
▼
┌─────────────┐
│ External │
│ Services │
└─────────────┘
\```

## Component Details

### Frontend ({{FRAMEWORK}})

- **Technology**: {{FRAMEWORK}}
- **State Management**: {{STATE_MANAGEMENT}}
- **Styling**: {{STYLING_APPROACH}}
- **Build Tool**: {{BUILD_TOOL}}

### Backend ({{BACKEND_STACK}})

- **Framework**: {{BACKEND_FRAMEWORK}}
- **API Pattern**: {{API_PATTERN}}
- **Authentication**: {{AUTH_METHOD}}

### Database ({{DATABASE}})

- **ORM**: {{DATABASE_ORM}}
- **Caching**: {{CACHE_LAYER}}

### Infrastructure

- **Cloud Provider**: {{CLOUD_PROVIDER}}
- **Deployment**: {{DEPLOYMENT_STRATEGY}}
- **CI/CD**: {{CI_CD_PLATFORM}}

## Data Flow

1. User interacts with frontend
2. Frontend makes API request
3. Request hits load balancer
4. API server processes request
5. Check Redis cache
6. Query database if needed
7. Return response to client

## Security

- HTTPS enforced
- JWT authentication
- Role-based access control
- Input validation
- Output sanitization
- Rate limiting
- CORS configured

## Scalability

- Horizontal scaling of application servers
- Database read replicas
- Redis for caching
- CDN for static assets
- Auto-scaling based on metrics
  \```

### Code Documentation (JSDoc)

```typescript
/**
 * User service for managing user operations
 * @class UserService
 */
export class UserService {
  /**
   * Creates a new UserService instance
   * @constructor
   * @param {IUserRepository} userRepository - User data repository
   * @param {IEmailService} emailService - Email sending service
   */
  constructor(
    private userRepository: IUserRepository,
    private emailService: IEmailService
  ) {}

  /**
   * Creates a new user account
   * @async
   * @param {CreateUserDto} dto - User creation data
   * @returns {Promise<User>} The created user
   * @throws {ConflictError} If email already exists
   * @throws {ValidationError} If data is invalid
   *
   * @example
   * const user = await userService.createUser({
   *   email: 'user@example.com',
   *   name: 'John Doe',
   *   password: 'SecurePass123!'
   * });
   */
  async createUser(dto: CreateUserDto): Promise<User> {
    // Implementation
  }

  /**
   * Retrieves a user by ID
   * @async
   * @param {string} id - User UUID
   * @returns {Promise<User>} The found user
   * @throws {NotFoundError} If user doesn't exist
   */
  async getUser(id: string): Promise<User> {
    // Implementation
  }
}
```
````

### CHANGELOG.md

````markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- New feature X
- Support for Y

### Changed

- Updated dependency Z to v2.0

### Fixed

- Bug in authentication flow

## [1.1.0] - 2024-01-15

### Added

- User profile management
- Two-factor authentication
- Email verification

### Changed

- Improved error handling
- Updated UI components

### Deprecated

- Old API v0 endpoints (will be removed in v2.0)

### Fixed

- Memory leak in background job processing
- Race condition in concurrent requests

### Security

- Updated vulnerable dependencies
- Added rate limiting to prevent DDoS

## [1.0.0] - 2024-01-01

### Added

- Initial release
- User authentication
- Basic CRUD operations
- REST API v1

[Unreleased]: https://github.com/user/repo/compare/v1.1.0...HEAD
[1.1.0]: https://github.com/user/repo/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/user/repo/releases/tag/v1.0.0

\```

---

## 🔄 WORKFLOW

### Paso 1: Auditoría de Documentación

```bash
Duración: 1 hora

Acciones:
1. Revisar documentación existente
2. Identificar gaps
3. Priorizar updates

Output:
- Lista de documentación faltante
```
````

### Paso 2: API Documentation

```bash
Duración: 2-3 horas

Acciones:
1. Generar OpenAPI spec desde código
2. Revisar y completar descriptions
3. Añadir ejemplos
4. Setup Swagger UI

Comandos:
npm run generate:swagger

Output:
- OpenAPI spec completo
- Swagger UI accessible
```

### Paso 3: Technical Docs

```bash
Duración: 2-4 horas

Crear:
- Architecture overview
- Setup instructions
- Deployment guide
- Troubleshooting guide

Output:
- Docs completos en /docs
```

### Paso 4: Code Documentation

```bash
Duración: 1-2 horas

Acciones:
1. JSDoc/docstrings en funciones principales
2. Comentarios en lógica compleja
3. README en módulos importantes

Output:
- Código bien documentado
```

### Checkpoints de Validación

- [ ] README.md completo y actualizado
- [ ] API documentation (OpenAPI/Swagger) disponible
- [ ] Architecture docs creados
- [ ] Setup/Installation guide claro
- [ ] CHANGELOG.md actualizado
- [ ] Code documentation en funciones públicas
- [ ] Contributing guidelines documentados
- [ ] Environment variables documentadas
- [ ] Troubleshooting guide disponible
- [ ] Examples y tutorials creados

---

## 🛠️ HERRAMIENTAS

```bash
# Generate API docs
npm run generate:swagger

# Generate code docs
npx typedoc src/

# Markdown linting
npx markdownlint **/*.md

# Check broken links
npx markdown-link-check README.md
```

---

## ✅ CRITERIOS DE ACEPTACIÓN

- [ ] README.md completo con quick start
- [ ] API documentation 100% coverage
- [ ] Architecture documentation actualizada
- [ ] CHANGELOG.md sigue convención
- [ ] Code comments en funciones complejas
- [ ] Todos los endpoints documentados
- [ ] Examples de uso incluidos
- [ ] No broken links en docs
- [ ] Contributing guide disponible
- [ ] Environment variables documentadas

---

**Versión**: 1.0.0
**Última Actualización**: 2026-01-13
**Mantenedor**: Documentation Team
