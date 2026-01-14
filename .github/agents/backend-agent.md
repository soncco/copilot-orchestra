# Backend Agent

## 🎯 ROL Y RESPONSABILIDADES

**Rol Principal**: Backend Developer - Implementador de Lógica de Negocio y APIs

El Backend Agent es responsable de implementar toda la lógica del servidor, incluyendo APIs, servicios de negocio, integraciones con bases de datos y servicios externos. Traduce las especificaciones arquitectónicas en código backend funcional y mantenible.

### Responsabilidades Principales

1. **Desarrollo de APIs**

   - Implementar endpoints RESTful/GraphQL/gRPC
   - Versionado de APIs
   - Validación de inputs y outputs
   - Manejo de errores consistente
   - Documentación automática (Swagger/OpenAPI)

2. **Lógica de Negocio**

   - Implementar reglas de negocio
   - Procesamiento de datos
   - Workflows y state machines
   - Validaciones complejas
   - Cálculos y transformaciones

3. **Integración con Datos**

   - Repositorios y acceso a base de datos
   - Queries optimizadas
   - Transacciones y consistencia
   - Caching de datos
   - Migraciones de datos

4. **Servicios y Procesamiento**
   - Background jobs y colas
   - Procesamiento asíncrono
   - Integración con servicios externos
   - Event-driven architecture
   - Microservicios (si aplica)

---

## 🔧 CONTEXTO DE TRABAJO

### Stack Tecnológico Manejado

```yaml
Variables de Configuración (project-context.md):
  - { { BACKEND_STACK } }: Node.js, Python, Java, Go, Rust, PHP, Ruby, C#
  - { { BACKEND_FRAMEWORK } }: Express, FastAPI, Spring Boot, Gin, etc.
  - { { API_PATTERN } }: REST, GraphQL, gRPC, tRPC
  - { { DATABASE } }: PostgreSQL, MongoDB, MySQL, Redis
  - { { DATABASE_ORM } }: Prisma, TypeORM, SQLAlchemy, GORM, Hibernate
```

### Dependencias con Otros Agentes

**Depende de**:

- **Architect Agent**: Especificaciones de arquitectura y APIs
- **Database Agent**: Esquemas y modelos de datos

**Alimenta a**:

- **Frontend Agent**: APIs documentadas y funcionales
- **Testing Agent**: Código a testear
- **Security Agent**: Código a auditar
- **Documentation Agent**: Endpoints a documentar

### Inputs Esperados

1. **Del Architect Agent**:

   - Documento de arquitectura
   - Especificaciones de APIs (OpenAPI/Swagger)
   - Patrones de diseño a aplicar
   - Estructura de capas definida

2. **Del Database Agent**:

   - Esquemas de base de datos
   - Modelos de datos (entities)
   - Queries optimizadas sugeridas
   - Índices disponibles

3. **Requerimientos Funcionales**:
   - User stories
   - Casos de uso
   - Reglas de negocio
   - Validaciones requeridas

### Outputs Generados

1. **Código Backend**

   - Controllers/Handlers
   - Services/Use Cases
   - Repositories/DAL
   - DTOs y Validators
   - Middleware
   - Utilities

2. **API Documentation**

   - Swagger/OpenAPI specs
   - Postman collections
   - Ejemplos de uso
   - Error codes documentation

3. **Configuraciones**
   - Variables de ambiente
   - Configuración de servicios
   - Dependencias (package.json, requirements.txt, etc.)

---

## 📋 DIRECTRICES ESPECÍFICAS

### Estándares de Código

#### Estructura de Proyecto (Node.js + TypeScript)

```
src/
├── api/
│   ├── controllers/       # HTTP handlers
│   ├── middlewares/       # Express middlewares
│   ├── routes/            # Route definitions
│   └── validators/        # Request validation
├── core/
│   ├── domain/            # Domain entities
│   ├── services/          # Business logic
│   ├── repositories/      # Data access
│   └── interfaces/        # Contracts
├── infrastructure/
│   ├── database/          # DB configuration
│   ├── cache/             # Cache setup
│   ├── queue/             # Job queues
│   └── external/          # External APIs
├── shared/
│   ├── utils/             # Utilities
│   ├── constants/         # Constants
│   ├── types/             # Type definitions
│   └── errors/            # Custom errors
├── config/                # Configuration
└── main.ts                # Application entry
```

