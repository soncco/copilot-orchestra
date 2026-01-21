# TravesIA Database - Guía de Migraciones

## 📋 Resumen

Este proyecto utiliza **SQL puro** para las migraciones iniciales, con planes de integrar Django ORM posteriormente. Esta guía documenta el proceso completo de setup y gestión de la base de datos.

---

## 🎯 Filosofía de Migraciones

### Fase 1: SQL Puro (Actual)

- ✅ Control total sobre el esquema
- ✅ Optimización específica de PostgreSQL
- ✅ Índices y constraints explícitos
- ✅ Triggers y funciones personalizadas

### Fase 2: Django ORM (Futuro)

- Integración con Django models
- Migraciones automáticas con `makemigrations`
- Compatibilidad con admin panel
- Testing más simple

---

## 🚀 Setup Inicial

### 1. Preparar Entorno

```bash
# Instalar PostgreSQL (macOS)
brew install postgresql@15
brew services start postgresql@15

# Instalar PostgreSQL (Ubuntu/Debian)
sudo apt update
sudo apt install postgresql-15 postgresql-contrib

# Verificar instalación
psql --version
```

### 2. Configurar Variables

```bash
# Crear archivo .env en la raíz del proyecto
cat > .env << EOF
DB_HOST=localhost
DB_PORT=5432
DB_NAME=travesia
DB_USER=postgres
DB_PASSWORD=tu_password_seguro
EOF

# Cargar variables
source .env
```

### 3. Ejecutar Setup

```bash
# Desde la raíz del proyecto
./database/scripts/init_database.sh
```

Esto ejecutará automáticamente:

1. Crear base de datos si no existe
2. Instalar extensiones PostgreSQL
3. Crear todos los esquemas en orden
4. Aplicar índices y constraints
5. Configurar triggers
6. Insertar datos de ejemplo

---

## 📁 Estructura de Migraciones

```
database/
├── schemas/
│   ├── 00_extensions.sql          # Extensiones PostgreSQL
│   ├── 01_circuit_management.sql  # Primera migración: Circuits
│   ├── 02_suppliers.sql           # Segunda migración: Suppliers
│   ├── 03_operations.sql          # Tercera migración: Operations
│   ├── 04_financial.sql           # Cuarta migración: Financial
│   ├── 05_documents.sql           # Quinta migración: Documents
│   ├── 06_auth_users.sql          # Sexta migración: Auth
│   └── 99_drop_all.sql            # Rollback completo
└── scripts/
    ├── init_database.sh            # Setup maestro
    ├── backup.sh                   # Backup
    └── restore.sh                  # Restore
```

---

## 🔄 Workflow de Cambios

### Agregar una Nueva Tabla

1. **Crear archivo de migración**:

```bash
touch database/schemas/07_nueva_funcionalidad.sql
```

2. **Escribir SQL**:

```sql
-- =====================================================
-- Nueva Funcionalidad
-- =====================================================

CREATE TABLE nueva_tabla (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nombre VARCHAR(200) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_nueva_tabla_nombre ON nueva_tabla(nombre);

CREATE TRIGGER update_nueva_tabla_updated_at
    BEFORE UPDATE ON nueva_tabla
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

3. **Actualizar script de init**:

```bash
# Editar database/scripts/init_database.sh
# Agregar línea:
execute_sql "$SCHEMA_DIR/07_nueva_funcionalidad.sql" "Nueva Funcionalidad"
```

4. **Aplicar migración**:

```bash
# Solo la nueva migración
psql -h $DB_HOST -U $DB_USER -d $DB_NAME -f database/schemas/07_nueva_funcionalidad.sql

# O reset completo
./database/scripts/init_database.sh
```

### Modificar una Tabla Existente

#### Opción A: Rollback y Recrear (Development)

```bash
# 1. Backup
./database/scripts/backup.sh

