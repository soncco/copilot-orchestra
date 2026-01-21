# Modelo de Datos - TravesIA

**Versión**: 1.0
**Fecha**: 2026-01-20
**Responsable**: Architect Agent

---

## Diagrama Entidad-Relación

### Vista General

```
┌──────────────────────────────────────────────────────────────────┐
│                    CIRCUIT MANAGEMENT CONTEXT                     │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│   ┌─────────┐      ┌────────┐      ┌───────────┐                │
│   │ Program │─────<│ Group  │─────<│ Passenger │                │
│   └─────────┘  1:M └────┬───┘  1:M └───────────┘                │
│                         │                                         │
│                         │ 1:M                                     │
│                         │                                         │
│                    ┌────▼──────┐   ┌────────┐                    │
│                    │ Itinerary │   │ Flight │                    │
│                    └───────────┘   └────────┘                    │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│                     OPERATIONS CONTEXT                            │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│   ┌────────┐      ┌────────────────┐                             │
│   │ Group  │─────<│ Transportation │                             │
│   └───┬────┘  1:M └────────────────┘                             │
│       │                                                           │
│       │ 1:M      ┌───────────────┐      ┌───────┐                │
│       ├─────────<│ Accommodation │─────>│ Hotel │                │
│       │          └───────────────┘  M:1 └───────┘                │
│       │                                                           │
│       │ 1:M      ┌────────────────┐                               │
│       ├─────────<│ SpecialService │                               │
│       │          └────────────────┘                               │
│       │                                                           │
│       │ 1:M      ┌──────────────────┐                             │
│       └─────────<│ StaffAssignment  │                             │
│                  └──────────────────┘                             │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│                  SUPPLIER MANAGEMENT CONTEXT                      │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│   ┌──────────┐      ┌─────────────────┐      ┌─────────────┐    │
│   │ Supplier │─────<│ SupplierService │─────<│ PricePeriod │    │
│   └──────────┘  1:M └─────────────────┘  1:M └─────────────┘    │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│                      FINANCIAL CONTEXT                            │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│   ┌────────┐      ┌───────────┐                                  │
│   │ Group  │─────<│ GroupCost │                                  │
│   └───┬────┘  1:M └───────────┘                                  │
│       │                                                           │
│       │ 1:M      ┌─────────────────┐                              │
│       ├─────────<│ AdditionalSale  │                              │
│       │          └─────────────────┘                              │
│       │                                                           │
│       │ 1:M      ┌────────────┐      ┌──────────────┐            │
│       ├─────────<│  Invoice   │─────<│ BankDeposit  │            │
│       │          └────────────┘  1:M └──────────────┘            │
│       │                                                           │
│       │ 1:M      ┌────────────┐                                  │
│       └─────────<│ Commission │                                  │
│                  └────────────┘                                  │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│                  DOCUMENT MANAGEMENT CONTEXT                      │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│   ┌────────┐      ┌──────────┐                                   │
│   │ Group  │─────<│ Document │                                   │
│   └────────┘  1:M └──────────┘                                   │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

---

## Entidades Detalladas

### Circuit Management Context

#### Program

Programas de viaje ofrecidos (Perbol Chil, Galer, etc.)

```python
class Program(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    duration_days = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

**Índices**:

- `idx_program_code` en `code`
- `idx_program_active` en `is_active`

---

#### Group

Grupos de viaje programados

```python
class GroupType(models.TextChoices):
    YOUNG = 'YOUNG', 'Jóvenes'
    ADULT = 'ADULT', 'Adultos'

class GroupStatus(models.TextChoices):
    PLANNED = 'PLANNED', 'Planificado'
    CONFIRMED = 'CONFIRMED', 'Confirmado'
    IN_PROGRESS = 'IN_PROGRESS', 'En Progreso'
    COMPLETED = 'COMPLETED', 'Completado'
    CANCELLED = 'CANCELLED', 'Cancelado'

class Group(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    program = models.ForeignKey(Program, on_delete=models.PROTECT, related_name='groups')
    code = models.CharField(max_length=50, unique=True)  # ej: PERBOL-2026-05
    year = models.IntegerField()
    departure_date = models.DateField()
    return_date = models.DateField()
    group_type = models.CharField(max_length=10, choices=GroupType.choices)
    status = models.CharField(max_length=20, choices=GroupStatus.choices, default=GroupStatus.PLANNED)
    max_capacity = models.IntegerField()
    current_count = models.IntegerField(default=0)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

**Índices**:

- `idx_group_program_year` en `(program_id, year)`
- `idx_group_dates` en `(departure_date, return_date)`
- `idx_group_status` en `status`

**Constraints**:

- `return_date > departure_date`
- `current_count <= max_capacity`

---

#### Passenger

Pasajeros de cada grupo

```python
class Passenger(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='passengers')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    passport_number = encrypt(models.CharField(max_length=20))  # Encriptado
    date_of_birth = models.DateField()
    nationality = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    emergency_contact_name = models.CharField(max_length=200)
    emergency_contact_phone = models.CharField(max_length=20)
    dietary_restrictions = models.TextField(blank=True)
    medical_conditions = encrypt(models.TextField(blank=True))  # Encriptado
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

**Índices**:

- `idx_passenger_group` en `group_id`
- `idx_passenger_passport` en `passport_number` (encriptado, búsqueda limitada)
- `idx_passenger_name` en `(last_name, first_name)`

---

#### Itinerary

Itinerario día a día del programa

```python
class Itinerary(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='itineraries')
    day_number = models.IntegerField()
    location = models.CharField(max_length=200)
    activities = models.JSONField()  # Lista de actividades
    description = models.TextField()
    meals_included = models.JSONField()  # {breakfast: true, lunch: false, dinner: true}
    accommodation_city = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['program', 'day_number']
        ordering = ['program', 'day_number']
```

---

#### Flight

Vuelos de cada grupo

```python
class Flight(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='flights')
    flight_number = models.CharField(max_length=20)
    airline = models.CharField(max_length=100)
    departure_airport = models.CharField(max_length=10)  # Código IATA
    arrival_airport = models.CharField(max_length=10)
    departure_datetime = models.DateTimeField()
    arrival_datetime = models.DateTimeField()
    booking_reference = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

**Índices**:

- `idx_flight_group` en `group_id`
- `idx_flight_date` en `departure_datetime`

---

### Operations Context

#### Transportation

```python
class TransportationType(models.TextChoices):
    BUS = 'BUS', 'Bus'
    TRAIN = 'TRAIN', 'Tren'
    FLIGHT = 'FLIGHT', 'Vuelo'
    PRIVATE = 'PRIVATE', 'Transporte Privado'
    BOAT = 'BOAT', 'Bote'

class Transportation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    group = models.ForeignKey('circuits.Group', on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=TransportationType.choices)
    provider = models.ForeignKey('suppliers.Supplier', on_delete=models.PROTECT)
    route = models.CharField(max_length=200)  # ej: "Lima - Cusco"
    departure_datetime = models.DateTimeField()
    arrival_datetime = models.DateTimeField()
    code = models.CharField(max_length=50, blank=True)  # ej: "SIFA", "Cruz del Sur"
    capacity = models.IntegerField()
    reserved_seats = models.IntegerField()
    booking_reference = models.CharField(max_length=100)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

---

#### Hotel

```python
class Hotel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    capacity = models.IntegerField()
    amenities = models.JSONField()  # {wifi: true, pool: true, restaurant: true}
    rating = models.DecimalField(max_digits=2, decimal_places=1, null=True)
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

---

#### Accommodation

```python
class AccommodationStatus(models.TextChoices):
    PENDING = 'PENDING', 'Pendiente'
    CONFIRMED = 'CONFIRMED', 'Confirmado'
    CANCELLED = 'CANCELLED', 'Cancelado'

class Accommodation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    hotel = models.ForeignKey(Hotel, on_delete=models.PROTECT)
    group = models.ForeignKey('circuits.Group', on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    rooms_reserved = models.IntegerField()
    room_type = models.CharField(max_length=50)  # ej: "Doble", "Triple"
    status = models.CharField(max_length=20, choices=AccommodationStatus.choices)
    booking_reference = models.CharField(max_length=100)
    special_requests = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

**Índices**:

- `idx_accommodation_hotel_dates` en `(hotel_id, check_in_date, check_out_date)`
- `idx_accommodation_group` en `group_id`

---

### Supplier Management Context

#### Supplier

```python
class SupplierType(models.TextChoices):
    TRANSPORT = 'TRANSPORT', 'Transporte'
    HOTEL = 'HOTEL', 'Hotel'
    RESTAURANT = 'RESTAURANT', 'Restaurante'
    GUIDE = 'GUIDE', 'Guía'
    ACTIVITY = 'ACTIVITY', 'Actividad'
    OTHER = 'OTHER', 'Otro'

class Supplier(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=SupplierType.choices)
    contact_name = models.CharField(max_length=200)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    tax_id = models.CharField(max_length=20)  # RUC en Perú
    bank_account = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

**Índices**:

- `idx_supplier_type_active` en `(type, is_active)`
- `idx_supplier_search` GIN index para full-text search en `(name, contact_name)`

---

### Financial Context

#### GroupCost

```python
class CostCategory(models.TextChoices):
    TRANSPORT = 'TRANSPORT', 'Transporte'
    ACCOMMODATION = 'ACCOMMODATION', 'Alojamiento'
    FOOD = 'FOOD', 'Alimentación'
    ACTIVITY = 'ACTIVITY', 'Actividad'
    GUIDE = 'GUIDE', 'Guía'
    PERMIT = 'PERMIT', 'Permiso'
    OTHER = 'OTHER', 'Otro'

class Currency(models.TextChoices):
    USD = 'USD', 'Dólares'
    PEN = 'PEN', 'Soles'

class GroupCost(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    group = models.ForeignKey('circuits.Group', on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=CostCategory.choices)
    description = models.CharField(max_length=500)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, choices=Currency.choices)
    payment_date = models.DateField()
    supplier = models.ForeignKey('suppliers.Supplier', on_delete=models.PROTECT, null=True)
    invoice_number = models.CharField(max_length=100, blank=True)
    payment_method = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

**Índices**:

- `idx_cost_group_category` en `(group_id, category)`
- `idx_cost_payment_date` en `payment_date`

---

#### Invoice

```python
class InvoiceStatus(models.TextChoices):
    DRAFT = 'DRAFT', 'Borrador'
    SENT = 'SENT', 'Enviada'
    PAID = 'PAID', 'Pagada'
    CANCELLED = 'CANCELLED', 'Anulada'

class Invoice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    group = models.ForeignKey('circuits.Group', on_delete=models.PROTECT)
    invoice_number = models.CharField(max_length=50, unique=True)
    sunat_cdr = models.CharField(max_length=200, blank=True)  # Constancia SUNAT
    issue_date = models.DateField()
    due_date = models.DateField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, choices=Currency.choices)
    status = models.CharField(max_length=20, choices=InvoiceStatus.choices)
    xml_file = models.CharField(max_length=500, blank=True)  # S3 path
    pdf_file = models.CharField(max_length=500, blank=True)  # S3 path
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

**Índices**:

- `idx_invoice_status_date` en `(status, issue_date)`
- `idx_invoice_number` en `invoice_number` (unique)

---

## Volumen Estimado de Datos

### Año 1 (2026)

| Entidad        | Registros/año | Acumulado 5 años |
| -------------- | ------------- | ---------------- |
| Programs       | 4-6           | ~10              |
| Groups         | 50            | 250              |
| Passengers     | 1,500         | 7,500            |
| Itineraries    | 200           | 500              |
| Flights        | 100           | 500              |
| Transportation | 500           | 2,500            |
| Accommodations | 600           | 3,000            |
| Hotels         | 50            | 100              |
| Suppliers      | 100           | 200              |
| Group Costs    | 2,000         | 10,000           |
| Invoices       | 200           | 1,000            |
| Documents      | 5,000         | 25,000           |

**Total estimado en 5 años**: ~50,000 registros principales + documentos en S3

---

## Estrategia de Particionamiento

**No requerido inicialmente**. Si el volumen crece significativamente:

```sql
-- Particionar tabla de costos por año
CREATE TABLE group_costs_2026 PARTITION OF group_costs
    FOR VALUES FROM ('2026-01-01') TO ('2027-01-01');

CREATE TABLE group_costs_2027 PARTITION OF group_costs
    FOR VALUES FROM ('2027-01-01') TO ('2028-01-01');
```

---

## Referencias

- [PostgreSQL Data Modeling Best Practices](https://www.postgresql.org/docs/current/ddl.html)
- [Django Models Documentation](https://docs.djangoproject.com/en/5.0/topics/db/models/)
- [Database Design Patterns](https://www.databaseanswers.org/data_models/)