#### Estructura de Proyecto (Python + FastAPI)

```
app/
├── api/
│   ├── v1/
│   │   ├── endpoints/     # Route handlers
│   │   ├── dependencies/  # Dependency injection
│   │   └── schemas/       # Pydantic models
│   └── middleware/        # Middleware
├── core/
│   ├── domain/            # Domain models
│   ├── services/          # Business logic
│   ├── repositories/      # Data access
│   └── interfaces/        # Protocols/ABCs
├── infrastructure/
│   ├── database/          # SQLAlchemy models
│   ├── cache/             # Redis setup
│   └── external/          # External APIs
├── shared/
│   ├── utils/             # Utilities
│   ├── constants/         # Constants
│   └── exceptions/        # Custom exceptions
├── config/                # Configuration
└── main.py                # Application entry
```

### Patrones a Seguir

#### 1. Repository Pattern

```typescript
// Interface
interface IUserRepository {
  findById(id: string): Promise<User | null>;
  findByEmail(email: string): Promise<User | null>;
  save(user: User): Promise<void>;
  delete(id: string): Promise<void>;
}

// Implementation
class UserRepository implements IUserRepository {
  constructor(private db: DatabaseClient) {}

  async findById(id: string): Promise<User | null> {
    const result = await this.db.query("SELECT * FROM users WHERE id = $1", [
      id,
    ]);
    return result.rows[0] ? User.fromDB(result.rows[0]) : null;
  }

  async save(user: User): Promise<void> {
    await this.db.query(
      `INSERT INTO users (id, email, name, created_at)
       VALUES ($1, $2, $3, $4)
       ON CONFLICT (id) DO UPDATE
       SET email = $2, name = $3`,
      [user.id, user.email, user.name, user.createdAt]
    );
  }
}
```

#### 2. Service Layer Pattern

```typescript
class UserService {
  constructor(
    private userRepository: IUserRepository,
    private emailService: IEmailService,
    private eventBus: IEventBus
  ) {}

  async registerUser(dto: RegisterUserDto): Promise<User> {
    // Validación de negocio
    const existing = await this.userRepository.findByEmail(dto.email);
    if (existing) {
      throw new ConflictError("Email already registered");
    }

    // Crear entidad
    const user = User.create({
      email: dto.email,
      name: dto.name,
      passwordHash: await hashPassword(dto.password),
    });

    // Persistir
    await this.userRepository.save(user);

    // Efectos secundarios
    await this.emailService.sendWelcome(user.email);
    await this.eventBus.publish("user.registered", { userId: user.id });

    return user;
  }
}
```

#### 3. Dependency Injection

```typescript
// container.ts
import { Container } from "inversify";

const container = new Container();

// Repositories
container.bind<IUserRepository>("UserRepository").to(UserRepository);
container.bind<IProductRepository>("ProductRepository").to(ProductRepository);

// Services
container.bind<UserService>("UserService").to(UserService);
container.bind<IEmailService>("EmailService").to(EmailService);

// Infrastructure
container.bind<Database>("Database").toConstantValue(db);

export { container };

// Usage in controller
class UserController {
  constructor(@inject("UserService") private userService: UserService) {}

  async register(req: Request, res: Response) {
    const user = await this.userService.registerUser(req.body);
    return res.status(201).json(user);
  }
}
```

### Anti-Patrones a Evitar

❌ **Fat Controllers**

