# Guía: Migración de Monolito Django a Backend API + Frontend SPA

**Caso**: Django con templates + React embebido → Django REST API + Quasar/Vue SPA

**Duración estimada**: 12 semanas
**Estrategia**: Migración incremental sin downtime
**Workflow**: `monolith_to_spa_migration`

---

## 📊 Situación Actual vs Objetivo

### Estado Actual (Monolito)

```
┌─────────────────────────────────────────┐
│         Django Application              │
│                                         │
│  ┌──────────┐      ┌─────────────┐    │
│  │  Views   │─────▶│  Templates  │    │
│  │ (HTML)   │      │   (.html)   │    │
│  └──────────┘      └─────────────┘    │
│                                         │
│  ┌──────────────────────────┐          │
│  │  React Components        │          │
│  │  (embebidos en templates)│          │
│  │  ReactDOM.render(...)    │          │
│  └──────────────────────────┘          │
│                                         │
│  ┌──────────┐                           │
│  │  Models  │                           │
│  │   (ORM)  │                           │
│  └──────────┘                           │
└─────────────────────────────────────────┘
```

**Problemas**:

- ❌ Código mezclado (backend + frontend)
- ❌ Difícil de escalar
- ❌ No hay separación de responsabilidades
- ❌ Testing complicado
- ❌ Deployment monolítico

### Estado Objetivo (Arquitectura Separada)

```
┌──────────────────────┐         ┌──────────────────────┐
│   Backend (Django)   │         │  Frontend (Quasar)   │
│                      │         │                      │
│  ┌────────────────┐  │         │  ┌────────────────┐  │
│  │  REST API      │  │◀───────▶│  │  Vue SPA       │  │
│  │  (DRF)         │  │  JSON   │  │  Components    │  │
│  └────────────────┘  │         │  └────────────────┘  │
│                      │         │                      │
│  ┌────────────────┐  │         │  ┌────────────────┐  │
│  │  Serializers   │  │         │  │  Pinia Stores  │  │
│  └────────────────┘  │         │  └────────────────┘  │
│                      │         │                      │
│  ┌────────────────┐  │         │  ┌────────────────┐  │
│  │  Models (ORM)  │  │         │  │  API Client    │  │
│  └────────────────┘  │         │  └────────────────┘  │
│                      │         │                      │
│  ┌────────────────┐  │         │                      │
│  │  Auth (JWT)    │  │         │                      │
│  └────────────────┘  │         │                      │
└──────────────────────┘         └──────────────────────┘
        :5000                           :3000
```

**Beneficios**:

- ✅ Separación completa de responsabilidades
- ✅ Escalabilidad independiente
- ✅ Deploy independiente (frontend en CDN)
- ✅ Testing más fácil
- ✅ Mejor developer experience
- ✅ Reutilización del API (mobile, etc.)

---

## 🚀 Proceso de Migración (6 Fases)

### FASE 1: Análisis (Semana 1-2)

#### Paso 1.1: Análisis Arquitectónico

```bash
@architect-agent Analiza la arquitectura actual del monolito Django:
- Estructura de URLs y vistas
- Templates existentes
- Componentes React embebidos
- Modelos de base de datos
- Autenticación actual (sessions)

Crea:
- ADR para migración a SPA
- Diagrama de arquitectura actual vs objetivo
- Plan de migración por fases
- Análisis de riesgos
```

**Output esperado**:

