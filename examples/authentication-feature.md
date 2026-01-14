# Example: Complete Authentication Feature

Este ejemplo muestra cómo el sistema de agentes trabaja en conjunto para implementar una feature completa de autenticación con OAuth.

## Workflow Ejecutado

```
Architect → Database → Backend → Frontend → Testing → Security → Code Review → Documentation → DevOps
```

---

## 1. Architect Agent Output

### ADR-001: Authentication Strategy

**Status**: Accepted
**Date**: 2026-01-13
**Decision Makers**: Architect Agent

#### Context

Necesitamos implementar autenticación segura que soporte:

- Email/password tradicional
- OAuth con Google
- Session management con JWT
- Refresh token rotation

#### Decision

Usaremos **OAuth 2.0 con PKCE** para flujos externos y **JWT** para session management.

**Justificación**:

- PKCE previene ataques de intercepción en mobile/SPA
- JWT permite stateless authentication
- Refresh tokens permiten sesiones largas sin comprometer seguridad

#### Architecture

```
┌─────────┐         ┌──────────┐         ┌─────────┐
│ Client  │────────▶│ Backend  │────────▶│  Google │
│  (SPA)  │◀────────│   API    │◀────────│  OAuth  │
└─────────┘         └──────────┘         └─────────┘
                          │
                          ▼
                    ┌──────────┐
                    │   DB     │
                    │  Users   │
                    │  Tokens  │
                    └──────────┘
```

### Handoff to Database Agent

**Files Created**:

- `docs/architecture/ADR-001-authentication.md`
- `docs/architecture/diagrams/auth-flow.mmd`

**Next Steps**:

1. Create users table with email, password hash, OAuth fields
2. Create refresh_tokens table
3. Add indexes for email lookups

---

## 2. Database Agent Output

### Schema Design

```prisma
// prisma/schema.prisma

model User {
  id            String    @id @default(cuid())
  email         String    @unique
  name          String?
  passwordHash  String?   // Null for OAuth-only users
  emailVerified Boolean   @default(false)

  // OAuth fields
  googleId      String?   @unique

  // Timestamps
  createdAt     DateTime  @default(now())
  updatedAt     DateTime  @updatedAt

  // Relations
  refreshTokens RefreshToken[]

  @@index([email])
  @@index([googleId])
}

model RefreshToken {
  id        String   @id @default(cuid())
  token     String   @unique
  userId    String
  expiresAt DateTime
  createdAt DateTime @default(now())

  user      User     @relation(fields: [userId], references: [id], onDelete: Cascade)

  @@index([userId])
  @@index([token])
}
```

### Migration

```bash
npx prisma migrate dev --name add_authentication
```

### Handoff to Backend Agent

**Files Created**:

- `prisma/schema.prisma` (updated)
- `prisma/migrations/xxx_add_authentication/`

**Next Steps**:

1. Implement AuthService class
2. Create /auth/login, /auth/refresh, /auth/logout endpoints
3. Implement JWT middleware
4. Add rate limiting

---

## 3. Backend Agent Output

### AuthService Implementation

```typescript
// src/features/auth/services/AuthService.ts

import bcrypt from "bcrypt";
import jwt from "jsonwebtoken";
import { prisma } from "@/infrastructure/database";

export class AuthService {
  /**
   * Register new user with email/password
   */
  async register(email: string, password: string, name?: string) {
    // Check if user exists
    const existing = await prisma.user.findUnique({ where: { email } });
    if (existing) {
      throw new AppError("Email already registered", 400);
    }

    // Hash password
    const passwordHash = await bcrypt.hash(password, 10);

    // Create user
    const user = await prisma.user.create({
      data: {
        email,
        passwordHash,
        name,
      },
    });

    // Generate tokens
    const { accessToken, refreshToken } = await this.generateTokens(user.id);

    return {
      user: this.sanitizeUser(user),
      accessToken,
      refreshToken,
    };
  }

  /**
   * Login with email/password
   */
  async login(email: string, password: string) {
    // Find user
    const user = await prisma.user.findUnique({ where: { email } });
    if (!user || !user.passwordHash) {
      throw new AppError("Invalid credentials", 401);
    }

    // Verify password
    const valid = await bcrypt.compare(password, user.passwordHash);
    if (!valid) {
      throw new AppError("Invalid credentials", 401);
    }

    // Generate tokens
    const { accessToken, refreshToken } = await this.generateTokens(user.id);

    return {
      user: this.sanitizeUser(user),
      accessToken,
      refreshToken,
    };
  }

  /**
   * Refresh access token
   */
  async refresh(refreshToken: string) {
    // Find refresh token
    const tokenRecord = await prisma.refreshToken.findUnique({
      where: { token: refreshToken },
      include: { user: true },
    });

    if (!tokenRecord) {
      throw new AppError("Invalid refresh token", 401);
    }

    // Check expiration
    if (tokenRecord.expiresAt < new Date()) {
      await prisma.refreshToken.delete({ where: { id: tokenRecord.id } });
      throw new AppError("Refresh token expired", 401);
    }

    // Generate new tokens (rotation)
    await prisma.refreshToken.delete({ where: { id: tokenRecord.id } });
    const tokens = await this.generateTokens(tokenRecord.userId);

    return tokens;
  }

  /**
   * Logout (invalidate refresh token)
   */
  async logout(refreshToken: string) {
    await prisma.refreshToken.deleteMany({
      where: { token: refreshToken },
    });
  }

  /**
   * Generate JWT access token and refresh token
   */
  private async generateTokens(userId: string) {
    // Access token (short-lived)
    const accessToken = jwt.sign({ userId }, process.env.JWT_SECRET!, {
      expiresIn: "15m",
    });

    // Refresh token (long-lived)
    const refreshToken = crypto.randomBytes(64).toString("hex");

    await prisma.refreshToken.create({
      data: {
        token: refreshToken,
        userId,
        expiresAt: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000), // 7 days
      },
    });

    return { accessToken, refreshToken };
  }

  private sanitizeUser(user: any) {
    const { passwordHash, ...sanitized } = user;
    return sanitized;
  }
}
```