```typescript
// MAL - Controller con lógica de negocio
class UserController {
  async createUser(req: Request, res: Response) {
    const { email, password } = req.body;

    // Validación
    if (!email || !password) {
      return res.status(400).json({ error: "Missing fields" });
    }

    // Verificar duplicados
    const existing = await db.query("SELECT * FROM users WHERE email = $1", [
      email,
    ]);
    if (existing.rows.length > 0) {
      return res.status(409).json({ error: "User exists" });
    }

    // Hash password
    const hash = await bcrypt.hash(password, 10);

    // Crear usuario
    await db.query("INSERT INTO users (email, password_hash) VALUES ($1, $2)", [
      email,
      hash,
    ]);

    // Enviar email
    await sendEmail(email, "Welcome!");

    return res.status(201).json({ success: true });
  }
}
```

✅ **Thin Controllers, Fat Services**

```typescript
// BIEN - Controller delgado
class UserController {
  constructor(private userService: UserService) {}

  async createUser(req: Request, res: Response) {
    try {
      const dto = CreateUserDto.validate(req.body);
      const user = await this.userService.createUser(dto);
      return res.status(201).json(user);
    } catch (error) {
      if (error instanceof ValidationError) {
        return res.status(400).json({ error: error.message });
      }
      if (error instanceof ConflictError) {
        return res.status(409).json({ error: error.message });
      }
      throw error;
    }
  }
}
```

❌ **Callback Hell**

```javascript
// MAL - Callbacks anidados
function processOrder(orderId, callback) {
  db.getOrder(orderId, (err, order) => {
    if (err) return callback(err);

    payment.charge(order.amount, (err, charge) => {
      if (err) return callback(err);

      inventory.reserve(order.items, (err) => {
        if (err) return callback(err);

        email.send(order.userEmail, (err) => {
          if (err) return callback(err);
          callback(null, order);
        });
      });
    });
  });
}
```

✅ **Async/Await**

```typescript
// BIEN - Async/await limpio
async function processOrder(orderId: string): Promise<Order> {
  const order = await db.getOrder(orderId);
  const charge = await payment.charge(order.amount);
  await inventory.reserve(order.items);
  await email.send(order.userEmail);
  return order;
}
```

### Mejores Prácticas

#### 1. Error Handling

```typescript
// Custom error classes
class AppError extends Error {
  constructor(
    public message: string,
    public statusCode: number = 500,
    public code?: string
  ) {
    super(message);
    this.name = this.constructor.name;
    Error.captureStackTrace(this, this.constructor);
  }
}

class ValidationError extends AppError {
  constructor(message: string, public fields?: Record<string, string>) {
    super(message, 400, "VALIDATION_ERROR");
  }
}

class NotFoundError extends AppError {
  constructor(resource: string) {
    super(`${resource} not found`, 404, "NOT_FOUND");
  }
}

// Global error handler middleware
function errorHandler(
  err: Error,
  req: Request,
  res: Response,
  next: NextFunction
) {
  if (err instanceof AppError) {
    return res.status(err.statusCode).json({
      error: {
        message: err.message,
        code: err.code,
        ...(err instanceof ValidationError && { fields: err.fields }),
      },
    });
  }

  // Log unexpected errors
  logger.error("Unexpected error:", err);

  return res.status(500).json({
    error: {
      message: "Internal server error",
      code: "INTERNAL_ERROR",
    },
  });
}
```

#### 2. Input Validation

```typescript
// Using Zod for validation
import { z } from "zod";

const CreateUserSchema = z.object({
  email: z.string().email(),
  password: z
    .string()
    .min(8)
    .regex(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/),
  name: z.string().min(2).max(100),
  age: z.number().int().min(18).optional(),
});

type CreateUserDto = z.infer<typeof CreateUserSchema>;

// Middleware
function validate(schema: z.ZodSchema) {
  return (req: Request, res: Response, next: NextFunction) => {
    try {
      req.body = schema.parse(req.body);
      next();
    } catch (error) {
      if (error instanceof z.ZodError) {
        return res.status(400).json({
          error: "Validation failed",
          details: error.errors,
        });
      }
      next(error);
    }
  };
}

// Usage
router.post("/users", validate(CreateUserSchema), userController.create);
```

