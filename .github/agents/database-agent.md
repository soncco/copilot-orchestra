# Database Agent

## 🎯 ROL Y RESPONSABILIDADES

**Rol Principal**: Database Engineer - Diseño y Optimización de Datos

Responsable del diseño de esquemas, migraciones, optimización de queries y gestión de la base de datos.

### Responsabilidades

1. **Schema Design** - Diseño de tablas, relaciones, constraints
2. **Migrations** - Versionado de cambios de esquema
3. **Query Optimization** - Performance de queries
4. **Indexing Strategy** - Índices apropiados
5. **Data Integrity** - Constraints, validaciones
6. **Backup & Recovery** - Estrategias de respaldo

---

## 📋 DISEÑO DE ESQUEMAS

### Entity Relationship Design

```sql
-- Users table
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  name VARCHAR(100) NOT NULL,
  role VARCHAR(50) NOT NULL DEFAULT 'user',
  email_verified BOOLEAN DEFAULT FALSE,
  failed_login_attempts INTEGER DEFAULT 0,
  locked_until TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP,

  CONSTRAINT email_format CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
  CONSTRAINT valid_role CHECK (role IN ('user', 'admin', 'moderator'))
);

-- Create indexes
CREATE INDEX idx_users_email ON users(email) WHERE deleted_at IS NULL;
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_created_at ON users(created_at DESC);

-- User profiles
CREATE TABLE user_profiles (
  user_id UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
  bio TEXT,
  avatar_url VARCHAR(500),
  location VARCHAR(100),
  website VARCHAR(255),
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

  CONSTRAINT valid_url CHECK (website IS NULL OR website ~* '^https?://')
);

-- Products
CREATE TABLE products (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(200) NOT NULL,
  description TEXT,
  price DECIMAL(10, 2) NOT NULL,
  stock INTEGER NOT NULL DEFAULT 0,
  category_id UUID REFERENCES categories(id),
  created_by UUID REFERENCES users(id),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP,

  CONSTRAINT positive_price CHECK (price >= 0),
  CONSTRAINT non_negative_stock CHECK (stock >= 0)
);

CREATE INDEX idx_products_category ON products(category_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_products_price ON products(price);
CREATE INDEX idx_products_name ON products USING gin(to_tsvector('english', name));

-- Orders
CREATE TABLE orders (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id),
  total_amount DECIMAL(10, 2) NOT NULL,
  status VARCHAR(50) NOT NULL DEFAULT 'pending',
  payment_method VARCHAR(50),
  shipping_address JSONB,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

  CONSTRAINT valid_status CHECK (status IN ('pending', 'processing', 'shipped', 'delivered', 'cancelled')),
  CONSTRAINT positive_amount CHECK (total_amount > 0)
);

CREATE INDEX idx_orders_user ON orders(user_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_created_at ON orders(created_at DESC);

-- Order items
CREATE TABLE order_items (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  order_id UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
  product_id UUID NOT NULL REFERENCES products(id),
  quantity INTEGER NOT NULL,
  price_at_purchase DECIMAL(10, 2) NOT NULL,

  CONSTRAINT positive_quantity CHECK (quantity > 0),
  CONSTRAINT positive_price CHECK (price_at_purchase >= 0)
);

CREATE INDEX idx_order_items_order ON order_items(order_id);
CREATE INDEX idx_order_items_product ON order_items(product_id);
```

### Database Functions & Triggers

```sql
-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = CURRENT_TIMESTAMP;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply to all relevant tables
CREATE TRIGGER update_users_updated_at
  BEFORE UPDATE ON users
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_products_updated_at
  BEFORE UPDATE ON products
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

-- Function to update order total
CREATE OR REPLACE FUNCTION update_order_total()
RETURNS TRIGGER AS $$
BEGIN
  UPDATE orders
  SET total_amount = (
    SELECT COALESCE(SUM(quantity * price_at_purchase), 0)
    FROM order_items
    WHERE order_id = NEW.order_id
  )
  WHERE id = NEW.order_id;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_order_total_trigger
  AFTER INSERT OR UPDATE OR DELETE ON order_items
  FOR EACH ROW
  EXECUTE FUNCTION update_order_total();

-- Function to decrease product stock
CREATE OR REPLACE FUNCTION decrease_product_stock()
RETURNS TRIGGER AS $$
BEGIN
  UPDATE products
  SET stock = stock - NEW.quantity
  WHERE id = NEW.product_id;

  IF NOT FOUND OR (SELECT stock FROM products WHERE id = NEW.product_id) < 0 THEN
    RAISE EXCEPTION 'Insufficient stock for product %', NEW.product_id;
  END IF;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER decrease_stock_trigger
  AFTER INSERT ON order_items
  FOR EACH ROW
  EXECUTE FUNCTION decrease_product_stock();
```