# 2. Drop y recrear
psql -h localhost -U postgres -d travesia -f database/schemas/99_drop_all.sql
./database/scripts/init_database.sh
```

#### Opción B: Alter Table (Production)

```sql
-- Crear migración específica
-- database/schemas/08_alter_groups.sql

ALTER TABLE groups
ADD COLUMN tour_conductor_notes TEXT;

CREATE INDEX idx_groups_conductor_notes
ON groups USING gin(to_tsvector('spanish', tour_conductor_notes))
WHERE tour_conductor_notes IS NOT NULL;
```

### Eliminar una Tabla

```sql
-- Siempre con CASCADE para dependencias
DROP TABLE IF EXISTS tabla_antigua CASCADE;
```

---

## 🧪 Testing de Migraciones

### Test en Ambiente Local

```bash
# 1. Crear base de datos de test
createdb travesia_test

# 2. Ejecutar migraciones
DB_NAME=travesia_test ./database/scripts/init_database.sh

# 3. Verificar resultado
psql -d travesia_test -c "\dt"

# 4. Limpiar
dropdb travesia_test
```

### Validar Integridad

```sql
-- Verificar foreign keys
SELECT
    conname AS constraint_name,
    conrelid::regclass AS table_name,
    confrelid::regclass AS referenced_table
FROM pg_constraint
WHERE contype = 'f'
ORDER BY conrelid::regclass::text;

-- Verificar constraints
SELECT
    conname,
    conrelid::regclass AS table_name,
    pg_get_constraintdef(oid)
FROM pg_constraint
WHERE contype = 'c';

-- Verificar triggers
SELECT
    trigger_name,
    event_object_table AS table_name,
    action_statement
FROM information_schema.triggers
WHERE trigger_schema = 'public';
```

---

## 📊 Versionado de Esquema

### Tabla de Versiones (Opcional)

```sql
-- Crear tabla de control de versiones
CREATE TABLE schema_migrations (
    version VARCHAR(50) PRIMARY KEY,
    description TEXT,
    applied_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    applied_by VARCHAR(100)
);

-- Registrar cada migración
INSERT INTO schema_migrations (version, description, applied_by) VALUES
    ('00', 'PostgreSQL Extensions', 'setup_script'),
    ('01', 'Circuit Management Context', 'setup_script'),
    ('02', 'Supplier Management Context', 'setup_script'),
    ('03', 'Operations Context', 'setup_script'),
    ('04', 'Financial Context', 'setup_script'),
    ('05', 'Document Management Context', 'setup_script'),
    ('06', 'Authentication & Users', 'setup_script');

-- Ver historial
SELECT * FROM schema_migrations ORDER BY applied_at DESC;
```

---

## 🔄 Rollback Strategies

### Rollback Completo

```bash
# Restaurar desde backup
./database/scripts/restore.sh ./backups/travesia_20260120_143000.backup.gz
```

### Rollback Específico

```sql
-- Revertir una migración específica
-- Ejemplo: Eliminar tabla agregada en migración 07

DROP TABLE IF EXISTS nueva_tabla CASCADE;

-- Actualizar versión
DELETE FROM schema_migrations WHERE version = '07';
```

### Rollback de ALTER

```sql
-- Revertir cambios de columna
ALTER TABLE groups DROP COLUMN IF EXISTS tour_conductor_notes;

-- Revertir índice
DROP INDEX IF EXISTS idx_groups_conductor_notes;
```

---

## 🚨 Precauciones en Producción

### Pre-Deploy Checklist

- [ ] Backup completo creado y verificado
- [ ] Migraciones probadas en staging
- [ ] Índices necesarios identificados
- [ ] Impacto en performance evaluado
- [ ] Rollback plan documentado
- [ ] Downtime estimado comunicado
- [ ] Monitoring habilitado

### Durante el Deploy

```bash
# 1. Activar modo mantenimiento
# 2. Crear backup
./database/scripts/backup.sh