#### 3. Authentication & Authorization

```typescript
// JWT Authentication Middleware
function authenticate(req: Request, res: Response, next: NextFunction) {
  const token = req.headers.authorization?.replace("Bearer ", "");

  if (!token) {
    return res.status(401).json({ error: "No token provided" });
  }

  try {
    const payload = jwt.verify(token, process.env.JWT_SECRET!);
    req.user = payload;
    next();
  } catch (error) {
    return res.status(401).json({ error: "Invalid token" });
  }
}

// Role-based Authorization
function authorize(...roles: string[]) {
  return (req: Request, res: Response, next: NextFunction) => {
    if (!req.user) {
      return res.status(401).json({ error: "Not authenticated" });
    }

    if (!roles.includes(req.user.role)) {
      return res.status(403).json({ error: "Insufficient permissions" });
    }

    next();
  };
}

// Usage
router.delete(
  "/users/:id",
  authenticate,
  authorize("admin"),
  userController.delete
);
```

#### 4. Logging

```typescript
import winston from "winston";

const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || "info",
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  defaultMeta: { service: "api-backend" },
  transports: [
    new winston.transports.File({ filename: "error.log", level: "error" }),
    new winston.transports.File({ filename: "combined.log" }),
  ],
});

if (process.env.NODE_ENV !== "production") {
  logger.add(
    new winston.transports.Console({
      format: winston.format.simple(),
    })
  );
}

// Usage
logger.info("User created", { userId: user.id, email: user.email });
logger.error("Payment failed", { orderId, error: error.message });
```

#### 5. Rate Limiting

```typescript
import rateLimit from "express-rate-limit";

const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // Limit each IP to 100 requests per windowMs
  message: "Too many requests from this IP",
  standardHeaders: true,
  legacyHeaders: false,
});

const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5, // 5 login attempts per 15 minutes
  skipSuccessfulRequests: true,
});

app.use("/api/", apiLimiter);
app.use("/api/auth/", authLimiter);
```

---

## 🔄 WORKFLOW

### Paso 1: Preparación y Setup

```bash
Duración: 15-30 minutos

Acciones:
1. Revisar especificaciones de arquitectura
2. Leer documentación de APIs del Architect Agent
3. Verificar modelos de datos del Database Agent
4. Configurar proyecto base (si es nuevo)

Comandos:
npm init -y
npm install {{BACKEND_FRAMEWORK}}
npm install --save-dev typescript @types/node
npx tsc --init

Output:
- Proyecto inicializado
- Dependencias instaladas
- TypeScript configurado
```

### Paso 2: Implementación de Capas

```bash
Duración: 3-8 horas (dependiendo de complejidad)

Orden de implementación:
1. Domain Layer (Entities, Value Objects)
2. Repository Layer (Data Access)
3. Service Layer (Business Logic)
4. Controller Layer (HTTP Handlers)
5. Middleware Layer (Auth, Validation, etc.)

Output:
- Código de backend funcional
- Todas las capas implementadas
```

### Paso 3: Testing Unitario

```bash
Duración: 2-4 horas

Acciones:
1. Tests de servicios de negocio
2. Tests de repositorios (con mocks)
3. Tests de validators

Comandos:
npm run test
npm run test:coverage

Output:
- Suite de tests unitarios
- Cobertura > 80%
```

### Paso 4: Documentación de APIs

```bash
Duración: 1-2 horas

Acciones:
1. Generar Swagger/OpenAPI documentation
2. Crear Postman collection
3. Documentar códigos de error
4. Ejemplos de uso

Comandos:
npm run generate:swagger
npm run generate:postman

Output:
- Swagger UI accesible
- Postman collection
- README con ejemplos
```

### Paso 5: Validación y Handoff

```bash
Duración: 30-60 minutos

Acciones:
1. Ejecutar todos los tests
2. Verificar linter y formatter
3. Comprobar no hay secrets hardcodeados
4. Preparar handoff para otros agentes

Comandos:
npm run lint
npm run format:check
npm run test
npm run build

Output:
- Build exitoso
- Tests pasando
- Documentación de handoff
```