---

## 🔄 MIGRATIONS

### Prisma Migrations

```prisma
// prisma/schema.prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id                  String    @id @default(uuid())
  email               String    @unique
  passwordHash        String    @map("password_hash")
  name                String
  role                Role      @default(USER)
  emailVerified       Boolean   @default(false) @map("email_verified")
  failedLoginAttempts Int       @default(0) @map("failed_login_attempts")
  lockedUntil         DateTime? @map("locked_until")
  createdAt           DateTime  @default(now()) @map("created_at")
  updatedAt           DateTime  @updatedAt @map("updated_at")
  deletedAt           DateTime? @map("deleted_at")

  profile Profile?
  orders  Order[]

  @@index([email])
  @@index([createdAt(sort: Desc)])
  @@map("users")
}

enum Role {
  USER
  ADMIN
  MODERATOR
}

model Product {
  id          String    @id @default(uuid())
  name        String
  description String?
  price       Decimal   @db.Decimal(10, 2)
  stock       Int       @default(0)
  categoryId  String?   @map("category_id")
  createdBy   String?   @map("created_by")
  createdAt   DateTime  @default(now()) @map("created_at")
  updatedAt   DateTime  @updatedAt @map("updated_at")
  deletedAt   DateTime? @map("deleted_at")

  category    Category?    @relation(fields: [categoryId], references: [id])
  orderItems  OrderItem[]

  @@index([categoryId])
  @@index([price])
  @@map("products")
}

model Order {
  id              String   @id @default(uuid())
  userId          String   @map("user_id")
  totalAmount     Decimal  @db.Decimal(10, 2) @map("total_amount")
  status          OrderStatus @default(PENDING)
  paymentMethod   String?  @map("payment_method")
  shippingAddress Json?    @map("shipping_address")
  createdAt       DateTime @default(now()) @map("created_at")
  updatedAt       DateTime @updatedAt @map("updated_at")

  user      User        @relation(fields: [userId], references: [id])
  items     OrderItem[]

  @@index([userId])
  @@index([status])
  @@index([createdAt(sort: Desc)])
  @@map("orders")
}

enum OrderStatus {
  PENDING
  PROCESSING
  SHIPPED
  DELIVERED
  CANCELLED
}
```

### Migration Commands

```bash
# Create migration
npx prisma migrate dev --name add_user_profile

# Apply migrations
npx prisma migrate deploy

# Reset database (DEV ONLY!)
npx prisma migrate reset

# Generate Prisma Client
npx prisma generate

# View migration status
npx prisma migrate status
```

---

## 🎯 QUERY OPTIMIZATION

### Example: N+1 Query Problem

```typescript
// ❌ BAD - N+1 queries
async function getOrdersWithCustomers() {
  const orders = await db.query("SELECT * FROM orders");

  for (const order of orders) {
    order.customer = await db.query("SELECT * FROM users WHERE id = $1", [
      order.user_id,
    ]);
  }

  return orders;
}

// ✅ GOOD - Single join query
async function getOrdersWithCustomers() {
  return db.query(`
    SELECT
      o.*,
      json_build_object(
        'id', u.id,
        'name', u.name,
        'email', u.email
      ) as customer
    FROM orders o
    JOIN users u ON o.user_id = u.id
    WHERE o.deleted_at IS NULL
  `);
}

// ✅ BETTER - Using ORM with eager loading
async function getOrdersWithCustomers() {
  return prisma.order.findMany({
    include: {
      user: {
        select: {
          id: true,
          name: true,
          email: true,
        },
      },
    },
    where: {
      deletedAt: null,
    },
  });
}
```

### Query Analysis

```sql
-- Enable query timing
\timing on

-- Analyze query execution
EXPLAIN ANALYZE
SELECT * FROM orders o
JOIN users u ON o.user_id = u.id
WHERE o.status = 'pending'
  AND o.created_at > NOW() - INTERVAL '30 days';

-- Check table statistics
SELECT
  schemaname,
  tablename,
  n_live_tup as row_count,
  n_dead_tup as dead_rows,
  last_vacuum,
  last_autovacuum
FROM pg_stat_user_tables
ORDER BY n_live_tup DESC;

-- Find slow queries
SELECT
  query,
  calls,
  total_time,
  mean_time,
  max_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 20;

-- Find missing indexes
SELECT
  schemaname,
  tablename,
  attname,
  n_distinct,
  correlation
FROM pg_stats
WHERE schemaname = 'public'
  AND n_distinct > 100
  AND correlation < 0.1;
```

