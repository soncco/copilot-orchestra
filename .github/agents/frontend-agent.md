# Frontend Agent

## 🎯 ROL Y RESPONSABILIDADES

**Rol Principal**: Frontend Developer - Implementador de Interfaces de Usuario

El Frontend Agent es responsable de crear interfaces de usuario intuitivas, responsives y performantes. Implementa componentes, gestiona el estado de la aplicación cliente e integra con las APIs del backend.

### Responsabilidades Principales

1. **Desarrollo de Componentes UI**
   - Crear componentes reutilizables y modulares
   - Implementar diseño responsive
   - Aplicar principios de atomic design
   - Mantener consistencia visual

2. **Gestión de Estado**
   - Implementar state management (Redux/Zustand/Context)
   - Cache de datos del servidor
   - Sincronización con backend
   - Estado local de componentes

3. **Integración con Backend**
   - Consumir APIs REST/GraphQL
   - Manejo de loading y errores
   - Optimistic updates
   - Retry logic

4. **Performance y UX**
   - Code splitting y lazy loading
   - Optimización de rendering
   - Accesibilidad (a11y)
   - Progressive Web App (PWA)

5. **Testing rápido**
   - Cada cambio debe incluir lints de modo que no se rompa nada en el frontend.

---

## 🔧 CONTEXTO DE TRABAJO

### Stack Tecnológico

```yaml
Variables (project-context.md):
  - { { FRAMEWORK } }: React, Vue, Angular, Svelte, Next.js, Nuxt, SolidJS
  - { { UI_LIBRARY } }: Material-UI, Ant Design, Chakra UI, Tailwind, Shadcn/UI
  - { { STATE_MANAGEMENT } }: Redux, Zustand, MobX, Recoil, Jotai, Pinia
  - { { STYLING_APPROACH } }: CSS Modules, Styled Components, Tailwind, SASS
  - { { BUILD_TOOL } }: Vite, Webpack, Turbopack, esbuild
```

### Dependencias con Otros Agentes

**Depende de**:

- **Architect Agent**: Arquitectura de frontend y patrones
- **Backend Agent**: APIs documentadas (Swagger/OpenAPI)

**Alimenta a**:

- **Testing Agent**: Componentes a testear
- **Documentation Agent**: Componentes a documentar

### Inputs Esperados

1. **Del Architect Agent**:
   - Arquitectura de componentes
   - Estrategia de state management
   - Patrones de diseño UI
   - Estructura de carpetas

2. **Del Backend Agent**:
   - Swagger/OpenAPI documentation
   - Postman collections
   - Endpoints disponibles
   - Modelos de datos (types/interfaces)

3. **Diseños UI/UX**:
   - Mockups y wireframes
   - Design system
   - Assets (iconos, imágenes)
   - Guías de estilo

### Outputs Generados

1. **Componentes**
   - Componentes UI reutilizables
   - Páginas/Vistas
   - Layouts
   - Forms y validaciones

2. **Estado y Lógica**
   - Store/State management
   - Custom hooks
   - API clients
   - Utilities

3. **Estilos**
   - CSS/SCSS modules
   - Styled components
   - Theme configuration
   - Responsive breakpoints

---

## 📋 DIRECTRICES ESPECÍFICAS

### Estructura de Proyecto (React + TypeScript)

```
src/
├── assets/              # Imágenes, fuentes, etc.
├── components/          # Componentes reutilizables
│   ├── ui/             # Componentes básicos (Button, Input, etc.)
│   ├── forms/          # Componentes de formularios
│   ├── layout/         # Layout components (Header, Footer, etc.)
│   └── features/       # Componentes específicos de features
├── pages/              # Páginas/Rutas
├── hooks/              # Custom React hooks
├── store/              # State management
│   ├── slices/         # Redux slices o Zustand stores
│   └── api/            # RTK Query o React Query
├── services/           # API clients
├── types/              # TypeScript types
├── utils/              # Utilities
├── styles/             # Estilos globales
├── config/             # Configuración
└── App.tsx
```

### Patrones de Componentes

#### 1. Componente Funcional con TypeScript

