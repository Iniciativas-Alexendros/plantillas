# mceod-overlays · Scaffolding L0–L3 para MCEOD

> **Módulo de plantillas overlay** que alimenta el orquestador
> `~/.claude/scripts/claude-deploy.sh` (MCEOD v2.0.0+).
> Importado desde `~/.claude/templates/` el **2026-05-28** como single source of truth versionada.

---

## Posición en el ecosistema `plantillas/`

| Módulo | Paradigma | Para qué |
|---|---|---|
| `dot-claude/` | **Canon completo** | `.claude/` listo para copiar a un repo (`cp -r ejemplo_dot_claude/ .claude/`) |
| `mceod-overlays/` | **Scaffolding por nivel** | MCEOD aplica L0–L3 selectivamente al árbol de scopes del operador (`$HOME` → repos → subproyectos) |

Coexisten: `dot-claude` cubre el caso “quiero `.claude/` en mi repo”; `mceod-overlays` cubre el caso “quiero gestionar la jerarquía completa de overlays bajo `$HOME` con auditoría y rollback”.

## Estructura

```
mceod-overlays/
├── L0/   # Transversal — $HOME/.claude (operador completo)
├── L1/   # Categoría    — $HOME/<dir>/.claude (Repositorios, Vaults, ml…)
├── L2/   # Repo         — $HOME/<dir>/<repo>/.claude (cuerpo CLAUDE.md vía /init)
└── L3/   # Subproyecto  — $HOME/<dir>/<repo>/<sub>/.claude
```

Cada nivel contiene `*.template` que `claude-deploy.sh render_tree` procesa con sustitución `{{VAR}}`:
- `settings.json.template`, `settings.local.json.example`, `gitignore.template` → renombrados a sus nombres finales.
- L0/L1: `CLAUDE.md.template` se renderiza directo.
- L2/L3: el cuerpo del `CLAUDE.md` lo emite `/init` real de Claude Code; MCEOD solo aporta `_INIT.md.template` (guía operador) y `overlay-metadata.template` (bloque BEGIN/END que `consolidate` inyecta en el CLAUDE.md generado).

## Ciclo MCEOD por nivel

- **L0/L1**: `apply` (cuerpo desde plantilla) → `check-drift` / `rollback`.
- **L2/L3**: `prepare` (scaffolding sin CLAUDE.md) → operador ejecuta `/init` → `consolidate` (inyecta overlay) → `verify`.

Detalle en `~/.claude/MCEOD.md`.

## Integración con `~/.claude/templates/`

`~/.claude/templates/` es **symlink** a este directorio:

```
~/.claude/templates -> ~/Repositorios/plantillas/mceod-overlays
```

Las ediciones se hacen en este repo (versionadas en git); MCEOD lee a través del symlink. El script `claude-deploy.sh` resuelve el path con `readlink -f` y registra el commit-sha activo en `~/.claude/audit/deployments.jsonl`.

## Validación

Pendiente: `validar_mceod_overlays.py` análogo al `validar_dot_claude.py` del módulo `dot-claude/`. Mientras tanto, `claude-deploy.sh dry-run` + `check-drift` cubren la verificación operativa.