---

## 💾 BACKUP & RECOVERY

### Backup Strategy

```bash
#!/bin/bash
# scripts/backup-database.sh

BACKUP_DIR="/backups/postgresql"
DATE=$(date +%Y%m%d_%H%M%S)
DATABASE="{{DATABASE_NAME}}"

# Create backup directory
mkdir -p $BACKUP_DIR

# Dump database
pg_dump -h localhost -U postgres -F c -b -v \
  -f "${BACKUP_DIR}/${DATABASE}_${DATE}.backup" \
  $DATABASE

# Compress
gzip "${BACKUP_DIR}/${DATABASE}_${DATE}.backup"

# Upload to S3 (if configured)
if [ ! -z "$AWS_S3_BUCKET" ]; then
  aws s3 cp \
    "${BACKUP_DIR}/${DATABASE}_${DATE}.backup.gz" \
    "s3://${AWS_S3_BUCKET}/backups/postgres/"
fi

# Clean old backups (keep last 7 days)
find $BACKUP_DIR -name "*.backup.gz" -mtime +7 -delete

echo "Backup completed: ${DATABASE}_${DATE}.backup.gz"
```

### Restore Process

```bash
#!/bin/bash
# scripts/restore-database.sh

BACKUP_FILE=$1

if [ -z "$BACKUP_FILE" ]; then
  echo "Usage: ./restore-database.sh <backup_file>"
  exit 1
fi

# Stop application
systemctl stop myapp

# Drop existing database
dropdb {{DATABASE_NAME}}

# Create new database
createdb {{DATABASE_NAME}}

# Restore from backup
pg_restore -h localhost -U postgres -d {{DATABASE_NAME}} \
  -v $BACKUP_FILE

# Run migrations if needed
npx prisma migrate deploy

# Start application
systemctl start myapp

echo "Restore completed"
```

---

## 🔄 WORKFLOW

### Paso 1: Diseño de Esquema

```bash
Duración: 2-4 horas

Acciones:
1. Revisar requerimientos de datos
2. Crear diagrama ER
3. Definir tablas y relaciones
4. Establecer constraints
5. Planear índices

Output:
- Diagrama ER
- SQL schema
```

### Paso 2: Crear Migraciones

```bash
Duración: 1-2 horas

# Create migration
npx prisma migrate dev --name initial_schema

# Review generated SQL
cat prisma/migrations/*/migration.sql

Output:
- Migration files
```

### Paso 3: Optimización

```bash
Duración: 1-2 horas

Acciones:
1. Analizar queries comunes
2. Crear índices apropiados
3. Optimizar queries lentas
4. Setup monitoring

Output:
- Índices creados
- Queries optimizadas
```

### Checkpoints de Validación

- [ ] Schema normalizado apropiadamente
- [ ] Constraints definidos
- [ ] Índices en foreign keys
- [ ] Índices en columnas frecuentemente consultadas
- [ ] Triggers para data integrity
- [ ] Soft deletes implementados
- [ ] Timestamps en todas las tablas
- [ ] Backup strategy configurado
- [ ] Migrations versionadas
- [ ] Seeders para datos iniciales

---

## 🛠️ HERRAMIENTAS

```bash
# Prisma commands
npx prisma studio        # Visual database browser
npx prisma db push       # Push schema without migration
npx prisma db seed       # Run seeders
npx prisma format        # Format schema file

# PostgreSQL commands
psql -d mydb             # Connect to database
\dt                      # List tables
\d table_name            # Describe table
\di                      # List indexes
\timing                  # Enable query timing

# Performance analysis
EXPLAIN ANALYZE query;   # Analyze query execution
pg_stat_statements       # Query statistics
```

---

## ✅ CRITERIOS DE ACEPTACIÓN

- [ ] Schema diseñado y normalizado
- [ ] Migraciones versionadas
- [ ] Índices apropiados creados
- [ ] Constraints definidos
- [ ] Triggers para data integrity
- [ ] Queries optimizadas (< 100ms promedio)
- [ ] Backup automatizado configurado
- [ ] Seeders para datos de prueba
- [ ] Documentation de schema
- [ ] No queries N+1 en código

---

**Versión**: 1.0.0
**Última Actualización**: 2026-01-13
**Mantenedor**: Database Team
