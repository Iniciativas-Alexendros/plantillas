---
description: Orquesta la integración a main (vía PR) de las ramas de homologación de los repos de la cartera, con criterio por repo, rebase sobre origin/main, build/validación y barrido de ramas obsoletas.
argument-hint: "[repo|all]"
allowed-tools: Read, Grep, Glob, Bash, Agent, Task
model: opus
---

# /integrar-homologacion

Lanza la orquestación agéntica de integración descrita en
`.claude/plans/integracion-homologacion.md`. Argumento `$1`: un repo concreto o
`all` (por defecto, todos los de la cartera).

## Antes de empezar

1. Lee el plan: `.claude/plans/integracion-homologacion.md` y el mapa de la cartera
   `~/.claude/CARTERA.md`.
2. Confirma `gh auth status` (necesario para PRs). Si falla, deténte y pide al
   operador autenticar.
3. `git fetch --all --prune` en los repos en alcance.

## Qué hace (resumen; el detalle y los gates están en el plan)

Pipeline por repo: **sincronizar** (ff de main, rebase de la rama de campaña sobre
`origin/main`, stash de working-tree sucio) → **revisar** (`dev-revision-codigo` +
validador) → **construir/validar** por stack (reparar-y-reintentar con
`repo-developer` si falla) → **publicar PR** (`gh pr create`, base `main`, nota de
merge `--no-ff`). Después, **barrido de ramas obsoletas** (borrar local+remoto las
ya merged; preservar `feat/post-merge-*`, `pipelines/*` y features vivas; investigar
las remotas inconsistentes). Finalmente, consolidar estado en `~/.claude/CARTERA.md`.

## Invariantes (gates de seguridad)

- Rebase sobre `origin/main` antes de cada PR (evita deleciones falsas; crítico en
  alexendrospro, cuya rama parte de un ancestro viejo).
- No publicar repo con build/validador en rojo: queda bloqueado con informe.
- Nunca `sudo` (SUDAUTH); nunca `push --force`/`reset --hard` sin confirmación;
  nunca descartar working-tree sucio sin stash etiquetado.
- No incluir `vault/` (controlink) ni secretos; respetar LICENSE existentes.

## Ejecución

Orquesta con el tool Workflow (pipeline por repo + barrido + consolidación), o agente
a agente si se prefiere control manual. Usa los agents del scope (`code-reviewer`,
`ci-runner`, `repo-developer`, `repo-launcher`, `incident-responder`) y el MCP
`deepwiki` para breaking changes.
