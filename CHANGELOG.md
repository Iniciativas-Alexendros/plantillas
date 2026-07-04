# Changelog

Todos los cambios destacables de este proyecto se documentan en este archivo.

El formato sigue [Keep a Changelog 1.1.0](https://keepachangelog.com/es-ES/1.1.0/),
y este proyecto se adhiere a [SemVer 2.0.0](https://semver.org/lang/es/).

## [Unreleased] — Consolidación de armonización y Bloque 2 en progreso

> Esta sección agrupa todos los cambios no publicados desde v1.0.0, incluyendo la
> refactorización Cross-platform Config, el módulo de estándares, los ajustes de
> CI/CD y la implementación inicial del Bloque 2 (paquete Python con CLI `plantillas`).

### Añadido

- Módulo `agent-config/`: fuente canónica YAML (`plantilla_agent_config.yaml`) que genera configuración para **Claude Code** (`~/.claude/`), **OpenCode** (`~/AGENTS.md`), **Devin** (`~/.config/devin/`) y **Windsurf/Cascade** (`~/.codeium/windsurf/memories/global_rules.md`).
- Generador `agent-config/generar_agent_configs.py` y validador `agent-config/validar_agent_config.py` con drift check entre la fuente y el directorio de ejemplo.
- Workflow `agent-config/.github/workflows/validar-agent-config.yml` y registro en `validar-todos.yml` y `validar_repo.py`.
- **`repositorios/docs-only/.markdownlint.json.tmpl`** — Configuración markdownlint para repos docs-only: `default: true` + desactiva **MD013** (line-length), **MD034** (no-bare-urls), **MD041** (first-line-heading), y configura **MD024** con `siblings_only: true` (permite headings duplicados en secciones distintas, compatible con CHANGELOG Keep-a-Changelog con múltiples secciones "Añadido"/"Fixed").
- **`tests/test_validadores.py`** — 12 tests nuevos para los checks reutilizables (`TestCheckArchivosProhibidos`, `TestCheckTamanioMaximo`, `TestCheckMergeConflicts`, `TestCheckSecrets`, `TestCheckGitignoreMinimo`).
- **`.github/workflows/README-post-merge.md`** — sección "Matriz de permisos" con tabla `permiso × feature` para que adoptantes puedan recortar a least-privilege estricto según los `enable_*` activos.
- Consolidación CI: 29 checks → 6 (4 propios + 2 externos) sin perder cobertura.
- Paquete Python `plantillas` (`pyproject.toml`, `src/plantillas/`, `modules.yaml`) con CLI unificada (`typer`), registry de validadores y tests (`pytest`).
- Workflow `.github/workflows/validar-paquete.yml` para lint, tests y `plantillas validate` en CI.
- Validador embebido de ejemplo en `src/plantillas/validators/agent_config.py`.
- Composite action `setup-validadores` para setup DRY de Python + pyyaml.
- Script `module-map.sh` para mapeo módulo→validador→ejemplo→plantilla.
- Workflow `release.yml` para releases automáticas por tag semver.
- Workflow `link-check.yml` para detección semanal de enlaces rotos.
- Directorios faltantes en `ejemplo_agente/tools/custom/` y `ejemplo_dot_claude/`.
- `ruff.toml` con configuración de linting para validadores.
- **Módulo `miniapps/`** — canon nuevo para SPA single-file tipo Claude.ai artifact (categorías: dashboard, explorer, tool, playbook; runtimes: browser, electron, static). Incluye `plantilla_miniapps.md`, `ejemplo_miniapps.md` (KPI dashboard), `validar_miniapps.py` y workflow CI.
- `validar_repo.py` acepta `plantilla_<base>.*` y `ejemplo_<base>.*` (glob por extensión) además de directorios, habilitando los formatos single-file `.md` y `.sh.template`.

### Eliminado

- Módulos `autoresearch/`, `cuadernos/`, `knowledge/` y `dot-claude/` (sustituidos por `agent-config/` y el repo de plantillas en sí). Se ha preservado backup en `.backups-YYYYMMDD-HHMMSS/` antes de borrar.
- **`agentes/_legacy_{plantilla,ejemplo}_agente_dir/`**, **`commands/_legacy_{plantilla,ejemplo}_command_dir/`**, **`hooks/_legacy_{plantilla,ejemplo}_hook_dir/`** — Purgados los 6 directorios legacy de la estructura multi-archivo previa a la reforma Canon-Runtime. Estaban preservados como retrocompat pero ya no se validan activamente; el canon single-file (`*.md` / `*.sh.template`) los sustituye por completo. Referencias eliminadas del árbol visual de `INDEX.md`. El historial de la migración se conserva en las entradas previas de este CHANGELOG.
- **`mceod-overlays/`** y **`.github/workflows/validar-mceod-overlays.yml`** — Eliminado el módulo MCEOD overlays (L0–L3 + `validar_mceod_overlays.py`) por estar deprecado/descatalogado. No estaba registrado en `DIRECTORIOS_PERMITIDOS`, por lo que hacía fallar `validar_repo.py --strict` (exit 1) en `main`. Todas las referencias estaban contenidas en su propio subárbol + el workflow; no quedan referencias colgantes en el repo. Nota operativa: el symlink local `~/.claude/templates → mceod-overlays` queda obsoleto.
- **`agentes/ejemplo_agente/`** — Eliminado un directorio fantasma (solo `tools/custom/README.md`) remanente de la estructura multi-archivo previa a Canon-Runtime, que coexistía con el fichero canónico `ejemplo_agente.md` y rompía `tests/test_smoke.py` al resolver el ejemplo al directorio en lugar del `.md`.

### Changed

- `INDEX.md`: actualizado a 12 módulos canónicos, eliminadas referencias a módulos borrados y añadida sección de `agent-config`.
- `.github/workflows/validar-todos.yml`: matriz reducida a 12 módulos.
- `validar_repo.py`: listas de directorios permitidos, módulos canónicos y mapeo de singulares actualizados; eliminada lógica muerta del módulo borrado `dot-claude` y del directorio descatalogado `mceod-overlays/`.
- `.pre-commit-config.yaml`: eliminados hooks de módulos borrados (`dot-claude`, `autoresearch`, `cuadernos`, `knowledge`) y añadida validación de `agent-config`.
- `agent-config/.github/workflows/validar-agent-config.yml`: pines SHA de acciones y permisos mínimos.
- `.github/scripts/module-map.sh`, `.github/workflows/pr-guardian.yml`, `.github/workflows/ci-global.yml`: sincronizados a los 12 módulos canónicos actuales y eliminados filtros/mapeos legacy.
- `CLAUDE.md`, `PROMPT_INICIO.md`, `CONTRIBUTING.md`, `ROADMAP.md`, `INTEGRACION.md`: limpiadas todas las referencias a módulos descartados (`dot-claude`, `autoresearch`, `cuadernos`, `knowledge`, `mceod-overlays`) y actualizados conteos/nombres a 12 módulos.
- `agent-config/generar_agent_configs.py`: reescrito el descriptor de `memory` para evitar referencia al módulo `knowledge`.
- `artefactos/README.md` y `repositorios/auditoria-canon-repo.sh`: eliminadas referencias a `cuadernos/`.
- `.gitignore`: añadidos patrones `*.backup`, `.venv/` y `docs/dossier-bloque2.html`.
- `validar_repo.py`: permite `src/`, `docs/`, `pyproject.toml`, `modules.yaml` y 12 módulos canónicos; marca `artefactos` y `estandares` como módulos especiales mientras migran a estructura canónica completa.

### Fixed

- **`validadores/checks.py`** — `check_archivos_vacios` excluye `.git/` del escaneo (sus objetos se marcaban como falsos «ficheros vacíos»).
- **`repositorios/validar_repositorio.py`** — `_check_readme` exime a repos docs-only (sin manifiesto de código) de las secciones `Stack`/`Instala`, que no aplican; siguen exigiéndose `Qué es`/`Estructura`/`Licencia`. `_check_empty_files` ignora `VERSIÓN`/`VERSION` (versión semántica de pocos bytes, contenido válido por diseño).

### Security

- Pinea todas las acciones de terceros a SHA con comentario de versión.
- Añade `permissions` explícitos y `persist-credentials: false` en los workflows de submódulos.
- Añade `actionlint` y `zizmor` al CI global; `zizmor` reporta 0 findings.

### Notas de migración

- El hardening del bootstrap de `dot-claude` (`cloud-env/bootstrap.sh` con verificación SHA256 y versiones pinedas) se conserva en el backup histórico; el módulo ya no forma parte del canon de 12 módulos.
- Repos que consumen agentes/commands/hooks/dot-claude del canon **viejo** seguirán funcionando porque los dirs legacy quedan preservados como `_legacy_*_dir/` y los validadores tienen modo retrocompatible (emiten warning y procesan el contenido legacy). Pasar a single-file recomendado, no obligatorio.
- `claude-init` debe actualizarse para emitir el formato single-file por defecto (out-of-scope de esta entrada; ver issue de seguimiento).
- Consumidores de `settings.json` deben migrar sus `hooks: {enabled, sources}` a `hooks: {<Evento>: [{matcher, hooks}]}`. Equivalencias documentadas en `dot-claude/plantilla_dot_claude/settings.json`.

### Documentación (Bloque 2)

- `README.md`: actualizado a 12 módulos y transición al paquete Python.
- `INDEX.md`: título genérico, nota de Bloque 2 y referencia al dossier.
- `CONTRIBUTING.md`: guía de `modules.yaml`, registry y validadores del Bloque 2.
- `ROADMAP.md`: sección del Bloque 2 con 7 fases y criterios de aceptación.
- `CLAUDE.md` y `PROMPT_INICIO.md`: stack y comandos del Bloque 2.
- `INTEGRACION.md`: referencias a `plantillas sync agent-config` y al dossier.
- `docs/adr/`: 3 ADRs (paquete Python, Pydantic+Jinja2, `modules.yaml`).
- `docs/cli.md`, `docs/modules-yaml.md`, `docs/validators.md`: documentación del Bloque 2.
- `agent-config/README.md`: esquema Pydantic, templates Jinja2 y CLI del Bloque 2.
- `docs/dossier-bloque2.html`: dossier visual interactivo (ignorado en GitHub).

### Añadido (Bloque 2 · sync + SPA regenerable)

- **Sync bidireccional** entre `plantillas/` y `~/.config/opencode/` para
  `skills` / `agents` (alias de `agentes`) / `commands`. Tres direcciones:
  `push` (plantillas → target), `pull` (target → `plantillas/<modulo>/_imported/`),
  `status` (dry-run que reporta drift). Subcomando CLI:
  `plantillas sync <module> --target opencode --direction {push,pull,status} [--yes]`.
- **Generador SPA** `docs/dossier-bloque2.html` (single-file, 5 tabs:
  Configurador, Catálogo, Mapa, Dossier, Índice; slider sepia↔nocturno;
  ARIA tabs; sin CDNs externos). Subcomando CLI:
  `plantillas generate dossier [--output PATH]`. 10 tests cubren render
  mínimo, ausencia de CDNs, JSON embebido, presencia de los 12 módulos,
  TOC con `docs/*.md`, tamaño <200KB, slider de tema, ARIA, ISO 8601
  y determinismo.
- **Registry robusto**: logging DEBUG por validador (embedded/script/none),
  timeout de 30s en `_run_script`, captura `TimeoutExpired` y exit code
  en `CalledProcessError`. Silencia `ImportError` además de
  `ModuleNotFoundError` en `discover_validators`.
- **Validadores embebidos**: `validators/__init__.py` con `__all__`
  reexportando `validate_agent_config`.
- **Paridad catálogo↔INDEX**: nuevo test
  `tests/test_catalog_yaml_index_parity.py` que garantiza que todo módulo
  canónico tenga referencia en `INDEX.md` y viceversa.
- **CI matrix Python 3.11/3.12/3.13** en `.github/workflows/validar-paquete.yml`.
- **Workflow de regeneración de SPA** (`.github/workflows/regenerar-spa.yml`):
  en cada push a `main` que cambie inputs del generador, regenera la SPA
  y abre un PR automático si hay drift.

### Cambiado

- `tests/test_smoke.py`: deriva `MODULOS` de `modules.yaml` en vez de la
  lista hardcodeada. FIXME documenta el fallo pre-existente en
  `agent-config/ejemplo_agent_config/AGENTS.md` (deuda no relacionada
  con este cambio).
- `modules.yaml`: añade bloque `sync: { target: opencode, subdir: skills }`
  al módulo `skills` declarando el target y subdirectorio canónico.
- `INDEX.md`: referencia al dossier ahora dice "single-file, 5 tabs,
  generado por `plantillas generate dossier`, CI lo regenera".
- `.gitignore`: `docs/dossier-bloque2.html` deja de estar ignorado (sale
  de la lista, ahora commiteable y regenerado por CI).

---

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