### API Routes

```typescript
// src/features/auth/routes.ts

import { Router } from "express";
import { AuthService } from "./services/AuthService";
import { rateLimiter } from "@/middleware/rateLimiter";

const router = Router();
const authService = new AuthService();

// POST /auth/register
router.post("/register", rateLimiter(5, "15m"), async (req, res) => {
  try {
    const { email, password, name } = req.body;

    // Validation
    if (!email || !password) {
      return res.status(400).json({ error: "Email and password required" });
    }

    const result = await authService.register(email, password, name);

    // Set refresh token in httpOnly cookie
    res.cookie("refreshToken", result.refreshToken, {
      httpOnly: true,
      secure: process.env.NODE_ENV === "production",
      sameSite: "strict",
      maxAge: 7 * 24 * 60 * 60 * 1000, // 7 days
    });

    res.status(201).json({
      user: result.user,
      accessToken: result.accessToken,
    });
  } catch (error) {
    console.error("Registration error:", error);
    res.status(error.statusCode || 500).json({ error: error.message });
  }
});

// POST /auth/login
router.post("/login", rateLimiter(5, "15m"), async (req, res) => {
  try {
    const { email, password } = req.body;

    const result = await authService.login(email, password);

    res.cookie("refreshToken", result.refreshToken, {
      httpOnly: true,
      secure: process.env.NODE_ENV === "production",
      sameSite: "strict",
      maxAge: 7 * 24 * 60 * 60 * 1000,
    });

    res.json({
      user: result.user,
      accessToken: result.accessToken,
    });
  } catch (error) {
    res.status(error.statusCode || 500).json({ error: error.message });
  }
});

// POST /auth/refresh
router.post("/refresh", async (req, res) => {
  try {
    const refreshToken = req.cookies.refreshToken;

    if (!refreshToken) {
      return res.status(401).json({ error: "No refresh token" });
    }

    const tokens = await authService.refresh(refreshToken);

    res.cookie("refreshToken", tokens.refreshToken, {
      httpOnly: true,
      secure: process.env.NODE_ENV === "production",
      sameSite: "strict",
      maxAge: 7 * 24 * 60 * 60 * 1000,
    });

    res.json({ accessToken: tokens.accessToken });
  } catch (error) {
    res.clearCookie("refreshToken");
    res.status(401).json({ error: error.message });
  }
});

// POST /auth/logout
router.post("/logout", async (req, res) => {
  try {
    const refreshToken = req.cookies.refreshToken;

    if (refreshToken) {
      await authService.logout(refreshToken);
    }

    res.clearCookie("refreshToken");
    res.json({ message: "Logged out successfully" });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

export default router;
```

### JWT Middleware

```typescript
// src/middleware/authenticate.ts

import jwt from "jsonwebtoken";
import { Request, Response, NextFunction } from "express";

export const authenticate = (
  req: Request,
  res: Response,
  next: NextFunction
) => {
  const authHeader = req.headers.authorization;

  if (!authHeader || !authHeader.startsWith("Bearer ")) {
    return res.status(401).json({ error: "No token provided" });
  }

  const token = authHeader.substring(7);

  try {
    const payload = jwt.verify(token, process.env.JWT_SECRET!) as {
      userId: string;
    };

    req.user = { id: payload.userId };
    next();
  } catch (error) {
    return res.status(401).json({ error: "Invalid token" });
  }
};
```

### Handoff to Frontend Agent

**Files Created**:

