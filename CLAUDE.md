# CLAUDE.md — plantillas

<proyecto>
Sistema de Plantillas Modulares para Claude Code: ecosistema `claude-init`-ready
para inicializar, validar y mantener componentes de Claude Code (12 módulos
canónicos: agentes, skills, commands, hooks, plugins, mcp, agent-config,
repositorios, miniapps, módulo, proyecto y estándares). Patrón estricto por módulo:
`plantilla_<x>` (playbook) + `ejemplo_<x>` (referencia funcional) +
`validar_<x>.py` (validador con `--strict`) + workflow CI propio.
Autor: Alejandro · Iniciativas Alexendros. Licencia MIT.
</proyecto>

<stack>
- Python 3.12+ (validadores y motor reusable; dependencia mínima: `pyyaml`).
- Bash (entrypoints: `claude-init`, `install.sh`, `update.sh`).
- Contenido en Markdown/YAML/JSON. CI: GitHub Actions. Calidad: pre-commit, ruff.
- Bloque 2: paquete `plantillas` (`pyproject.toml`), CLI con Click, Pydantic v2, Jinja2, uv.
Comandos REALES (verificados en README/PROMPT_INICIO/claude-init):
- `claude-init --list` · `claude-init --modulo <nombre> --nombre mi-x`
- `claude-init --repositorio --nombre mi-repo` · `claude-init --proyecto`
- `python validar_repo.py --strict` (validador global de raíz)
- `python <modulo>/validar_<modulo>.py <ruta> --strict` (validador por módulo)
- `python tests/test_smoke.py` o `pytest tests/ -v` (smoke + unit; requiere pytest)
- `pre-commit run --all-files`
Bloque 2 (futuro):
- `uv pip install -e .` · `plantillas validate --all --strict`
- `plantillas sync agent-config [--dry-run]` · `plantillas new <tipo> --nombre <nombre>`
- `plantillas config list`
</stack>

<estado>
Activo. README declara v1.0.0; CHANGELOG documenta la refactorización
Cross-platform Config. 12 módulos canónicos con validador, workflow CI propio y
smoke tests. Branch protection + pre-commit + ruff/yamllint/shellcheck activos.
En transición al Bloque 2: paquete Python con CLI `plantillas`, catálogo
`modules.yaml` y motor de validación por registry.
</estado>

<arquitectura>
- Raíz: docs core (README, INDEX, ROADMAP, CHANGELOG, INTEGRACION, PROMPT_INICIO,
  CONTRIBUTING, CODE_OF_CONDUCT), entrypoints (`claude-init`, `install.sh`,
  `update.sh`), `validar_repo.py`, configs (`ruff.toml`, `.pre-commit-config.yaml`,
  `requirements.txt`).
- `validadores/`: motor reusable (`base.py` con BaseValidator [protegido, F401
  suprimido en ruff], `checks.py`, `reporte.py`).
- Un directorio por módulo canónico (agentes, skills, commands, hooks, plugins,
  mcp, agent-config, miniapps, modulo, proyecto, repositorios, estandares)
  con su `validar_<x>.py` y workflow CI.
- `repositorios/`: sub-perfiles (comun, docs-only, infra, mcp-server,
  library-design-system, dotfiles-config) + scripts de canon/auditoría.
- `.github/workflows/`: CI por módulo + globales (ci-global, pr-guardian,
  security-scan, release, link-check, validar-todos, libs `_lib-*`).
- `tests/`: `test_smoke.py`, `test_validadores.py`. `.claude/`: hook session-start.
- Bloque 2: `src/plantillas/` (framework), `pyproject.toml`, `modules.yaml`,
  `docs/dossier-bloque2.html` (artefacto visual, no sincronizado en GitHub).
</arquitectura>

<pendiente>
- Bloque 2: reestructura como paquete Python con CLI `plantillas`, registry de
  validadores, `modules.yaml` y agent-config Pydantic + Jinja2 (en planificación).
- ROADMAP Fase 3: versionado por módulo (manifest) y releases automatizadas
  vía GitHub Actions (3.1.3 / 3.1.4, ⏳) — puede migrarse al Bloque 2.
- ROADMAP Fase 3: prettier/yamlfmt en pre-commit, coverage de documentación
  (3.3.4 / 3.3.5, ⏳).
- ROADMAP Fase 4 completa (métricas de uso, dashboard de calidad, alertas,
  revisión periódica de enlaces/specs) ⏳ — puede absorberse por el dossier del
  Bloque 2.
- Consolidar entradas `[Unreleased]` en CHANGELOG en una sección única.
- Único TODO en código es lógica de detección del validador
  (`hooks/validar_hook.py`), no deuda pendiente.
</pendiente>

<notas>
- Reglas de oro (PROMPT_INICIO): no improvisar estructuras (usar plantilla del
  módulo); validar antes de commit (`python validar_repo.py --strict` o,
  en Bloque 2, `plantillas validate --all --strict` + `pre-commit run --all-files`);
  Conventional Commits; archivos core de raíz, estructura de módulos y `.gitignore`
  protegidos por CI; main con branch protection (todo por PR + review + checks verdes).
- Documentación clave: README, INDEX, ROADMAP, CHANGELOG, CONTRIBUTING, INTEGRACION,
  PROMPT_INICIO, CODE_OF_CONDUCT; docs/cli.md, docs/modules-yaml.md,
  docs/validators.md; dossier HTML del Bloque 2 en `docs/dossier-bloque2.html`.
- Inferido (sin ejecutar): el sistema es funcional — evidencia: 12 validadores,
  smoke tests que copian/validan cada plantilla, CI verde en historial, badge
  "validación 12/12". No se ejecutó nada para confirmar.
- Ubicación esperada en uso real: `~/.claude/plantillas` (symlink); remoto
  `github.com/Alexendros/plantillas`.
</notas>