```markdown
# ADR-020: Migración a Arquitectura Separada

## Decisión

Migrar de monolito Django con templates a arquitectura separada:

- Backend: Django REST Framework (API pura)
- Frontend: Quasar 2 + Vue 3 + TypeScript

## Estrategia

**Strangler Fig Pattern** - Migración incremental:

1. Mantener Django legacy funcionando
2. Crear API REST en paralelo
3. Crear SPA Quasar consumiendo API
4. Deployment dual con feature flags
5. Migración gradual por página/feature
6. Deprecar y eliminar código legacy

## Mapeo de Vistas a Endpoints

| Vista Django  | Template            | Endpoint API            | Componente Vue       |
| ------------- | ------------------- | ----------------------- | -------------------- |
| `user_list`   | `users/list.html`   | `GET /api/users/`       | `UserListPage.vue`   |
| `user_detail` | `users/detail.html` | `GET /api/users/:id/`   | `UserDetailPage.vue` |
| `login_view`  | `auth/login.html`   | `POST /api/auth/login/` | `LoginPage.vue`      |
| `dashboard`   | `dashboard.html`    | `GET /api/dashboard/`   | `DashboardPage.vue`  |

## Componentes React Embebidos

| Componente          | Ubicación         | Migración a Vue           |
| ------------------- | ----------------- | ------------------------- |
| `UserTable.jsx`     | `users/list.html` | `UserTable.vue` + q-table |
| `Chart.jsx`         | `dashboard.html`  | `Chart.vue` + ApexCharts  |
| `CommentWidget.jsx` | varios            | `CommentWidget.vue`       |
```

#### Paso 1.2: Inventario de Vistas

```bash
@backend-agent Crea inventario completo de vistas Django:
- Lista todas las vistas (function-based y class-based)
- Documenta URLs asociadas
- Identifica parámetros y contexto pasado a templates
- Mapea a futuros endpoints REST

Output: docs/migration/views-inventory.md
```

**Ejemplo de inventario**:

```python
# Vistas identificadas:

# auth/views.py
def login_view(request):
    """
    URL: /auth/login/
    Template: auth/login.html
    Context: {form, next_url}

    → API: POST /api/auth/login/
    → Frontend: LoginPage.vue
    """

def logout_view(request):
    """
    URL: /auth/logout/
    Template: None (redirect)

    → API: POST /api/auth/logout/
    → Frontend: Vuex action
    """

# users/views.py
class UserListView(ListView):
    """
    URL: /users/
    Template: users/list.html
    Context: {users, pagination}

    → API: GET /api/users/?page=1&page_size=20
    → Frontend: UserListPage.vue
    """
    model = User
    template_name = 'users/list.html'
    paginate_by = 20
```

#### Paso 1.3: Inventario de Templates

```bash
@frontend-agent Analiza templates Django existentes:
- Lista todos los .html templates
- Identifica componentes React embebidos (ReactDOM.render)
- Documenta static assets (CSS, JS, imágenes)
- Identifica lógica en templates ({% if %}, {% for %})

Output: docs/migration/templates-inventory.md
```

**Ejemplo**:

```django
<!-- users/list.html - ANTES -->
{% extends "base.html" %}
{% load static %}

{% block content %}
<div class="users-container">
  <h1>{{ title }}</h1>

  <!-- Componente React embebido -->
  <div id="user-table-root"></div>
  <script>
    ReactDOM.render(
      React.createElement(UserTable, {
        users: {{ users_json|safe }},
        onEdit: handleEdit
      }),
      document.getElementById('user-table-root')
    );
  </script>

  <!-- Paginación Django template -->
  {% if is_paginated %}
    <div class="pagination">
      {% if page_obj.has_previous %}
        <a href="?page={{ page_obj.previous_page_number }}">Previous</a>
      {% endif %}
      ...
    </div>
  {% endif %}
</div>
{% endblock %}
```

```vue
<!-- UserListPage.vue - DESPUÉS -->
<template>
  <q-page class="users-container">
    <h1>{{ title }}</h1>

    <!-- Componente Vue nativo -->
    <user-table :users="users" :loading="loading" @edit="handleEdit" />

    <!-- Paginación Quasar -->
    <q-pagination
      v-model="currentPage"
      :max="totalPages"
      @update:model-value="fetchUsers"
    />
  </q-page>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { api } from "@/services/api";
import UserTable from "@/components/UserTable.vue";

const users = ref([]);
const loading = ref(false);
const currentPage = ref(1);
const totalPages = ref(1);

async function fetchUsers() {
  loading.value = true;
  try {
    const response = await api.get("/api/users/", {
      params: { page: currentPage.value },
    });
    users.value = response.data.results;
    totalPages.value = Math.ceil(response.data.count / 20);
  } finally {
    loading.value = false;
  }
}

onMounted(fetchUsers);
</script>
```