# 3. Aplicar migración con timeout
psql -v ON_ERROR_STOP=1 \
     --set statement_timeout=30000 \
     -f database/schemas/nueva_migracion.sql

# 4. Verificar
psql -c "SELECT COUNT(*) FROM nueva_tabla;"

# 5. Desactivar modo mantenimiento
```

### Post-Deploy

```sql
-- Actualizar estadísticas
ANALYZE;

-- Verificar índices usados
SELECT
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
WHERE idx_scan = 0
ORDER BY schemaname, tablename;
```

---

## 🔗 Integración con Django (Fase 2)

### Generar Models desde DB

```bash
# Instalar django
pip install django psycopg2-binary

# Inspeccionar DB y generar models
python manage.py inspectdb > apps/circuits/models_generated.py

# Revisar y ajustar manualmente
```

### Crear Migraciones Django

```bash
# Después de ajustar models
python manage.py makemigrations

# Marcar como aplicadas (fake)
python manage.py migrate --fake-initial
```

### Sincronizar Cambios

```sql
-- Si Django crea una migración, exportar a SQL
python manage.py sqlmigrate app_name migration_name > nueva_migracion.sql

-- Aplicar directamente
psql -f nueva_migracion.sql
```

---

## 📝 Best Practices

### Naming Conventions

```sql
-- Migraciones: ##_nombre_descriptivo.sql
01_circuit_management.sql
02_suppliers.sql

-- Índices: idx_<tabla>_<columnas>
idx_groups_program_year

-- Constraints: <tabla>_<tipo>_<nombre>
groups_valid_dates_check

-- Triggers: update_<tabla>_<acción>
update_groups_updated_at
```

### Comentarios

```sql
-- Siempre comentar tablas y columnas importantes
COMMENT ON TABLE groups IS 'Travel groups scheduled for specific programs';
COMMENT ON COLUMN groups.code IS 'Unique identifier (e.g., PERBOL-2026-05)';
```

### Transacciones

```sql
-- Envolver cambios en transacciones
BEGIN;

ALTER TABLE groups ADD COLUMN nueva_columna TEXT;
CREATE INDEX idx_groups_nueva ON groups(nueva_columna);

-- Verificar
SELECT COUNT(*) FROM groups;

COMMIT;
-- o ROLLBACK si algo salió mal
```

---

## 🐛 Troubleshooting

### Migración Bloqueada

```sql
-- Ver locks activos
SELECT
    pid,
    usename,
    pg_blocking_pids(pid) as blocked_by,
    query
FROM pg_stat_activity
WHERE datname = 'travesia';

-- Terminar proceso bloqueante
SELECT pg_terminate_backend(pid);
```

### Migración Lenta

```sql
-- Crear índice de forma concurrente (no bloquea)
CREATE INDEX CONCURRENTLY idx_groups_new ON groups(nueva_columna);

-- Agregar columna con default más tarde
ALTER TABLE groups ADD COLUMN nueva_columna TEXT;
UPDATE groups SET nueva_columna = 'valor' WHERE condicion;
```

### Error de Constraint

```sql
-- Validar datos antes de agregar constraint
SELECT * FROM groups
WHERE return_date <= departure_date;

-- Corregir datos
UPDATE groups
SET return_date = departure_date + INTERVAL '1 day'
WHERE return_date <= departure_date;

-- Luego agregar constraint
ALTER TABLE groups
ADD CONSTRAINT valid_dates CHECK (return_date > departure_date);
```

---

## 📚 Referencias

- [PostgreSQL ALTER TABLE](https://www.postgresql.org/docs/15/sql-altertable.html)
- [Django Migrations](https://docs.djangoproject.com/en/5.0/topics/migrations/)
- [Database Migration Best Practices](https://www.postgresql.org/docs/15/ddl-alter.html)

---

**Versión**: 1.0  
**Fecha**: 2026-01-20  
**Mantenedor**: Database Agent
