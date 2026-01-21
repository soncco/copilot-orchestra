# TravesIA Database - Quick Reference

## 📊 Tablas por Contexto

### Circuit Management Context (5 tablas)

| Tabla         | Propósito                                     | Registros Estimados |
| ------------- | --------------------------------------------- | ------------------- |
| `programs`    | Programas de viaje (Perbol Chil, Galer, etc.) | ~10                 |
| `groups`      | Grupos programados por año                    | 50/año              |
| `passengers`  | Pasajeros de cada grupo                       | 1,500/año           |
| `itineraries` | Itinerario día a día                          | ~200                |
| `flights`     | Información de vuelos                         | 100/año             |

### Supplier Management Context (4 tablas)

| Tabla               | Propósito                | Registros Estimados |
| ------------------- | ------------------------ | ------------------- |
| `suppliers`         | Proveedores de servicios | ~200                |
| `supplier_services` | Servicios ofrecidos      | ~500                |
| `price_periods`     | Precios por período      | ~1,000              |
| `exchange_rates`    | Tasas de cambio USD/PEN  | ~365/año            |

### Operations Context (6 tablas)

| Tabla               | Propósito                                 | Registros Estimados |
| ------------------- | ----------------------------------------- | ------------------- |
| `hotels`            | Hoteles disponibles                       | ~100                |
| `transportation`    | Transporte para grupos                    | 500/año             |
| `accommodations`    | Reservas de hotel                         | 600/año             |
| `special_services`  | Servicios especiales (Machu Picchu, etc.) | 200/año             |
| `staff`             | Personal (guías, cocineros, etc.)         | ~50                 |
| `staff_assignments` | Asignaciones de personal                  | 300/año             |

### Financial Context (5 tablas)

| Tabla              | Propósito              | Registros Estimados |
| ------------------ | ---------------------- | ------------------- |
| `group_costs`      | Costos por grupo       | 2,000/año           |
| `additional_sales` | Ventas adicionales     | 500/año             |
| `commissions`      | Comisiones de personal | 100/año             |
| `invoices`         | Facturas SUNAT         | 200/año             |
| `bank_deposits`    | Depósitos bancarios    | 200/año             |

### Document Management Context (1 tabla)

| Tabla       | Propósito                      | Registros Estimados |
| ----------- | ------------------------------ | ------------------- |
| `documents` | Referencias a documentos en S3 | 5,000/año           |

### Authentication & Users Context (3 tablas)

| Tabla           | Propósito             | Registros Estimados |
| --------------- | --------------------- | ------------------- |
| `users`         | Usuarios del sistema  | ~20                 |
| `user_sessions` | Sesiones activas JWT  | ~50                 |
| `audit_log`     | Registro de auditoría | 10,000/año          |

---

## 🔑 Relaciones Principales

```
programs
  └── groups (1:M)
       ├── passengers (1:M)
       ├── flights (1:M)
       ├── transportation (1:M)
       ├── accommodations (1:M)
       ├── special_services (1:M)
       ├── group_costs (1:M)
       ├── additional_sales (1:M)
       ├── commissions (1:M)
       ├── invoices (1:M)
       ├── documents (1:M)
       └── staff_assignments (1:M)

suppliers
  ├── supplier_services (1:M)
  │    └── price_periods (1:M)
  ├── transportation (1:M)
  └── group_costs (1:M)

hotels
  └── accommodations (1:M)

staff
  └── staff_assignments (1:M)

invoices
  └── bank_deposits (1:M)
```

---

## 📋 ENUMS Reference

### group_type

- `YOUNG` - Grupos de jóvenes
- `ADULT` - Grupos de adultos

### group_status

- `PLANNED` - Planificado
- `CONFIRMED` - Confirmado
- `IN_PROGRESS` - En progreso
- `COMPLETED` - Completado
- `CANCELLED` - Cancelado

### supplier_type

