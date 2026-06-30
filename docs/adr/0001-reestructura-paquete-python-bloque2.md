# ADR 0001 — Reestructurar el repo como paquete Python con CLI unificado

## Estado

Propuesto (Bloque 2).

## Contexto

El repo de plantillas creció como una colección de scripts sueltos en la raíz:
cada módulo tiene su `validar_<modulo>.py`, las listas de módulos están
duplicadas en `.github/workflows/validar-todos.yml`, `tests/test_smoke.py`,
`.pre-commit-config.yaml` y `validar_repo.py`, y los validadores importan el
motor reusable mediante `sys.path.insert`. Esto dificulta:

- Añadir nuevos módulos (hay que tocar 4+ archivos).
- Testar los validadores (dependen de la raíz del repo).
- Reutilizar el motor en otros repos (no es un paquete instalable).
- Centralizar la configuración (CI, pre-commit y tests pueden desincronizarse).

## Decisión

Convertir el repo en un paquete Python estándar con:

- `pyproject.toml` como manifest.
- `src/plantillas/` como raíz del paquete.
- CLI `plantillas` implementado con `click`.
- Motor de validación en `src/plantillas/validators/`.
- Catálogo de módulos en `modules.yaml` (única fuente de verdad).
- Wrappers de compatibilidad para los scripts actuales.

## Consecuencias

### Positivas

- Instalación reproducible: `uv pip install -e .`.
- Tests unitarios sin depender de la raíz del repo.
- Nuevos módulos se registran en `modules.yaml` y en el registry de validadores.
- CI, pre-commit y tests leen el mismo catálogo.
- Salida de validación uniforme (`json`, `github`, `text`).

### Negativas

- Requiere reescribir imports y añadir `pyproject.toml`.
- Los scripts actuales deben mantenerse como wrappers temporalmente.
- Mayor complejidad inicial para contribuidores ocasionales.

## Alternativas consideradas

- **Mantener scripts sueltos**: simple pero no escala. Rechazado.
- **Usar `setuptools` con `setup.py`**: `pyproject.toml` es el estándar actual. Rechazado.
- **Separar el framework en otro repo**: añade overhead de sincronización. Rechazado; el framework vive en el mismo repo.
