# Architecture Decision Records (ADRs)

Este directorio contiene las decisiones arquitectónicas importantes del proyecto.

## ¿Qué es un ADR?

Un ADR (Architecture Decision Record) documenta una decisión arquitectónica significativa junto con su contexto y consecuencias.

## Cuándo Crear un ADR

Crea un ADR cuando:

- Elijas entre múltiples alternativas técnicas significativas
- Tomes decisiones que afecten la estructura del sistema
- Selecciones tecnologías, frameworks o herramientas clave
- Cambies decisiones arquitectónicas previas

## Template ADR

Usa este template al crear nuevos ADRs:

```markdown
# ADR-XXX: [Título de la Decisión]

**Status**: [Proposed | Accepted | Deprecated | Superseded]
**Date**: YYYY-MM-DD
**Decision Makers**: [Nombres o roles]
**Supersedes**: [ADR-XXX] (si aplica)

## Context

[Describe el contexto y el problema que motivó la decisión.
¿Qué fuerzas están en juego? ¿Qué restricciones existen?]

## Decision

[Describe la decisión tomada. Sé específico y conciso.]

## Alternatives Considered

### Alternative 1: [Nombre]

**Pros**:

- [Pro 1]
- [Pro 2]

**Cons**:

- [Con 1]
- [Con 2]

### Alternative 2: [Nombre]

**Pros**:

- [Pro 1]

**Cons**:

- [Con 1]

## Consequences

### Positive

- [Consecuencia positiva 1]
- [Consecuencia positiva 2]

### Negative

- [Consecuencia negativa 1]
- [Consecuencia negativa 2]

### Neutral

- [Cambios necesarios, aprendizajes, etc.]

## Implementation Notes

[Detalles de implementación, consideraciones técnicas, pasos siguientes]

## Related Decisions

- [ADR-XXX: Título relacionado]
- [ADR-YYY: Otro título relacionado]

## References

- [Link a documentación]
- [Link a discusiones]
- [Link a benchmarks]
```

## Ejemplo: ADR-001

Ver ejemplo completo en `examples/authentication-feature.md`

## Numeración

- ADR-001, ADR-002, etc.
- Secuencial, nunca reutilizar números
- Usar 3 dígitos con padding: 001, 002, etc.

## Status Lifecycle

```
Proposed → Accepted → [Deprecated | Superseded]
           ↓
       Rejected
```

- **Proposed**: Propuesta en discusión
- **Accepted**: Decisión aceptada e implementada
- **Deprecated**: Ya no se recomienda pero aún en uso
- **Superseded**: Reemplazada por otra decisión (especifica cuál)
- **Rejected**: Propuesta rechazada (documentar por qué)

## Comandos Útiles

### Crear Nuevo ADR

```bash
# Listar ADRs existentes
ls -l docs/architecture/decisions/

# Crear nuevo (obtener próximo número)
NEXT_NUM=$(printf "%03d" $(($(ls docs/architecture/decisions/ | grep -oP '^\d+' | sort -n | tail -1) + 1)))

# Copiar template
cp docs/architecture/ADR-TEMPLATE.md docs/architecture/decisions/ADR-${NEXT_NUM}-mi-decision.md
```

### Buscar ADRs

```bash
# Buscar por keyword
grep -r "database" docs/architecture/decisions/

# Listar solo aceptados
grep -l "Status: Accepted" docs/architecture/decisions/*.md
```

## Best Practices

### 1. Sé Conciso

- ADRs no son specs completas
- Enfócate en la decisión y su justificación
- Enlaces a docs detalladas si es necesario

### 2. Documenta el Contexto

- ¿Por qué era necesario decidir?
- ¿Qué restricciones había?
- ¿Qué alternativas se consideraron?

### 3. Explica las Consecuencias

- No solo las positivas
- Documenta trade-offs
- Incluye consecuencias a largo plazo

### 4. Actualiza Status

- Marca como Deprecated cuando cambies
- Crea ADR nuevo que superseda (no edites el viejo)
- Mantén historia de decisiones

### 5. Vincular Decisiones Relacionadas

- Referencias a ADRs relacionados
- Cadenas de decisiones
- Evolución del pensamiento

## Ejemplo ADR Completo

```markdown
# ADR-001: Use PostgreSQL as Primary Database

**Status**: Accepted
**Date**: 2026-01-10
**Decision Makers**: Architect Agent, Backend Team

## Context

We need a relational database for our SaaS application that handles:

- User authentication and authorization
- Transactional data (orders, payments)
- Complex queries with joins
- ACID guarantees
- Scalability to 100k+ users

## Decision

We will use PostgreSQL as our primary database.

## Alternatives Considered

### Alternative 1: MySQL

**Pros**:

- Wide adoption
- Good performance
- Many hosting options

**Cons**:

- Less advanced JSON support
- Weaker full-text search
- License concerns (Oracle)

### Alternative 2: MongoDB

**Pros**:

- Flexible schema
- Horizontal scaling
- Good for rapid prototyping

**Cons**:

- No ACID transactions (initially)
- Eventual consistency challenges
- Not ideal for complex joins

## Consequences

### Positive

- Excellent ACID compliance
- Advanced JSON support (JSONB)
- Powerful full-text search
- Rich extension ecosystem (PostGIS, etc.)
- Strong community and tooling

### Negative

- Vertical scaling primary approach
- More complex clustering than MongoDB
- Requires careful index management

### Neutral

- Team needs to learn PostgreSQL-specific features
- Will use Prisma ORM for abstraction
- Hosting costs similar to alternatives

## Implementation Notes

- Use PostgreSQL 15+
- Enable JSONB for flexible fields
- Set up proper indexes from start
- Use connection pooling (PgBouncer)
- Backups via automated snapshots

## Related Decisions

- ADR-002: Use Prisma as ORM
- ADR-005: Database migration strategy

## References

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Why Postgres](https://www.craigkerstiens.com/2017/04/30/why-postgres-five-years-later/)
```

---

**Mantén tus ADRs actualizados y documenta todas las decisiones importantes!**
