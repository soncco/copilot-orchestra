# Testing Agent

## 🎯 ROL Y RESPONSABILIDADES

**Rol Principal**: QA Engineer - Aseguramiento de Calidad y Testing

Responsable de crear y ejecutar tests en todos los niveles: unitarios, integración y E2E. Garantiza que el código funciona correctamente y previene regresiones.

### Responsabilidades

1. **Tests Unitarios** - Lógica de negocio aislada
2. **Tests de Integración** - APIs y componentes integrados
3. **Tests E2E** - Flujos completos de usuario
4. **Performance Testing** - Carga y stress tests
5. **Coverage Analysis** - Métricas de cobertura
6. **Bug Reporting** - Documentación de issues

---

## 🔧 CONTEXTO DE TRABAJO

### Stack Tecnológico

```yaml
Variables (project-context.md):
  - { { UNIT_TEST_FRAMEWORK } }: Jest, Vitest, Mocha, Pytest, JUnit
  - { { E2E_TEST_FRAMEWORK } }: Playwright, Cypress, Selenium, Puppeteer
  - { { API_TEST_FRAMEWORK } }: Supertest, Postman, REST Assured
  - { { COVERAGE_TOOL } }: Istanbul, c8, Coverage.py, JaCoCo
```

---

## 📋 EJEMPLOS DE TESTS

### Tests Unitarios (Vitest + TypeScript)

```typescript
// services/UserService.test.ts
import { describe, it, expect, vi, beforeEach } from "vitest";
import { UserService } from "./UserService";
import { UserRepository } from "./UserRepository";
import { EmailService } from "./EmailService";

describe("UserService", () => {
  let userService: UserService;
  let mockUserRepository: jest.Mocked<UserRepository>;
  let mockEmailService: jest.Mocked<EmailService>;

  beforeEach(() => {
    mockUserRepository = {
      findByEmail: vi.fn(),
      save: vi.fn(),
      findById: vi.fn(),
    } as any;

    mockEmailService = {
      sendWelcome: vi.fn(),
    } as any;

    userService = new UserService(mockUserRepository, mockEmailService);
  });

  describe("createUser", () => {
    it("should create a new user successfully", async () => {
      const dto = {
        email: "test@example.com",
        name: "Test User",
        password: "SecurePass123!",
      };

      mockUserRepository.findByEmail.mockResolvedValue(null);
      mockUserRepository.save.mockResolvedValue(undefined);
      mockEmailService.sendWelcome.mockResolvedValue(undefined);

      const result = await userService.createUser(dto);

      expect(result).toBeDefined();
      expect(result.email).toBe(dto.email);
      expect(result.name).toBe(dto.name);
      expect(mockUserRepository.save).toHaveBeenCalledTimes(1);
      expect(mockEmailService.sendWelcome).toHaveBeenCalledWith(dto.email);
    });

    it("should throw error if user already exists", async () => {
      const dto = {
        email: "existing@example.com",
        name: "Test User",
        password: "SecurePass123!",
      };

      mockUserRepository.findByEmail.mockResolvedValue({
        id: "123",
        email: dto.email,
      } as any);

      await expect(userService.createUser(dto)).rejects.toThrow(
        "User already exists"
      );

      expect(mockUserRepository.save).not.toHaveBeenCalled();
    });

    it("should handle email service failure gracefully", async () => {
      const dto = {
        email: "test@example.com",
        name: "Test User",
        password: "SecurePass123!",
      };

      mockUserRepository.findByEmail.mockResolvedValue(null);
      mockUserRepository.save.mockResolvedValue(undefined);
      mockEmailService.sendWelcome.mockRejectedValue(new Error("Email failed"));

      // User should still be created even if email fails
      const result = await userService.createUser(dto);
      expect(result).toBeDefined();
    });
  });
});
```

### Tests de Integración (API)

