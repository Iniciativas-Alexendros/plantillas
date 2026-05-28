# Plantilla MCEOD L1 — Categoría

- Versión: 1.0.0
- Fecha: 2026-05-27
- Nivel: L1 (agregador de categoría, p. ej. `~/Repositorios/.claude/`, `~/ShellScripts/.claude/`)
- Propósito: compartir convenciones entre los proyectos de una misma categoría sin saturar L0 ni duplicarlas en cada L2.

## Placeholders disponibles
- `{{CATEGORY_NAME}}` — nombre humano de la categoría (Repositorios, ShellScripts).
- `{{CATEGORY_PATH}}` — ruta absoluta del directorio padre.

## Cuándo aplicar L1 vs L0/L2
- L0: la convención afecta a todo el `$HOME`.
- L1: la convención afecta solo a los proyectos de una categoría concreta.
- L2: la convención es exclusiva de un repo.

## Procedimiento
```
~/.claude/scripts/claude-deploy.sh apply --level=L1 \
    --scope=/home/alexendros/Repositorios \
    --var CATEGORY_NAME="Repositorios" \
    --var CATEGORY_PATH="/home/alexendros/Repositorios"
```

## Archivos
- `CLAUDE.md.template` — normas de la categoría, hereda de L0.
- `settings.json.template` — esqueleto mínimo, sin secretos.
- `settings.local.json.example` — esqueleto local; NO se versiona.
- `gitignore.template` — entradas mínimas.
