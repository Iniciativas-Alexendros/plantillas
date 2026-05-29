# Plantilla MCEOD L0 — Global

- Versión: 1.0.0
- Fecha: 2026-05-27
- Nivel: L0 (configuración global del usuario en `~/.claude/`)
- Propósito: definir el canon transversal del operador (idioma, normas de scripting, SUDAUTH, distinciones lingüísticas) y servir como punto de referencia para L1/L2/L3.

## Placeholders disponibles
- `{{USER_NAME}}` — nombre humano del operador.
- `{{USER_EMAIL}}` — correo del operador.

## Procedimiento de aplicación
```
~/.claude/scripts/claude-deploy.sh apply --level=L0 --scope="$HOME" \
    --var USER_NAME="Alexendros" --var USER_EMAIL="<correo>"
```

El comando renderiza la plantilla a `~/.claude/`, valida JSON con `jq`, ejecuta `shellcheck` sobre `hooks/` si está disponible y registra la operación en `~/.claude/audit/deployments.jsonl`.

## Archivos
- `CLAUDE.md.template` — normas transversales del operador.
- `settings.json.template` — compartible. Espejo de `~/.claude/settings.json`.
- `settings.local.json.example` — esqueleto local; NO se versiona.
- `gitignore.template` — entradas mínimas para el `.gitignore` global.

## Versionado
SemVer. Cambios incompatibles en la anatomía requieren bump MAJOR.
