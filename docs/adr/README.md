# Architecture Decision Records (ADRs)

Este directorio contiene los Architecture Decision Records (ADRs) del proyecto TravesIA. Los ADRs documentan decisiones arquitectónicas importantes con su contexto, alternativas consideradas y consecuencias.

---

## ¿Qué es un ADR?

Un ADR (Architecture Decision Record) es un documento que captura una decisión arquitectónica importante junto con su contexto y consecuencias. Ayuda a:

- Entender **por qué** se tomó una decisión
- Evaluar alternativas que se consideraron
- Anticipar consecuencias (positivas y negativas)
- Facilitar onboarding de nuevos miembros del equipo
- Evitar re-litigar decisiones ya tomadas

---

## Formato de ADR

Cada ADR sigue esta estructura:

```markdown
# ADR-XXXX: [Título de la Decisión]

**Fecha**: YYYY-MM-DD
**Status**: Proposed | Accepted | Deprecated | Superseded
**Decisor**: [Nombre o rol]

## Contexto

[Describe el contexto y el problema que se está resolviendo]

## Decisión

[La decisión tomada]

## Alternativas Consideradas

[Opciones que se evaluaron]

## Justificación

[Por qué se eligió esta opción]

## Consecuencias

[Impactos positivos y negativos]

## Referencias

[Enlaces a documentación relevante]
```

---

## Índice de ADRs

| #                                               | Título                                  | Fecha      | Status      |
| ----------------------------------------------- | --------------------------------------- | ---------- | ----------- |
| [0001](./0001-django-rest-framework.md)         | Django REST Framework para API Backend  | 2026-01-20 | ✅ Accepted |
| [0002](./0002-postgresql-database.md)           | PostgreSQL como Base de Datos Principal | 2026-01-20 | ✅ Accepted |
| [0003](./0003-monolith-modular-architecture.md) | Arquitectura Monolito Modular           | 2026-01-20 | ✅ Accepted |

---

## Estados Posibles

- **Proposed** 📝: La decisión está propuesta pero no finalizada
- **Accepted** ✅: La decisión ha sido aceptada y está en implementación
- **Deprecated** ⚠️: La decisión ya no es válida pero se mantiene por contexto histórico
- **Superseded** 🔄: Reemplazada por otra ADR (indicar cuál)

---

## Proceso para Crear un ADR

1. **Identificar la necesidad**: ¿Es una decisión significativa que afecta la arquitectura?
2. **Usar el template**: Copiar estructura del formato estándar
3. **Investigar alternativas**: Documentar al menos 2-3 opciones
4. **Proponer**: Crear PR con status "Proposed"
5. **Discutir**: Equipo revisa y comenta
6. **Decidir**: Actualizar status a "Accepted" o archivar
7. **Implementar**: Proceder con la implementación

---

## Cuándo Crear un ADR

✅ **SÍ crear ADR para**:

- Selección de frameworks principales (Django, Vue, etc.)
- Patrones arquitectónicos (monolito vs microservicios)
- Bases de datos y sistemas de persistencia
- Estrategias de autenticación
- Integraciones con servicios externos críticos
- Cambios que afectan múltiples bounded contexts

❌ **NO crear ADR para**:

- Decisiones tácticas de implementación
- Elección de bibliotecas menores
- Cambios de configuración
- Refactorings internos sin impacto arquitectónico

---

## Revisión Periódica

Los ADRs deben revisarse periódicamente (cada 6 meses) para validar que:

- Siguen siendo relevantes
- Las consecuencias anticipadas se cumplieron
- No hay mejores alternativas disponibles

---

## Herramientas

```bash
# Crear nuevo ADR
./scripts/create-adr.sh "Título de la decisión"

# Listar todos los ADRs
ls -la docs/adr/*.md

# Buscar ADRs por keyword
grep -r "keyword" docs/adr/
```

---

## Referencias

- [ADR GitHub](https://adr.github.io/)
- [Documenting Architecture Decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- [ADR Tools](https://github.com/npryce/adr-tools)
