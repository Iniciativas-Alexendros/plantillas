# CLAUDE.md — plantillas

<proyecto>
Sistema de Plantillas Modulares para Claude Code: ecosistema `claude-init`-ready
para inicializar, validar y mantener componentes de Claude Code (agentes, skills,
commands, hooks, plugins, mcp, dot-claude, repositorios + módulos canon nuevos:
miniapps, autoresearch, cuadernos, knowledge). Patrón estricto por módulo:
`plantilla_<x>` (playbook) + `ejemplo_<x>` (referencia funcional) +
`validar_<x>.py` (validador con `--strict`) + workflow CI propio.
Autor: Alejandro · Iniciativas Alexendros. Licencia MIT.
</proyecto>

<stack>
- Python 3.12+ (validadores y motor reusable; única dependencia: `pyyaml`).
- Bash (entrypoints: `claude-init`, `install.sh`, `update.sh`).
- Contenido en Markdown/YAML/JSON. CI: GitHub Actions. Calidad: pre-commit, ruff.
Comandos REALES (verificados en README/PROMPT_INICIO/claude-init):
- `claude-init --list` · `claude-init --modulo <nombre> --nombre mi-x`
- `claude-init --repositorio --nombre mi-repo` · `claude-init --proyecto`
- `python validar_repo.py --strict` (validador global de raíz)
- `python <modulo>/validar_<modulo>.py <ruta> --strict` (validador por módulo)
- `python tests/test_smoke.py` o `pytest tests/ -v` (smoke + unit; requiere pytest)
- `pre-commit run --all-files`
</stack>

<estado>
Activo. 42 commits; último 2026-06-19 (rama main). README declara v1.0.0;
CHANGELOG tiene varias entradas `[Unreleased]` (trabajo reciente: calibración CI
docs-only, plantilla L1 fullstack, fix validadores). ROADMAP: Fases 1-3
completadas; Fase 4 (operación/mantenimiento) pendiente. Madurez alta:
14 validadores, ~16 workflows CI, tests, pre-commit, branch protection documentada.
</estado>

<arquitectura>
- Raíz: docs core (README, INDEX, ROADMAP, CHANGELOG, INTEGRACION, PROMPT_INICIO,
  CONTRIBUTING, CODE_OF_CONDUCT), entrypoints (`claude-init`, `install.sh`,
  `update.sh`), `validar_repo.py`, configs (`ruff.toml`, `.pre-commit-config.yaml`,
  `requirements.txt`).
- `validadores/`: motor reusable (`base.py` con BaseValidator [protegido, F401
  suprimido en ruff], `checks.py`, `reporte.py`).
- Un directorio por módulo (agentes, skills, commands, hooks, plugins, mcp,
  dot-claude, miniapps, autoresearch, cuadernos, knowledge, modulo, proyecto,
  repositorios, mceod-overlays) cada uno con su `validar_<x>.py`.
- `repositorios/`: sub-perfiles (comun, docs-only, infra, mcp-server,
  library-design-system, dotfiles-config) + scripts de canon/auditoría.
- `.github/workflows/`: CI por módulo + globales (ci-global, pr-guardian,
  security-scan, release, link-check, validar-todos, libs `_lib-*`).
- `tests/`: `test_smoke.py`, `test_validadores.py`. `.claude/`: hook session-start.
</arquitectura>

<pendiente>
- ROADMAP Fase 3: versionado por módulo (manifest) y releases automatizadas
  vía GitHub Actions (3.1.3 / 3.1.4, ⏳).
- ROADMAP Fase 3: prettier/yamlfmt en pre-commit, coverage de documentación
  (3.3.4 / 3.3.5, ⏳).
- ROADMAP Fase 4 completa (métricas de uso, dashboard de calidad, alertas,
  revisión periódica de enlaces/specs) ⏳.
- Varias entradas `[Unreleased]` en CHANGELOG sin consolidar en una versión.
- Único TODO en código es lógica de detección del validador
  (`hooks/validar_hook.py`), no deuda pendiente.
</pendiente>

<notas>
- Reglas de oro (PROMPT_INICIO): no improvisar estructuras (usar plantilla del
  módulo); validar antes de commit (`python validar_repo.py --strict` +
  `pre-commit run --all-files`); Conventional Commits; archivos core de raíz,
  estructura de módulos y `.gitignore` protegidos por CI; main con branch
  protection (todo por PR + review + checks verdes).
- Inferido (sin ejecutar): el sistema es funcional — evidencia: 14 validadores,
  smoke tests que copian/validan cada plantilla, CI verde en historial, badge
  "validación 8/8". No se ejecutó nada para confirmar.
- Ubicación esperada en uso real: `~/.claude/plantillas` (symlink); remoto
  `github.com/Alexendros/plantillas`.
- `mceod-overlays/` fue eliminado y reintroducido en commits recientes; revisar
  su estado actual antes de tocarlo.
</notas>
