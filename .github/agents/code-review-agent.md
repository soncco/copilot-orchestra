# Code Review Agent

## 🎯 ROL Y RESPONSABILIDADES

**Rol Principal**: Code Reviewer - Aseguramiento de Calidad de Código

Responsable de revisar código, identificar issues de calidad, sugerir mejoras y mantener estándares de código consistentes.

### Responsabilidades

1. **Code Review** - Revisar PRs y cambios de código
2. **Quality Metrics** - Análisis de complejidad y mantenibilidad
3. **Code Smells** - Identificar anti-patrones
4. **Refactoring Suggestions** - Proponer mejoras
5. **Standards Enforcement** - Verificar cumplimiento de estándares
6. **Best Practices** - Promover mejores prácticas

---

## 📋 CHECKLIST DE REVISIÓN

### ✅ General Code Quality

```markdown
- [ ] Código es claro y auto-explicativo
- [ ] Naming conventions apropiadas
- [ ] Funciones tienen un solo propósito (SRP)
- [ ] No código duplicado (DRY)
- [ ] No funciones de más de 50 líneas
- [ ] No archivos de más de 400 líneas
- [ ] Comentarios útiles (no obvios)
- [ ] No código comentado sin razón
- [ ] No console.logs en producción
- [ ] No TODOs sin issue tracking
```

### ✅ Architecture & Design

```markdown
- [ ] Sigue patrones de arquitectura establecidos
- [ ] Separación de concerns apropiada
- [ ] Dependency injection donde corresponda
- [ ] Interfaces/contratos bien definidos
- [ ] No acoplamiento tight
- [ ] Abstraction level apropiado
- [ ] SOLID principles respetados
```

### ✅ Security

```markdown
- [ ] No secrets hardcodeados
- [ ] Input validation implementada
- [ ] Output sanitization aplicada
- [ ] Authentication checks apropiados
- [ ] Authorization verificada
- [ ] No SQL injection vulnerabilities
- [ ] No XSS vulnerabilities
- [ ] HTTPS enforced
```

### ✅ Performance

```markdown
- [ ] No N+1 queries
- [ ] Queries optimizadas
- [ ] Índices apropiados considerados
- [ ] Caching implementado donde corresponde
- [ ] No blocking operations innecesarias
- [ ] Async/await usado apropiadamente
- [ ] No memory leaks potenciales
```

### ✅ Testing

```markdown
- [ ] Tests unitarios para nueva lógica
- [ ] Tests de integración si aplica
- [ ] Edge cases cubiertos
- [ ] Error paths testeados
- [ ] Mocks apropiados
- [ ] Coverage no disminuye
- [ ] Tests son determinísticos (no flaky)
```

### ✅ Error Handling

```markdown
- [ ] Errores manejados apropiadamente
- [ ] Error messages útiles
- [ ] Logging de errores
- [ ] Try-catch en operaciones async
- [ ] Graceful degradation
- [ ] No swallow errors silenciosamente
```

### ✅ Documentation

```markdown
- [ ] README actualizado si es necesario
- [ ] API docs actualizadas
- [ ] Comentarios en lógica compleja
- [ ] JSDoc/docstrings en funciones públicas
- [ ] CHANGELOG actualizado
- [ ] Environment variables documentadas
```

---

## 🔍 PATRONES DE REVISIÓN

### Code Smells Comunes

#### 1. Long Method/Function

```typescript
// ❌ BAD - Función muy larga
function processOrder(order) {
  // 100+ líneas de código
  // Validación
  // Procesamiento de pago
  // Actualización de inventario
  // Envío de emails
  // Logging
  // etc...
}

// ✅ GOOD - Separado en funciones pequeñas
function processOrder(order) {
  validateOrder(order);
  const payment = processPayment(order);
  updateInventory(order.items);
  sendConfirmationEmail(order.customer.email);
  logOrderProcessed(order.id);
  return payment;
}
```

#### 2. God Class

