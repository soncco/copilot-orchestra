# Contributing Guide - Multi-Agent Orchestration System

Bienvenido al sistema de orquestación multi-agente para desarrollo SaaS. Esta guía explica cómo usar los agentes de forma efectiva y contribuir al proyecto.

## 📋 Tabla de Contenidos

- [Introducción al Sistema de Agentes](#introducción-al-sistema-de-agentes)
- [Agentes Disponibles](#agentes-disponibles)
- [Workflows Predefinidos](#workflows-predefinidos)
- [Cómo Usar los Agentes](#cómo-usar-los-agentes)
- [Handoff Protocol](#handoff-protocol)
- [Estándares de Código](#estándares-de-código)
- [Testing](#testing)
- [Proceso de Review](#proceso-de-review)
- [FAQ](#faq)

---

## 🤖 Introducción al Sistema de Agentes

Este proyecto utiliza un sistema de orquestación donde múltiples agentes especializados trabajan en conjunto para desarrollar, testear, y desplegar features.

### Principios Fundamentales

1. **Separación de Responsabilidades**: Cada agente tiene un dominio específico
2. **Modularidad**: Los agentes son intercambiables y reutilizables
3. **Documentación Continua**: Todo cambio debe estar documentado
4. **Framework Agnostic**: Soporta múltiples tecnologías vía configuración

### Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────┐
│                   GitHub Copilot                         │
│              (Orchestration Layer)                       │
└────────────┬────────────────────────────────────────────┘
             │
             │ Reads Configuration
             ├──────────────────┬──────────────────┬───────
             │                  │                  │
             ▼                  ▼                  ▼
    ┌────────────────┐  ┌─────────────┐  ┌──────────────┐
    │ copilot-       │  │ agents-     │  │ project-     │
    │ instructions   │  │ config.json │  │ context.md   │
    └────────────────┘  └─────────────┘  └──────────────┘
             │                  │                  │
             │ Defines          │ Orchestrates     │ Provides
             │ Global Rules     │ Workflows        │ Variables
             │                  │                  │
             ▼                  ▼                  ▼
    ┌────────────────────────────────────────────────────┐
    │              .github/agents/*.md                    │
    │   (Individual Agent Definitions)                    │
    │                                                      │
    │  • architect-agent.md                               │
    │  • backend-agent.md                                 │
    │  • frontend-agent.md                                │
    │  • devops-agent.md                                  │
    │  • security-agent.md                                │
    │  • testing-agent.md                                 │
    │  • documentation-agent.md                           │
    │  • code-review-agent.md                             │
    │  • database-agent.md                                │
    │  • integration-agent.md                             │
    └────────────────────────────────────────────────────┘
```

---

## 👥 Agentes Disponibles

### Core Agents

#### 1. **Architect Agent**

- **Responsabilidad**: Diseño de arquitectura, decisiones técnicas, ADRs
- **Cuándo usar**: Nueva feature, refactoring mayor, cambios arquitectónicos
- **Output**: Diagramas C4, ADRs, especificaciones técnicas

#### 2. **Backend Agent**

- **Responsabilidad**: Lógica de negocio, APIs, servicios
- **Cuándo usar**: Implementar endpoints, lógica de negocio, integraciones
- **Output**: Código backend, tests unitarios

#### 3. **Frontend Agent**

- **Responsabilidad**: UI/UX, componentes, estado
- **Cuándo usar**: Interfaces de usuario, componentes React, state management
- **Output**: Componentes, hooks, páginas

#### 4. **DevOps Agent**

- **Responsabilidad**: CI/CD, deployments, infraestructura
- **Cuándo usar**: Configurar pipelines, Dockerfiles, K8s manifests
- **Output**: Workflows CI/CD, configuración cloud

#### 5. **Security Agent**

- **Responsabilidad**: Auditoría de seguridad, vulnerabilidades
- **Cuándo usar**: Revisar seguridad, implementar autenticación, auditorías
- **Output**: Reportes de seguridad, fixes

#### 6. **Testing Agent**

- **Responsabilidad**: Tests unitarios, integración, E2E
- **Cuándo usar**: Crear tests, verificar coverage, testing de regresión
- **Output**: Suite de tests, reportes de coverage

#### 7. **Documentation Agent**

- **Responsabilidad**: Documentación técnica, READMEs, API docs
- **Cuándo usar**: Documentar APIs, actualizar guías, crear ejemplos
- **Output**: Markdown docs, OpenAPI specs

#### 8. **Code Review Agent**

- **Responsabilidad**: Revisión de código, calidad, estándares
- **Cuándo usar**: Review de PRs, validación de estándares
- **Output**: Feedback de code review

### Auxiliary Agents

#### 9. **Database Agent**

- **Responsabilidad**: Schema, migraciones, optimización de queries
- **Cuándo usar**: Cambios en DB, migraciones, optimización
- **Output**: Schemas, migrations, índices

#### 10. **Integration Agent**

- **Responsabilidad**: APIs externas, webhooks, OAuth
- **Cuándo usar**: Integrar servicios third-party
- **Output**: Clients de APIs, webhook handlers

---

## 🔄 Workflows Predefinidos

### 1. Feature Development Workflow

```
Start
  │
  ▼
┌──────────────────┐
│ Architect Agent  │ ← Diseña la arquitectura
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Database Agent   │ ← Schema changes (si aplica)
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Backend Agent    │ ← Implementa API/lógica
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Frontend Agent   │ ← Implementa UI
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Testing Agent    │ ← Crea tests
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Security Agent   │ ← Audita seguridad
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Code Review      │ ← Revisa calidad
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Documentation    │ ← Actualiza docs
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ DevOps Agent     │ ← Deployment
└────────┬─────────┘
         │
         ▼
       Done
```

**Ejemplo de uso:**

```bash
# En tu PR description o commit message:
@architect-agent Please design the authentication flow for social login
```

El Architect Agent creará un ADR y especificación técnica, luego automáticamente pasará al siguiente agente.

### 2. Bug Fix Workflow

```
Start → Testing Agent (reproduce) → [Backend/Frontend] (fix) →
Testing Agent (verify) → Code Review → DevOps (deploy si crítico)
```

### 3. Refactor Workflow

```
Start → Architect Agent (propone) → Code Review Agent (identifica) →
[Agente responsable] (implementa) → Testing Agent (verifica regresiones) →
Documentation Agent (actualiza)
```

### 4. Deployment Workflow

```
Start → Code Review (final check) → Security Agent (audit) →
Testing Agent (E2E) → DevOps Agent (deploy)
```

---

## 🎯 Cómo Usar los Agentes

### Método 1: Mediante GitHub Copilot Chat

```
User: @architect-agent Design the payment processing module

Copilot: [Reads architect-agent.md and creates architecture]
```

### Método 2: En Pull Requests

Agrega en el PR description:

```markdown
## Agent Workflow

- [ ] @architect-agent - Design review
- [ ] @backend-agent - API implementation
- [ ] @frontend-agent - UI components
- [ ] @testing-agent - Test coverage
- [ ] @security-agent - Security audit
- [ ] @code-review-agent - Final review
```

### Método 3: Comandos en Commits

```bash
git commit -m "feat: add user authentication

@architect-agent: Reviewed OAuth flow
@security-agent: Validated JWT implementation
@testing-agent: Added unit and integration tests
"
```

---

## 🤝 Handoff Protocol

Cuando un agente completa su trabajo, debe usar este formato para pasar al siguiente:

```markdown
## Handoff a [AGENTE_DESTINO]

**Completado por**: Architect Agent
**Fecha**: 2026-01-13
**Branch**: feature/user-authentication

### Archivos Modificados

- `docs/architecture/ADR-001-authentication.md` (nuevo)
- `docs/architecture/diagrams/auth-flow.md` (nuevo)

### Decisiones Técnicas

- Usar OAuth 2.0 con PKCE flow
- JWT para session management
- Refresh token rotation

### Dependencias Nuevas

- `jsonwebtoken` (^9.0.0)
- `bcrypt` (^5.1.0)

### Configuraciones Cambiadas

- Agregado `JWT_SECRET` a `.env.example`
- Agregado `JWT_EXPIRES_IN` configuración

### Próximos Pasos para Backend Agent

1. Implementar `AuthService` class
2. Crear endpoints: `/auth/login`, `/auth/refresh`, `/auth/logout`
3. Implementar JWT middleware
4. Agregar rate limiting a auth endpoints

### Notas Especiales

- Asegurar que refresh tokens se guarden en httpOnly cookies
- Implementar token blacklist para logout
- Considerar Redis para session storage en producción

### Validación Requerida

- [ ] JWT secret length mínimo 32 caracteres
- [ ] Refresh tokens expire en 7 días
- [ ] Access tokens expire en 15 minutos
- [ ] Rate limit: 5 intentos de login por minuto

---

@backend-agent Ready for implementation
```

---

## 💻 Estándares de Código

### Convenciones de Nombres

```typescript
// ✅ CORRECTO
class UserService {}
const getUserById = () => {};
const MAX_RETRIES = 3;

// ❌ INCORRECTO
class userservice {}
const get_user_by_id = () => {};
const maxRetries = 3; // Debería ser UPPER_SNAKE_CASE para constantes
```

### Estructura de Archivos

```
src/
├── features/              # Feature-based organization
│   ├── auth/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── services/
│   │   └── types/
│   ├── users/
│   └── payments/
├── shared/               # Código compartido
│   ├── components/
│   ├── utils/
│   ├── hooks/
│   └── types/
└── infrastructure/       # Config, setup
    ├── api/
    ├── database/
    └── config/
```

### Error Handling

```typescript
// ✅ CORRECTO
try {
  const user = await userService.getById(id);
  logger.info("User fetched successfully", { userId: id });
  return user;
} catch (error) {
  logger.error("Failed to fetch user", {
    userId: id,
    error: error.message,
  });

  throw new AppError("User not found", 404);
}

// ❌ INCORRECTO
try {
  const user = await userService.getById(id);
  return user;
} catch (error) {
  console.log(error); // No usar console.log
  throw error; // No exponer detalles internos
}
```

---

## 🧪 Testing

### Coverage Requirements

- **Mínimo**: 80% coverage
- **Critical paths**: 100% coverage
- **Unit tests**: Toda lógica de negocio
- **Integration tests**: Todos los endpoints
- **E2E tests**: Flujos críticos de usuario

### Test Structure

```typescript
// user.service.test.ts
describe("UserService", () => {
  describe("createUser", () => {
    it("should create user with valid data", async () => {
      // Arrange
      const userData = { email: "test@example.com", name: "Test" };

      // Act
      const user = await userService.createUser(userData);

      // Assert
      expect(user).toHaveProperty("id");
      expect(user.email).toBe(userData.email);
    });

    it("should throw error with duplicate email", async () => {
      // Arrange
      const userData = { email: "existing@example.com", name: "Test" };

      // Act & Assert
      await expect(userService.createUser(userData)).rejects.toThrow(
        "Email already exists"
      );
    });
  });
});
```

### Ejecutar Tests

```bash
# Unit tests
npm run test

# Watch mode
npm run test:watch

# Coverage
npm run test:coverage

# E2E tests
npm run test:e2e

# Specific file
npm test -- user.service.test.ts
```

---

## 👀 Proceso de Review

### Checklist de Code Review

```markdown
## Code Review Checklist

### Funcionalidad

- [ ] El código hace lo que debe hacer
- [ ] No hay bugs evidentes
- [ ] Edge cases considerados

### Código

- [ ] Sigue convenciones de naming
- [ ] No hay código duplicado (DRY)
- [ ] Funciones < 50 líneas
- [ ] Complejidad ciclomática aceptable

### Tests

- [ ] Tests nuevos para nueva funcionalidad
- [ ] Tests pasan exitosamente
- [ ] Coverage >= 80%

### Seguridad

- [ ] Input validation implementado
- [ ] No hay SQL injection vulnerabilities
- [ ] Secrets no hardcodeados
- [ ] Authentication/authorization correcto

### Performance

- [ ] No N+1 queries
- [ ] Índices apropiados en DB
- [ ] No memory leaks evidentes

### Documentación

- [ ] Código autoexplicativo o comentado
- [ ] README actualizado si aplica
- [ ] API docs actualizados
```

---

## ❓ FAQ

### ¿Cómo empiezo a trabajar en una nueva feature?

1. Crea un branch: `git checkout -b feature/my-feature`
2. Consulta al **Architect Agent** para diseñar la solución
3. Sigue el workflow predefinido
4. Haz handoffs apropiados entre agentes
5. Asegura que todos los checkpoints pasen

### ¿Qué hago si dos agentes tienen opiniones conflictivas?

El **Architect Agent** tiene la última palabra en decisiones arquitectónicas. Si hay conflicto:

1. Consulta primero al Architect Agent
2. Documenta la decisión en un ADR
3. Comunica la decisión a los otros agentes

### ¿Cómo actualizo las variables del proyecto?

Edita `project-context.md`:

```markdown
**Framework Frontend**: {{FRAMEWORK}} → React 18
**Backend Stack**: {{BACKEND_STACK}} → Node.js + Express
```

Todos los agentes leerán estas variables.

### ¿Puedo saltarme pasos del workflow?

No se recomienda, pero para features pequeñas puedes usar un workflow simplificado:

```
Architect (quick review) → Implementation → Testing → Deploy
```

### ¿Cómo reporto un bug?

1. Usa el **Testing Agent** para reproducir el bug
2. Documenta steps to reproduce
3. El agente responsable (Backend/Frontend) lo corrige
4. Testing Agent verifica el fix

---

## 📚 Recursos Adicionales

- **Arquitectura**: `docs/architecture/`
- **API Docs**: `docs/api/`
- **Ejemplos**: `examples/`
- **ADRs**: `docs/architecture/decisions/`

---

## 🤝 Contribuciones

Para contribuir a este sistema de agentes:

1. Fork el proyecto
2. Crea un branch para tu feature
3. Sigue el workflow de agentes
4. Asegura tests y documentation
5. Crea un Pull Request

---

**Última actualización**: 2026-01-13
**Versión**: 1.0.0
**Mantenedores**: Dev Team
