# Plantilla MCEOD L3 — Subproyecto

- Versión: 1.0.0
- Fecha: 2026-05-27
- Nivel: L3 (subproyecto dentro de un monorepo)
- Criterio de uso: aplicar SOLO cuando el subproyecto pertenece a disciplinas claramente distintas del L2 padre (p. ej. IaC + frontend + ML en un mismo repo).

## Placeholders disponibles
- `{{SUBPROJECT_NAME}}` — nombre del subproyecto.
- `{{PARENT_REPO}}` — ruta o nombre del repo padre.

## Procedimiento
```
~/.claude/scripts/claude-deploy.sh apply --level=L3 \
    --scope=/home/alexendros/Repositorios/<repo>/<subproject> \
    --var SUBPROJECT_NAME="<sub>" \
    --var PARENT_REPO="<repo>"
```

## Convención
- L3 no duplica L2. Solo declara overrides.
- Si el override es marginal, no se crea L3: se ajusta el CLAUDE.md del L2.