- `TRANSPORT` - Transporte
- `HOTEL` - Hotel
- `RESTAURANT` - Restaurante
- `GUIDE` - Guía
- `ACTIVITY` - Actividad
- `OTHER` - Otro

### currency

- `USD` - Dólares
- `PEN` - Soles peruanos

### transportation_type

- `BUS` - Bus
- `TRAIN` - Tren
- `FLIGHT` - Vuelo
- `PRIVATE` - Transporte privado
- `BOAT` - Bote

### accommodation_status

- `PENDING` - Pendiente
- `CONFIRMED` - Confirmado
- `CANCELLED` - Cancelado

### special_service_type

- `MACHU_PICCHU` - Entrada Machu Picchu
- `SALCANTAY` - Logística Salcantay
- `GUIDE` - Guía
- `ENTRANCE_FEE` - Entrada
- `ACTIVITY` - Actividad
- `OTHER` - Otro

### staff_role

- `GUIDE` - Guía
- `COOK` - Cocinero
- `MULETEER` - Arriero
- `TOUR_CONDUCTOR` - Conductor de tour
- `DRIVER` - Conductor
- `OTHER` - Otro

### cost_category

- `TRANSPORT` - Transporte
- `ACCOMMODATION` - Alojamiento
- `FOOD` - Alimentación
- `ACTIVITY` - Actividad
- `GUIDE` - Guía
- `PERMIT` - Permiso
- `OTHER` - Otro

### invoice_status

- `DRAFT` - Borrador
- `SENT` - Enviada
- `PAID` - Pagada
- `CANCELLED` - Anulada

### payment_method

- `CASH` - Efectivo
- `BANK_TRANSFER` - Transferencia bancaria
- `CREDIT_CARD` - Tarjeta de crédito
- `DEBIT_CARD` - Tarjeta de débito
- `CHECK` - Cheque
- `OTHER` - Otro

### commission_type

- `TOUR_CONDUCTOR` - Conductor de tour
- `GUIDE` - Guía
- `SALES` - Ventas
- `OTHER` - Otro

### user_role

- `ADMIN` - Administrador
- `OPERATIONS_MANAGER` - Gerente de operaciones
- `TOUR_CONDUCTOR` - Conductor de tour
- `ACCOUNTANT` - Contador
- `VIEWER` - Visualizador

### document_category

- `INVOICE` - Factura
- `TICKET` - Ticket
- `PASSPORT` - Pasaporte
- `CONTRACT` - Contrato
- `ITINERARY` - Itinerario
- `RECEIPT` - Recibo
- `REPORT` - Reporte
- `OTHER` - Otro

### audit_action

- `CREATE` - Crear
- `UPDATE` - Actualizar
- `DELETE` - Eliminar
- `VIEW` - Ver
- `LOGIN` - Inicio de sesión
- `LOGOUT` - Cierre de sesión

---

## 🔍 Índices Más Importantes

### Performance Crítica

```sql
idx_groups_program_year         -- Búsqueda de grupos
idx_passengers_group            -- Pasajeros por grupo
idx_group_costs_group_category  -- Costos financieros
idx_invoices_status_date        -- Facturas por estado
```

### Full-Text Search

```sql
idx_suppliers_search            -- Búsqueda de proveedores
idx_documents_search            -- Búsqueda de documentos
```

### Fechas y Rangos

```sql
idx_groups_dates                -- Grupos por fechas
idx_accommodations_hotel_dates  -- Disponibilidad de hoteles
idx_price_periods_dates         -- Precios vigentes
```

---

## ⚡ Queries Comunes

### Obtener grupos activos de 2026

```sql
SELECT g.code, g.departure_date, p.name, COUNT(pass.id) as passenger_count
FROM groups g
JOIN programs p ON g.program_id = p.id
LEFT JOIN passengers pass ON g.id = pass.group_id
WHERE g.year = 2026
  AND g.status IN ('CONFIRMED', 'IN_PROGRESS')
GROUP BY g.id, g.code, g.departure_date, p.name
ORDER BY g.departure_date;
```

