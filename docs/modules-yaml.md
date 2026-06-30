# Catálogo `modules.yaml`

`modules.yaml` es la fuente de verdad del sistema de plantillas. Define los módulos canónicos, sus metadatos, validadores y comandos de inicialización.

## Ubicación

```
modules.yaml
```

Se lee mediante `plantillas.catalog.load_catalog()`.

## Esquema

```yaml
version: "2.0.0-dev"
modules:
  - id: agent-config
    name: Configuración cross-platform para agentes
    description: Fuente canónica YAML que genera configuración para Claude Code, OpenCode, Devin y Windsurf/Cascade.
    type: module
    path: agent-config
    validator: agent-config/validar_agent_config.py
    example: agent-config
    template: agent-config/plantilla_agent_config.yaml
    tags: [config, agents, cross-platform]
    init_command: "plantillas sync agent-config"
```

## Campos

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `version` | string | Sí | Versión del catálogo. |
| `modules` | lista | Sí | Lista de entradas de módulo. |
| `modules[].id` | string | Sí | Identificador único y kebab-case. |
| `modules[].name` | string | Sí | Nombre legible. |
| `modules[].description` | string | Sí | Descripción de una línea. |
| `modules[].type` | string | Sí | `module`, `meta`, `docs` o `tool`. |
| `modules[].path` | string | Sí | Directorio del módulo relativo a la raíz. |
| `modules[].validator` | string | No | Ruta al validador legacy. |
| `modules[].example` | string | No | Ruta al ejemplo o directorio de ejemplo. |
| `modules[].template` | string | No | Ruta a la plantilla principal. |
| `modules[].tags` | lista | No | Etiquetas para clasificación. |
| `modules[].init_command` | string | No | Comando recomendado para inicializar el módulo. |

## Tipos de módulo

- `module`: módulo canónico con validador y ejemplo.
- `meta`: módulos de soporte como `modulo` o `proyecto`.
- `docs`: documentación transversal como ADRs o el dossier.
- `tool`: utilidades internas del sistema.

## Consumidores

- `plantillas.cli`: lista, valida y sincroniza módulos.
- `plantillas.registry`: descubre validadores embebidos o delega en scripts legacy.
- `validar_repo.py`: valida la estructura de raíz y de módulos.

## Tests

```bash
pytest tests/test_catalog.py -v
```

El test carga el catálogo y verifica que todos los módulos canónicos estén presentes.
