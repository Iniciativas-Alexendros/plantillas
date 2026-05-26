# Changelog

Todos los cambios destacables de este proyecto se documentan en este archivo.

El formato sigue [Keep a Changelog 1.1.0](https://keepachangelog.com/es/1.1.0/),
y este proyecto se adhiere a [SemVer 2.0.0](https://semver.org/lang/es/).

## [Unreleased] — Canon-Runtime Alignment (BREAKING)

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