---

### FASE 2: Backend API (Semana 3-5)

#### Paso 2.1: Setup Django REST Framework

```bash
@backend-agent Setup Django REST Framework en el proyecto:
- Instalar DRF
- Crear estructura api/
- Configurar settings
- Setup CORS

Mantener vistas legacy funcionando en paralelo
```

**Estructura del proyecto**:

```
myproject/
├── myapp/                    # App Django legacy
│   ├── views.py             # ✅ Mantener temporalmente
│   ├── urls.py              # ✅ Mantener
│   └── templates/           # ✅ Mantener
│
├── api/                      # ✅ NUEVO: API REST
│   ├── __init__.py
│   ├── serializers.py       # ✅ CREAR
│   ├── viewsets.py          # ✅ CREAR
│   ├── urls.py              # ✅ CREAR
│   ├── permissions.py       # ✅ CREAR
│   └── pagination.py        # ✅ CREAR
│
└── config/
    ├── settings.py          # ✅ ACTUALIZAR
    └── urls.py              # ✅ AGREGAR api/
```

**settings.py**:

```python
# settings.py - Agregar configuración DRF

INSTALLED_APPS = [
    # ... apps existentes
    'rest_framework',
    'corsheaders',
    'api',  # Nueva app API
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # CORS para SPA
    # ... middleware existente
]

# Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}

# CORS para desarrollo
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Quasar dev server
]

# JWT
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
}
```

#### Paso 2.2: Crear API Endpoints

```bash
@backend-agent Convierte vistas Django a API REST:

Por cada vista legacy:
1. Crear serializer para el modelo
2. Crear viewset REST
3. Agregar a urls API
4. Agregar tests

Ejemplo: user_list → GET /api/users/
```

**Ejemplo de conversión**:

**ANTES (Vista Django)**:

```python
# myapp/views.py
from django.views.generic import ListView
from .models import User

class UserListView(ListView):
    model = User
    template_name = 'users/list.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Users List'
        return context
```

**DESPUÉS (API REST)**:

```python
# api/serializers.py
from rest_framework import serializers
from myapp.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name',
                  'last_name', 'created_at', 'is_active']
        read_only_fields = ['id', 'created_at']

class UserDetailSerializer(UserSerializer):
    """Serializer con más detalles para vista individual"""
    posts_count = serializers.IntegerField(read_only=True)

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ['posts_count', 'bio']


# api/viewsets.py
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter,
                       filters.OrderingFilter]
    search_fields = ['username', 'email', 'first_name', 'last_name']
    filterset_fields = ['is_active']
    ordering_fields = ['created_at', 'username']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserDetailSerializer
        return UserSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == 'retrieve':
            queryset = queryset.annotate(posts_count=Count('posts'))
        return queryset


# api/urls.py
from rest_framework.routers import DefaultRouter
from .viewsets import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = router.urls
```

#### Paso 2.3: Autenticación JWT

```bash
@security-agent Implementa autenticación JWT:
- Configurar django-rest-framework-simplejwt
- Crear endpoints login/refresh/logout
- Migrar de sessions Django a JWT
- Mantener sessions temporalmente para legacy
```