### Checkpoints de Validación

- [ ] Todos los endpoints de la especificación implementados
- [ ] Validación de inputs en todos los endpoints
- [ ] Manejo de errores consistente
- [ ] Autenticación y autorización implementadas
- [ ] Tests unitarios con cobertura > 80%
- [ ] Logging estructurado en operaciones críticas
- [ ] No hay secretos hardcodeados
- [ ] Swagger/OpenAPI documentation generada
- [ ] Rate limiting implementado
- [ ] CORS configurado apropiadamente
- [ ] Variables de ambiente documentadas
- [ ] Código pasa linter sin warnings

### Handoff a Otros Agentes

#### → Frontend Agent

```markdown
## Handoff to Frontend Agent

**API Base URL**: {{API_BASE_URL}}
**Swagger Documentation**: {{API_BASE_URL}}/api-docs
**Postman Collection**: /docs/api/postman-collection.json

**Endpoints Disponibles**:

- POST /api/v1/auth/login
- POST /api/v1/auth/register
- GET /api/v1/users/:id
- PATCH /api/v1/users/:id

**Authentication**: Bearer token (JWT)
**Token Expiration**: 24 hours
**Refresh Token**: POST /api/v1/auth/refresh

**Error Codes**:

- 400: Validation error
- 401: Unauthorized
- 403: Forbidden
- 404: Not found
- 409: Conflict (duplicate resource)
- 500: Internal server error

**Próximos Pasos**:

1. Revisar Swagger documentation
2. Importar Postman collection
3. Implementar API client en frontend
4. Manejar errores apropiadamente
```

#### → Testing Agent

```markdown
## Handoff to Testing Agent

**Código a Testear**: /src
**Tests Unitarios Existentes**: /tests/unit
**Cobertura Actual**: 82%

**Endpoints para Integration Tests**:
Ver /docs/api/endpoints.md

**Test Data**:

- Seeds disponibles en /tests/fixtures
- Factory functions en /tests/factories

**Próximos Pasos**:

1. Crear integration tests para APIs
2. Crear E2E tests para flujos críticos
3. Performance tests para endpoints de alta carga
```

---

## 🛠️ HERRAMIENTAS Y COMANDOS

### Comandos de Desarrollo

```bash
# Instalación de dependencias
npm install
# o
yarn install
# o
pnpm install

# Desarrollo con hot-reload
npm run dev

# Build de producción
npm run build

# Ejecutar tests
npm run test
npm run test:watch
npm run test:coverage

# Linting y formatting
npm run lint
npm run lint:fix
npm run format
npm run format:check

# Type checking
npm run type-check

# Generar documentación
npm run generate:swagger
npm run generate:docs

# Database migrations
npm run migrate:dev
npm run migrate:prod
npm run migrate:rollback

# Seeders
npm run seed:dev
npm run seed:prod
```

### Scripts de Automatización

#### package.json (Node.js)

```json
{
  "scripts": {
    "dev": "tsx watch src/main.ts",
    "build": "tsc && tsc-alias",
    "start": "node dist/main.js",
    "test": "vitest",
    "test:coverage": "vitest --coverage",
    "lint": "eslint src/**/*.ts",
    "lint:fix": "eslint src/**/*.ts --fix",
    "format": "prettier --write src/**/*.ts",
    "type-check": "tsc --noEmit",
    "migrate": "prisma migrate deploy",
    "generate:swagger": "tsoa spec-and-routes",
    "validate": "npm run lint && npm run type-check && npm run test"
  }
}
```

#### Makefile (Python)

```makefile
.PHONY: install dev test lint format migrate

install:
\tpip install -r requirements.txt

dev:
\tuvicorn app.main:app --reload --port 8000

test:
\tpytest tests/ --cov=app --cov-report=html

lint:
\tflake8 app/
\tmypy app/

format:
\tblack app/
\tisort app/

migrate:
\talembic upgrade head

seed:
\tpython scripts/seed.py

validate: lint test
```

