# Plantilla MCEOD L1 — Categoría (fullstack/devops)

- Versión: 2.0.0
- Nivel: L1 (agregador de categoría, p. ej. `~/Repositorios/.claude/`)
- Propósito: dotar a una categoría de **proyectos de código** de contexto y tools
  comunes de ingeniería (git/GitHub, CI/CD, build/test, revisión e integración).

## Placeholders disponibles
- `{{CATEGORY_NAME}}` — nombre humano de la categoría (Repositorios).
- `{{CATEGORY_PATH}}` — ruta absoluta del directorio padre.

## Cuándo aplicar L1 vs L0/L2
- L0: la convención afecta a todo el `$HOME`.
- L1: convenciones/tools comunes a los proyectos de una categoría de código.
- L2: convención exclusiva de un repo.

## Procedimiento
```
~/.claude/scripts/claude-deploy.sh apply --level=L1 \
    --scope=/home/alexendros/Repositorios \
    --var CATEGORY_NAME="Repositorios" \
    --var CATEGORY_PATH="/home/alexendros/Repositorios" --force
```
`--force` sobrescribe los ficheros coincidentes del scope (crea backup automático).
`render_tree` copia el árbol recursivamente y omite los `README.md`.

## Archivos que emite al scope
- `CLAUDE.md` — contexto devops de la categoría, hereda de L0/AXIS.
- `settings.json` — allow-list git/gh/build + ask (push --force, delete) + deny
  (sudo, reset --hard, lectura de secretos). Claves del esquema oficial.
- `settings.local.json.example` — esqueleto local; NO se versiona.
- `.gitignore` — settings.local.json, node_modules, .venv, etc.
- `agents/` — code-reviewer, ci-runner, repo-developer, repo-launcher, incident-responder
  (adaptados del canon de controlink-operator; sin acoplamiento al runtime DCC).
- `skills/` — dev-revision-codigo, dev-estrategia-tests, app-ci-cd, app-despliegue, app-docker.
- `commands/` — `integrar-homologacion` (orquesta integración de ramas a main vía PR).
- `plans/` — `integracion-homologacion.md` (plan que lanza el command).

## Alcance (caveat de genericidad)
Esta plantilla L1 está orientada a categorías de **código** (Repositorios). Para una
categoría no-código (p. ej. ShellScripts si quisiera otra semántica), conviene una
variante propia; ShellScripts ya desplegado con la L1 v1.0.0 genérica no se ve afectado
salvo re-`apply`.
