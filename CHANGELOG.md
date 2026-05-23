# Changelog

Todos los cambios destacables de este proyecto se documentan en este archivo.

El formato sigue [Keep a Changelog 1.1.0](https://keepachangelog.com/es/1.1.0/),
y este proyecto se adhiere a [SemVer 2.0.0](https://semver.org/lang/es/).

## [Unreleased]

### Added

- Fase 3: Ecosistema — scripts de instalación, CONTRIBUTING.md, tests, pre-commit hooks.
- Workflow `release.yml` para releases automáticas por tag semver (ROADMAP 3.1.4).
- Workflow `link-check.yml` para detección semanal de enlaces rotos (ROADMAP 4.2.1).
- Composite action `setup-validadores` para setup DRY de Python + pyyaml + pip cache.
- Script centralizado `module-map.sh` para mapeo módulo→validador→ejemplo→plantilla.

### Fixed

- Vulnerabilidad de inyección de código en `pr-guardian.yml` (título del PR).
- Deadlock lógico entre `protected-files` y `changelog-check` en `pr-guardian.yml`.
- Job `resumen` roto en `ci-global.yml` (expresiones dinámicas no resueltas).
- Directorios faltantes en `ejemplo_agente` y `ejemplo_dot_claude`.
- Rutas incorrectas en `test_smoke.py` para módulos especiales (modulo, proyecto).
- TruffleHog pineado a versión estable `v3.88.29`.

### Changed

- `validar-todos.yml` refactorizado con module-map (elimina ~80 líneas de if/elif).
- `lint-markdown` y `lint-shell` usan `continue-on-error` para visibilidad en GitHub UI.

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