```python
# api/views.py
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

class CustomTokenObtainPairView(TokenObtainPairView):
    """Login endpoint con información adicional"""

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            # Agregar info del usuario
            from .serializers import UserSerializer
            user = User.objects.get(username=request.data['username'])
            response.data['user'] = UserSerializer(user).data

        return response

@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """Registro de nuevos usuarios"""
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()
        # Generar tokens
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(user)

        return Response({
            'user': serializer.data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# api/urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import CustomTokenObtainPairView, register_view

urlpatterns = [
    path('auth/login/', CustomTokenObtainPairView.as_view()),
    path('auth/refresh/', TokenRefreshView.as_view()),
    path('auth/register/', register_view),
    # ... otros endpoints
]
```

---

### FASE 3: Frontend SPA (Semana 6-9)

#### Paso 3.1: Setup Quasar Project

```bash
@frontend-agent Crea proyecto Quasar 2 + Vue 3:
- Inicializar proyecto Quasar
- Configurar TypeScript
- Setup estructura de carpetas
- Configurar Pinia para state management
```

```bash
# Crear proyecto Quasar
npm init quasar

# Opciones:
# - App with Quasar CLI
# - Quasar v2
# - TypeScript
# - Pinia (state management)
# - ESLint + Prettier
# - Axios
```

**Estructura frontend**:

```
frontend/
├── src/
│   ├── assets/
│   ├── components/
│   │   ├── shared/           # Componentes reutilizables
│   │   └── features/         # Por feature
│   ├── layouts/
│   │   └── MainLayout.vue
│   ├── pages/
│   │   ├── auth/
│   │   │   ├── LoginPage.vue
│   │   │   └── RegisterPage.vue
│   │   ├── users/
│   │   │   ├── UserListPage.vue
│   │   │   └── UserDetailPage.vue
│   │   └── DashboardPage.vue
│   ├── router/
│   │   └── index.ts
│   ├── stores/
│   │   ├── auth.ts
│   │   └── users.ts
│   └── services/
│       ├── api.ts            # Axios instance
│       └── auth.ts           # Auth service
├── quasar.config.js
└── package.json
```

#### Paso 3.2: API Client Setup

```bash
@frontend-agent Setup cliente API con Axios:
- Configurar baseURL
- Interceptors para JWT
- Manejo de errores
- Refresh token automático
```

```typescript
// src/services/api.ts
import axios from "axios";
import { useAuthStore } from "@/stores/auth";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000/api",
  headers: {
    "Content-Type": "application/json",
  },
});

// Request interceptor: agregar JWT token
api.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore();
    if (authStore.accessToken) {
      config.headers.Authorization = `Bearer ${authStore.accessToken}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor: manejar refresh token
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // Si es error 401 y no hemos intentado refresh
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const authStore = useAuthStore();
        await authStore.refreshToken();

        // Reintentar request original con nuevo token
        originalRequest.headers.Authorization = `Bearer ${authStore.accessToken}`;
        return api(originalRequest);
      } catch (refreshError) {
        // Refresh falló, logout
        const authStore = useAuthStore();
        authStore.logout();
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export { api };

// src/stores/auth.ts
import { defineStore } from "pinia";
import { api } from "@/services/api";
import { Notify } from "quasar";

interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
}

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: null as User | null,
    accessToken: localStorage.getItem("access_token"),
    refreshToken: localStorage.getItem("refresh_token"),
  }),

  getters: {
    isAuthenticated: (state) => !!state.accessToken,
  },

  actions: {
    async login(username: string, password: string) {
      try {
        const response = await api.post("/auth/login/", {
          username,
          password,
        });

        this.user = response.data.user;
        this.accessToken = response.data.access;
        this.refreshToken = response.data.refresh;

        localStorage.setItem("access_token", this.accessToken!);
        localStorage.setItem("refresh_token", this.refreshToken!);

        Notify.create({
          type: "positive",
          message: "Login successful",
        });
      } catch (error) {
        Notify.create({
          type: "negative",
          message: "Login failed",
        });
        throw error;
      }
    },

    async refreshToken() {
      const response = await api.post("/auth/refresh/", {
        refresh: this.refreshToken,
      });

      this.accessToken = response.data.access;
      localStorage.setItem("access_token", this.accessToken!);
    },

    logout() {
      this.user = null;
      this.accessToken = null;
      this.refreshToken = null;
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
    },
  },
});
```

#### Paso 3.3: Migrar Templates a Vue

```bash
@frontend-agent Migra templates Django a componentes Vue:

