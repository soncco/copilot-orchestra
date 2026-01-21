# TravesIA Database Setup

## 📋 Descripción

Este directorio contiene todos los esquemas SQL, scripts de inicialización y utilidades para la base de datos PostgreSQL de TravesIA.

---

## 📁 Estructura de Archivos

```
database/
├── schemas/                    # Esquemas SQL por contexto
│   ├── 00_extensions.sql      # Extensiones PostgreSQL
│   ├── 01_circuit_management.sql
│   ├── 02_suppliers.sql
│   ├── 03_operations.sql
│   ├── 04_financial.sql
│   ├── 05_documents.sql
│   ├── 06_auth_users.sql
│   └── 99_drop_all.sql        # Script para limpiar todo
├── scripts/                    # Scripts de utilidades
│   ├── init_database.sh       # Setup inicial completo
│   ├── backup.sh              # Backup de la base de datos
│   └── restore.sh             # Restaurar desde backup
└── README.md                   # Este archivo
```

---

## 🚀 Setup Inicial

### Prerrequisitos

- PostgreSQL 15+ instalado y corriendo
- Cliente `psql` disponible en PATH
- Variables de entorno configuradas (ver abajo)

### Variables de Entorno

```bash
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=travesia
export DB_USER=postgres
export DB_PASSWORD=your_password_here
```

### Inicializar Base de Datos

```bash
# Dar permisos de ejecución a los scripts
chmod +x database/scripts/*.sh

# Ejecutar setup inicial
./database/scripts/init_database.sh
```

Este script ejecutará todos los archivos SQL en orden y creará:

- ✅ Extensiones PostgreSQL necesarias
- ✅ Todas las tablas organizadas por bounded context
- ✅ Índices para optimización de queries
- ✅ Triggers para timestamps automáticos
- ✅ Constraints para integridad de datos
- ✅ Datos de ejemplo (programas y usuario admin)

---

## 📊 Esquema de Base de Datos

### Bounded Contexts

#### 1. Circuit Management (`01_circuit_management.sql`)

**Tablas**: `programs`, `groups`, `passengers`, `itineraries`, `flights`

Gestiona los programas de viaje, grupos programados, pasajeros y sus itinerarios.

#### 2. Supplier Management (`02_suppliers.sql`)

**Tablas**: `suppliers`, `supplier_services`, `price_periods`, `exchange_rates`

Administra proveedores, sus servicios, precios por períodos y tasas de cambio.

#### 3. Operations (`03_operations.sql`)

**Tablas**: `hotels`, `transportation`, `accommodations`, `special_services`, `staff`, `staff_assignments`

"La Biblia Digital" - gestiona transporte, hoteles, servicios especiales y asignación de personal.

#### 4. Financial (`04_financial.sql`)

**Tablas**: `group_costs`, `additional_sales`, `commissions`, `invoices`, `bank_deposits`

Costos multi-moneda, ventas adicionales, comisiones, facturación SUNAT y depósitos bancarios.

#### 5. Document Management (`05_documents.sql`)

**Tablas**: `documents`

Repositorio digital con referencias a S3 para todos los documentos.

#### 6. Authentication & Users (`06_auth_users.sql`)

**Tablas**: `users`, `user_sessions`, `audit_log`

Sistema de autenticación, sesiones JWT y auditoría completa.

---

## 🔧 Scripts de Utilidades

### Backup

Crear backup comprimido de la base de datos:

```bash
./database/scripts/backup.sh
```

Características:

- Formato custom de PostgreSQL (comprimido)
- Guardado en `./backups/`
- Limpieza automática (mantiene últimos 7 días)
- Upload opcional a S3 (si `AWS_S3_BUCKET` está configurado)

### Restore

Restaurar desde un backup:

```bash
./database/scripts/restore.sh ./backups/travesia_20260120_143000.backup.gz
```

⚠️ **ADVERTENCIA**: Esto eliminará todos los datos actuales.

### Reset Completo

Para limpiar toda la base de datos:

```bash
psql -h localhost -U postgres -d travesia -f database/schemas/99_drop_all.sql
```

Luego volver a ejecutar el setup inicial.

---

## 📝 Convenciones

### Naming Conventions

- **Tablas**: Plural, snake_case (`users`, `group_costs`)
- **Columnas**: snake_case (`first_name`, `created_at`)
- **Enums**: UPPER_CASE (`YOUNG`, `CONFIRMED`)
- **Índices**: `idx_<table>_<columns>` (`idx_groups_program_year`)

### Tipos de Datos

- **IDs**: UUID (generados con `uuid_generate_v4()`)
- **Timestamps**: TIMESTAMPTZ (con zona horaria)
- **Moneda**: NUMERIC(12, 2) para cantidades
- **Texto largo**: TEXT sin límite
- **JSON**: JSONB para mejor performance

### Constraints

