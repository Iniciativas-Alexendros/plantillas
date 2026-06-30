# Motor de validación del Bloque 2

El sistema de validación se basa en un registro (`ValidatorRegistry`) que puede ejecutar validadores embebidos en Python o delegar en los scripts legacy de cada módulo.

## Arquitectura

```
modules.yaml
    ↓
plantillas.catalog.load_catalog()
    ↓
plantillas.registry.ValidatorRegistry
    ├─ plantillas.validators.<id> (validadores embebidos)
    └─ <módulo>/validar_*.py (scripts legacy)
```

## Cómo añadir un validador embebido

Crear `src/plantillas/validators/<id>.py` con una función `validate`:

```python
from pathlib import Path
from plantillas.catalog import Module
from plantillas.registry import ValidationResult, ValidatorFn


def validate(module: Module, root: Path) -> ValidationResult:
    target = root / module.path
    if not (target / "README.md").exists():
        return ValidationResult(module.id, False, "Falta README.md")
    return ValidationResult(module.id, True, "OK")
```

El registry descubre automáticamente los módulos importables.

## Cómo mantener un validador legacy

Si el módulo tiene `validator: <módulo>/validar_*.py` en `modules.yaml`, el registry ejecuta:

```bash
python <script> <path> --strict
```

Si el script no existe, el registry reporta `No validator configured` y no falla.

## Salida

Los validadores devuelven `ValidationResult`:

- `ok`: bool.
- `message`: descripción del resultado.

## Formato de salida CLI

```text
✅ agentes: OK
⚠️ artefactos: No validator configured
❌ commands: Validation failed: ...
```

## Tests

```bash
pytest tests/test_registry.py -v   # pendiente de crear
pytest tests/test_cli.py -v
```

## Migración planeada

A largo plazo, los validadores legacy se migrarán a `plantillas.validators.<id>` para facilitar tests y reutilizar checks entre módulos.