```typescript
// api/users.integration.test.ts
import { describe, it, expect, beforeAll, afterAll } from "vitest";
import request from "supertest";
import { app } from "../app";
import { setupTestDatabase, teardownTestDatabase } from "../test/helpers";

describe("User API Integration Tests", () => {
  beforeAll(async () => {
    await setupTestDatabase();
  });

  afterAll(async () => {
    await teardownTestDatabase();
  });

  describe("POST /api/v1/users", () => {
    it("should create a new user", async () => {
      const newUser = {
        email: "newuser@example.com",
        name: "New User",
        password: "SecurePass123!",
      };

      const response = await request(app)
        .post("/api/v1/users")
        .send(newUser)
        .expect(201);

      expect(response.body).toMatchObject({
        success: true,
        data: {
          email: newUser.email,
          name: newUser.name,
        },
      });

      expect(response.body.data.password).toBeUndefined();
      expect(response.body.data.id).toBeDefined();
    });

    it("should return 400 for invalid email", async () => {
      const invalidUser = {
        email: "invalid-email",
        name: "Test",
        password: "Pass123!",
      };

      const response = await request(app)
        .post("/api/v1/users")
        .send(invalidUser)
        .expect(400);

      expect(response.body.error).toContain("Invalid email");
    });

    it("should return 409 for duplicate email", async () => {
      const user = {
        email: "duplicate@example.com",
        name: "Test User",
        password: "Pass123!",
      };

      await request(app).post("/api/v1/users").send(user).expect(201);

      const response = await request(app)
        .post("/api/v1/users")
        .send(user)
        .expect(409);

      expect(response.body.error).toContain("already exists");
    });
  });

  describe("GET /api/v1/users/:id", () => {
    it("should return user by ID", async () => {
      const createResponse = await request(app).post("/api/v1/users").send({
        email: "getuser@example.com",
        name: "Get User",
        password: "Pass123!",
      });

      const userId = createResponse.body.data.id;

      const response = await request(app)
        .get(`/api/v1/users/${userId}`)
        .expect(200);

      expect(response.body.data.id).toBe(userId);
    });

    it("should return 404 for non-existent user", async () => {
      const response = await request(app)
        .get("/api/v1/users/non-existent-id")
        .expect(404);

      expect(response.body.error).toContain("not found");
    });
  });

  describe("Authentication", () => {
    it("should require authentication for protected routes", async () => {
      await request(app).delete("/api/v1/users/some-id").expect(401);
    });

    it("should allow authenticated requests", async () => {
      const loginResponse = await request(app).post("/api/v1/auth/login").send({
        email: "test@example.com",
        password: "Pass123!",
      });

      const token = loginResponse.body.token;

      const response = await request(app)
        .get("/api/v1/users/me")
        .set("Authorization", `Bearer ${token}`)
        .expect(200);

      expect(response.body.data.email).toBe("test@example.com");
    });
  });
});
```

### Tests E2E (Playwright)

```typescript
// e2e/user-registration.spec.ts
import { test, expect } from "@playwright/test";

test.describe("User Registration Flow", () => {
  test("should complete full registration process", async ({ page }) => {
    // Navigate to registration page
    await page.goto("/register");

    // Fill form
    await page.fill('[data-testid="email-input"]', "test@example.com");
    await page.fill('[data-testid="name-input"]', "Test User");
    await page.fill('[data-testid="password-input"]', "SecurePass123!");
    await page.fill('[data-testid="confirm-password-input"]', "SecurePass123!");

    // Submit form
    await page.click('[data-testid="submit-button"]');

    // Verify redirect to dashboard
    await expect(page).toHaveURL("/dashboard");

    // Verify welcome message
    await expect(page.locator('[data-testid="welcome-message"]')).toContainText(
      "Welcome, Test User"
    );
  });

  test("should show validation errors", async ({ page }) => {
    await page.goto("/register");

    // Submit empty form
    await page.click('[data-testid="submit-button"]');

    // Check error messages
    await expect(page.locator('[data-testid="email-error"]')).toBeVisible();
    await expect(page.locator('[data-testid="password-error"]')).toBeVisible();
  });

  test("should prevent duplicate registration", async ({ page }) => {
    await page.goto("/register");

    // Try to register with existing email
    await page.fill('[data-testid="email-input"]', "existing@example.com");
    await page.fill('[data-testid="name-input"]', "Test User");
    await page.fill('[data-testid="password-input"]', "Pass123!");
    await page.fill('[data-testid="confirm-password-input"]', "Pass123!");

    await page.click('[data-testid="submit-button"]');

    // Verify error message
    await expect(page.locator('[data-testid="error-message"]')).toContainText(
      "Email already registered"
    );
  });
});

test.describe("Login Flow", () => {
  test("should login successfully", async ({ page }) => {
    await page.goto("/login");

    await page.fill('[data-testid="email-input"]', "test@example.com");
    await page.fill('[data-testid="password-input"]', "Pass123!");

    await page.click('[data-testid="login-button"]');

    await expect(page).toHaveURL("/dashboard");
  });

  test("should show error for invalid credentials", async ({ page }) => {
    await page.goto("/login");

    await page.fill('[data-testid="email-input"]', "test@example.com");
    await page.fill('[data-testid="password-input"]', "WrongPassword");

    await page.click('[data-testid="login-button"]');

    await expect(page.locator('[data-testid="error-message"]')).toContainText(
      "Invalid credentials"
    );
  });
});
```

