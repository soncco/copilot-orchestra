# ADR-0002: PostgreSQL como Base de Datos Principal

**Fecha**: 2026-01-20
**Status**: ✅ Accepted
**Decisor**: Architect Agent

---

## Contexto

TravesIA necesita almacenar datos estructurados con relaciones complejas:

- Grupos de viaje con múltiples pasajeros
- Itinerarios detallados con actividades
- Proveedores con servicios y precios por períodos
- Transacciones financieras multi-moneda con consistencia ACID
- Documentos con metadata

**Volumen esperado**:

- 50 grupos/año × 30 pasajeros promedio = ~1,500 pasajeros/año
- Datos históricos acumulativos (5+ años)
- Crecimiento moderado anual

---

## Decisión

**Usaremos PostgreSQL 15+ como base de datos principal.**

---

## Alternativas Consideradas

### Opción 1: MySQL

**Pros**:

- Ampliamente usado y conocido
- Buen performance en lecturas
- Replicación robusta

**Contras**:

- JSON support inferior a PostgreSQL
- Funcionalidades avanzadas limitadas
- Full-text search menos potente
- Extensiones limitadas

### Opción 2: MongoDB

**Pros**:

- Esquema flexible
- Escalado horizontal nativo
- Queries rápidas en documentos grandes

**Contras**:

- Consistencia eventual (no ACID completo)
- JOIN operations complejas e ineficientes
- No apropiado para transacciones financieras
- Integridad referencial manual

### Opción 3: PostgreSQL (Seleccionada)

**Pros**:

- ACID completo (crítico para finanzas)
- JSON/JSONB support excelente
- Full-text search nativo (búsquedas de proveedores, pasajeros)
- Extensiones poderosas (pg_trgm, postgis si se necesita)
- Transacciones robustas
- Django ORM integración perfecta
- Window functions y CTEs para reportes complejos
- Replicación y backup maduros

**Contras**:

- Escalado horizontal más complejo que NoSQL
- Requiere tuning de índices cuidadoso
- Sharding manual si fuera necesario

---

## Justificación

1. **Transacciones Financieras**: ACID es no negociable para pagos, facturación SUNAT
2. **Relaciones Complejas**: El modelo de datos tiene múltiples relaciones (grupos → pasajeros → vuelos)
3. **JSON Support**: Necesario para itinerarios flexibles, metadata de documentos
4. **Full-Text Search**: Búsqueda de proveedores, pasajeros por nombre/pasaporte
5. **Django ORM**: Integración nativa y excelente soporte
6. **Madurez**: Probado en millones de aplicaciones críticas

---

## Consecuencias

### Positivas ✅

- Consistencia garantizada en transacciones financieras
- Integridad referencial automática (Foreign Keys)
- Queries complejas con JOINs eficientes
- Extensiones para necesidades futuras (búsqueda geográfica con PostGIS)
- Backup y recovery robustos
- Excelente tooling (pgAdmin, pg_stat_statements)

### Negativas ⚠️

- Escalado vertical preferido inicialmente
- Requiere vacuuming periódico
- Performance degrada sin índices apropiados

### Riesgos y Mitigaciones

| Riesgo                 | Probabilidad | Impacto | Mitigación                                              |
| ---------------------- | ------------ | ------- | ------------------------------------------------------- |
| Performance en queries | Media        | Medio   | Índices cuidadosos, EXPLAIN ANALYZE, query optimization |
| Crecimiento de datos   | Baja         | Medio   | Particionamiento de tablas históricas, archivado anual  |
| Backup failures        | Baja         | Alto    | Automated backups, point-in-time recovery, replicas     |

---

## Implementación

### Extensiones Requeridas

```sql
-- Full-text search en español
CREATE EXTENSION IF NOT EXISTS unaccent;
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- UUID generation
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
```

### Configuración Optimizada

```ini
# postgresql.conf (para servidor mediano)
shared_buffers = 2GB
effective_cache_size = 6GB
maintenance_work_mem = 512MB
checkpoint_completion_target = 0.9
wal_buffers = 16MB
default_statistics_target = 100
random_page_cost = 1.1  # Para SSD
effective_io_concurrency = 200
work_mem = 10MB
min_wal_size = 1GB
max_wal_size = 4GB
max_worker_processes = 4
max_parallel_workers_per_gather = 2
max_parallel_workers = 4
```

### Estrategia de Backup

```bash
# Backup diario automatizado
pg_dump -Fc travesia > backup_$(date +%Y%m%d).dump

# Retention policy
# - Diarios: 7 días
# - Semanales: 4 semanas
# - Mensuales: 12 meses
# - Anuales: indefinido
```

### Índices Críticos

```sql
-- Consultas frecuentes
CREATE INDEX idx_group_program_year ON groups(program_id, year);
CREATE INDEX idx_group_dates ON groups(departure_date, return_date);
CREATE INDEX idx_passenger_group ON passengers(group_id);
CREATE INDEX idx_passenger_passport ON passengers(passport_number);

-- Full-text search
CREATE INDEX idx_supplier_search ON suppliers
    USING gin(to_tsvector('spanish', name || ' ' || contact_name));

-- Financial queries
CREATE INDEX idx_cost_group_category ON group_costs(group_id, category);
CREATE INDEX idx_invoice_status_date ON invoices(status, issue_date);
```

---

## Monitoreo

### Métricas a Rastrear

- Query performance (pg_stat_statements)
- Cache hit ratio (> 99%)
- Connection pool usage
- Disk I/O
- Replication lag (si aplica)
- Slow queries (> 500ms)

### Herramientas

- **pgAdmin**: GUI management
- **pg_stat_statements**: Query analytics
- **pgBadger**: Log analyzer
- **AWS RDS Performance Insights**: Si se usa AWS RDS

---

## Referencias

- [PostgreSQL Documentation](https://www.postgresql.org/docs/15/)
- [Django PostgreSQL-specific features](https://docs.djangoproject.com/en/5.0/ref/contrib/postgres/)
- [PgTune](https://pgtune.leopard.in.ua/) - Configuration optimizer

---

**Revisión**: Pendiente
**Próxima Revisión**: 2026-07-20 (6 meses)
