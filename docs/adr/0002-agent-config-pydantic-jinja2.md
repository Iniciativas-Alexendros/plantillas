# ADR 0002: Esquema Pydantic y plantillas Jinja2 para agent-config

## Estado

Aceptado — en implementación (Bloque 2).

## Contexto

El módulo `agent-config` genera configuración cross-platform para Claude Code, OpenCode, Devin y Windsurf/Cascade a partir de una fuente YAML canónica. El generador actual (`generar_agent_configs.py`) es un script procedural que transforma directamente la fuente en cada artefacto. Esto dificulta:

- Validar la estructura de la fuente antes de generar.
- Reutilizar fragmentos entre plataformas.
- Testear la lógica de generación de forma aislada.
- Extender el formato sin romper consumidores.

## Decisión

Introducir un modelo de datos explícito con **Pydantic** para la fuente canónica y **Jinja2** como motor de plantillas para generar los artefactos de cada plataforma.

- El modelo Pydantic vive en `src/plantillas/agent_config/schema.py`.
- Las plantillas Jinja2 viven en `src/plantillas/agent_config/templates/`.
- El comando `plantillas sync agent-config` valida el esquema, renderiza y aplica los cambios con backup opcional.

## Consecuencias

- Validación temprana y mensajes de error claros.
- Separación entre datos (YAML) y presentación (Jinja2).
- Tests unitarios del modelo y del renderizado sin tocar el sistema de archivos.
- El generador procedural actual sigue siendo la implementación de referencia hasta que `sync` esté completo.

## Alternativas consideradas

- **Mantener el generador procedural**: rechazado por dificultad de testeo y acoplamiento.
- **Dataclasses en lugar de Pydantic**: Pydantic aporta validación, serialización y errores descriptivos sin código adicional.
- **Mustache en lugar de Jinja2**: Jinja2 es el estándar en el ecosistema Python y permite filtros personalizados.