- ✅ Foreign Keys con `ON DELETE` apropiado
- ✅ Check constraints para validaciones
- ✅ Unique constraints donde aplica
- ✅ Not null en campos obligatorios

---

## 🔍 Queries Útiles

### Ver todas las tablas

```sql
SELECT
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

### Verificar índices

```sql
SELECT
    tablename,
    indexname,
    indexdef
FROM pg_indexes
WHERE schemaname = 'public'
ORDER BY tablename, indexname;
```

### Estadísticas de tablas

```sql
SELECT
    schemaname,
    tablename,
    n_live_tup AS row_count,
    n_dead_tup AS dead_rows,
    last_vacuum,
    last_autovacuum
FROM pg_stat_user_tables
ORDER BY n_live_tup DESC;
```

### Buscar queries lentas

```sql
SELECT
    query,
    calls,
    total_time,
    mean_time,
    max_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 20;
```

---

## 🔐 Seguridad

### Usuario Admin por Defecto

El script de inicialización crea un usuario admin:

- **Username**: `admin`
- **Email**: `admin@travesia.com`
- **Password**: `admin123`

⚠️ **CAMBIAR INMEDIATAMENTE EN PRODUCCIÓN**

### Datos Sensibles

Los siguientes campos deben ser encriptados a nivel de aplicación:

- `passengers.passport_number`
- `passengers.medical_conditions`
- `users.mfa_secret`

Django manejará esto con `django-cryptography`.

### Audit Trail

Todas las acciones significativas se registran en `audit_log`:

- CREATE, UPDATE, DELETE operations
- User logins/logouts
- IP address y user agent
- JSON diff de cambios

---

## 🧪 Testing

### Verificar Setup

```sql
-- Contar tablas creadas
SELECT COUNT(*) FROM information_schema.tables
WHERE table_schema = 'public';
-- Debe retornar: 22

-- Verificar extensiones
SELECT extname FROM pg_extension
WHERE extname IN ('uuid-ossp', 'unaccent', 'pg_trgm', 'pgcrypto');
-- Debe retornar las 4 extensiones

-- Verificar datos de ejemplo
SELECT COUNT(*) FROM programs;
-- Debe retornar: 4

SELECT COUNT(*) FROM users;
-- Debe retornar: 1 (admin)
```

### Datos de Prueba

Para desarrollo, puedes agregar más datos de prueba:

```sql
-- Insertar grupo de ejemplo
INSERT INTO groups (program_id, code, year, departure_date, return_date, group_type, max_capacity)
SELECT
    id,
    'PERBOL-2026-01',
    2026,
    '2026-06-15',
    '2026-07-05',
    'YOUNG',
    30
FROM programs
WHERE code = 'PERBOL_CHIL';
```

---

## 📈 Optimización

### Índices Críticos

Los siguientes índices son críticos para performance:

```sql
-- Búsquedas de grupos por programa y año
idx_groups_program_year

-- Búsquedas de pasajeros por grupo
idx_passengers_group

-- Búsquedas financieras
idx_group_costs_group_category
idx_invoices_status_date

-- Full-text search
idx_suppliers_search
idx_documents_search
```

### Mantenimiento

Ejecutar periódicamente:

```sql
-- Vacuum y análisis
VACUUM ANALYZE;

-- Reindex si es necesario
REINDEX DATABASE travesia;

-- Actualizar estadísticas
ANALYZE;
```

---

## 🐛 Troubleshooting

### Error: "database already exists"

```bash
# Eliminar y recrear
dropdb travesia
createdb travesia
./database/scripts/init_database.sh
```

### Error: "extension already exists"

Es normal, las extensiones no se pueden crear dos veces. El script continúa sin problemas.

### Error: "permission denied"

```bash
# Asegurarse de tener permisos
chmod +x database/scripts/*.sh

# Verificar usuario PostgreSQL
psql -h localhost -U postgres -c "SELECT current_user;"
```

### Conexión rechazada

```bash
# Verificar que PostgreSQL esté corriendo
pg_isready -h localhost -p 5432

# Iniciar PostgreSQL (macOS)
brew services start postgresql@15

# Iniciar PostgreSQL (Linux)
sudo systemctl start postgresql
```

---

## 📚 Referencias

- [PostgreSQL Documentation](https://www.postgresql.org/docs/15/)
- [Django PostgreSQL Features](https://docs.djangoproject.com/en/5.0/ref/contrib/postgres/)
- [Architecture Plan](../docs/architecture/architecture-plan.md)
- [Data Model](../docs/architecture/data-model.md)

---

## 🔄 Próximos Pasos

1. ✅ Esquemas SQL creados
2. ✅ Scripts de utilidades listos
3. ⏳ Crear modelos Django
4. ⏳ Generar migraciones Django
5. ⏳ Configurar Django settings
6. ⏳ Implementar serializers y views

---

**Versión**: 1.0
**Última Actualización**: 2026-01-20
**Mantenedor**: Database Agent
