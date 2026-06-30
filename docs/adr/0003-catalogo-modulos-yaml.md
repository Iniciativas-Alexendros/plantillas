# ADR 0003: Catálogo central de módulos en `modules.yaml`

## Estado

Aceptado — en implementación (Bloque 2).

## Contexto

La información sobre los módulos canónicos estaba dispersa entre `validar_repo.py` (listas hardcodeadas), `INDEX.md`, `README.md` y los propios directorios de cada módulo. Esto provocaba inconsistencias cuando se añadía o modificaba un módulo.

## Decisión

Crear un catálogo central en `modules.yaml` con la definición de cada módulo: `id`, `name`, `description`, `type`, `path`, `validator`, `example`, `template`, `tags` e `init_command`.

- El catálogo se lee con Pydantic (`src/plantillas/catalog.py`).
- `validar_repo.py` y la CLI lo consumen como fuente de verdad.
- Los tests verifican que todos los módulos canónicos estén presentes y que los scripts a los que apuntan existan.

## Consecuencias

- Una sola fuente de verdad para los módulos.
- Reducción de listas duplicadas en validadores y documentación.
- Facilidad para añadir metadatos futuros (versiones, dependencias, estado experimental).
- Los consumidores legacy deben migrar gradualmente a leer `modules.yaml`.

## Alternativas consideradas

- **JSON**: YAML es más legible para editores humanos y es el formato habitual de la configuración de agentes.
- **TOML**: menos adecuado para listas de objetos anidados.
- **Inventario en Python**: añadiría dependencia de código para cualquier consumidor no Python.
