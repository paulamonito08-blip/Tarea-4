# Sistema Integral de Gestión de Clientes, Servicios y Reservas

## Descripción del proyecto

Este proyecto fue desarrollado para la actividad Fase 4 del curso de Programación (213023) de la Universidad Nacional Abierta y a Distancia - UNAD.

El sistema simula la gestión de clientes, servicios y reservas para la empresa ficticia **Software FJ**, aplicando los principios fundamentales de la Programación Orientada a Objetos (POO) y manejo avanzado de excepciones en Python.

La aplicación funciona sin bases de datos y utiliza únicamente objetos, listas y archivos de texto para el registro de eventos y errores.

---

## Objetivos del proyecto

- Aplicar Programación Orientada a Objetos en Python.
- Implementar abstracción, herencia, polimorfismo y encapsulación.
- Utilizar manejo avanzado de excepciones.
- Simular operaciones reales de reservas y servicios.
- Garantizar estabilidad y robustez del sistema ante errores.

---

## Tecnologías utilizadas

- Python 3
- Programación Orientada a Objetos (POO)
- Git y GitHub

---

## Funcionalidades principales

### Gestión de clientes
- Registro de clientes válidos e inválidos.
- Validación de nombres, identificación y correo electrónico.
- Encapsulación de datos mediante propiedades.

### Gestión de servicios
El sistema incluye tres servicios especializados:

- RoomService
- EquipmentService
- AdvisoryService

Cada servicio implementa:
- Polimorfismo
- Métodos sobrescritos
- Validaciones personalizadas
- Cálculo de costos con impuestos y descuentos

### Gestión de reservas
- Confirmación de reservas
- Cancelación de reservas
- Procesamiento de reservas
- Validación de disponibilidad de servicios

### Manejo de excepciones
El sistema implementa:
- Excepciones personalizadas
- try/except
- try/except/else
- try/except/finally
- Encadenamiento de excepciones

### Registro de logs
Todos los errores y eventos importantes son almacenados automáticamente en:

```bash
log.txt