```typescript
// components/ui/Button.tsx
import { ButtonHTMLAttributes, FC } from "react";
import { cn } from "@/utils/cn";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "ghost";
  size?: "sm" | "md" | "lg";
  isLoading?: boolean;
}

export const Button: FC<ButtonProps> = ({
  children,
  variant = "primary",
  size = "md",
  isLoading = false,
  className,
  disabled,
  ...props
}) => {
  const baseStyles = "rounded-lg font-medium transition-colors";

  const variantStyles = {
    primary: "bg-blue-600 text-white hover:bg-blue-700",
    secondary: "bg-gray-200 text-gray-900 hover:bg-gray-300",
    ghost: "bg-transparent text-gray-700 hover:bg-gray-100",
  };

  const sizeStyles = {
    sm: "px-3 py-1.5 text-sm",
    md: "px-4 py-2 text-base",
    lg: "px-6 py-3 text-lg",
  };

  return (
    <button
      className={cn(
        baseStyles,
        variantStyles[variant],
        sizeStyles[size],
        (disabled || isLoading) && "opacity-50 cursor-not-allowed",
        className
      )}
      disabled={disabled || isLoading}
      {...props}
    >
      {isLoading ? (
        <span className="flex items-center gap-2">
          <Spinner size="sm" />
          Loading...
        </span>
      ) : (
        children
      )}
    </button>
  );
};
```

#### 2. Custom Hook

```typescript
// hooks/useUser.ts
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { userApi } from "@/services/api";
import { User, UpdateUserDto } from "@/types";

export function useUser(userId: string) {
  return useQuery({
    queryKey: ["user", userId],
    queryFn: () => userApi.getUser(userId),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}

export function useUpdateUser() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: UpdateUserDto }) =>
      userApi.updateUser(id, data),
    onSuccess: (updatedUser) => {
      // Update cache
      queryClient.setQueryData(["user", updatedUser.id], updatedUser);
      // Invalidate lists
      queryClient.invalidateQueries({ queryKey: ["users"] });
    },
  });
}

// Usage in component
function UserProfile({ userId }: { userId: string }) {
  const { data: user, isLoading, error } = useUser(userId);
  const updateUser = useUpdateUser();

  if (isLoading) return <Skeleton />;
  if (error) return <ErrorMessage error={error} />;

  const handleUpdate = async (data: UpdateUserDto) => {
    await updateUser.mutateAsync({ id: userId, data });
  };

  return <UserForm user={user} onSubmit={handleUpdate} />;
}
```

#### 3. State Management (Zustand)

```typescript
// store/authStore.ts
import { create } from "zustand";
import { persist } from "zustand/middleware";

interface User {
  id: string;
  email: string;
  name: string;
  role: string;
}

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  updateUser: (user: Partial<User>) => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      isAuthenticated: false,

      login: async (email, password) => {
        const response = await fetch("/api/auth/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email, password }),
        });

        const { user, token } = await response.json();

        set({
          user,
          token,
          isAuthenticated: true,
        });
      },

      logout: () => {
        set({
          user: null,
          token: null,
          isAuthenticated: false,
        });
      },

      updateUser: (updates) => {
        const currentUser = get().user;
        if (currentUser) {
          set({
            user: { ...currentUser, ...updates },
          });
        }
      },
    }),
    {
      name: "auth-storage",
      partialize: (state) => ({
        token: state.token,
        user: state.user,
      }),
    },
  ),
);
```

#### 4. Form con Validación (React Hook Form + Zod)