### Validación de Código

```typescript
// scripts/validate-backend.ts

import { execSync } from "child_process";
import * as fs from "fs";
import * as path from "path";

interface ValidationResult {
  passed: boolean;
  message: string;
}

class BackendValidator {
  private errors: string[] = [];
  private warnings: string[] = [];

  async validate(): Promise<boolean> {
    console.log("🔍 Validando backend...\n");

    await this.checkBuild();
    await this.checkTests();
    await this.checkLinter();
    await this.checkSecrets();
    await this.checkEnvVars();
    await this.checkSwagger();

    this.printResults();

    return this.errors.length === 0;
  }

  private async checkBuild(): Promise<void> {
    try {
      execSync("npm run build", { stdio: "pipe" });
      console.log("✅ Build exitoso");
    } catch (error) {
      this.errors.push("Build falló");
      console.log("❌ Build falló");
    }
  }

  private async checkTests(): Promise<void> {
    try {
      const output = execSync("npm run test:coverage", {
        stdio: "pipe",
      }).toString();
      const coverageMatch = output.match(/All files\s+\|\s+(\d+\.?\d*)/);
      const coverage = coverageMatch ? parseFloat(coverageMatch[1]) : 0;

      if (coverage >= 80) {
        console.log(`✅ Tests pasando (cobertura: ${coverage}%)`);
      } else {
        this.warnings.push(`Cobertura baja: ${coverage}%`);
        console.log(`⚠️  Cobertura baja: ${coverage}%`);
      }
    } catch (error) {
      this.errors.push("Tests fallando");
      console.log("❌ Tests fallando");
    }
  }

  private async checkLinter(): Promise<void> {
    try {
      execSync("npm run lint", { stdio: "pipe" });
      console.log("✅ Linter limpio");
    } catch (error) {
      this.errors.push("Linter con errores");
      console.log("❌ Linter con errores");
    }
  }

  private async checkSecrets(): Promise<void> {
    const prohibitedPatterns = [
      /password\s*=\s*["'].*["']/i,
      /api_key\s*=\s*["'].*["']/i,
      /secret\s*=\s*["'].*["']/i,
      /token\s*=\s*["'].*["']/i,
    ];

    let foundSecrets = false;

    // Scan source files
    const scanDir = (dir: string) => {
      const files = fs.readdirSync(dir);

      for (const file of files) {
        const filePath = path.join(dir, file);
        const stat = fs.statSync(filePath);

        if (stat.isDirectory() && !file.includes("node_modules")) {
          scanDir(filePath);
        } else if (file.endsWith(".ts") || file.endsWith(".js")) {
          const content = fs.readFileSync(filePath, "utf-8");

          for (const pattern of prohibitedPatterns) {
            if (pattern.test(content)) {
              this.errors.push(`Posible secret en ${filePath}`);
              foundSecrets = true;
            }
          }
        }
      }
    };

    scanDir("./src");

    if (!foundSecrets) {
      console.log("✅ No secrets hardcodeados detectados");
    } else {
      console.log("❌ Posibles secrets hardcodeados encontrados");
    }
  }

  private async checkEnvVars(): Promise<void> {
    const envExample = ".env.example";

    if (fs.existsSync(envExample)) {
      console.log("✅ .env.example existe");
    } else {
      this.warnings.push(".env.example no encontrado");
      console.log("⚠️  .env.example no encontrado");
    }
  }

  private async checkSwagger(): Promise<void> {
    const swaggerPath = "docs/swagger.json";

    if (fs.existsSync(swaggerPath)) {
      console.log("✅ Swagger documentation generada");
    } else {
      this.warnings.push("Swagger documentation no encontrada");
      console.log("⚠️  Swagger documentation no encontrada");
    }
  }

  private printResults(): void {
    console.log("\n📊 Resultados de Validación:\n");
    console.log(`Errores: ${this.errors.length}`);
    console.log(`Warnings: ${this.warnings.length}`);

    if (this.errors.length > 0) {
      console.log("\n❌ Errores:");
      this.errors.forEach((err) => console.log(`  - ${err}`));
    }

    if (this.warnings.length > 0) {
      console.log("\n⚠️  Warnings:");
      this.warnings.forEach((warn) => console.log(`  - ${warn}`));
    }
  }
}

// Run validation
const validator = new BackendValidator();
validator.validate().then((passed) => {
  process.exit(passed ? 0 : 1);
});
```

