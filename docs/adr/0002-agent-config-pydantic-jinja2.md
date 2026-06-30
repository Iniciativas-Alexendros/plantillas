# ADR 0002 — Usar Pydantic y Jinja2 para agent-config

## Estado

Propuesto (Bloque 2).

## Contexto

`agent-config` genera 6 artefactos cross-platform a partir de
`plantilla_agent_config.yaml`. Actualmente los renderers están implementados en
Python puro (`generar_agent_configs.py`), mezclando lógica de negocio con
formato de salida. Esto hace que:

- Sea difícil validar que el YAML fuente cumple un esquema.
- Sea difícil testar la salida sin escribir en `$HOME`.
- Añadir un nuevo target requiera tocar código Python.
- El drift check sea más complejo de mantener.

## Decisión

- Modelar el YAML fuente con **Pydantic v2** (`AgentConfig`).
- Usar **Jinja2** para los templates de cada target (Claude, OpenCode, Devin, Windsurf).
- Generar los artefactos en un directorio de ejemplo (`ejemplo_agent_config/`) y
  comparar con snapshot tests.
- Exponer la sincronización como `plantillas sync agent-config`.

## Consecuencias

### Positivas

- Validación estricta del YAML fuente al cargar.
- Tests deterministas sin mutar `$HOME`.
- Añadir un nuevo target = añadir un template `.j2`.
- Separación clara entre datos (`AgentConfig`) y presentación (Jinja2).

### Negativas

- Añade dependencias (`pydantic`, `jinja2`).
- Requiere migrar los renderers actuales a templates.
- El template debe mantenerse alineado con los cambios de schema.

## Alternativas consideradas

- **Renderers Python puro**: actualmente en uso, pero difícil de testar. Rechazado para el Bloque 2.
- **Dataclasses + manual**: menos seguro que Pydantic. Rechazado.
- **JSON Schema**: útil para validación, pero no da modelos tipados. Rechazado.
