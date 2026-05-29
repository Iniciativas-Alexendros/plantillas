# Changelog · mceod-overlays

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