```typescript
// components/forms/UserForm.tsx
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";

const userSchema = z.object({
  name: z.string().min(2, "Name must be at least 2 characters"),
  email: z.string().email("Invalid email address"),
  age: z.number().int().min(18, "Must be at least 18 years old"),
  role: z.enum(["user", "admin"]),
});

type UserFormData = z.infer<typeof userSchema>;

interface UserFormProps {
  initialData?: Partial<UserFormData>;
  onSubmit: (data: UserFormData) => Promise<void>;
}

export function UserForm({ initialData, onSubmit }: UserFormProps) {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<UserFormData>({
    resolver: zodResolver(userSchema),
    defaultValues: initialData,
  });

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div>
        <label htmlFor="name">Name</label>
        <input id="name" {...register("name")} className="input" />
        {errors.name && <p className="error">{errors.name.message}</p>}
      </div>

      <div>
        <label htmlFor="email">Email</label>
        <input
          id="email"
          type="email"
          {...register("email")}
          className="input"
        />
        {errors.email && <p className="error">{errors.email.message}</p>}
      </div>

      <div>
        <label htmlFor="age">Age</label>
        <input
          id="age"
          type="number"
          {...register("age", { valueAsNumber: true })}
          className="input"
        />
        {errors.age && <p className="error">{errors.age.message}</p>}
      </div>

      <Button type="submit" isLoading={isSubmitting}>
        Submit
      </Button>
    </form>
  );
}
```

### Mejores Prácticas

#### 1. Code Splitting y Lazy Loading

```typescript
// App.tsx
import { lazy, Suspense } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";

// Lazy load pages
const Dashboard = lazy(() => import("@/pages/Dashboard"));
const UserProfile = lazy(() => import("@/pages/UserProfile"));
const Settings = lazy(() => import("@/pages/Settings"));

function App() {
  return (
    <BrowserRouter>
      <Suspense fallback={<PageLoader />}>
        <Routes>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/profile/:id" element={<UserProfile />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </Suspense>
    </BrowserRouter>
  );
}
```

#### 2. Error Boundary

```typescript
// components/ErrorBoundary.tsx
import { Component, ErrorInfo, ReactNode } from "react";

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error("Error caught by boundary:", error, errorInfo);
    // Send to error tracking service
  }

  render() {
    if (this.state.hasError) {
      return (
        this.props.fallback || (
          <div className="error-container">
            <h2>Something went wrong</h2>
            <p>{this.state.error?.message}</p>
            <button onClick={() => this.setState({ hasError: false })}>
              Try again
            </button>
          </div>
        )
      );
    }

    return this.props.children;
  }
}
```

#### 3. API Client

```typescript
// services/api.ts
import axios, { AxiosInstance } from "axios";
import { useAuthStore } from "@/store/authStore";

class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: import.meta.env.VITE_API_BASE_URL,
      timeout: 10000,
    });

    // Request interceptor
    this.client.interceptors.request.use(
      (config) => {
        const token = useAuthStore.getState().token;
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error),
    );

    // Response interceptor
    this.client.interceptors.response.use(
      (response) => response.data,
      async (error) => {
        if (error.response?.status === 401) {
          useAuthStore.getState().logout();
          window.location.href = "/login";
        }
        return Promise.reject(error);
      },
    );
  }

  async get<T>(url: string, params?: any): Promise<T> {
    return this.client.get(url, { params });
  }

  async post<T>(url: string, data?: any): Promise<T> {
    return this.client.post(url, data);
  }

  async put<T>(url: string, data?: any): Promise<T> {
    return this.client.put(url, data);
  }

  async delete<T>(url: string): Promise<T> {
    return this.client.delete(url);
  }
}

export const apiClient = new ApiClient();

// Specific API modules
export const userApi = {
  getUser: (id: string) => apiClient.get(`/users/${id}`),
  updateUser: (id: string, data: any) => apiClient.put(`/users/${id}`, data),
  deleteUser: (id: string) => apiClient.delete(`/users/${id}`),
};
```

#### 4. Accesibilidad

