# Integración Cruzada entre Módulos

> **Propósito**: Guía de cómo combinar agentes, skills, commands, hooks, MCP,
> plugins, miniapps y `agent-config` para construir configuraciones `.claude/`
> completas y coherentes.
>
> Actualizado tras la refactorización **Cross-platform Config** 2026-06-30
> (12 módulos canónicos).

---

## Mapa de relaciones

```
┌────────────────────────────────────────────────────────────────────────┐
│                       agent-config (reglas globales)                     │
│                                                                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────────┐  │
│  │  agents/     │  │  skills/     │  │  commands/                   │  │
│  │ (orquesta)   │←─┤ (conocim.)   │  │  (acciones manuales)         │  │
│  └──────┬───────┘  └──────┬───────┘  └──────────────────────────────┘  │
│         │                 │                                            │
│         └─────────────────┼──────────────┐                             │
│                           ↓              ↓                             │
│                  ┌──────────────┐ ┌──────────────┐                     │
│                  │ hooks/.sh    │ │  mcp.json    │←── MCP servers      │
│                  │ (seguridad)  │ │  (servers)   │                     │
│                  └──────────────┘ └──────────────┘                     │
│                                                                        │
│  ── Artefactos consumidos por agentes y skills ──────────────────────  │
│                                                                        │
│  ┌────────────┐                                                        │
│  │ miniapps/  │                                                        │
│  │ (SPA)      │                                                        │
│  └────────────┘                                                        │
│                                                                        │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │              plugins/ (empaquetado)                              │  │
│  │  Agente + Skills + Hooks + MCP + Miniapps → unidad distribuible  │  │
│  └──────────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────┘
```

---

## Patrones de integración

### 1. Agente + Skills

Un agente declara las skills que usa en el frontmatter del `.md` single-file:

```yaml
---
name: backend-dev
description: >
  Agente backend con skills de testing y seguridad. Invocar cuando una
  tarea toque API/DB de un proyecto Node/Python.
tools: [Read, Grep, Glob, Edit, Write, Bash, Agent]
model: sonnet
primary_skill: dev-arquitectura
---
```

Las skills se referencian por slug kebab (`dev-arquitectura`, `app-testing`).
Claude las carga cuando la descripción del agente o de la skill matchea el trigger del operador.

### 2. Agente + Subagentes

El agente orquestador delega a especialistas declarados en su sección `## Subagents`:

```markdown
## Subagents

| Subagente | Cuándo invocar | Devuelve |
|---|---|---|
| `Explore` | Codebase no familiar, >3 archivos | Markdown con paths + extractos |
| `code-reviewer` | Post-ejecución obligatoria | Hallazgos por severidad |
```

**Regla**: el orquestador nunca hace el trabajo técnico; delega y sintetiza.

### 3. Hooks (canon `.sh.template`) + Skills

Un hook single-file declara su matcher en cabecera y devuelve JSON al runtime:

```bash
#!/usr/bin/env bash
set -euo pipefail
# name: pre-bash-secret-guard
# matcher: PreToolUse
# tool_pattern: Bash(*)
# description: Bloquea ejecución de Bash si el comando contiene tokens.
# version: 0.1.0

input=$(cat)
cmd=$(echo "$input" | jq -r '.tool_input.command // "')
if grep -qE 'gh[pousr]_[A-Za-z0-9_]{36,}|sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}' <<< "$cmd"; then
  echo '{"decision":"deny","reason":"Token detectado en comando bash"}'
  exit 0
fi
echo '{"decision":"allow"}'
```

El hook se instala referenciándolo en `settings.json`:

```json
"hooks": {
  "PreToolUse": [
    {"matcher": "Bash", "hooks": [{"type": "command", "command": "~/.claude/hooks/pre-bash-secret-guard.sh"}]}
  ]
}
```

### 4. Commands + Skills

Un command single-file invoca skills como parte de su flujo:

```markdown
---
description: >
  /test-cobertura — ejecuta tests con cobertura y devuelve informe.
argument-hint: "<path> [--update-snapshots]"
allowed-tools: [Bash, Read, Grep]
---

## Instrucciones
1. Detectar runner (Jest/Vitest/pytest) por ficheros del proyecto.
2. Ejecutar con cobertura activada.
3. Activar skill `app-calidad` si la cobertura baja del umbral.
```

### 5. MCP + Agente/Skills

Un MCP server expone tools que el agente consume vía `mcp.json` separado:

```json
{
  "mcpServers": {
    "utils": {
      "command": "python",
      "args": ["mcp-servers/utils/server.py"]
    }
  }
}
```

> ⚠️ `mcp.json` vive en archivo separado, NO dentro de `settings.json`.

### 6. Miniapps (canon) consumidas por skills

Una skill que entrega visualización genera una mini-app reutilizable:

```yaml
---
name: kpi-mensual
description: >
  Mini-app dashboard que renderiza KPIs financieros mensuales.
category: dashboard
runtime: browser
version: 0.1.0
last_updated: 2026-05-23
---
```

La skill `COM_finanzas` puede referenciar `~/.claude/miniapps/kpi-mensual/` cuando el operador pide un resumen mensual.

### 7. agent-config como capa de control global

`agent-config/plantilla_agent_config.yaml` es la fuente canónica de reglas del operador, estilo, flujo, seguridad y herramientas. El generador emite:

- `~/.claude/CLAUDE.md` para Claude Code.
- `~/AGENTS.md` para OpenCode.
- `~/.config/devin/AGENTS.md` + `~/.config/devin/config.json` para Devin.
- `~/.codeium/windsurf/memories/global_rules.md` para Windsurf/Cascade.

