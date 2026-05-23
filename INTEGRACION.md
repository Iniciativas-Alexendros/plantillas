# Integración Cruzada entre Módulos

> **Propósito**: Guía de cómo combinar agentes, skills, commands, hooks, MCP servers
> y plugins para construir configuraciones `.claude/` completas y coherentes.

---

## Mapa de relaciones

```
┌─────────────────────────────────────────────────────────────────┐
│                     .claude/ (dot-claude)                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │   agents/   │  │  skills/    │  │       commands/         │  │
│  │  (orquesta) │←─┤  (conocim.) │  │  (acciones manuales)    │  │
│  └──────┬──────┘  └──────┬──────┘  └─────────────────────────┘  │
│         │                │                                       │
│         └────────────────┼──────────────────┐                    │
│                          ↓                  ↓                    │
│                   ┌─────────────┐    ┌─────────────┐             │
│                   │   hooks/    │    │   mcp.json  │←── MCP      │
│                   │ (seguridad) │    │  (servers)  │    servers   │
│                   └─────────────┘    └─────────────┘             │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              plugins/ (empaquetado)                      │   │
│  │  Agente + Skills + Hooks + MCP → unidad distribuible     │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Patrones de integración

### 1. Agente + Skills

Un agente declara las skills que necesita en su `AGENT.md` frontmatter:

```yaml
---
name: backend-dev
skills:
  - testing-pytest
  - api-security
---
```

Claude carga automáticamente `testing-pytest/SKILL.md` y `api-security/SKILL.md`
cuando detecta que la tarea del usuario coincide con sus descripciones.

**Flujo**:
1. Usuario: "Escribe tests para este endpoint"
2. Claude detecta trigger de `testing-pytest` → carga la skill
3. Aplica reglas de la skill + contexto del agente

### 2. Agente + Subagentes

El agente orquestador delega a especialistas:

```
agents/
├── backend-dev/
│   ├── AGENT.md          ← Orquestador
│   └── subagents/
│       ├── database-expert.md
│       └── security-auditor.md
```

**Regla**: El orquestador nunca hace el trabajo técnico; delega y sintetiza resultados.

### 3. Hooks + Skills

Un hook puede activar skills de forma condicional:

```yaml
# hooks/pre-tool-use.yaml
triggers:
  - tool: Bash
    condition: 'command matches "pytest"'
    action: allow
    post_action: activate_skill(testing-pytest)