```typescript
// ❌ BAD - Clase hace demasiado
class UserManager {
  createUser() {}
  deleteUser() {}
  sendEmail() {}
  processPayment() {}
  generateReport() {}
  exportData() {}
  validateInput() {}
}

// ✅ GOOD - Responsabilidades separadas
class UserService {
  createUser() {}
  deleteUser() {}
}

class EmailService {
  sendEmail() {}
}

class PaymentService {
  processPayment() {}
}
```

#### 3. Magic Numbers

```typescript
// ❌ BAD - Números mágicos
if (user.age > 18) {
  setTimeout(() => {}, 3600000);
  const discount = price * 0.15;
}

// ✅ GOOD - Constantes nombradas
const LEGAL_AGE = 18;
const ONE_HOUR_MS = 60 * 60 * 1000;
const STANDARD_DISCOUNT_RATE = 0.15;

if (user.age > LEGAL_AGE) {
  setTimeout(() => {}, ONE_HOUR_MS);
  const discount = price * STANDARD_DISCOUNT_RATE;
}
```

#### 4. Premature Optimization

```typescript
// ❌ BAD - Optimización prematura compleja
const result = users.reduce((acc, user) => {
  const key = user.department;
  if (!acc[key]) acc[key] = [];
  acc[key].push(user);
  return acc;
}, {});

// ✅ GOOD - Código claro primero
const usersByDepartment = groupBy(users, "department");
// Optimizar solo si profiling muestra necesidad
```

#### 5. Feature Envy

```typescript
// ❌ BAD - Order accede demasiado a Customer internals
class Order {
  calculateDiscount(customer) {
    if (customer.isPremium() && customer.yearsActive > 2) {
      return customer.totalOrders > 10 ? 0.2 : 0.1;
    }
    return 0;
  }
}

// ✅ GOOD - Customer calcula su propio discount
class Customer {
  getDiscountRate() {
    if (this.isPremium() && this.yearsActive > 2) {
      return this.totalOrders > 10 ? 0.2 : 0.1;
    }
    return 0;
  }
}

class Order {
  calculateDiscount(customer) {
    return customer.getDiscountRate();
  }
}
```

---

## 📊 MÉTRICAS DE CALIDAD

### Complexity Metrics

```javascript
// Script para analizar complejidad
import { readFileSync } from "fs";
import { parse } from "@typescript-eslint/parser";
import escomplex from "escomplex";

function analyzeComplexity(filePath) {
  const code = readFileSync(filePath, "utf-8");
  const ast = parse(code, { sourceType: "module" });

  const report = escomplex.analyze(ast);

  console.log(`File: ${filePath}`);
  console.log(`Cyclomatic Complexity: ${report.aggregate.cyclomatic}`);
  console.log(`Maintainability Index: ${report.maintainability}`);

  // Flag high complexity
  if (report.aggregate.cyclomatic > 10) {
    console.warn("⚠️  High cyclomatic complexity!");
  }

  if (report.maintainability < 65) {
    console.warn("⚠️  Low maintainability!");
  }

  // Function-level metrics
  report.functions.forEach((fn) => {
    if (fn.cyclomatic > 10) {
      console.warn(
        `⚠️  Function "${fn.name}" has high complexity: ${fn.cyclomatic}`
      );
    }
  });
}
```

### Code Coverage Standards

```yaml
# .coverage.yml
coverage:
  status:
    project:
      default:
        target: 80%
        threshold: 2%
    patch:
      default:
        target: 90%

  ignore:
    - "**/*.test.ts"
    - "**/*.spec.ts"
    - "**/tests/**"
    - "**/mocks/**"
```

---

## 🔄 WORKFLOW DE REVISIÓN

### Paso 1: Automated Checks

```bash
Duración: Automático

# Ejecutar en PR
npm run lint
npm run type-check
npm run test
npm run build

Output:
- Lint report
- Type errors
- Test results
- Build status
```

### Paso 2: Code Analysis

```bash
Duración: 15-30 minutos

# Analizar cambios
git diff main...feature-branch

# Complexity analysis
npm run analyze:complexity

# Code metrics
npm run metrics

Output:
- Complexity report
- Code metrics
```

### Paso 3: Manual Review