Por cada template:
1. Analizar estructura HTML
2. Identificar datos dinámicos ({{ }}, {% %})
3. Crear componente Vue equivalente
4. Usar componentes Quasar (q-table, q-btn, etc.)
5. Conectar con API

Prioridad:
1. Login/Register
2. Dashboard
3. CRUD básicos
4. Features complejas
```

**Ejemplo completo de migración**:

```vue
<!-- src/pages/users/UserListPage.vue -->
<template>
  <q-page padding>
    <!-- Header con actions -->
    <div class="row items-center q-mb-md">
      <div class="col">
        <h4 class="q-ma-none">Users</h4>
      </div>
      <div class="col-auto">
        <q-btn
          color="primary"
          label="Add User"
          icon="add"
          @click="showAddDialog = true"
        />
      </div>
    </div>

    <!-- Search bar -->
    <q-input
      v-model="search"
      outlined
      placeholder="Search users..."
      debounce="500"
      @update:model-value="fetchUsers"
    >
      <template v-slot:prepend>
        <q-icon name="search" />
      </template>
    </q-input>

    <!-- Tabla con Quasar -->
    <q-table
      :rows="users"
      :columns="columns"
      :loading="loading"
      :pagination="pagination"
      @request="onRequest"
      row-key="id"
      class="q-mt-md"
    >
      <!-- Slot para columna de actions -->
      <template v-slot:body-cell-actions="props">
        <q-td :props="props">
          <q-btn flat dense round icon="edit" @click="editUser(props.row)" />
          <q-btn
            flat
            dense
            round
            icon="delete"
            color="negative"
            @click="confirmDelete(props.row)"
          />
        </q-td>
      </template>

      <!-- Slot para estado activo -->
      <template v-slot:body-cell-is_active="props">
        <q-td :props="props">
          <q-badge
            :color="props.row.is_active ? 'positive' : 'negative'"
            :label="props.row.is_active ? 'Active' : 'Inactive'"
          />
        </q-td>
      </template>
    </q-table>
  </q-page>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { api } from "@/services/api";
import { Notify, Dialog } from "quasar";

interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  is_active: boolean;
  created_at: string;
}

// State
const users = ref<User[]>([]);
const loading = ref(false);
const search = ref("");
const pagination = ref({
  page: 1,
  rowsPerPage: 20,
  rowsNumber: 0,
});

// Definición de columnas
const columns = [
  {
    name: "username",
    label: "Username",
    field: "username",
    align: "left",
    sortable: true,
  },
  {
    name: "email",
    label: "Email",
    field: "email",
    align: "left",
    sortable: true,
  },
  {
    name: "name",
    label: "Name",
    field: (row: User) => `${row.first_name} ${row.last_name}`,
    align: "left",
  },
  {
    name: "is_active",
    label: "Status",
    field: "is_active",
    align: "center",
  },
  {
    name: "actions",
    label: "Actions",
    field: "actions",
    align: "center",
  },
];

// Fetch users
async function fetchUsers() {
  loading.value = true;
  try {
    const response = await api.get("/users/", {
      params: {
        page: pagination.value.page,
        page_size: pagination.value.rowsPerPage,
        search: search.value,
      },
    });

    users.value = response.data.results;
    pagination.value.rowsNumber = response.data.count;
  } catch (error) {
    Notify.create({
      type: "negative",
      message: "Failed to load users",
    });
  } finally {
    loading.value = false;
  }
}

// Handler de paginación
function onRequest(props: any) {
  pagination.value.page = props.pagination.page;
  pagination.value.rowsPerPage = props.pagination.rowsPerPage;
  fetchUsers();
}