```

Esto permite que, tras ejecutar `pytest`, Claude tenga cargada la skill de testing
para interpretar resultados y sugerir mejoras.

### 4. Commands + Skills

Un command puede activar una skill como parte de su flujo:

```markdown
# commands/test/COMMAND.md
## Instrucciones
1. Ejecutar tests (`pytest` / `npm test`).
2. Activar skill `testing-pytest` para analizar fallos.
3. Sugerir fixes basados en reglas de la skill.
```

### 5. MCP + Agente/Skills

Un MCP server expone tools que el agente consume:

```json
// tools/mcp.json
{
  "mcpServers": {
    "utils": {
      "command": "python",
      "args": ["mcp-servers/utils/server.py"]
    }
  }
}
```

La skill `api-security` puede usar `get_timestamp` del MCP server para
auditar logs con marca temporal precisa.

### 6. Plugin = Todo junto

Un plugin empaqueta la integración completa:

```json
// plugin.json
{
  "name": "backend-toolkit",
  "components": {
    "agents": ["backend-dev"],
    "skills": ["testing-pytest", "api-security"],
    "hooks": ["pre-tool-use"],
    "mcpServers": ["utils"]
  }
}
```

Instalar el plugin equivale a instalar toda la cadena de integración de una vez.

---

## Decision tree: ¿Qué módulo necesito?

| Si quiero... | Uso | Ejemplo |
|---|---|---|
| Conocimiento persistente que se active automáticamente | **Skill** | `testing-pytest` se activa al mencionar "tests" |
| Una acción que el usuario invoque explícitamente | **Command** | `/deploy` para staging |
| Controlar o auditar comportamiento del agente | **Hook** | PreToolUse que pide confirmación antes de `rm -rf` |
| Exponer datos/tools externas a Claude | **MCP Server** | `get_weather` o integración con API propia |
| Empaquetar todo lo anterior para distribuir | **Plugin** | `backend-toolkit` con 2 skills + 1 hook + 1 MCP |
| Orquestar múltiples especialistas | **Agente** | `backend-dev` delega a `database-expert` y `security-auditor` |
| Configurar un proyecto/entorno completo | **dot-claude** | `~/.claude/` con agents, skills, commands, hooks, MCP |

---

## Anti-patrones de integración

### ❌ Skill que hace de Command
Una skill que solo se activa manualmente vía `/nombre` está mal diseñada.
**Fix**: Convertir a command si es acción puntual; o reescribir la description
para que sea triggerable automáticamente.

### ❌ Agente sin delegación
Un agente que intenta hacer todo directamente sin subagentes.
**Fix**: Delegar tareas técnicas a subagentes especializados.

### ❌ Hook demasiado restrictivo
Un hook que bloquea todo sin clasificación de riesgo.
**Fix**: Usar niveles gray/green/amber/red con acciones diferenciadas.

### ❌ MCP sin schema de input
Una tool que acepta cualquier input sin validación.
**Fix**: Definir `inputSchema` con tipos, enums y campos requeridos.

### ❌ Plugin con dependencias circulares
Plugin A depende de Plugin B, y B depende de A.
**Fix**: Extraer dependencia común a un tercer plugin base.

---

## Ejemplo completo: Proyecto backend

```
mi-proyecto/
├── .claude/
│   ├── CLAUDE.md              ← Reglas globales del proyecto
│   ├── settings.json          ← Model=sonnet, idioma=es
│   ├── mcp.json               ← MCP servers del proyecto
│   │
│   ├── agents/
│   │   └── backend-dev/       ← Orquestador con skills + subagentes
│   │       ├── AGENT.md
│   │       ├── prompts/
│   │       ├── subagents/
│   │       │   ├── database-expert.md
│   │       │   └── security-auditor.md
│   │       └── skills/        ← Symlinks a skills globales
│   │
│   ├── skills/
│   │   ├── testing-pytest/    ← Skill global (instalada vía plugin)
│   │   │   └── SKILL.md
│   │   └── api-security/
│   │       └── SKILL.md
│   │
│   ├── commands/
│   │   ├── deploy.md          ← /deploy
│   │   ├── test.md            ← /test
│   │   └── review.md          ← /review
│   │
│   ├── hooks/
│   │   ├── pre-tool-use.yaml  ← Seguridad + backups
│   │   ├── post-save.yaml     ← Formateo automático
│   │   └── on-error.yaml      ← Reintentos + escalación
│   │
│   └── plugins/
│       └── backend-toolkit/   ← Plugin que empaqueta todo
│           └── plugin.json
│
└── src/
    └── ...
```

### Flujo de trabajo

1. **Developer escribe código** → Guarda archivo → `post-save.yaml` formatea automáticamente.
2. **Developer invoca `/test`** → Command ejecuta tests → Si fallan, skill `testing-pytest` se activa para sugerir fixes.
3. **Developer invoca `/deploy`** → Command detecta cambios → Hook `pre-tool-use` valida que no haya comandos peligrosos en el deploy script.
4. **Error en deploy** → Hook `on-error` clasifica el error → Si es retryable, reintenta 3 veces con backoff → Si persiste, escala al agente `backend-dev`.
5. **Agente `backend-dev` analiza** → Delega a `security-auditor` si el error es de permisos → Sintetiza respuesta final.

---

## Referencias

- [Claude Code: Subagents](https://code.claude.com/docs/en/sub-agents.md)
- [Claude Code: Skills](https://code.claude.com/docs/en/skills.md)
- [Claude Code: Commands](https://code.claude.com/docs/en/commands.md)
- [Claude Code: Hooks](https://code.claude.com/docs/en/hooks.md)
- [MCP Spec](https://modelcontextprotocol.io/specification/2025-11-25/index.md)
