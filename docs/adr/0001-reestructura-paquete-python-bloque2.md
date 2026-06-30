# ADR 0001: Reestructura del repositorio como paquete Python (Bloque 2)

## Estado

Aceptado — en implementación (Bloque 2).

## Contexto

El sistema de plantillas empezó como una colección de directorios con scripts de validación independientes. Cada módulo tenía su propio validador, workflow de CI y mecanismo de copia manual. A medida que creció a 12 módulos canónicos, surgieron problemas de mantenimiento:

- Duplicación de lógica entre validadores.
- Dificultad para descubrir qué módulos existen y qué validan.
- Instalación dependiente de clonar el repositorio completo.
- Falta de una interfaz unificada para validar, sincronizar y crear módulos.

## Decisión

Convertir el repositorio en un paquete Python moderno (`src/plantillas/`) con:

- `pyproject.toml` usando `hatchling` como build backend.
- CLI unificada `plantillas` construida con `typer`.
- Catálogo central `modules.yaml` como única fuente de verdad de los módulos.
- Registry de validadores que puede delegar en scripts legacy o ejecutar validadores embebidos en `plantillas.validators`.
- Dependencias: `pyyaml`, `pydantic`, `jinja2`, `typer`, `pytest` y `ruff`.

## Consecuencias

- Se reduce la duplicación: el CLI y el catálogo orquestan a los validadores.
- La instalación se simplifica a `pip install -e .`.
- Los validadores legacy siguen funcionando durante la transición.
- Se añade complejidad inicial: entorno virtual, dependencias y packaging.
- El repositorio deja de ser solo una carpeta de plantillas; pasa a ser también un proyecto Python.

## Alternativas consideradas

- **Mantener scripts independientes**: rechazado por escalabilidad y duplicación.
- **Poetry en lugar de hatchling**: rechazado para mantener el build system ligero y estándar (PEP 621/518).
- **Click en lugar de typer**: typer aporta tipado, anotaciones y testing integrado con menos código.
