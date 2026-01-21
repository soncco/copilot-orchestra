# ADR-0001: Django REST Framework para API Backend

**Fecha**: 2026-01-20
**Status**: ✅ Accepted
**Decisor**: Architect Agent

---

## Contexto

TravesIA requiere una API REST robusta para gestionar operaciones de turismo (grupos, itinerarios, proveedores, finanzas). El backend debe:

- Soportar autenticación JWT con MFA
- Proporcionar serialización y validación de datos
- Generar documentación automática (OpenAPI/Swagger)
- Manejar permisos granulares (RBAC)
- Integrar nativamente con Django ORM

---

## Decisión

**Usaremos Django REST Framework (DRF) para construir la API REST.**

---

## Alternativas Consideradas

### Opción 1: FastAPI

**Pros**:

- Performance superior (async/await nativo)
- Documentación OpenAPI automática
- Type hints nativos (Pydantic)
- Más moderno y ligero

**Contras**:

- Ecosystem menos maduro que Django
- Requiere SQLAlchemy en lugar de Django ORM
- Menos bibliotecas de terceros
- Equipo menos familiarizado

### Opción 2: Flask + Flask-RESTful

**Pros**:

- Más ligero que Django
- Flexible y minimalista
- Amplio ecosystem

**Contras**:

- Requiere más configuración manual
- Sin admin panel out-of-the-box
- Menos features empresariales
- Autenticación requiere más trabajo

### Opción 3: Django REST Framework (Seleccionada)

**Pros**:

- Integración perfecta con Django
- Admin panel para gestión rápida
- Browsable API para desarrollo
- JWT authentication con django-rest-framework-simplejwt
- Amplio ecosystem de plugins
- Serializers con validación robusta
- Generación automática OpenAPI

**Contras**:

- Más pesado que FastAPI
- Performance ligeramente inferior
- Async support limitado (mejorando en Django 4+)

---

## Justificación

1. **Django ORM**: Ya decidido en project-context.md, DRF es la opción natural
2. **Admin Panel**: Acelera desarrollo permitiendo gestión manual cuando sea necesario
3. **Madurez**: Framework probado en producción con millones de usuarios
4. **Documentación**: Documentación exhaustiva y comunidad activa
5. **Ecosystem**: Amplia variedad de paquetes de terceros (django-filter, drf-spectacular, etc.)
6. **Performance**: Suficiente para los 50 grupos/año esperados (no es bottleneck)

---

## Consecuencias

### Positivas ✅

- Desarrollo más rápido gracias a features out-of-the-box
- Admin panel para operaciones manuales de emergencia
- Browsable API facilita testing y debugging
- Documentación automática con drf-spectacular
- Autenticación JWT con MFA implementable fácilmente

### Negativas ⚠️

- Performance no tan alta como FastAPI (aceptable para volumen esperado)
- Async support limitado (no crítico para este proyecto)
- Footprint más grande que alternativas minimalistas

### Riesgos y Mitigaciones

| Riesgo                   | Probabilidad | Impacto | Mitigación                                       |
| ------------------------ | ------------ | ------- | ------------------------------------------------ |
| Performance insuficiente | Baja         | Medio   | Implementar caching con Redis, optimizar queries |
| Curva de aprendizaje     | Baja         | Bajo    | Documentación exhaustiva disponible              |

---

## Implementación

### Paquetes Principales

```python
# requirements.txt
Django==5.0
djangorestframework==3.14
djangorestframework-simplejwt==5.3
drf-spectacular==0.27  # OpenAPI/Swagger
django-filter==23.5
django-cors-headers==4.3
```

### Configuración Base

```python
# settings.py
INSTALLED_APPS = [
    'rest_framework',
    'rest_framework_simplejwt',
    'drf_spectacular',
    'django_filters',
    'corsheaders',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.OrderingFilter',
        'rest_framework.filters.SearchFilter',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
}
```

---

## Referencias

- [Django REST Framework Documentation](https://www.django-rest-framework.org/)
- [JWT Authentication Best Practices](https://jwt.io/introduction)
- [drf-spectacular Documentation](https://drf-spectacular.readthedocs.io/)

---

**Revisión**: Pendiente
**Próxima Revisión**: 2026-07-20 (6 meses)