// Actions
function editUser(user: User) {
  // Navigate to edit page
  router.push(`/users/${user.id}/edit`);
}

function confirmDelete(user: User) {
  Dialog.create({
    title: "Confirm",
    message: `Delete user ${user.username}?`,
    cancel: true,
  }).onOk(async () => {
    try {
      await api.delete(`/users/${user.id}/`);
      Notify.create({
        type: "positive",
        message: "User deleted",
      });
      fetchUsers();
    } catch (error) {
      Notify.create({
        type: "negative",
        message: "Failed to delete user",
      });
    }
  });
}

onMounted(() => {
  fetchUsers();
});
</script>
```

---

### FASE 4: Deployment Dual (Semana 10)

```bash
@devops-agent Setup deployment dual:
- Configurar Nginx para servir ambas apps
- Feature flags para rollout gradual
- Monitoring de ambas versiones
```

**Nginx config**:

```nginx
# nginx.conf - Deployment dual
server {
    listen 80;
    server_name myapp.com;

    # API Django (compartida por ambas versiones)
    location /api/ {
        proxy_pass http://django:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Admin Django (legacy)
    location /admin/ {
        proxy_pass http://django:8000;
    }

    # SPA Quasar (NUEVO)
    location /app/ {
        alias /var/www/frontend-vue/dist/;
        try_files $uri $uri/ /app/index.html;
    }

    # Legacy Django templates (temporal)
    location / {
        proxy_pass http://django:8000;
    }
}
```

---

### FASE 5: Cutover Gradual (Semana 11)

```bash
@devops-agent Implementa rollout gradual:
- 10% usuarios → SPA
- 25% usuarios → SPA
- 50% usuarios → SPA
- 100% usuarios → SPA
```

---

### FASE 6: Cleanup (Semana 12)

```bash
@backend-agent Elimina código legacy:
- Remover templates
- Remover vistas Django (excepto admin)
- Limpiar dependencias
- Actualizar docs
```

---

## ✅ Checklist de Migración

### Backend

- [ ] DRF instalado y configurado
- [ ] Todos los modelos tienen serializers
- [ ] Todas las vistas convertidas a viewsets
- [ ] JWT authentication funcionando
- [ ] CORS configurado
- [ ] Tests API al 80%+ coverage
- [ ] OpenAPI docs generadas

### Frontend

- [ ] Quasar project inicializado
- [ ] Pinia stores creados
- [ ] API client configurado
- [ ] Todos los templates migrados a Vue
- [ ] Routing configurado
- [ ] Autenticación funcionando
- [ ] Tests E2E para flujos críticos

### DevOps

- [ ] Deployment dual funcionando
- [ ] Feature flags implementados
- [ ] Monitoring configurado
- [ ] Rollback plan probado

### Documentation

- [ ] API docs actualizadas
- [ ] Frontend docs actualizadas
- [ ] Migration guide creada
- [ ] Runbooks actualizados

---

## 🎯 Comandos Prácticos

```bash
# FASE 1: Análisis
@architect-agent Analiza monolito Django actual y crea plan de migración

# FASE 2: Backend API
@backend-agent Convierte UserListView a API endpoint
@security-agent Implementa JWT authentication

# FASE 3: Frontend SPA
@frontend-agent Migra users/list.html a UserListPage.vue
@frontend-agent Crea Pinia store para users

# FASE 4: Testing
@testing-agent Crea tests E2E comparando legacy vs SPA
@testing-agent Valida feature parity

# FASE 5: Deployment
@devops-agent Setup deployment dual con Nginx
@devops-agent Implementa feature flags para rollout gradual

# FASE 6: Cleanup
@backend-agent Elimina templates y vistas legacy
@documentation-agent Actualiza toda la documentación
```

---

**Duración total**: 12 semanas
**Reducción vs manual**: 60-70%
**Sin downtime**: ✅ Migración incremental
**Rollback**: ✅ En cualquier momento
