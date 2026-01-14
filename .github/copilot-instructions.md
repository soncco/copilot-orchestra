# GitHub Copilot - Instrucciones Globales del Proyecto

## Contexto General del Sistema

Este es un sistema de orquestación multi-agente diseñado para el desarrollo de proyectos SaaS. Cada agente tiene responsabilidades específicas y trabaja de forma coordinada siguiendo workflows predefinidos.

## Principios Fundamentales

### 1. Modularidad y Separación de Responsabilidades

- Cada agente es independiente y tiene un ámbito de acción claramente definido
- No mezclar responsabilidades entre agentes
- Respetar los límites de cada dominio

### 2. Intercambiabilidad de Tecnologías

- El sistema está diseñado para soportar múltiples stacks tecnológicos
- Utilizar siempre las variables de configuración definidas en `project-context.md`
- No hardcodear frameworks o tecnologías específicas sin verificar el contexto

### 3. Documentación Continua

- Cada cambio debe estar documentado
- Actualizar documentación antes de implementar
- Mantener sincronizados código y documentación

## Workflow de Desarrollo

### Al Implementar una Nueva Feature

1. **Consultar al Architect Agent** para validar el diseño
2. **Backend Agent** implementa la lógica de negocio
3. **Database Agent** maneja cambios en el modelo de datos
4. **Frontend Agent** implementa la UI
5. **Testing Agent** crea los tests correspondientes
6. **Security Agent** audita los cambios
7. **Code Review Agent** revisa la calidad
8. **Documentation Agent** actualiza la documentación
9. **DevOps Agent** prepara el deployment

### Al Corregir un Bug

1. **Testing Agent** reproduce y documenta el bug
2. **Agente responsable** (Backend/Frontend/etc) corrige el issue
3. **Testing Agent** verifica la corrección
4. **Code Review Agent** revisa el fix
5. **DevOps Agent** despliega si es crítico

### Al Hacer Refactoring

1. **Architect Agent** propone y valida el cambio
2. **Code Review Agent** identifica áreas de mejora
3. **Agente responsable** implementa el refactor
4. **Testing Agent** asegura que no hay regresiones
5. **Documentation Agent** actualiza docs técnicas

## Variables de Contexto

Siempre consultar `project-context.md` para obtener:

- `{{FRAMEWORK}}` - Framework frontend
- `{{BACKEND_STACK}}` - Stack backend
- `{{DATABASE}}` - Sistema de base de datos
- `{{CLOUD_PROVIDER}}` - Proveedor cloud
- `{{AUTH_METHOD}}` - Método de autenticación
- `{{DEPLOYMENT_STRATEGY}}` - Estrategia de despliegue

## Estándares de Código

### Convenciones de Nombres

- **Variables**: camelCase para JavaScript/TypeScript, snake_case para Python
- **Funciones**: verbos descriptivos (getUserById, processPayment)
- **Clases**: PascalCase (UserService, PaymentProcessor)
- **Constantes**: UPPER_SNAKE_CASE (MAX_RETRIES, API_ENDPOINT)

### Estructura de Archivos

```
src/
├── features/           # Organización por feature
│   ├── auth/
│   ├── users/
│   └── payments/
├── shared/            # Código compartido
│   ├── components/
│   ├── utils/
│   └── types/
└── infrastructure/    # Configuración y setup
```

### Gestión de Errores

- Siempre usar try-catch en operaciones asíncronas
- Logging estructurado con niveles apropiados
- Mensajes de error claros y accionables
- No exponer detalles de implementación en producción

### Tests

- Cobertura mínima: 80%
- Tests unitarios para lógica de negocio
- Tests de integración para APIs
- Tests E2E para flujos críticos

## Protocolo de Comunicación entre Agentes

### Handoff de Contexto

Cuando un agente completa su trabajo y pasa a otro:

```markdown
## Handoff a [AGENTE_DESTINO]

**Completado por**: [AGENTE_ORIGEN]
**Fecha**: [TIMESTAMP]
**Archivos modificados**: [LISTA]
**Dependencias nuevas**: [LISTA]
**Configuraciones cambiadas**: [LISTA]
**Próximos pasos**: [ACCIONES]
**Notas especiales**: [CONSIDERACIONES]
```

