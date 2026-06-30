# ADR 0003 — Catálogo central de módulos en `modules.yaml`

## Estado

Propuesto (Bloque 2).

## Contexto

La lista de módulos canónicos está duplicada en al menos cuatro lugares:

- `.github/workflows/validar-todos.yml` (matriz de CI).
- `tests/test_smoke.py` (`MODULOS`).
- `.pre-commit-config.yaml` (hook `validate-modules`).
- `validar_repo.py` (`MODULOS_CANONICOS`, `DIRECTORIOS_PERMITIDOS`).

Cualquier cambio (añadir/renombrar/eliminar un módulo) requiere editar todos
esos archivos, lo que genera riesgo de desincronización.

## Decisión

Crear un `modules.yaml` en la raíz del repo como **única fuente de verdad**. Cada
entrada describe:

- `name`: nombre del módulo (kebab-case).
- `type`: `single-file`, `directory`, `special`.
- `validator`: path al script/entry point del validador.
- `example`: path al ejemplo o plantilla.
- `template`: path a la plantilla (opcional).
- `singular`: forma singular para el CLI.
- `description`: descripción corta.

CI, pre-commit, tests y el CLI leerán este archivo. Se añadirá un test de sync
que compare `modules.yaml` con `INDEX.md` y `README.md`.

## Consecuencias

### Positivas

- Un solo lugar para añadir/renombrar/eliminar módulos.
- CI, tests y pre-commit siempre consistentes.
- El CLI puede generar ayuda dinámica (`plantillas config list`).
- Posibilita validar que todos los módulos listados existen físicamente.

### Negativas

- Añade una dependencia crítica: si `modules.yaml` es inválido, todo el sistema falla.
- Requiere parser y test de sync.
- Los workflows actuales deben migrar a leer el YAML.

## Alternativas consideradas

- **JSON**: menos legible para humanos. Rechazado.
- **Python puro (`modules.py`)**: requiere importar código para leer configuración. Rechazado.
- **Mantener duplicación**: no escala. Rechazado.
