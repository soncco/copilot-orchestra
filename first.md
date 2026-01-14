# CONTEXTO DEL PROYECTO

Estoy construyendo un sistema base de orquestación multi-agente reutilizable para desarrollo de proyectos SaaS. Este sistema será la plantilla inicial para múltiples proyectos futuros, donde solo cambiaremos el framework/plataforma específico.

# OBJETIVO

Crear la estructura completa de archivos y configuraciones para orquestar agentes de desarrollo, donde cada agente tiene responsabilidades específicas en el ciclo de vida del software.

# ESTRUCTURA REQUERIDA

## 1. Archivos de Configuración Base

Genera los siguientes archivos en la raíz del proyecto:

- `.github/copilot-instructions.md` - Instrucciones globales para Copilot
- `.github/agents/` - Directorio para definiciones de agentes
- `agents-config.json` - Configuración central de orquestación
- `project-context.md` - Contexto compartido entre agentes
- `.copilot/agents.yml` - Definición de agentes y sus roles

## 2. Agentes Necesarios

Crea definiciones individuales para cada agente en `.github/agents/`:

### Agentes Core:

1. **architect-agent.md** - Diseño de arquitectura, decisiones técnicas, patrones
2. **backend-agent.md** - Desarrollo de APIs, lógica de negocio, base de datos
3. **frontend-agent.md** - UI/UX, componentes, estado cliente
4. **devops-agent.md** - CI/CD, infraestructura, deployment, contenedores
5. **security-agent.md** - Auditoría de seguridad, vulnerabilidades, best practices
6. **testing-agent.md** - Tests unitarios, integración, E2E
7. **documentation-agent.md** - Documentación técnica, API docs, README
8. **code-review-agent.md** - Revisión de código, calidad, estándares

### Agentes Auxiliares:

9. **database-agent.md** - Modelado, migraciones, optimización queries
10. **integration-agent.md** - Integraciones third-party, webhooks, APIs externas

## 3. Estructura de Cada Agente

Cada archivo de agente debe incluir:

```markdown
# [NOMBRE_AGENTE]

## ROL Y RESPONSABILIDADES

[Descripción clara del rol]

## CONTEXTO DE TRABAJO

- Stack tecnológico que maneja
- Dependencias con otros agentes
- Inputs esperados
- Outputs generados

## DIRECTRICES ESPECÍFICAS

- Estándares de código
- Patrones a seguir
- Anti-patrones a evitar
- Mejores prácticas

## WORKFLOW

1. Paso a paso de su proceso
2. Checkpoints de validación
3. Handoff a otros agentes

## HERRAMIENTAS Y COMANDOS

- Comandos CLI relevantes
- Scripts de automatización
- Validaciones

## PLANTILLAS Y EJEMPLOS

[Código de ejemplo relevante]
```

## 4. Sistema de Orquestación

En `agents-config.json` incluye:

```json
{
  "orchestration": {
    "version": "1.0.0",
    "project_type": "saas-generic",
    "agents": [],
    "workflows": {
      "feature_development": [],
      "bug_fix": [],
      "refactor": [],
      "deployment": []
    },
    "communication": {
      "handoff_protocol": "",
      "shared_context": ""
    }
  }
}
```

## 5. Variables de Configuración

En `project-context.md` define:

- `{{FRAMEWORK}}` - Framework principal (React/Vue/Angular/Next/etc)
- `{{BACKEND_STACK}}` - Node/Python/Java/Go/etc
- `{{DATABASE}}` - PostgreSQL/MongoDB/MySQL/etc
- `{{CLOUD_PROVIDER}}` - AWS/GCP/Azure
- `{{AUTH_METHOD}}` - JWT/OAuth/Session
- `{{DEPLOYMENT_STRATEGY}}` - Docker/Kubernetes/Serverless

# REQUISITOS ESPECÍFICOS

1. **Modularidad Total**: Cada agente debe ser independiente y reutilizable
2. **Intercambiabilidad**: Fácil swap de frameworks sin romper la orquestación
3. **Documentación Inline**: Cada decisión debe estar documentada
4. **Workflow Claro**: Diagramas de flujo entre agentes
5. **Validaciones**: Checkpoints automáticos en cada handoff
6. **Versionado**: Sistema de versionado para evolución de agentes

# OUTPUTS ESPERADOS

Genera TODOS los archivos mencionados con contenido completo, no placeholders. Cada agente debe tener:

- Mínimo 100 líneas de especificación detallada
- Ejemplos de código concretos
- Scripts de validación
- Criterios de aceptación

# CONSIDERACIONES ADICIALES

- Usa Markdown para documentación
- JSON/YAML para configuración
- Incluye scripts de inicialización
- Crea un `setup.sh` para bootstrap del proyecto
- Añade `CONTRIBUTING.md` con guía de uso de agentes

# TONO Y ESTILO

- Técnico y preciso
- Enfocado en automatización
- Pensado para escalabilidad
- Documentación exhaustiva pero clara

---

**INSTRUCCIÓN FINAL**: Genera PRIMERO la estructura de carpetas completa, LUEGO cada archivo con contenido real (no TODOs), comenzando por los agentes core y el sistema de orquestación.