### Checkpoints de Validación

Cada agente debe validar antes de continuar:

- ✅ Código compila/ejecuta sin errores
- ✅ Tests pasan exitosamente
- ✅ Linter no reporta warnings críticos
- ✅ Documentación actualizada
- ✅ No hay secretos o credenciales hardcodeadas

## Comandos y Automatización

### Validación Rápida

```bash
# Verificar estado del proyecto
npm run validate        # o python validate.py
npm run test           # Ejecutar suite de tests
npm run lint           # Verificar estilo
npm run type-check     # Verificar tipos (TypeScript)
```

### Pre-commit Hooks

- Formato automático de código
- Validación de commits convencionales
- Ejecución de tests afectados
- Verificación de secretos

## Seguridad

### Reglas No Negociables

- ❌ No commits de secretos, API keys o credenciales
- ❌ No deshabilitar validaciones de seguridad
- ❌ No SQL injection vulnerable code
- ❌ No exponer endpoints sin autenticación
- ✅ Siempre sanitizar inputs de usuario
- ✅ Usar HTTPS en producción
- ✅ Implementar rate limiting
- ✅ Validar y escapar outputs

## Patrones Recomendados

### Arquitectura

- **Repository Pattern** para acceso a datos
- **Service Layer** para lógica de negocio
- **Dependency Injection** para testing
- **Factory Pattern** para creación de objetos complejos

### APIs REST

- Usar verbos HTTP correctamente (GET, POST, PUT, DELETE, PATCH)
- Códigos de estado apropiados (200, 201, 400, 401, 404, 500)
- Versionado de APIs (/api/v1/)
- Paginación para listas grandes

### Estado y Cache

- Inmutabilidad donde sea posible
- Cache en múltiples niveles (browser, CDN, server, DB)
- Invalidación de cache clara y predecible

## Anti-Patrones a Evitar

- ❌ God Objects/Classes omnipotentes
- ❌ Callback Hell / Promises anidadas
- ❌ Código duplicado (DRY principle)
- ❌ Funciones de más de 50 líneas
- ❌ Acoplamiento tight entre módulos
- ❌ Variables globales
- ❌ Mutación de parámetros de función

## Optimización de Performance

### Frontend

- Code splitting y lazy loading
- Optimización de imágenes
- Minimización de re-renders
- Debouncing/Throttling de eventos

### Backend

- Query optimization (N+1 problem)
- Connection pooling
- Caching estratégico
- Procesamiento asíncrono de tareas pesadas

### Base de Datos

- Índices apropiados
- Denormalización cuando sea necesario
- Particionamiento de tablas grandes
- Query analysis y optimization

## Accesibilidad y UX

- Cumplir con WCAG 2.1 nivel AA
- Diseño responsive (mobile-first)
- Tiempos de carga < 3 segundos
- Estados de loading claros
- Mensajes de error útiles

## Versionado y Releases

### Semantic Versioning

- MAJOR.MINOR.PATCH
- MAJOR: Breaking changes
- MINOR: Nuevas features backward-compatible
- PATCH: Bug fixes

### Conventional Commits

```
feat: nueva funcionalidad
fix: corrección de bug
docs: cambios en documentación
style: formato, punto y coma faltante, etc
refactor: refactorización de código
test: adición de tests
chore: actualización de build tasks, configs, etc
```

## Recursos y Referencias

- **Configuración central**: `agents-config.json`
- **Contexto del proyecto**: `project-context.md`
- **Guía de contribución**: `CONTRIBUTING.md`
- **Agentes disponibles**: `.github/agents/`

## Notas Finales

Este sistema es una plantilla reutilizable. Cada proyecto nuevo debe:

1. Copiar esta estructura base
2. Actualizar `project-context.md` con las tecnologías específicas
3. Ajustar `agents-config.json` según necesidades
4. Mantener la separación de responsabilidades entre agentes
5. Documentar cualquier desviación de los estándares

**Última actualización**: Enero 2026
**Versión del sistema**: 1.0.0
