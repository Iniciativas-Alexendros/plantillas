# Changelog · mceod-overlays

## [v2.0.0-L1devops] — 2026-05-29

### L1 orientada a fullstack/devops

- `L1/CLAUDE.md.template` reescrito (v2.0.0): contexto devops de categoría de código
  (git/PR, build/test por stack, SUDAUTH, herencia L0/AXIS, punteros a CARTERA.md).
- `L1/settings.json.template`: allow-list git/gh/pnpm/cargo/python/docker + `ask`
  (push --force, gh pr merge, borrado de ramas) + `deny` (sudo, reset --hard, lectura
  de secretos). Claves del esquema oficial de Claude Code.
- `L1/gitignore.template`: añade node_modules, .venv, __pycache__, etc.
- Nuevos subdirectorios desplegables por `render_tree` (copia recursiva):
  - `L1/agents/`: code-reviewer, ci-runner, repo-developer, repo-launcher,
    incident-responder (adaptados del canon controlink-operator, sin runtime DCC).
  - `L1/skills/`: dev-revision-codigo, dev-estrategia-tests, app-ci-cd, app-despliegue,
    app-docker.
  - `L1/commands/`: integrar-homologacion.
  - `L1/plans/`: integracion-homologacion.md.
- Caveat: la L1 queda orientada a código (Repositorios). ShellScripts conserva la
  L1 v1.0.0 genérica salvo re-apply.

## [v1.0.0] — 2026-05-28

### Import inicial

- Importado desde `~/.claude/templates/` (estado pre-symlink).
- Niveles L0, L1, L2, L3 incluidos.
- Excluidos del traslado: `L2/CLAUDE.md.template.deprecated`, `L3/CLAUDE.md.template.deprecated` (MCEOD v2.0.0+ delega el cuerpo CLAUDE.md a `/init`).

### Origen

Reforma MCEOD v2.0.0 (Prepare → Init → Verify → Consolidate). Plantillas alineadas con la convención de marcadores `MCEOD:BEGIN`/`MCEOD:END` para overlays idempotentes en L2/L3.

### Sincronización con `~/.claude/templates/`

Tras este commit:

```
~/.claude/templates -> ~/Repositorios/plantillas/mceod-overlays
```

MCEOD lee a través del symlink; ediciones futuras se hacen en este repo.