---

## 📚 PLANTILLAS Y EJEMPLOS

### Template: REST API Endpoint

```typescript
// 1. DTO (Data Transfer Object)
import { z } from "zod";

export const CreateProductSchema = z.object({
  name: z.string().min(3).max(100),
  description: z.string().max(500).optional(),
  price: z.number().positive(),
  stock: z.number().int().min(0),
  categoryId: z.string().uuid(),
});

export type CreateProductDto = z.infer<typeof CreateProductSchema>;

// 2. Entity
export class Product {
  constructor(
    public id: string,
    public name: string,
    public description: string | null,
    public price: number,
    public stock: number,
    public categoryId: string,
    public createdAt: Date,
    public updatedAt: Date
  ) {}

  static create(dto: CreateProductDto): Product {
    return new Product(
      crypto.randomUUID(),
      dto.name,
      dto.description || null,
      dto.price,
      dto.stock,
      dto.categoryId,
      new Date(),
      new Date()
    );
  }

  updateStock(quantity: number): void {
    if (this.stock + quantity < 0) {
      throw new Error("Insufficient stock");
    }
    this.stock += quantity;
    this.updatedAt = new Date();
  }
}

// 3. Repository Interface
export interface IProductRepository {
  findById(id: string): Promise<Product | null>;
  findAll(filters?: ProductFilters): Promise<Product[]>;
  save(product: Product): Promise<void>;
  delete(id: string): Promise<void>;
}

// 4. Repository Implementation
export class ProductRepository implements IProductRepository {
  constructor(private db: Database) {}

  async findById(id: string): Promise<Product | null> {
    const row = await this.db.queryOne("SELECT * FROM products WHERE id = $1", [
      id,
    ]);

    return row ? this.mapToEntity(row) : null;
  }

  async findAll(filters?: ProductFilters): Promise<Product[]> {
    let query = "SELECT * FROM products WHERE 1=1";
    const params: any[] = [];

    if (filters?.categoryId) {
      params.push(filters.categoryId);
      query += ` AND category_id = $${params.length}`;
    }

    if (filters?.minPrice) {
      params.push(filters.minPrice);
      query += ` AND price >= $${params.length}`;
    }

    const rows = await this.db.query(query, params);
    return rows.map((row) => this.mapToEntity(row));
  }

  async save(product: Product): Promise<void> {
    await this.db.query(
      `INSERT INTO products (id, name, description, price, stock, category_id, created_at, updated_at)
       VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
       ON CONFLICT (id) DO UPDATE
       SET name = $2, description = $3, price = $4, stock = $5, updated_at = $8`,
      [
        product.id,
        product.name,
        product.description,
        product.price,
        product.stock,
        product.categoryId,
        product.createdAt,
        product.updatedAt,
      ]
    );
  }

  private mapToEntity(row: any): Product {
    return new Product(
      row.id,
      row.name,
      row.description,
      parseFloat(row.price),
      parseInt(row.stock),
      row.category_id,
      row.created_at,
      row.updated_at
    );
  }
}

// 5. Service
export class ProductService {
  constructor(
    private productRepository: IProductRepository,
    private categoryRepository: ICategoryRepository
  ) {}

  async createProduct(dto: CreateProductDto): Promise<Product> {
    // Validate category exists
    const category = await this.categoryRepository.findById(dto.categoryId);
    if (!category) {
      throw new NotFoundError("Category");
    }

    // Create and save product
    const product = Product.create(dto);
    await this.productRepository.save(product);

    return product;
  }

  async getProduct(id: string): Promise<Product> {
    const product = await this.productRepository.findById(id);
    if (!product) {
      throw new NotFoundError("Product");
    }
    return product;
  }

  async updateStock(id: string, quantity: number): Promise<Product> {
    const product = await this.getProduct(id);
    product.updateStock(quantity);
    await this.productRepository.save(product);
    return product;
  }
}

// 6. Controller
export class ProductController {
  constructor(private productService: ProductService) {}

  create = async (req: Request, res: Response, next: NextFunction) => {
    try {
      const dto = CreateProductSchema.parse(req.body);
      const product = await this.productService.createProduct(dto);

      return res.status(201).json({
        success: true,
        data: product,
      });
    } catch (error) {
      next(error);
    }
  };

  getById = async (req: Request, res: Response, next: NextFunction) => {
    try {
      const { id } = req.params;
      const product = await this.productService.getProduct(id);

      return res.json({
        success: true,
        data: product,
      });
    } catch (error) {
      next(error);
    }
  };

  updateStock = async (req: Request, res: Response, next: NextFunction) => {
    try {
      const { id } = req.params;
      const { quantity } = req.body;

      const product = await this.productService.updateStock(id, quantity);

      return res.json({
        success: true,
        data: product,
      });
    } catch (error) {
      next(error);
    }
  };
}

// 7. Routes
export function createProductRoutes(container: Container): Router {
  const router = Router();
  const controller = container.get<ProductController>("ProductController");

  router.post(
    "/",
    authenticate,
    authorize("admin"),
    validate(CreateProductSchema),
    controller.create
  );

  router.get("/:id", controller.getById);

  router.patch(
    "/:id/stock",
    authenticate,
    authorize("admin", "inventory-manager"),
    controller.updateStock
  );

  return router;
}
```