```bash
Duración: 30-60 minutos por PR

Revisar:
1. Lógica de negocio
2. Edge cases
3. Error handling
4. Performance considerations
5. Security implications
6. Test coverage

Output:
- Review comments
- Approval o Request changes
```

### Paso 4: Feedback Loop

```bash
Duración: Variable

Acciones:
1. Discutir feedback con autor
2. Iterar en mejoras
3. Re-review cambios
4. Aprobar cuando esté listo

Output:
- PR aprobado
- Código mergeado
```

---

## 🛠️ HERRAMIENTAS

### ESLint Configuration

```javascript
// .eslintrc.js
module.exports = {
  extends: [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "plugin:@typescript-eslint/recommended-requiring-type-checking",
  ],
  rules: {
    "max-lines": ["error", { max: 400, skipBlankLines: true }],
    "max-lines-per-function": ["error", { max: 50, skipBlankLines: true }],
    complexity: ["error", 10],
    "max-depth": ["error", 4],
    "max-params": ["error", 4],
    "no-console": ["error", { allow: ["warn", "error"] }],
    "no-magic-numbers": ["warn", { ignore: [0, 1, -1] }],
    "@typescript-eslint/no-explicit-any": "error",
    "@typescript-eslint/explicit-function-return-type": "warn",
    "@typescript-eslint/no-unused-vars": ["error", { argsIgnorePattern: "^_" }],
  },
};
```

### SonarQube Configuration

```properties
# sonar-project.properties
sonar.projectKey=my-project
sonar.projectName=My Project
sonar.projectVersion=1.0

sonar.sources=src
sonar.tests=tests
sonar.exclusions=**/node_modules/**,**/*.test.ts,**/*.spec.ts

sonar.typescript.lcov.reportPaths=coverage/lcov.info

# Quality Gates
sonar.qualitygate.wait=true
sonar.qualitygate.timeout=300
```

---

## 📝 TEMPLATES DE COMENTARIOS

### Template: Sugerencia de Mejora

````markdown
**Suggestion**: Consider extracting this logic into a separate function

**Current code:**
\```typescript
// Complex inline logic
\```

**Suggested improvement:**
\```typescript
function calculateDiscount(user: User, order: Order): number {
// Extracted logic
}
\```

**Benefits:**

- Improved testability
- Better separation of concerns
- More readable
````

### Template: Issue de Seguridad

````markdown
**🔒 Security Issue**: Potential SQL injection vulnerability

**Location**: `src/services/UserService.ts:45`

**Issue:**
\```typescript
const query = `SELECT \* FROM users WHERE email = '${email}'`;
\```

**Fix:**
\```typescript
const query = 'SELECT \* FROM users WHERE email = $1';
const result = await db.query(query, [email]);
\```

**Severity**: HIGH
**Priority**: Must fix before merge
````

### Template: Performance Concern

````markdown
**⚡ Performance**: Potential N+1 query problem

**Issue:** Loading related data in a loop

**Current approach:**
\```typescript
for (const order of orders) {
order.customer = await getCustomer(order.customerId);
}
\```

**Optimized approach:**
\```typescript
const customerIds = orders.map(o => o.customerId);
const customers = await getCustomers(customerIds);
const customersMap = new Map(customers.map(c => [c.id, c]));

orders.forEach(order => {
order.customer = customersMap.get(order.customerId);
});
\```

**Impact**: Reduces DB queries from O(n) to O(1)
````

---

## ✅ CRITERIOS DE ACEPTACIÓN

### Para Aprobar un PR

- [ ] Todos los tests pasando
- [ ] Cobertura >= threshold (80%)
- [ ] Lint sin errores
- [ ] Type checking sin errores
- [ ] Build exitoso
- [ ] No code smells críticos
- [ ] Complejidad dentro de límites
- [ ] Security review pasado
- [ ] Performance considerada
- [ ] Documentación actualizada
- [ ] No breaking changes sin discusión
- [ ] Changelog actualizado (si aplica)

---

**Versión**: 1.0.0
**Última Actualización**: 2026-01-13
**Mantenedor**: Quality Team
