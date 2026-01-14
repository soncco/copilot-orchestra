# API Documentation

Esta carpeta contiene la documentación completa de las APIs del proyecto.

## Estructura

```
api/
├── README.md              # Este archivo
├── openapi.yaml          # Especificación OpenAPI 3.0
├── endpoints/            # Documentación detallada por endpoint
│   ├── auth.md
│   ├── users.md
│   └── ...
└── examples/             # Ejemplos de requests/responses
    ├── authentication.md
    └── ...
```

## OpenAPI / Swagger

Toda nuestra API está documentada usando OpenAPI 3.0.

### Ver Documentación Interactiva

```bash
# Opción 1: Swagger UI (recomendado)
npx swagger-ui-watcher docs/api/openapi.yaml

# Opción 2: Redoc
npx redoc-cli serve docs/api/openapi.yaml

# Opción 3: En producción
# Visita: https://api.example.com/docs
```

### Generar Tipos TypeScript desde OpenAPI

```bash
npx openapi-typescript docs/api/openapi.yaml --output src/types/api.ts
```

## Template OpenAPI

```yaml
openapi: 3.0.0
info:
  title: Your SaaS API
  version: 1.0.0
  description: API documentation for Your SaaS platform
  contact:
    name: API Support
    email: api@example.com
  license:
    name: MIT
    url: https://opensource.org/licenses/MIT

servers:
  - url: http://localhost:3000/api
    description: Development server
  - url: https://staging-api.example.com/api
    description: Staging server
  - url: https://api.example.com/api
    description: Production server

tags:
  - name: Authentication
    description: User authentication endpoints
  - name: Users
    description: User management endpoints
  - name: Products
    description: Product catalog endpoints

paths:
  /auth/register:
    post:
      tags:
        - Authentication
      summary: Register new user
      description: Create a new user account with email and password
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
                  minLength: 8
                  example: SecurePassword123!
                name:
                  type: string
                  example: John Doe
      responses:
        "201":
          description: User successfully registered
          content:
            application/json:
              schema:
                type: object
                properties:
                  user:
                    $ref: "#/components/schemas/User"
                  accessToken:
                    type: string
                    example: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
        "400":
          description: Invalid input or email already exists
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Error"
        "429":
          description: Too many requests
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Error"

  /auth/login:
    post:
      tags:
        - Authentication
      summary: Login user
      description: Authenticate user with email and password
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
                password:
                  type: string
                  format: password
      responses:
        "200":
          description: Successfully authenticated
          headers:
            Set-Cookie:
              description: Refresh token in httpOnly cookie
              schema:
                type: string
                example: refreshToken=abc123; HttpOnly; Secure; SameSite=Strict
          content:
            application/json:
              schema:
                type: object
                properties:
                  user:
                    $ref: "#/components/schemas/User"
                  accessToken:
                    type: string
        "401":
          description: Invalid credentials
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Error"

  /users/me:
    get:
      tags:
        - Users
      summary: Get current user
      description: Retrieve information about the authenticated user
      security:
        - BearerAuth: []
      responses:
        "200":
          description: User information
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/User"
        "401":
          description: Not authenticated
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Error"

components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: string
          example: clx123abc456
        email:
          type: string
          format: email
          example: user@example.com
        name:
          type: string
          example: John Doe
        emailVerified:
          type: boolean
          example: false
        createdAt:
          type: string
          format: date-time
          example: 2026-01-13T10:30:00Z
        updatedAt:
          type: string
          format: date-time
          example: 2026-01-13T10:30:00Z

    Error:
      type: object
      properties:
        error:
          type: string
          example: Invalid credentials
        code:
          type: string
          example: AUTH_001
        details:
          type: object

  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: JWT token obtained from /auth/login or /auth/register

  responses:
    UnauthorizedError:
      description: Access token is missing or invalid
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/Error"

    NotFoundError:
      description: Resource not found
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/Error"

    ValidationError:
      description: Invalid input data
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/Error"
```

## Endpoints por Categoría

### Authentication

- `POST /auth/register` - Register new user
- `POST /auth/login` - Login with email/password
- `POST /auth/refresh` - Refresh access token
- `POST /auth/logout` - Logout user
- `GET /auth/google` - OAuth with Google
- `GET /auth/google/callback` - Google OAuth callback

### Users

- `GET /users/me` - Get current user
- `PUT /users/me` - Update current user
- `DELETE /users/me` - Delete account
- `GET /users/:id` - Get user by ID (admin)

## Rate Limiting

Todas las APIs tienen rate limiting:

| Endpoint          | Límite        | Ventana    |
| ----------------- | ------------- | ---------- |
| `/auth/register`  | 5 requests    | 15 minutos |
| `/auth/login`     | 5 requests    | 15 minutos |
| `/auth/*` (otros) | 20 requests   | 15 minutos |
| `/users/*`        | 100 requests  | 15 minutos |
| Otros endpoints   | 1000 requests | 15 minutos |

Headers de respuesta:

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1642089600
```

## Authentication

### JWT Access Token

Bearer token en header Authorization:

```bash
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Expiración**: 15 minutos

### Refresh Token

httpOnly cookie automáticamente manejado por el browser:

```
Set-Cookie: refreshToken=abc123...; HttpOnly; Secure; SameSite=Strict
```

**Expiración**: 7 días

### Renovar Token

```bash
POST /auth/refresh
# Cookie refreshToken enviado automáticamente
```

Respuesta:

```json
{
  "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

## Error Codes

| Code       | Description            |
| ---------- | ---------------------- |
| `AUTH_001` | Invalid credentials    |
| `AUTH_002` | Token expired          |
| `AUTH_003` | Token invalid          |
| `AUTH_004` | Refresh token expired  |
| `VAL_001`  | Validation error       |
| `VAL_002`  | Missing required field |
| `RES_001`  | Resource not found     |
| `PERM_001` | Permission denied      |
| `RATE_001` | Rate limit exceeded    |

## Ejemplo de Request/Response

### Register User

**Request:**

```bash
curl -X POST http://localhost:3000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "SecurePass123!",
    "name": "John Doe"
  }'
```

**Response (201):**

```json
{
  "user": {
    "id": "clx123abc456",
    "email": "john@example.com",
    "name": "John Doe",
    "emailVerified": false,
    "createdAt": "2026-01-13T10:30:00Z",
    "updatedAt": "2026-01-13T10:30:00Z"
  },
  "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

## Postman Collection

Importa la collection de Postman:

```bash
# Generar collection desde OpenAPI
npx openapi-to-postmanv2 -s docs/api/openapi.yaml -o postman-collection.json

# Importar en Postman: File → Import → postman-collection.json
```

## Testing APIs

### Con curl

```bash
# Variables
export API_URL="http://localhost:3000/api"
export TOKEN="your-access-token"

# Authenticated request
curl -X GET $API_URL/users/me \
  -H "Authorization: Bearer $TOKEN"
```

### Con HTTPie

```bash
http POST :3000/api/auth/login \
  email=user@example.com \
  password=SecurePass123!
```

### Con VS Code REST Client

Crea archivo `requests.http`:

```http
### Register
POST http://localhost:3000/api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "name": "Test User"
}

### Login
POST http://localhost:3000/api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123!"
}

### Get Current User
GET http://localhost:3000/api/users/me
Authorization: Bearer {{accessToken}}
```

---

**Mantén la documentación actualizada con cada cambio en la API!**
