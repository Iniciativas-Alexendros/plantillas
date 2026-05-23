# ejemplo-agente

> Agente orquestador de software engineering con patrón hub-and-spoke

## Qué es

`ejemplo-agente` es un **agente orquestador funcional** que demuestra cómo
se ve un agente completamente configurado siguiendo las mejores prácticas
de Anthropic, OpenAI, y Google.

A diferencia de `plantilla_agente` (que es un kit de construcción con
instrucciones), este directorio contiene un agente **listo para usar**:
prompts concretos, skills funcionales, subagentes definidos, y configuración
operativa.

## Arquitectura

```
ejemplo-agente/
├── AGENT.md              ← Definición principal (frontmatter + instrucciones)
├── README.md             ← Este archivo
├── config/               ← Configuración y permisos
│   ├── settings.json     ← Config técnica (modelo, tokens, MCP)
│   └── permissions.yaml  ← Guardrails de seguridad
├── prompts/              ← Prompts sistema y especializados
│   ├── system.md         ← Principios operativos
│   ├── persona.md        ← Personalidad y tono
│   └── tasks/            ← Prompts por tipo de tarea
│       ├── explore.md    ← Exploración de codebase
│       ├── plan.md       ← Planificación técnica
│       └── execute.md    ← Ejecución de cambios
├── tools/                ← Catálogo de herramientas
│   ├── README.md         ← Documentación de tools
│   └── mcp.json          ← Configuración MCP servers
├── skills/               ← Skills embebidas
│   └── diagramador/
│       └── SKILL.md      ← Generación de diagramas Mermaid
├── memory/               ← Memoria de sesión
│   └── context.md
├── hooks/                ← Interceptores de ejecución
│   └── pre-tool-use.yaml ← Validación de seguridad pre-tool
├── subagents/            ← Especialistas
│   ├── explorer.md       ← Mapeo no destructivo
│   ├── planner.md        ← Diseño de approaches
│   └── reviewer.md       ← Revisión de calidad
└── references/           ← Documentación de referencia
    ├── architecture.md   ← Patrón hub-and-spoke, decisiones
    └── best-practices.md ← Síntesis oficial
```

## Uso

### Activación

Este agente se detecta automáticamente si está en:
- `~/.claude/agents/` (global)
- `./.claude/agents/` (proyecto)

### Invocación manual

```
/ejemplo-agente <tu tarea aquí>
```

### Ejemplos de uso

```
/ejemplo-agente Explora este codebase y dime la arquitectura
/ejemplo-agente Planifica la implementación de auth JWT
/ejemplo-agente Revisa los últimos cambios de seguridad
```

## Diferencia con `plantilla_agente`

| | `plantilla_agente` | `ejemplo_agente` |
|---|---|---|
| **Propósito** | Construir nuevos agentes | Usar directamente como referencia |
| **Contenido** | Instrucciones + placeholders | Contenido real y funcional |
| **Destinatario** | LLM constructor | Usuario final |
| **Estado** | Plantilla incompleta | Agente operativo |

## Licencia

MIT — Úsalo como punto de partida para tus propios agentes.

---

*Agente construido con la plantilla `plantilla_agente` de ~/.claude/plantillas/agentes/*