- `src/features/auth/services/AuthService.ts`
- `src/features/auth/routes.ts`
- `src/middleware/authenticate.ts`
- `src/middleware/rateLimiter.ts`

**Next Steps**:

1. Create useAuth hook
2. Implement login/register forms
3. Add protected route wrapper
4. Handle token refresh

---

## 4. Frontend Agent Output

### useAuth Hook

```typescript
// src/features/auth/hooks/useAuth.ts

import { create } from "zustand";
import { persist } from "zustand/middleware";

interface User {
  id: string;
  email: string;
  name?: string;
}

interface AuthState {
  user: User | null;
  accessToken: string | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, name?: string) => Promise<void>;
  logout: () => Promise<void>;
  refresh: () => Promise<void>;
}

export const useAuth = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      accessToken: null,
      isAuthenticated: false,

      login: async (email, password) => {
        const response = await fetch("/api/auth/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email, password }),
          credentials: "include", // Important for cookies
        });

        if (!response.ok) {
          const error = await response.json();
          throw new Error(error.message);
        }

        const { user, accessToken } = await response.json();

        set({
          user,
          accessToken,
          isAuthenticated: true,
        });
      },

      register: async (email, password, name) => {
        const response = await fetch("/api/auth/register", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email, password, name }),
          credentials: "include",
        });

        if (!response.ok) {
          const error = await response.json();
          throw new Error(error.message);
        }

        const { user, accessToken } = await response.json();

        set({
          user,
          accessToken,
          isAuthenticated: true,
        });
      },

      logout: async () => {
        await fetch("/api/auth/logout", {
          method: "POST",
          credentials: "include",
        });

        set({
          user: null,
          accessToken: null,
          isAuthenticated: false,
        });
      },

      refresh: async () => {
        try {
          const response = await fetch("/api/auth/refresh", {
            method: "POST",
            credentials: "include",
          });

          if (response.ok) {
            const { accessToken } = await response.json();
            set({ accessToken });
          } else {
            // Refresh failed, log out
            set({
              user: null,
              accessToken: null,
              isAuthenticated: false,
            });
          }
        } catch (error) {
          console.error("Token refresh failed:", error);
        }
      },
    }),
    {
      name: "auth-storage",
      partialize: (state) => ({
        user: state.user,
        accessToken: state.accessToken,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
);

// Auto-refresh token before expiration
setInterval(() => {
  const { isAuthenticated, refresh } = useAuth.getState();
  if (isAuthenticated) {
    refresh();
  }
}, 10 * 60 * 1000); // Every 10 minutes
```

### Login Form Component

```typescript
// src/features/auth/components/LoginForm.tsx

import { useState } from "react";
import { useAuth } from "../hooks/useAuth";
import { useNavigate } from "react-router-dom";

export function LoginForm() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const login = useAuth((state) => state.login);
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      await login(email, password);
      navigate("/dashboard");
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label htmlFor="email" className="block text-sm font-medium">
          Email
        </label>
        <input
          id="email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          className="mt-1 block w-full rounded-md border px-3 py-2"
        />
      </div>

      <div>
        <label htmlFor="password" className="block text-sm font-medium">
          Password
        </label>
        <input
          id="password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          className="mt-1 block w-full rounded-md border px-3 py-2"
        />
      </div>

      {error && <div className="text-red-600 text-sm">{error}</div>}

      <button
        type="submit"
        disabled={loading}
        className="w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700 disabled:opacity-50"
      >
        {loading ? "Logging in..." : "Log In"}
      </button>
    </form>
  );
}
```

### Protected Route Component

```typescript
// src/components/ProtectedRoute.tsx

import { Navigate } from "react-router-dom";
import { useAuth } from "@/features/auth/hooks/useAuth";

interface ProtectedRouteProps {
  children: React.ReactNode;
}

export function ProtectedRoute({ children }: ProtectedRouteProps) {
  const isAuthenticated = useAuth((state) => state.isAuthenticated);

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
}
```

### Handoff to Testing Agent

**Files Created**:

- `src/features/auth/hooks/useAuth.ts`
- `src/features/auth/components/LoginForm.tsx`
- `src/features/auth/components/RegisterForm.tsx`
- `src/components/ProtectedRoute.tsx`

**Next Steps**:

1. Unit tests for AuthService
2. Integration tests for auth endpoints
3. E2E tests for login/register flows

---

## Summary

Este ejemplo demuestra:

✅ **Separación de responsabilidades** - Cada agente maneja su dominio
✅ **Handoff protocol** - Contexto claro entre agentes
✅ **Documentación continua** - ADRs, comentarios, ejemplos
✅ **Best practices** - Security, testing, error handling
✅ **Framework-agnostic** - Usa variables del proyecto

**Archivos totales creados**: ~15
**Tiempo estimado con agentes**: 4-6 horas
**Tiempo estimado manual**: 12-16 horas
**Reducción**: 60-70%
