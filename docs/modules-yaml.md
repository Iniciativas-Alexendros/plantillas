# `modules.yaml` — Catálogo de módulos

> Estado: propuesto / en implementación. Será la única fuente de verdad para
> CI, pre-commit, tests y el CLI del Bloque 2.

## Ubicación

`modules.yaml` en la raíz del repo.

## Esquema

```yaml
version: "1.0"
modules:
  - name: agentes
    type: single-file
    validator: agentes/validar_agente.py
    example: agentes/ejemplo_agente.md
    template: agentes/plantilla_agente.md
    singular: agente
    description: Orquestador hub-and-spoke con subagentes

  - name: skills
    type: directory
    validator: skills/validar_skill.py
    example: skills/ejemplo_skill
    template: skills/plantilla_skill
    singular: skill
    description: Skills auto-activables por descripción

  - name: agent-config
    type: special
    validator: agent-config/validar_agent_config.py
    example: agent-config
    template: ""
    singular: agent_config
    description: Configuración cross-platform para agentes
```

## Campos

| Campo | Tipo | Requerido | Descripción |
| ----- | ---- | --------- | ----------- |
| `name` | string | ✅ | Nombre del módulo en `kebab-case`. |
| `type` | string | ✅ | `single-file`, `directory` o `special`. |
| `validator` | string | ✅ | Path al script o entry point del validador. |
| `example` | string | ✅ | Path al ejemplo o, para módulos especiales, a la raíz del módulo. |
| `template` | string | ❌ | Path a la plantilla. |
| `singular` | string | ✅ | Forma singular para mensajes del CLI. |
| `description` | string | ✅ | Descripción corta. |

## Tipos

- `single-file`: el ejemplo y la plantilla son archivos (`.md`, `.sh.template`).
- `directory`: el ejemplo y la plantilla son directorios.
- `special`: el módulo no sigue el patrón estándar (ej. `agent-config`, `modulo`, `proyecto`).

## Consumidores

- `plantillas validate --all` carga `modules.yaml` y ejecuta cada validador.
- CI (`ci.yml`) lo usa para construir la matriz de jobs.
- `pre-commit` lo usa para ejecutar validadores en los ejemplos.
- `tests/test_smoke.py` lo usa para generar casos de prueba.
- `validar_repo.py` lo usa para comprobar `DIRECTORIOS_PERMITIDOS`.

## Test de sync

El test `test_modules_yaml_sync` verifica que:

- Todos los módulos de `modules.yaml` aparecen en `INDEX.md`.
- `README.md` contiene los 12 nombres de módulo.
- Los paths indicados existen físicamente.
- No hay módulos duplicados.
