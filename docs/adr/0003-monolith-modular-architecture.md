# ADR-0003: Arquitectura Monolito Modular

**Fecha**: 2026-01-20
**Status**: ✅ Accepted
**Decisor**: Architect Agent

---

## Contexto

Necesitamos decidir el patrón arquitectónico general para TravesIA. Las opciones principales son:

1. **Monolito tradicional**: Todo en una aplicación sin separación clara
2. **Monolito modular**: Una aplicación con módulos bien definidos
3. **Microservicios**: Servicios independientes comunicados por red

**Características del proyecto**:

- Equipo pequeño (Innovación)
- Volumen moderado (50 grupos/año)
- Complejidad de negocio alta
- Múltiples bounded contexts identificados
- Primera versión con deadline de 3 meses

---

## Decisión

**Implementaremos una arquitectura de Monolito Modular con Django Apps.**

Cada bounded context será una Django app independiente con sus propios modelos, vistas, serializers y lógica de negocio.

---

## Alternativas Consideradas

### Opción 1: Monolito Tradicional

**Pros**:

- Desarrollo más rápido inicialmente
- Sin complejidad de comunicación entre servicios
- Deployment simple

**Contras**:

- Código acoplado difícil de mantener
- Sin separación clara de responsabilidades
- Difícil de escalar componentes específicos
- Testing complejo
- Alto acoplamiento

### Opción 2: Microservicios

**Pros**:

- Escalado independiente por servicio
- Tecnologías diferentes por servicio
- Deploy independiente
- Aislamiento de fallos

**Contras**:

- Complejidad operacional alta
- Overhead de comunicación de red
- Distributed transactions complejas
- Requiere service mesh, API gateway
- Equipo pequeño puede verse abrumado
- Debugging más difícil
- Costo de infraestructura mayor

### Opción 3: Monolito Modular (Seleccionada)

**Pros**:

- Separación clara de bounded contexts
- Bajo acoplamiento entre módulos
- Deploy simple (una aplicación)
- Transacciones simples (misma DB)
- Debugging más fácil
- Menor costo de infraestructura
- Migración futura a microservicios posible
- Testing más simple

**Contras**:

- Escalado horizontal de toda la app
- No se pueden usar tecnologías diferentes por módulo
- Deploy de todo el sistema

---

## Justificación

1. **Equipo Pequeño**: Un monolito es más manejable con recursos limitados
2. **Time-to-Market**: Desarrollo y deployment más rápidos
3. **Volumen**: 50 grupos/año no requieren microservicios
4. **Complejidad Justa**: Módulos separados pero comunicación in-process
5. **Evolutivo**: Permite migrar a microservicios en el futuro si es necesario

---

## Consecuencias

### Positivas ✅

- Desarrollo más rápido (3 meses factible)
- Deployment simple con Docker
- Debugging y logging centralizados
- Transacciones ACID entre módulos
- Menor overhead operacional
- Codebase único facilita refactoring
- Testing más simple (integration tests in-memory)

### Negativas ⚠️

- Escalado de toda la aplicación (no por módulo)
- Deploy de todo el sistema para cualquier cambio
- Stack tecnológico único

### Riesgos y Mitigaciones

| Riesgo                     | Probabilidad | Impacto | Mitigación                                             |
| -------------------------- | ------------ | ------- | ------------------------------------------------------ |
| Acoplamiento entre módulos | Media        | Alto    | Enforced boundaries, code reviews, arquitectura clara  |
| Crecimiento descontrolado  | Media        | Medio   | Monitoreo de métricas de código, refactoring periódico |
| Performance insuficiente   | Baja         | Medio   | Caching, optimización de queries, escalado vertical    |

---

## Implementación

### Estructura de Proyecto

```
travesia/
├── manage.py
├── config/
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   ├── staging.py
│   │   └── production.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── circuits/              # Circuit Management Context
│   │   ├── models/
│   │   │   ├── program.py
│   │   │   ├── group.py
│   │   │   ├── passenger.py
│   │   │   └── itinerary.py
│   │   ├── serializers/
│   │   ├── views/
│   │   ├── repositories/
│   │   ├── services/
│   │   └── urls.py
│   ├── operations/            # Operations Context
│   │   ├── models/
│   │   │   ├── transportation.py
│   │   │   ├── accommodation.py
│   │   │   └── special_service.py
│   │   ├── serializers/
│   │   ├── views/
│   │   └── urls.py
│   ├── suppliers/             # Supplier Management Context
│   ├── financial/             # Financial Context
│   ├── documents/             # Document Management Context
│   └── analytics/             # Analytics Context
├── core/
│   ├── authentication/        # Auth común
│   ├── common/               # Utilities compartidas
│   │   ├── models.py        # BaseModel, TimeStampedModel
│   │   ├── exceptions.py
│   │   └── validators.py
│   └── integrations/         # Integraciones externas
│       ├── sunat/
│       ├── aws/
│       └── email/
├── static/
├── media/
└── tests/
    ├── integration/
    └── e2e/
```

