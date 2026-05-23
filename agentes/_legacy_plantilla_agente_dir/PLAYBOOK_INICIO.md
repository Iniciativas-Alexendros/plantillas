# PLAYBOOK DE INICIO · Plantilla de Agente para Claude Code

> **Para quién es esto**: Para ti, LLM, que vas a usar esta plantilla para crear
> un nuevo agente o adaptar uno existente. Este directorio es un **playbook
> completo de autorrelleno**: cada archivo explica QUÉ debe contener, POR QUÉ,
> y CÓMO desarrollarlo.

---

## ¿Qué es esta plantilla?

`plantilla_agente` es un **esqueleto de agente orquestador** basado en las
mejores prácticas oficiales de:

- **Anthropic** (Claude Code / Agent SDK / MCP)
- **OpenAI** (Agents SDK)
- **Google** (Agent Development Kit)

No es un agente funcional por sí solo. Es un **kit de construcción** que tú
(LLM) debes completar siguiendo las instrucciones de cada archivo.

---

## Flujo de trabajo: Cómo usar esta plantilla

### Paso 0: Entender el objetivo

Antes de tocar nada, responde estas preguntas:

1. **¿Qué problema resuelve el agente?** (ej: "Revisa código de seguridad",
   "Genera documentación técnica", "Orquesta despliegues")
2. **¿Quién lo usará?** (desarrollador junior, tech lead, DevOps, legal...)
3. **¿Qué herramientas necesita?** (solo filesystem, o también APIs, DBs, GitHub...)
4. **¿Es un agente único o un sistema multi-agente?** (orquestador + especialistas)

### Paso 1: Copiar la plantilla

```bash
# Global (disponible en todos los proyectos)
cp -r ~/.claude/plantillas/agentes/plantilla_agente ~/.claude/agents/MI_AGENTE

# O por proyecto (solo en este repo)
cp -r ~/.claude/plantillas/agentes/plantilla_agente ./.claude/agents/MI_AGENTE
```

> **IMPORTANTE**: Reemplaza `MI_AGENTE` por un nombre descriptivo en
> `kebab-case` (ej: `security-reviewer`, `deploy-orchestrator`).

### Paso 2: Autorrellenar siguiendo el orden

**NO hagas todos los archivos a la vez.** Sigue este orden; cada paso informa
el siguiente:

| Orden | Archivo | Qué defines aquí |
|-------|---------|------------------|
| 1 | `AGENT.md` | Identidad, modelo, tools, permisos del agente principal |
| 2 | `prompts/persona.md` | Personalidad, tono, valores, sesgos a vigilar |
| 3 | `prompts/system.md` | Principios operativos, flujo de trabajo, estilo de output |
| 4 | `config/settings.json` | Config técnica: tokens, timeouts, MCP, observability |
| 5 | `config/permissions.yaml` | Guardrails de seguridad granular |
| 6 | `prompts/tasks/*.md` | Prompts especializados por tipo de tarea |
| 7 | `subagents/*.md` | Subagentes especializados (si aplica multi-agente) |
| 8 | `skills/__SKILL_NOMBRE__/SKILL.md` | Skills reutilizables embebidas |
| 9 | `tools/mcp.json` | Servidores MCP externos a conectar |
| 10 | `hooks/*.yaml` | Hooks de interceptación (pre/post tool) |
| 11 | `memory/context.md` | Plantilla de memoria de sesión |
| 12 | `references/*.md` | Documentación de referencia del dominio |
| 13 | `README.md` | Documentación final para el usuario humano |

### Paso 3: Validar

Después de completar, ejecuta este checklist:

- [ ] `AGENT.md` tiene `name` y `description` específicos del dominio.
- [ ] `description` explica CUÁNDO usar el agente (triggers de invocación).
- [ ] `tools` lista solo las necesarias (principio de mínimo privilegio).
- [ ] `subagents/*.md` definen roles NO solapados (cada uno tiene un propósito único).
- [ ] `permissions.yaml` tiene al menos una regla `denylist` en `bash` y `filesystem`.
- [ ] `skills/__SKILL_NOMBRE__/` ha sido renombrada y contiene reglas reales del dominio.
- [ ] `tools/mcp.json` solo incluye servidores que el usuario realmente tiene configurados.
- [ ] `PLAYBOOK_INICIO.md` se elimina o se reemplaza por `README.md` personalizado.

