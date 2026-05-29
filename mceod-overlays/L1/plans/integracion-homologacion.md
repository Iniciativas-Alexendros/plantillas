# Plan — Orquestación agéntica de integración (PRs) + saneamiento de ramas

> Plan alojado en el scope L1 devops. Lánzalo con `/integrar-homologacion`.
> Estado git verificado al diseñarlo; revalida con `git fetch --all --prune` antes de
> ejecutar (puede haber cambiado desde entonces).

## Context

La campaña de homologación dejó 13 repos propios bajo `~/Repositorios/` con su
trabajo en **rama+worktree de campaña** (`homologacion-docs`; `fix-validador-b4` en
`plantillas`), **sin push**. Objetivo: revisar los diffs, actualizar las ramas
(campaña + preexistentes ya no funcionales) e **integrar a `main`** vía PR, con
criterio por repo, herramientas y objetivos claros.

Hallazgos git que condicionan el diseño:

- **La campaña es puramente documental/boilerplate** en los 13. Los diffs "masivos"
  (alexendrosme −1534, alexendrospro −1096, etc.) son **artefacto direccional**: se
  midieron contra `main` local en vez del punto base real. Contra `merge-base(origin/main)`
  el cambio real es solo docs + `.github/*` + `.claude/` + ADR.
- **Ningún `main` local tiene commits exclusivos**. Cuatro repos tienen `main` local
  **BEHIND** `origin/main`: alexendrosme 7, Atlaps 4, design-system_(revision) 4,
  proton-mail-mcp 1. → basta fast-forward del `main` local.
- **Dos cambios funcionales deliberados** (única excepción a "solo docs"): fix B4 en
  `plantillas/validadores/base.py` (+tests) y bump **Next.js 16** en
  `alexendrospro/package.json` (+ refactor de templates de issues).
- **`alexendrospro`: la rama de campaña parte de un ancestro viejo** de `origin/main`.
  Hay que **rebasarla sobre `origin/main` actual antes del PR**, o el PR mostrará
  deleciones falsas. Conflicto posible en `package.json` (preservar Next 16 + deps de main).
- **Working-trees sucios**: `xek-cluster` (10) y 1–2 ficheros en casi todos. Stashear
  con etiqueta + reportar antes de tocar.
- **~40 ramas preexistentes obsoletas** candidatas a borrado; preservar `feat/post-merge-*`,
  `pipelines/*` y features activas; dos **remotas inconsistentes** a investigar antes
  de borrar: `Atlaps/fix/layout-test-react-19` y `design-system_(revision)/fix/remove-wrong-ci-yml`.

**Decisiones del operador (confirmadas):** integración vía **PR en GitHub**; ramas
obsoletas **borrar local + remoto**; integración del PR **merge commit `--no-ff`**;
ante fallo de validación/build **intentar arreglar y reintentar**, bloquear si no se logra.

**Restricciones AXIS/L0:** SUDAUTH; `set -o pipefail`; hipótesis vs afirmación; sin emojis.

## Arquitectura de la orquestación

Con **Workflow**: **pipeline por repo** (sin barreras) + fase de **barrido de ramas** +
consolidación. Cada repo lo procesa un agente con criterio/herramientas propios.

### Fase 0 — Preparación

1. `gh auth status` y `git --version`; abortar si `gh` no está autenticado.
2. `git -C <repo> fetch --all --prune` en los 13.
3. Snapshot del estado por repo (ramas, worktrees, sucio).

### Fase 1 — Integración por repo (fan-out, pipeline 4 etapas)

- **E1 · Sincronizar**: stash del working-tree sucio con etiqueta `pre-integracion-<repo>`;
  ff de `main` a `origin/main`; **rebase de la rama de campaña sobre `origin/main`**;
  resolver conflictos (disjuntos salvo `package.json` en alexendrospro y `base.py` en
  plantillas). Recalcular `git diff origin/main..<rama> --stat`.
