# Plantilla MCEOD L2 — Proyecto

- Versión: 1.0.0
- Fecha: 2026-05-27
- Nivel: L2 (configuración de un repositorio individual)
- Propósito: aislar instrucciones, skills, hooks, permisos y MCP propios del repo sin contaminar L0 ni L1.

## Placeholders disponibles
- `{{REPO_NAME}}` — nombre corto del repo.
- `{{REPO_PURPOSE}}` — descripción del propósito del repo en una frase.
- `{{REPO_STACK}}` — stack tecnológico principal.
- `{{REPO_OWNERS}}` — operador(es) responsables.

## Cuándo aplicar L2 vs L1/L3
- L1: la convención es propia de toda la categoría.
- L2: la convención es exclusiva del repo.
- L3: solo si el repo es monorepo con subproyectos de disciplinas claramente distintas.

## Procedimiento
```
~/.claude/scripts/claude-deploy.sh apply --level=L2 \
    --scope=/home/alexendros/Repositorios/<repo> \
    --var REPO_NAME="<repo>" \
    --var REPO_PURPOSE="..." \
    --var REPO_STACK="..." \
    --var REPO_OWNERS="..."
```

## Estructura desplegada
- `CLAUDE.md` — instrucciones del repo.
- `settings.json` — compartible, sin secretos.
- `settings.local.json.example` — el operador lo copia a `settings.local.json` (no versionado).
- `permissions/`, `skills/`, `agents/`, `commands/`, `hooks/` — directorios reservados.

## Convenciones heredadas
- Hereda de `~/.claude/CLAUDE.md` (L0) y, si existe, del L1 de su categoría.
- Las excepciones se documentan en el CLAUDE.md del propio L2.