### Paso 4: Probar

1. Invoca el agente: `/nombre-del-agente <tarea de prueba>`
2. Verifica que carga correctamente (sin errores de parseo).
3. Verifica que el comportamiento se alinea con la persona definida.
4. Itera: ajusta prompts, permisos, o subagentes según observaciones.

---

## Reglas de oro para el autorrelleno

1. **Especificidad > Genericidad**: "Revisa código" es malo. "Revisa código
   Python buscando race conditions y SQL injection" es bueno.
2. **Mínimo privilegio**: Lista solo las tools que necesita. Es más fácil
   añadir después que quitar.
3. **Un subagente = una responsabilidad**: Si un subagente hace 3 cosas,
   divídelo en 3.
4. **Los prompts son código**: Trátalos con la misma rigurosidad que el código
   de producción. Testéalos.
5. **Documenta las decisiones**: Si eliges un approach arquitectónico, pon el
   "por qué" en `references/architecture.md`.

---

## Referencias oficiales (consultar durante el desarrollo)

| Recurso | URL | Para qué usarlo |
|---------|-----|-----------------|
| Claude Code Docs (índice) | https://code.claude.com/docs/llms.txt | Todo sobre skills, subagents, hooks |
| Subagents Reference | https://code.claude.com/docs/en/sub-agents.md | Sintaxis de frontmatter, herencia, tools |
| Skills in SDK | https://code.claude.com/docs/en/agent-sdk/skills.md | Estructura SKILL.md, progressive disclosure |
| Hooks Reference | https://code.claude.com/docs/en/hooks.md | Eventos, schemas, async hooks |
| MCP Spec | https://modelcontextprotocol.io/specification/2025-11-25/index.md | Protocolo completo tools/resources/prompts |
| MCP Tools | https://modelcontextprotocol.io/specification/2025-11-25/server/tools.md | Definición de tools, schemas, errores |
| OpenAI Agents SDK | https://openai.github.io/openai-agents-python/ | Patrones handoff, guardrails, tracing |
| Google ADK Docs | https://google.github.io/adk-docs/ | Multi-agent hierarchy, A2A, deployment |

---

## Estructura visual de la plantilla

```
plantilla_agente/
├── PLAYBOOK_INICIO.md          ← ESTE ARCHIVO (eliminar tras usar)
├── AGENT.md                    ← Paso 1: Identidad del agente
├── README.md                   ← Paso 13: Doc para usuario humano
├── config/
│   ├── settings.json           ← Paso 4: Config técnica
│   └── permissions.yaml        ← Paso 5: Guardrails
├── prompts/
│   ├── system.md               ← Paso 3: Principios operativos
│   ├── persona.md              ← Paso 2: Personalidad
│   └── tasks/
│       ├── explore.md          ← Paso 6: Prompt exploración
│       ├── plan.md             ← Paso 6: Prompt planificación
│       └── execute.md          ← Paso 6: Prompt ejecución
├── tools/
│   ├── README.md               ← Catálogo de tools disponibles
│   ├── mcp.json                ← Paso 9: Servidores MCP
│   └── custom/                 ← (reservado) Tools custom
├── skills/
│   └── __SKILL_NOMBRE__/       ← Paso 8: Skills embebidas
│       └── SKILL.md
├── memory/
│   └── context.md              ← Paso 11: Memoria de sesión
├── hooks/
│   └── pre-tool-use.yaml       ← Paso 10: Hooks
├── subagents/                  ← Paso 7: Especialistas
│   ├── explorer.md
│   ├── planner.md
│   └── reviewer.md
└── references/                 ← Paso 12: Documentación dominio
    ├── architecture.md
    └── best-practices.md
```

---

## Nota final

> Esta plantilla fue construida a partir de una investigación de fuentes
> oficiales de Anthropic, OpenAI, y Google en mayo de 2026. Si las APIs o
> convenciones han cambiado, consulta los enlaces de referencia oficiales
> arriba antes de completar el agente.

**¡Manos a la obra! Empieza por `AGENT.md`.**