- **E2 · Revisar**: skill `dev-revision-codigo` (envuelve `/code-review`) + validador
  (`validar_repositorio.py --strict`; `validar_repo.py --strict` para `plantillas`).
  Gate: validador en verde.
- **E3 · Construir/validar por stack**: build/test nativo. Si falla → `repo-developer`
  repara lo mínimo y revalida; si tras N intentos sigue rojo → **bloquea ese repo**.
- **E4 · Publicar**: `git push -u origin <rama>`; `gh pr create` base `main`, título
  `homologación: <repo>`, cuerpo con resumen, diff real, validador/build, riesgos y la
  nota **"mergear con --no-ff"**. Devolver URL del PR.

### Fase 2 — Barrido de ramas obsoletas

Clasificar cada rama no-default: `MUERTA` (merged en `origin/main` o sin valor y muy
atrás), `VIVA` (preservar) o `DUDOSA`. **Borrar local+remoto solo las MUERTAS**
(`git branch -d` + `git push origin --delete`); nunca `-D` sin merged. Las remotas
inconsistentes se investigan y se dejan a decisión del operador. Informe.

### Fase 3 — Consolidación

Actualizar `~/.claude/CARTERA.md` (sección "Integración PRs — <fecha>") con URL de PR,
veredicto validador/build, ramas borradas/dudosas y caveats. Actualizar memoria
`project_homologacion_cartera`.

## Criterio por repo (dossiers)

- **Webapp** (`alexendrospro`, `alexendrosme`, `afiladocs`, `Atlaps`): `pnpm install &&
  pnpm build`; Playwright si existe; lint.
  - `alexendrospro` (ALTO): PR con **Next 16 verde**; reparación de `async params`/`proxy.ts`;
    `deepwiki` sobre `vercel/next.js`. Rebase obligatorio (base vieja).
  - `alexendrosme`: solo-docs tras rebase; ff de main (BEHIND 7).
  - `Atlaps`: ff de main (BEHIND 4); investigar `fix/layout-test-react-19`.
  - `afiladocs`: solo-docs; no tocar P0b Stripe LIVE (acto del operador).
- **MCP**: `trenchpass` (Rust) `cargo build`+`clippy`; `proton-mail-mcp` (TS) `pnpm
  build`/`test`, ff de main (BEHIND 1).
- **Design-system** (`azero`, `revision`): `node scripts/validate-tokens.mjs` /
  `validate-contrast.mjs`. `revision`: ff de main (BEHIND 4); investigar `fix/remove-wrong-ci-yml`.
- **Infra/registro**: `infra-runners` `docker compose config` + prohibir `:latest`
  (MCP `hostinger`); `GV-ERRA` `python tools/validate.py`; `xek-cluster` resolver
  primero los 10 cambios sin commitear + `shellcheck`.
- **Motor** `plantillas` (rama `fix-validador-b4`): `pytest` + `validar_repo.py --strict`;
  decidir el smoke pre-existente en rojo.
- **Canon** `controlink-operator`: solo canon root; **no incluir `canonical/` ni `vault/`**;
  documentar B2 como caveat.

## Gates de seguridad (invariantes)

- Nunca `sudo` (SUDAUTH). Nunca `-D` de rama no-merged sin certeza.
- Nunca descartar working-tree sucio sin **stash etiquetado** + reporte.
- No publicar repo con build/validador en rojo (bloqueado con informe).
- No incluir en PRs `vault/` ni secretos; respetar LICENSE existentes.
- **Rebase sobre `origin/main` antes de cada PR** (evita deleciones falsas).

## Verificación end-to-end

1. `git diff origin/main..<rama> --stat` limpio (solo-docs salvo B4 y Next16) tras rebase.
2. Validador verde por repo; build/test verde (o repo bloqueado con causa).
3. PR abierto por repo con URL y cuerpo estructurado (incluye "merge `--no-ff`").
4. Ramas obsoletas confirmadas borradas (local+remoto); vivas intactas; dudosas listadas.
5. `CARTERA.md` y memoria reflejan PRs, builds, ramas y caveats.