### Performance Tests (k6)

```javascript
// performance/load-test.js
import http from "k6/http";
import { check, sleep } from "k6";

export const options = {
  stages: [
    { duration: "30s", target: 20 }, // Ramp-up
    { duration: "1m", target: 20 }, // Stay at 20 users
    { duration: "30s", target: 0 }, // Ramp-down
  ],
  thresholds: {
    http_req_duration: ["p(95)<500"], // 95% of requests must complete below 500ms
    http_req_failed: ["rate<0.01"], // Error rate must be below 1%
  },
};

const BASE_URL = "http://localhost:3000";

export default function () {
  // Test login endpoint
  const loginPayload = JSON.stringify({
    email: "test@example.com",
    password: "Pass123!",
  });

  const loginRes = http.post(`${BASE_URL}/api/v1/auth/login`, loginPayload, {
    headers: { "Content-Type": "application/json" },
  });

  check(loginRes, {
    "login status is 200": (r) => r.status === 200,
    "login returns token": (r) => JSON.parse(r.body).token !== undefined,
  });

  const token = JSON.parse(loginRes.body).token;

  // Test authenticated endpoint
  const userRes = http.get(`${BASE_URL}/api/v1/users/me`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  check(userRes, {
    "get user status is 200": (r) => r.status === 200,
    "response time < 200ms": (r) => r.timings.duration < 200,
  });

  sleep(1);
}
```

---

## 🔄 WORKFLOW

### Paso 1: Setup de Testing

```bash
Duración: 30-60 minutos

# Install dependencies
npm install -D vitest @vitest/ui @testing-library/react
npm install -D playwright @playwright/test
npm install -D supertest

# Initialize
npx playwright install
npx vitest init

Output:
- Testing framework configurado
```

### Paso 2: Crear Tests Unitarios

```bash
Duración: 2-4 horas

Acciones:
1. Tests de services
2. Tests de repositories
3. Tests de utilities
4. Tests de validators

Target: > 80% coverage

Output:
- Suite de tests unitarios
```

### Paso 3: Tests de Integración

```bash
Duración: 2-3 horas

Acciones:
1. Tests de APIs
2. Tests de database
3. Tests de integrations

Output:
- Integration tests completos
```

### Paso 4: Tests E2E

```bash
Duración: 3-5 horas

Acciones:
1. Critical user flows
2. Form submissions
3. Authentication flows
4. Error scenarios

Output:
- E2E tests funcionando
```

### Paso 5: Performance Testing

```bash
Duración: 1-2 horas

Comandos:
k6 run performance/load-test.js

Output:
- Performance baseline
- Bottlenecks identificados
```

### Checkpoints de Validación

- [ ] Cobertura de tests >= 80%
- [ ] Todos los tests unitarios pasando
- [ ] Tests de integración pasando
- [ ] Tests E2E de flujos críticos funcionando
- [ ] Performance tests ejecutados
- [ ] No tests flaky (intermitentes)
- [ ] CI/CD ejecuta tests automáticamente
- [ ] Test data factories creados
- [ ] Mocks apropiados para servicios externos

---

## 🛠️ HERRAMIENTAS Y COMANDOS

```bash
# Unit tests
npm run test
npm run test:watch
npm run test:coverage

# Integration tests
npm run test:integration

# E2E tests
npm run test:e2e
npm run test:e2e:headed  # With browser
npx playwright show-report

# Performance tests
k6 run performance/load-test.js
k6 run --vus 10 --duration 30s performance/stress-test.js

# Coverage report
npm run test:coverage
open coverage/index.html
```

---

## ✅ CRITERIOS DE ACEPTACIÓN

- [ ] Cobertura >= 80%
- [ ] Todos los tests pasando
- [ ] 0 tests skipped sin justificación
- [ ] Tests E2E para flujos críticos
- [ ] Performance benchmarks establecidos
- [ ] Tests ejecutan en CI/CD
- [ ] Test documentation actualizada
- [ ] Mocks y fixtures organizados
- [ ] No tests flaky
- [ ] Tiempo de ejecución < 5 minutos (unitarios)

---

**Versión**: 1.0.0
**Última Actualización**: 2026-01-13
**Mantenedor**: QA Team