Todo módulo instalado individualmente (`skills/`, `commands/`, `hooks/`, etc.) debe respetar la jerarquía declarada en `agent-config`: primero el deterministico, luego reglas globales, luego memory auto-generada.

---

## Decision tree: ¿Qué módulo necesito?

| Si quiero... | Uso | Ejemplo |
|---|---|---|
| Conocimiento persistente que se active automáticamente | **Skill** | `app-testing` se activa al mencionar "tests" |
| Acción que el usuario invoque explícitamente | **Command** | `/test-cobertura` |
| Controlar/auditar comportamiento del agente | **Hook** | PreToolUse que bloquea tokens |
| Exponer datos/tools externas a Claude | **MCP Server** | API de meteorología propia |
| Empaquetar todo para distribuir | **Plugin** | `backend-toolkit` |
| Orquestar especialistas | **Agente** | `backend-dev` delega a `database-expert` |
| Configuración global cross-platform | **agent-config** | `plantilla_agent_config.yaml` |
| Crear una SPA reutilizable | **Miniapp** | Dashboard KPIs single-file |

---

## Anti-patrones de integración

### ❌ Skill que hace de Command
Una skill que solo se activa manualmente con `/nombre` está mal diseñada.
**Fix**: Si es acción puntual del operador, conviértela en command; si es conocimiento, reescribe el `description` para que dispare automáticamente.

### ❌ Agente sin delegación
Un agente que intenta hacer todo sin subagentes.
**Fix**: Delegar tareas técnicas a subagentes especializados (sección `## Subagents`).

### ❌ Hook demasiado restrictivo
Un hook que bloquea todo sin clasificación.
**Fix**: Usar niveles `gray/green/amber/red` con acciones diferenciadas; emitir `{decision: "allow"}` con contexto en lugar de `deny` por defecto.

### ❌ MCP sin schema de input
Una tool MCP que acepta cualquier input sin validación.
**Fix**: Definir `inputSchema` con tipos, enums y campos requeridos.

### ❌ Plugin con dependencias circulares
Plugin A depende de B, y B de A.
**Fix**: Extraer dependencia común a un tercer plugin base.

### ❌ Miniapp con JS externo sin SRI
Dashboard que carga react/tailwind desde CDN sin `integrity=`.
**Fix**: Inline todo el JS/CSS, o si CDN es imprescindible, añadir hash SRI.

### ❌ `settings.json` con claves obsoletas
`hooks: {enabled: true, sources: [...]}` o `skills: {autoDiscover: true}` ya no son schema runtime.
**Fix**: Migrar a `hooks: {PreToolUse: [...], PostToolUse: [...]}` y borrar `skills.autoDiscover/preload`.

### ❌ Reglas duplicadas entre agent-config y CLAUDE.md local
El generador ya emite la capa global. No duplicarlas en `CLAUDE.md` de cada proyecto.
**Fix**: Usar `agent-config` para verdades globales; reservar `CLAUDE.md` del proyecto para contexto específico de ese repo.

---

## Ejemplo completo: Proyecto backend con módulos canónicos

```
mi-proyecto/
├── .claude/
│   ├── CLAUDE.md                       ← Contexto del proyecto (específico)
│   ├── settings.json                   ← Schema runtime: permissions + hooks + env
│   ├── mcp.json                        ← MCP servers (archivo separado)
│   │
│   ├── agents/
│   │   └── backend-dev.md              ← Single-file canon
│   │
│   ├── skills/
│   │   ├── app-testing/SKILL.md
│   │   └── app-seguridad/SKILL.md
│   │
│   ├── commands/
│   │   ├── test-cobertura.md           ← Single-file canon
│   │   └── deploy.md
│   │
│   ├── hooks/
│   │   ├── pre-bash-secret-guard.sh    ← Renombrado .sh, +x
│   │   └── post-format.sh
│   │
│   ├── miniapps/
│   │   └── kpi-mensual/
│   │       ├── kpi-mensual.md          ← Descriptor canon
│   │       └── kpi-mensual.html        ← SPA opcional
│   │
│   └── plugins/
│       └── backend-toolkit/plugin.json ← Empaqueta lo anterior
│
└── src/...
```

### Flujo de trabajo

1. **Operador escribe código** → Guarda archivo → hook `post-format.sh` formatea.
2. **Operador invoca `/test-cobertura`** → Command lanza tests → Si la cobertura cae, skill `app-testing` se activa para sugerir tests adicionales.
3. **Operador pregunta "¿qué diferencia hay entre tools y allowed-tools?"** → Skill `claude-code-guide` responde desde su `description`/reglas; no reabre el debate.
4. **Cierre mensual** → Operador abre `miniapps/kpi-mensual/kpi-mensual.html` para revisar KPIs antes de registrar en `EVENTOS.md`.
5. **Hook bloquea push con token** → `pre-bash-secret-guard.sh` detecta `gh_token_...` en comando `git push` y emite `{decision: "deny", reason: ...}`.

---

## Referencias

- [Claude Code: Subagents](https://code.claude.com/docs/en/sub-agents.md)
- [Claude Code: Skills](https://code.claude.com/docs/en/skills.md)
- [Claude Code: Commands](https://code.claude.com/docs/en/commands.md)
- [Claude Code: Hooks](https://code.claude.com/docs/en/hooks.md)
- [Claude Code: Settings](https://code.claude.com/docs/en/settings.md)
- [MCP Spec](https://modelcontextprotocol.io/specification/)
- CHANGELOG entrada `[Unreleased] — Cross-platform Config Refactor` — este repo