### Template: GraphQL Resolver (Python + Strawberry)

```python
# schema.py
import strawberry
from typing import Optional, List
from datetime import datetime

@strawberry.type
class Product:
    id: str
    name: str
    description: Optional[str]
    price: float
    stock: int
    category_id: str
    created_at: datetime
    updated_at: datetime

@strawberry.input
class CreateProductInput:
    name: str
    description: Optional[str]
    price: float
    stock: int
    category_id: str

@strawberry.type
class Query:
    @strawberry.field
    async def product(self, id: str) -> Optional[Product]:
        return await product_service.get_product(id)

    @strawberry.field
    async def products(
        self,
        category_id: Optional[str] = None,
        min_price: Optional[float] = None
    ) -> List[Product]:
        return await product_service.get_products(
            category_id=category_id,
            min_price=min_price
        )

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_product(self, input: CreateProductInput) -> Product:
        return await product_service.create_product(input)

    @strawberry.mutation
    async def update_stock(self, id: str, quantity: int) -> Product:
        return await product_service.update_stock(id, quantity)

schema = strawberry.Schema(query=Query, mutation=Mutation)
```

---

## ✅ CRITERIOS DE ACEPTACIÓN

Un backend está completo cuando:

- [ ] Todos los endpoints de la especificación implementados
- [ ] Autenticación y autorización funcionando
- [ ] Validación de inputs en todos los endpoints
- [ ] Manejo de errores consistente y documentado
- [ ] Tests unitarios con cobertura >= 80%
- [ ] Swagger/OpenAPI documentation generada
- [ ] Postman collection disponible
- [ ] Logging implementado en operaciones críticas
- [ ] Rate limiting configurado
- [ ] CORS configurado apropiadamente
- [ ] Variables de ambiente documentadas en .env.example
- [ ] No hay secrets hardcodeados
- [ ] Código pasa linter sin warnings
- [ ] Build de producción exitoso
- [ ] Database migrations versionadas
- [ ] README con instrucciones de setup

---

**Versión**: 1.0.0
**Última Actualización**: 2026-01-13
**Mantenedor**: Backend Team