### Principios de Diseño de Módulos

#### 1. Bajo Acoplamiento

```python
# ❌ MAL - Acoplamiento directo
from apps.financial.models import Invoice

class Group(models.Model):
    def generate_invoice(self):
        invoice = Invoice.objects.create(...)  # Dependencia directa

# ✅ BIEN - A través de eventos o servicios
from django.dispatch import receiver
from apps.circuits.signals import group_completed

@receiver(group_completed)
def create_invoice_for_group(sender, group_id, **kwargs):
    # Financial app escucha eventos de circuits app
    InvoiceService().create_from_group(group_id)
```

#### 2. Alta Cohesión

```python
# Cada app contiene TODO lo relacionado a su dominio
apps/circuits/
├── models/          # Modelos de dominio
├── serializers/     # Serialización API
├── views/           # Views/ViewSets
├── repositories/    # Acceso a datos
├── services/        # Lógica de negocio
├── signals.py       # Eventos del dominio
├── exceptions.py    # Excepciones específicas
└── urls.py          # URLs del módulo
```

#### 3. Interfaz Pública Clara

```python
# apps/circuits/__init__.py
# Exponer solo lo necesario
from .services import GroupService, PassengerService
from .models import Group, Passenger

__all__ = [
    'GroupService',
    'PassengerService',
    'Group',
    'Passenger',
]
```

### Comunicación Entre Módulos

```python
# Opción 1: Signals de Django
from django.dispatch import Signal, receiver

group_completed = Signal()

# En circuits/views.py
class GroupViewSet(viewsets.ModelViewSet):
    def complete_group(self, request, pk):
        group = self.get_object()
        group.status = 'COMPLETED'
        group.save()
        group_completed.send(sender=self.__class__, group_id=group.id)

# En financial/handlers.py
@receiver(group_completed)
def generate_liquidation(sender, group_id, **kwargs):
    AnalyticsService().generate_group_liquidation(group_id)
```

```python
# Opción 2: Service Layer
# apps/circuits/services/group_service.py
class GroupService:
    def complete_group(self, group_id):
        group = self.repository.find_by_id(group_id)
        group.status = 'COMPLETED'
        self.repository.save(group)

        # Llamar a otros servicios
        from apps.financial.services import InvoiceService
        InvoiceService().finalize_group_invoices(group_id)
```

---

## Migración Futura a Microservicios

Si el volumen crece significativamente, la estructura modular facilita la migración:

```
Monolito Modular                 →    Microservicios

apps/circuits/                   →    circuits-service/
apps/operations/                 →    operations-service/
apps/financial/                  →    financial-service/
```

**Indicadores para migrar**:

- \> 200 grupos/año
- Equipos especializados por contexto
- Necesidad de escalar componentes específicos independientemente
- Diferentes SLAs por servicio

---

## Herramientas de Monitoreo

```python
# Detectar violaciones de boundaries entre módulos
# scripts/check_module_dependencies.py

import ast
import os

ALLOWED_DEPENDENCIES = {
    'circuits': ['core.common', 'core.authentication'],
    'operations': ['core.common', 'circuits.models'],
    'financial': ['core.common', 'circuits.models', 'suppliers.models'],
}

def check_imports():
    violations = []
    for app in os.listdir('apps'):
        # Analizar imports y verificar contra ALLOWED_DEPENDENCIES
        pass
    return violations
```

---

## Referencias

- [Modular Monolith Architecture](https://www.kamilgrzybek.com/design/modular-monolith-primer/)
- [Django Apps Best Practices](https://docs.djangoproject.com/en/5.0/ref/applications/)
- [Monolith to Microservices](https://martinfowler.com/articles/break-monolith-into-microservices.html)

---

**Revisión**: Pendiente
**Próxima Revisión**: 2026-07-20 o cuando se alcancen 150 grupos/año
**Criterios de Re-evaluación**: Crecimiento > 200%, equipos > 10 personas, necesidad de escalar módulos independientemente