### Costos totales por grupo

```sql
SELECT
    g.code,
    SUM(CASE WHEN gc.currency = 'USD' THEN gc.amount ELSE 0 END) as total_usd,
    SUM(CASE WHEN gc.currency = 'PEN' THEN gc.amount ELSE 0 END) as total_pen
FROM groups g
LEFT JOIN group_costs gc ON g.id = gc.group_id
WHERE g.id = 'group-uuid-here'
GROUP BY g.code;
```

### Disponibilidad de hotel

```sql
SELECT
    h.name,
    h.capacity,
    COUNT(a.id) as reservations,
    h.capacity - COUNT(a.id) as available
FROM hotels h
LEFT JOIN accommodations a ON h.id = a.hotel_id
    AND a.check_in_date <= '2026-06-20'
    AND a.check_out_date >= '2026-06-15'
    AND a.status = 'CONFIRMED'
WHERE h.city = 'Cusco'
  AND h.is_active = TRUE
GROUP BY h.id, h.name, h.capacity;
```

### Facturas pendientes

```sql
SELECT
    i.invoice_number,
    i.issue_date,
    i.due_date,
    i.amount,
    i.currency,
    g.code as group_code
FROM invoices i
JOIN groups g ON i.group_id = g.id
WHERE i.status IN ('DRAFT', 'SENT')
  AND i.due_date < CURRENT_DATE + INTERVAL '7 days'
ORDER BY i.due_date;
```

### Proveedores por rating

```sql
SELECT
    s.name,
    s.type,
    s.rating,
    COUNT(DISTINCT ss.id) as services_count,
    COUNT(DISTINCT gc.id) as transactions_count
FROM suppliers s
LEFT JOIN supplier_services ss ON s.id = ss.supplier_id
LEFT JOIN group_costs gc ON s.id = gc.supplier_id
WHERE s.is_active = TRUE
GROUP BY s.id, s.name, s.type, s.rating
ORDER BY s.rating DESC NULLS LAST;
```

---

## 🛠️ Comandos de Mantenimiento

### Ver tamaño de tablas

```sql
SELECT
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC
LIMIT 10;
```

### Vacuum y análisis

```sql
VACUUM ANALYZE groups;
VACUUM ANALYZE passengers;
VACUUM ANALYZE group_costs;
```

### Estadísticas de queries

```sql
-- Requiere pg_stat_statements
SELECT
    LEFT(query, 50) as query_start,
    calls,
    ROUND(mean_time::numeric, 2) as avg_ms,
    ROUND(total_time::numeric, 2) as total_ms
FROM pg_stat_statements
WHERE query NOT LIKE '%pg_stat_statements%'
ORDER BY mean_time DESC
LIMIT 20;
```

---

## 🔐 Seguridad

### Campos que requieren encriptación en app

- `passengers.passport_number`
- `passengers.medical_conditions`
- `users.mfa_secret`
- `users.password_hash` (bcrypt/argon2)

### Datos sensibles

- Toda información financiera
- Pasaportes y datos personales
- Documentos confidenciales (`is_confidential = TRUE`)

### Audit trail

Todas las operaciones críticas se registran en `audit_log`:

- Cambios en grupos
- Transacciones financieras
- Cambios en proveedores
- Acciones de usuarios

---

## 📦 Backups

### Estrategia recomendada

- **Diarios**: Mantener 7 días
- **Semanales**: Mantener 4 semanas
- **Mensuales**: Mantener 12 meses
- **Anuales**: Indefinido

### Comando manual

```bash
./database/scripts/backup.sh
```

### Verificar backups

```bash
ls -lh ./backups/
```

---

**Versión**: 1.0
**Fecha**: 2026-01-20
**Mantenedor**: Database Agent
