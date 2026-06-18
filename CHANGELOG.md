# Changelog

Todos los cambios destacables de este proyecto se documentan en este archivo.

El formato sigue [Keep a Changelog 1.1.0](https://keepachangelog.com/es/1.1.0/),
y este proyecto se adhiere a [SemVer 2.0.0](https://semver.org/lang/es/).

## [Unreleased] — lychee docs-only: no fallar sin enlaces

### Fixed

- **`repositorios/docs-only/ci.yml.tmpl`** — Añadido `failIfEmpty: false` al job `link-check`. lychee-action trae `failIfEmpty: true` por defecto, que marcaba fallo cuando los globs acotados (docs de proyecto) no contenían ningún enlace externo — caso normal en repos docs pequeños. «Sin enlaces» no es un error.

---

## [Unreleased] — Acotar CI docs-only a docs de proyecto

### Changed

- **`repositorios/docs-only/ci.yml.tmpl`** — `markdownlint` y `link-check` se limitan a los **docs de proyecto** (ficheros canónicos en raíz, `docs/**`, `.github/**`) en lugar de `**/*.md`. El **contenido de autor** (p.ej. `definiciones/`, `documentacion/`) deja de lintearse: es prosa, no documentación de proyecto, y aplicarle reglas de estilo markdown (MD040/MD033/MD036/MD060…) generaba ruido sin valor (172→11→0 errores tras acotar). Cada repo puede ampliar los globs en su copia si quiere lintar su contenido.

---

## [Unreleased] — Calibrar CI docs-only

### Fixed

- **`repositorios/docs-only/ci.yml.tmpl`** — CI para el perfil docs-only, inexistente hasta ahora. Dos jobs: `markdownlint` (DavidAnson/markdownlint-cli2-action@v23.2.0, glob `**/*.md`, recoge `.markdownlint.json` automáticamente) y `link-check` (lycheeverse/lychee-action@v2.8.0, args `--verbose --no-progress --exclude-loopback`). Eliminado `--exclude-mail`, que no existe en lychee-action v2.8.0 y causaba `unexpected argument` (exit 2). Los correos no se tratan como enlaces por defecto en lychee, así que el flag no era necesario.

### Added

- **`repositorios/docs-only/.markdownlint.json.tmpl`** — Configuración markdownlint para repos docs-only: `default: true` + desactiva **MD013** (line-length), **MD034** (no-bare-urls), **MD041** (first-line-heading), y configura **MD024** con `siblings_only: true` (permite headings duplicados en secciones distintas, compatible con CHANGELOG Keep-a-Changelog con múltiples secciones "Añadido"/"Fixed").

---

## [Unreleased] — Bump actions a Node 24 (fin deprecación Node 20)

### Changed

- **`.github/workflows/ci-global.yml`**, **`.github/workflows/link-check.yml`**, **`.github/workflows/pr-guardian.yml`**, **`.github/workflows/release.yml`**, **`.github/workflows/security-scan.yml`**, **`.github/workflows/validar-todos.yml`**, **`.github/workflows/_lib-lint-aggregate.yml`**, **`.github/actions/setup-validadores/action.yml`** — Bump de `actions/checkout@v4 → @v6` y `actions/setup-python@v5 → @v6` en los 8 ficheros con deuda Node 20. GitHub fuerza el runtime **Node 24** para las actions desde **2026-06-16** y ha deprecado Node 20: `checkout@v4` y `setup-python@v5` corren sobre Node 20 y emitían warnings de deprecación camino a fallo duro. Las nuevas majors (`checkout@v6.0.3`, `setup-python@v6.2.0`, últimas estables) corren sobre Node 24. Se fija a tag de major (`@v6`), no a `@main` ni a SHA. Además, **checkout unificado a @v6 en todo el repo**, incluidos los reusables `_lib-detect-stack`, `_lib-supply-chain`, `_lib-release-please` y `_lib-lint-aggregate` que ya estaban en v5 (Node 24): por coherencia se deja un único pin `actions/checkout@v6` en todos los workflows, no solo en los 8 ficheros con deuda Node 20.

## [Unreleased] — Fix job-summary command injection

### Fixed

- **`.github/actions/job-summary/action.yml`** — Los valores dinámicos (`inputs.*` y contexto `github.*`) se interpolaban con `${{ }}` directamente dentro del bloque `run:` de bash. Un `input` con backticks (p.ej. `notes` conteniendo `` `latest` ``) se evaluaba como command substitution → `latest: command not found` (exit 127), tumbando todo job que usara la action (Release de los repos consumidores fallaba en cada push a `main`). Además abría una vía de command injection. Ahora todos los valores se pasan por bloque `env:` (`IN_*`, `GH_*`) y el script los lee como `$VAR` (datos, no código). Cierra el exit 127 y la superficie de inyección de golpe.

## [Unreleased] — Homologación: perfiles rust-mcp/infra, fix motor docs-only, catálogo

### Added

- **`repositorios/rust-mcp/`** — Perfil para MCP servers en Rust (caso `trenchpass`). CI `fmt`/`clippy`/`test`/`build`/`audit` (`rustsec/audit-check@v2`), `.gitignore` Rust (conserva `Cargo.lock`), `README`/`ARCHITECTURE`, `dependabot` cargo. Licencia documentada **AGPL-3.0** (compatibilidad copyleft con `sequoia-openpgp`; MIT infringiría).
- **`repositorios/infra/`** — Perfil Docker/compose (`infra-stacks`, `infra-runners`). CI con `validate-compose`, `yamllint`, `hadolint` y **gate anti `:latest`** (regla dura del proyecto).
- **`repositorios/comun/.pre-commit-config.yaml.tmpl`** — Pre-commit portable con **gitleaks v8.30.1** (secret-scan, antes inexistente) + base, y bloques por stack (JS/Python/Rust) activables.
- **`repositorios/repos.yaml`** — Perfil `infra` y `rust-mcp` añadidos al esquema; 7 fichas nuevas (`check-scripts`, `design-system_azero`, `enfoke`, `infra-runners`, `infra-stacks`, `trenchpass`, `website-alexendrosdev`) reconciliadas por URL de remoto en la homologación 2026-06.

### Fixed

- **`validadores/checks.py`** — `check_archivos_vacios` excluye `.git/` del escaneo (sus objetos se marcaban como falsos «ficheros vacíos»).
- **`repositorios/validar_repositorio.py`** — `_check_readme` exime a repos docs-only (sin manifiesto de código) de las secciones `Stack`/`Instala`, que no aplican; siguen exigiéndose `Qué es`/`Estructura`/`Licencia`. `_check_empty_files` ignora `VERSIÓN`/`VERSION` (versión semántica de pocos bytes, contenido válido por diseño).

---

## [Unreleased] — Fix CI Security Scan

### Fixed

- **`.github/workflows/security-scan.yml`** — El step de TruffleHog pasaba `base: default_branch` y `head: HEAD`, que en un push/merge a `main` resuelven al mismo commit → la action abortaba con `BASE and HEAD commits are the same` (exit 1). El job `Security Scan` llevaba fallando en cada merge a `main` (8+ pushes consecutivos). Ahora escanea el árbol de trabajo completo (`path: ./` sin `base`/`head`), cubriendo PR, push y `workflow_dispatch` por igual, manteniendo `--only-verified`.

---

## [Unreleased] — Optimización deep-scroll

### Changed

- **`validadores/checks.py`**, **`validadores/__init__.py`**, **`validar_repo.py`** — Extraídos a `checks.py` cinco checks genéricos a nivel repositorio, ahora reutilizables por cualquier validador: `check_archivos_prohibidos`, `check_tamanio_maximo`, `check_merge_conflicts`, `check_secrets`, `check_gitignore_minimo`. `validar_repo.py` pasa de 517 a 416 líneas; sus métodos `_check_*` correspondientes son wrappers finos sobre el motor compartido. Comportamiento idéntico (mismos nombres de check y mensajes).

- **`README.md`**, **`INDEX.md`** — `PROMPT_INICIO.md` (prompt de contexto de mantenedor) referenciado en la tabla «Documentación clave» del README y en «Scripts de bootstrap» de INDEX. Antes existía en raíz sin ninguna referencia en el repo (archivo huérfano).

### Added

- **`tests/test_validadores.py`** — 12 tests nuevos para los checks reutilizables (`TestCheckArchivosProhibidos`, `TestCheckTamanioMaximo`, `TestCheckMergeConflicts`, `TestCheckSecrets`, `TestCheckGitignoreMinimo`).

### Removed

- **`agentes/_legacy_{plantilla,ejemplo}_agente_dir/`**, **`commands/_legacy_{plantilla,ejemplo}_command_dir/`**, **`hooks/_legacy_{plantilla,ejemplo}_hook_dir/`** — Purgados los 6 directorios legacy de la estructura multi-archivo previa a la reforma Canon-Runtime. Estaban preservados como retrocompat pero ya no se validan activamente; el canon single-file (`*.md` / `*.sh.template`) los sustituye por completo. Referencias eliminadas del árbol visual de `INDEX.md`. El historial de la migración se conserva en las entradas previas de este CHANGELOG.

- **`mceod-overlays/`** y **`.github/workflows/validar-mceod-overlays.yml`** — Eliminado el módulo MCEOD overlays (L0–L3 + `validar_mceod_overlays.py`) por estar deprecado/descatalogado. No estaba registrado en `DIRECTORIOS_PERMITIDOS`, por lo que hacía fallar `validar_repo.py --strict` (exit 1) en `main`. Todas las referencias estaban contenidas en su propio subárbol + el workflow; no quedan referencias colgantes en el repo. Nota operativa: el symlink local `~/.claude/templates → mceod-overlays` queda obsoleto.

- **`agentes/ejemplo_agente/`** — Eliminado un directorio fantasma (solo `tools/custom/README.md`) remanente de la estructura multi-archivo previa a Canon-Runtime, que coexistía con el fichero canónico `ejemplo_agente.md` y rompía `tests/test_smoke.py` al resolver el ejemplo al directorio en lugar del `.md`.

---

## [Unreleased] — Post-Merge Template v1.1 polish

### Changed

- **`.github/actions/detect-stack/action.yml`** — Detección de Docker ahora recursiva (`repo_find -name 'Dockerfile*'`). Monorepos con `apps/*/Dockerfile`, `services/*/Dockerfile`, etc. ahora activan correctamente el job `hadolint`. Antes solo se chequeaba la raíz.

- **`.github/workflows/_lib-lint-aggregate.yml`** — `osv-scanner` migrado del wrapper `google/osv-scanner-action/osv-scanner-action@v2.3.8` (exit 127, no usable directamente según Google) al binario CLI oficial (`osv-scanner_linux_amd64`). Pre-check de lockfiles: si no hay (`package-lock.json` / `pnpm-lock.yaml` / `yarn.lock` / `Cargo.lock` / `requirements.txt` / `poetry.lock` / `Pipfile.lock` / `go.sum` / `composer.lock`), outcome=skipped (no es failure). Vulnerabilidades detectadas → outcome=warn (no fail).

- **`.github/workflows/_lib-failure-report.yml`** — Clasificador global pasa de 2 estados (ok/fail) a 3 tiers:
  - 🟢 `ok` — todo verde o skipped
  - 🟡 `warn` — solo linters tienen `failure` o `warn` outcome (informativo, no abre issue auto)
  - 🔴 `fail` — supply-chain o release jobs estructurales fallan (sí abre issue auto tras racha)

  Coherente con la filosofía "máxima info en fallo, no bloqueo fatal": OSV vulns o linters quisquillosos no degradan el sticky a rojo. Issue auto reservado para regresiones de blast radius alto.

- **`.github/workflows/_lib-{detect-stack,lint-aggregate,release-please,supply-chain}.yml`** — Bump de actions a versiones Node 24-compatible: `actions/checkout@v4 → @v5`, `actions/upload-artifact@v4 → @v5`, `actions/setup-node@v4 → @v5`. Anticipa la deprecación de Node 20 en runners (forzada 2026-06-02).

---

## [Unreleased] — Post-Merge Template · least-privilege polish

### Changed

- **`.github/workflows/_lib-post-merge.yml`**, **`_lib-supply-chain.yml`**, **`repositorios/ejemplo_repositorio/.github/workflows/post-merge.yml`**, **`.github/workflows/post-merge.yml`** (dogfood) — eliminado `packages: write` de todos los bloques `permissions:`. Era declarado pero nunca consumido por la lib. Los repos que publican imágenes a GHCR (trenchpass, proton-mail-mcp) lo declaran en su `release.yml` propio. Flag de Devin en `Alexendros/mi-website-profesional#42`.

### Added

- **`.github/workflows/README-post-merge.md`** — sección "Matriz de permisos" con tabla `permiso × feature` para que adoptantes puedan recortar a least-privilege estricto según los `enable_*` activos.

---

## [Unreleased] — Post-Merge Template

### Added

- **`.github/workflows/_lib-post-merge.yml`** — Orquestador reusable. Único punto de entrada para consumidores; llama detect-stack y fan-out a sub-libs.
- **`.github/workflows/_lib-detect-stack.yml`** — Reusable wf, expone outputs `has_ts/has_rust/has_python/has_docker/has_markdown/has_shell/is_monorepo/is_docs_only/languages/release_type`.
- **`.github/workflows/_lib-lint-aggregate.yml`** — Linters punta 2026 en paralelo, non-blocking: actionlint+zizmor, gitleaks, yamllint, shellcheck, hadolint, markdownlint-cli2, lychee, Biome o ESLint, Ruff, cargo-deny+clippy, osv-scanner. Reviewdog reporter `github-check`.
- **`.github/workflows/_lib-supply-chain.yml`** — syft → CycloneDX SBOM + `actions/attest-build-provenance@v2` (SLSA L3 nativo, OIDC, cero secrets).
- **`.github/workflows/_lib-release-please.yml`** — Wrapper `googleapis/release-please-action@v4` con `release-type` autodetectado (manifest/node/rust/python/simple). Opt-in vía `enable_release`.
- **`.github/workflows/_lib-failure-report.yml`** — Stack profesional de notificación: sticky commit-comment siempre, step-summary rico, issue auto sticky tras racha de fallos consecutivos (`>=streak_threshold_open`, anti-flake), auto-cierre tras racha verde (`>=streak_threshold_close`).
- **`.github/actions/detect-stack/action.yml`** — Composite con la heurística (file-presence based). Inline-usable.
- **`.github/actions/reviewdog-multi/action.yml`** — Bootstrap de reviewdog con `fail_on_error: false`.
- **`.github/actions/sticky-issue/action.yml`** — Upsert idempotente vía marker HTML. Soporta `create-or-update` y `close-if-streak`.
- **`.github/actions/sticky-commit-comment/action.yml`** — Comentario sticky al commit (no PR), marker HTML idempotente.
- **`repositorios/ejemplo_repositorio/.github/workflows/post-merge.yml`** — Caller plantilla copy-paste-ready.
- **`.github/workflows/README-post-merge.md`** — Documentación adopción (3 pasos), inputs, stacks soportados, troubleshooting, versionado.

Disparable cross-repo vía `uses: Alexendros/plantillas/.github/workflows/_lib-post-merge.yml@v1`. Pilotos planificados: plantillas (dogfood), afiladocs, xek-cluster. Resto en sprint posterior tras validación.

---

## [Unreleased] — Canon-Runtime Alignment (BREAKING)

### Changed

- **`.github/workflows/pr-guardian.yml`** — saca `install.sh` y `.pre-commit-config.yaml` de la lista `PROTECTED` (step 3). Son configuración operativa: deben poder modificarse en PRs de lint/CI sin issue previo. El resto del contrato (Conventional Commits, tamaño, CHANGELOG en cambios de módulo, placeholders) se mantiene. Workflow renombrado a "Guardián de PRs" (i18n).
- **`CONTRIBUTING.md`** — sincroniza la lista de archivos protegidos con `pr-guardian.yml` (saca `install.sh` y `.pre-commit-config.yaml` de "protegidos" y los reclasifica como "configuración operativa"). Renombra "PR Guardian" → "Guardián de PRs" en la sección de checks.

### Fixed

- **Lint verde · pre-commit 13/13**:
  - `repositorios/auditoria-canon-repo.sh`: la rama de fallback (sin `yq`) tenía un `|` al inicio de línea tras el heredoc `PY`, lo que rompía `bash -n` (SC1046/SC1047/SC1072/SC1073/SC1133). Reescrita usando `while read -r slug; do …; done < <(python3 - <<PY … PY)`, simétrica con la rama `yq`.
  - `dot-claude/ejemplo_dot_claude/rc/xek-bash.sh`: añadida directiva `# shellcheck shell=bash` (SC2148) y reemplazado `alias localip="…"` por una función equivalente (SC2142: los aliases bash no admiten `$1/$2`).
  - `.pre-commit-config.yaml`:
    - hook `trailing-whitespace`: `args: ["--markdown-linebreak-ext=md"]` para preservar los saltos de línea markdown (dos espacios al final) en `.md`.
    - hook `detect-placeholders`: añadido `exclude: '(^|/)(_legacy_|plantilla_|__[A-Z_]+__)|^\.pre-commit-config\.yaml$'`. La regex matcheaba placeholders intencionales en las plantillas-fuente y en el propio archivo de configuración.

### Added

- Consolidación CI: 29 checks → 6 (4 propios + 2 externos) sin perder cobertura.
- Composite action `setup-validadores` para setup DRY de Python + pyyaml.
- Script `module-map.sh` para mapeo módulo→validador→ejemplo→plantilla.
- Workflow `release.yml` para releases automáticas por tag semver.
- Workflow `link-check.yml` para detección semanal de enlaces rotos.
- Directorios faltantes en `ejemplo_agente/tools/custom/` y `ejemplo_dot_claude/`.
- `ruff.toml` con configuración de linting para validadores.
- **Módulo `miniapps/`** — canon nuevo para SPA single-file tipo Claude.ai artifact (categorías: dashboard, explorer, tool, playbook; runtimes: browser, electron, static). Incluye `plantilla_miniapps.md`, `ejemplo_miniapps.md` (KPI dashboard), `validar_miniapps.py` y workflow CI.
- **Módulo `autoresearch/`** — canon nuevo para cuadernos de investigación automatizada con frontmatter `topic/sources/status/confidence`. Incluye ejemplo real sobre prompt caching vs memory en Claude API.
- **Módulo `cuadernos/`** — canon nuevo para notas estructuradas del operador (kinds: idea, log, decision, playbook). Ejemplo: decisión de colapsar plantillas a single-file.
- **Módulo `knowledge/`** — canon nuevo para artículos KB referenciables con frontmatter `domain/references/authority/status`. Ejemplo: diferencia entre `tools` (agente) y `allowed-tools` (command).
- **`knowledge/roadmap-omnios-illumos.md`** — roadmap operativo de instalación OmniOS de cero a primera zona corriendo: ZFS root + `beadm`, red `dladm`/`ipadm`, IPS (`pkg`), RBAC en lugar de sudo total, SMF, zonas, bhyve opcional, snapshots/BE, endurecimiento, y cheatsheet Linux → illumos.
- **`knowledge/multirooterso.md`** — artículo sobre identidad del root en Unix: UID 0 local, debilidad de `hostid`/`machine-id`, decomposición vía capabilities y namespaces en Linux, equivalentes en illumos/OmniOS (RBAC, privileges, zonas). Evidencia recogida localmente en contenedor Ubuntu 24.04.
- `validar_repo.py` acepta `plantilla_<base>.*` y `ejemplo_<base>.*` (glob por extensión) además de directorios, habilitando los formatos single-file `.md` y `.sh.template`.
- Workflow `validar-todos.yml` reescrito a matriz declarativa explícita con 14 módulos canon y soporte per-módulo de plantilla/ejemplo como file o dir.
- **`dot-claude/ejemplo_dot_claude/cloud-env/`** — copia canónica versionada del bootstrap para el diálogo "Actualizar entorno en la nube" de Claude Code on the web: `env-vars.env` (variables de entorno) + `bootstrap.sh` (script de configuración) + `README.md`. Diseño **XEK-ENV v3.1**, sucesor de OMNI-ENV v3.0-FINAL: 7 tiers toggleables (`CORE`/`PY`/`SHELL`/`AI`/`OFFICE`/`LEGAL`/`WEB`) vía env vars, cache diaria por stamp (<5s en sesiones repetidas), idempotente, tolerante a apt offline, sin secretos. Pre-stagea `~/.claude/` desde `ejemplo_dot_claude/`.
- **`dot-claude/ejemplo_dot_claude/rc/`** — rcfiles que el bootstrap pre-stagea cuando los tiers SHELL/PY están on: `xek-bash.sh` (alias modernos con fd/bat/eza/delta, integraciones starship/zoxide/atuin/direnv, fzf keybindings), `xek-zsh.zsh` (zinit + fast-syntax-highlighting + autosuggestions + fzf-tab + history-substring-search), `starship.toml` (prompt cross-shell), `ipython_config.py` (autoload polars/pandas/numpy/httpx/pydantic/rich).
- **XEK-ENV v3.2** — bump del bootstrap horizontal:
  - **Tier RUNTIMES** (nuevo, on): instala `mise` y materializa `node@$NODE_VERSION` (default **24**) y `python@$PYTHON_VERSION` (default 3.13). PATH del entorno pone `~/.local/share/mise/shims` primero, con `/opt/node22/bin` como fallback (preserva el `claude` CLI). `mise.toml` / `.tool-versions` per-repo siguen funcionando.
  - **Tier NET** (nuevo, on): herramientas de diagnóstico y optimización de red para LAN y VPS — `mtr-tiny`, `iperf3`, `nmap`, `tcpdump`, `ngrep`, `traceroute`, `whois`, `socat`, `mosh`, `autossh`, `sshpass`, `nethogs`, `iftop`, `bmon`, `tmux`, `screen`, `rclone`, `restic`, `netcat-openbsd`, `wireguard-tools`, `gping` (cargo), `bandwhich` (cargo), `croc` (binario GitHub).
  - **Tier DOCKER** (nuevo, on): containerización — `docker-compose-plugin`, `docker-buildx-plugin`, `buildah`, `skopeo`, `lazydocker`, `dive`, `ctop`, `hadolint`, `trivy` (apt repo Aqua Security).
  - Tier CORE añade `direnv`, `jq`, `yq`, `bc` y opcional `bun upgrade --stable` (via `BUN_AUTO_UPGRADE`).
  - Tier WEB ahora ejecuta `corepack prepare pnpm@latest --activate` y `yarn@stable --activate` sobre Node 24.
  - rcfiles (`xek-bash.sh`, `xek-zsh.zsh`) activan `mise` y añaden aliases de red (`myip`, `localip`, `ports`, `trace`, `scan`, `bench`, `ssh-keep`, `tunl`, `rtunl`) y docker (`d`, `dc`, `dps`, `dlogs`, `ld`, `dscan`, `dlint`, `dlayers`).
  - Pre-stage de `~/.claude/` ahora excluye `cloud-env/` y `rc/` (no son contenido de `~/.claude/`).
  - Banner muestra versión de Node detectada vs target.
- **XEK-ENV v3.3** — Bun-first + polish:
  - **Bun como gestor de paquetes JS por defecto**: `bun upgrade --stable` ya corría en CORE (toggleable con `BUN_AUTO_UPGRADE=0`); ahora los rcfiles añaden aliases dedicados (`b`, `bi`, `ba`, `bad`, `bag`, `brm`, `bup`, `bx`, `br`, `bt`, `bd`, `bw`, `bbuild`, `bnew`, `bu`). Política: respetar `pnpm-lock.yaml`/`package-lock.json` si están pinned; corepack sigue activo para fallbacks.
  - **`env-vars.general.env`** — variante ligera con tiers AI/OFFICE/NET/DOCKER/LEGAL apagados por defecto (frío 20–40s). El `env-vars.env` original queda como variante "minado" (todo on excepto LEGAL).
  - **`apt-get update` deduplicado** por stamp diario (`APT_STAMP`) → ahorra 4–8s en cold start; tier DOCKER invalida el stamp tras añadir el repo de Trivy.
  - Banner reporta versión de Python y Bun además de Node.
  - `env-vars.env` añade `XEK_ENV_NAME` (etiqueta de entorno en el banner) y `BUN_INSTALL=/home/user/.bun`.
  - README documenta la política Bun-first y advierte explícitamente del error común de pegar `bootstrap.sh` en el campo "Variables de entorno" del diálogo (que rompe el PATH al no expandir `$HOME`).

### Changed (BREAKING)

- **`agentes/plantilla_agente/`** colapsado a single-file `agentes/plantilla_agente.md` con frontmatter runtime (`name`, `description`, `tools`, `model`, opcional `effort`/`permission_scope`/`primary_skill`) y secciones canon (`System`, `Persona`, `Tasks`, `Tools MCP`, `Memory`, `Subagents`, `References`). El dir antiguo queda en `agentes/_legacy_plantilla_agente_dir/`.
- **`agentes/ejemplo_agente/`** colapsado a single-file `agentes/ejemplo_agente.md` (orquestador hub-and-spoke con primary_skill `dev-arquitectura`). El dir antiguo queda en `agentes/_legacy_ejemplo_agente_dir/`.
- **`agentes/validar_agente.py`** reescrito a v3.0.0: valida single-file `.md`, secciones canon, `name` kebab-case, tools en lista canon (incluye `mcp__*`), `model` en `{opus, sonnet, haiku, opusplan}`. Modo legado dir-input emite warning y valida `AGENT.md` interior.
- **`commands/plantilla_command/`** colapsado a single-file `commands/plantilla_command.md`. Frontmatter `description` + opcionales `argument-hint`/`allowed-tools`. Secciones canon: `Trigger`, `Instrucciones`, `Parámetros`, `Output esperado`, `Restricciones`, `Referencias`. Validador v2.0.0.
- **`commands/ejemplo_command/`** colapsado a single-file `commands/ejemplo_command.md` (`/test-cobertura` multi-runner Jest/Vitest/pytest). Dir antiguo en `commands/_legacy_ejemplo_command_dir/`.
- **`hooks/plantilla_hook/`** colapsado a `hooks/plantilla_hook.sh.template` (shebang + cabecera declarativa `# name`/`# matcher`/`# tool_pattern`/`# description`/`# version` + body placeholder JSON `{decision, reason}`) + `hooks/HOOK.md` documental. Validador v3.0.0.
- **`hooks/ejemplo_hook/`** colapsado a `hooks/ejemplo_hook.sh.template` (`pre-bash-secret-guard`, PreToolUse, escanea patrones GitHub/OpenAI/AWS).
- **`dot-claude/plantilla_dot_claude/settings.json`** alineado al schema runtime real de Claude Code 2.1.x: `permissions.{allow, deny}` (listas), `hooks.<Evento>: [{matcher, hooks: [{type:"command", command:"..."}]}]`, `env: {KEY: VAL}`. Eliminadas claves obsoletas: `skillListingBudgetFraction`, `hooks.{enabled,sources,autoDiscover}`, `skills.{autoDiscover,preload}`, `mcp.servers`, `output.{language,style}` (esta última equivalente runtime es `env.CLAUDE_LANG`).
- **`dot-claude/plantilla_dot_claude/CLAUDE.md`** y `ejemplo_dot_claude/CLAUDE.md` actualizados a árbol plano (sin `herramientas/`): 13 dirs canon en raíz `~/.claude/` (agents, skills, commands, hooks, scripts, plugins, mcp, miniapps, autoresearch, cuadernos, knowledge, artefactos, projects).
- **`dot-claude/validar_dot_claude.py`** reescrito a v2.0.0: valida schema runtime real, detecta claves legacy (warning), comprueba `mcp.json` separado y `CLAUDE.md` sin referencias a `herramientas/`.

### Migration notes

- Repos que consumen agentes/commands/hooks/dot-claude del canon **viejo** seguirán funcionando porque los dirs legacy quedan preservados como `_legacy_*_dir/` y los validadores tienen modo retrocompatible (emiten warning y procesan el contenido legacy). Pasar a single-file recomendado, no obligatorio.
- `claude-init` debe actualizarse para emitir el formato single-file por defecto (out-of-scope de esta entrada; ver issue de seguimiento).
- Consumidores de `settings.json` deben migrar sus `hooks: {enabled, sources}` a `hooks: {<Evento>: [{matcher, hooks}]}`. Equivalencias documentadas en `dot-claude/plantilla_dot_claude/settings.json`.

## [1.0.0] — 2026-05-23

### Added

- Fase 1: MVP — 7 módulos base (agentes, skills, commands, hooks, plugins, mcp, dot-claude).
  - Cada módulo con `plantilla_X/` (playbook instructivo) y `ejemplo_X/` (referencia funcional).
  - Índice maestro `INDEX.md` con navegación a todos los módulos.
  - `ROADMAP.md` con plan de 4 fases.
- Fase 2: Robustecimiento.
  - Motor de validación reusable en `validadores/` (`BaseValidator`, 5 checks reutilizables).
  - Validador específico para cada módulo (7 validadores, todos pasan `--strict`).
  - CI/CD individual por módulo + workflow central `validar-todos.yml`.
  - Ejemplos enriquecidos: ≥2 ejemplos funcionales por módulo.
  - `INTEGRACION.md` con mapa de relaciones, decision tree, anti-patrones, ejemplo completo.
- Iteración 2.4: Afinado de repositorios.
  - Módulo `repositorios/` con playbook completo (`REPOSITORIO.md`, `METODOLOGIA.md`, `LLM_GUIDE.md`, `ESTRUCTURA.md`).
  - Ejemplo funcional con 20+ community health files.
  - Scripts `aplica-canon-repo.sh` y `auditoria-canon-repo.sh`.
  - Fuente de verdad `repos.yaml` con 14+ repositorios catalogados.