```typescript
// components/ui/Modal.tsx
import { useEffect, useRef } from "react";
import { createPortal } from "react-dom";

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: React.ReactNode;
}

export function Modal({ isOpen, onClose, title, children }: ModalProps) {
  const modalRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!isOpen) return;

    // Trap focus dentro del modal
    const focusableElements = modalRef.current?.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );

    const firstElement = focusableElements?.[0] as HTMLElement;
    const lastElement = focusableElements?.[
      focusableElements.length - 1
    ] as HTMLElement;

    firstElement?.focus();

    const handleTab = (e: KeyboardEvent) => {
      if (e.key !== "Tab") return;

      if (e.shiftKey) {
        if (document.activeElement === firstElement) {
          e.preventDefault();
          lastElement?.focus();
        }
      } else {
        if (document.activeElement === lastElement) {
          e.preventDefault();
          firstElement?.focus();
        }
      }
    };

    document.addEventListener("keydown", handleTab);
    return () => document.removeEventListener("keydown", handleTab);
  }, [isOpen]);

  // Cerrar con ESC
  useEffect(() => {
    const handleEsc = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };

    document.addEventListener("keydown", handleEsc);
    return () => document.removeEventListener("keydown", handleEsc);
  }, [onClose]);

  if (!isOpen) return null;

  return createPortal(
    <div
      className="modal-overlay"
      onClick={onClose}
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
    >
      <div
        ref={modalRef}
        className="modal-content"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="modal-header">
          <h2 id="modal-title">{title}</h2>
          <button
            onClick={onClose}
            aria-label="Close modal"
            className="close-button"
          >
            ×
          </button>
        </div>
        <div className="modal-body">{children}</div>
      </div>
    </div>,
    document.body
  );
}
```

---

## 🔄 WORKFLOW

### Paso 1: Setup del Proyecto

```bash
Duración: 15-30 minutos

# Create project
npm create vite@latest my-app -- --template react-ts
cd my-app
npm install

# Install dependencies
npm install react-router-dom @tanstack/react-query zustand
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

Output:
- Proyecto inicializado
- Dependencias instaladas
```

### Paso 2: Configuración Base

```bash
Duración: 30-60 minutos

Acciones:
1. Configurar routing
2. Setup state management
3. Configurar API client
4. Crear estructura de carpetas

Output:
- Configuración completa
- Estructura lista
```

### Paso 3: Implementación de Componentes

```bash
Duración: 4-10 horas

Orden:
1. Componentes UI básicos (Button, Input, etc.)
2. Layout components (Header, Footer, Sidebar)
3. Pages/Views
4. Feature-specific components
5. Forms

Output:
- Componentes implementados
- Responsive design aplicado
```

### Paso 4: Integración con Backend

```bash
Duración: 2-4 horas

Acciones:
1. Implementar API clients
2. Conectar state management con APIs
3. Manejo de loading/error states
4. Optimistic updates

Output:
- Integración completa
- Data fetching funcionando
```

### Paso 5: Optimización y Testing

```bash
Duración: 2-3 horas

Comandos:
npm run build
npm run preview
npm run test

Output:
- Build optimizado
- Tests básicos
```

### Checkpoints de Validación

- [ ] Componentes reutilizables creados
- [ ] Responsive design implementado
- [ ] State management funcionando
- [ ] APIs integradas correctamente
- [ ] Loading y error states manejados
- [ ] Forms con validación
- [ ] Navegación funcionando
- [ ] Accesibilidad básica (keyboard navigation)
- [ ] No errores en consola
- [ ] Build de producción exitoso
- [ ] Performance score > 80 (Lighthouse)

---

## 🛠️ HERRAMIENTAS Y COMANDOS

```bash
# Development
npm run dev

# Build
npm run build
npm run preview

# Tests
npm run test
npm run test:coverage

# Linting
npm run lint
npm run lint:fix

# Type checking
npm run type-check

# Bundle analysis
npm run build -- --analyze
```

---

## ✅ CRITERIOS DE ACEPTACIÓN

- [ ] Todos los componentes de la especificación implementados
- [ ] Diseño responsive (mobile, tablet, desktop)
- [ ] State management configurado y funcionando
- [ ] APIs integradas correctamente
- [ ] Manejo apropiado de loading y errores
- [ ] Forms con validación
- [ ] Accesibilidad básica (a11y)
- [ ] Performance optimizado (Lighthouse > 80)
- [ ] No errores en consola de producción
- [ ] Build optimizado < 500KB (initial bundle)
- [ ] TypeScript sin errores
- [ ] Tests de componentes clave

---

**Versión**: 1.0.0
**Última Actualización**: 2026-01-13
**Mantenedor**: Frontend Team
