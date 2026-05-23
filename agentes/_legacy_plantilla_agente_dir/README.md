# [Nombre del Agente]

> [Tagline de una línea que describa qué hace este agente]

## Qué es

[Descripción de 2-3 párrafos del agente: su propósito, su dominio, y
quién lo usaría.]

## Arquitectura

```
[Nombre del agente]/
├── AGENT.md              ← Definición principal del agente
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
│   ├── mcp.json          ← Configuración MCP servers
│   └── custom/           ← Herramientas custom
├── skills/               ← Skills embebidas
│   └── [nombre-skill]/
│       └── SKILL.md
├── memory/               ← Memoria de sesión
│   └── context.md
├── hooks/                ← Interceptores de ejecución
│   └── pre-tool-use.yaml
├── subagents/            ← Especialistas
│   ├── explorer.md       ← Mapeo no destructivo
│   ├── planner.md        ← Diseño de approaches
│   └── reviewer.md       ← Revisión de calidad
└── references/           ← Documentación de referencia
    ├── architecture.md   ← Decisiones arquitectónicas
    └── best-practices.md ← Mejores prácticas del dominio
```

## Uso

### Activación

Este agente se detecta automáticamente si está en:
- `~/.claude/agents/` (global)
- `./.claude/agents/` (proyecto)

### Invocación manual

```
/[nombre-del-agente] <tu tarea aquí>
```

### Ejemplos de uso

```
/[nombre-del-agente] [ejemplo de tarea 1]
/[nombre-del-agente] [ejemplo de tarea 2]
```

## Personalización

Para adaptar este agente a tus necesidades:

1. Copia el directorio:
   ```bash
   cp -r [nombre-del-agente] mi-agente-personalizado
   ```
2. Edita `AGENT.md` para cambiar el nombre, descripción, y modelo.
3. Adapta `prompts/persona.md` al tono y personalidad deseados.
4. Configura `tools/mcp.json` con tus servidores MCP.
5. Ajusta `subagents/` según necesidades especializadas.

## Dependencias

- [Requisito 1]
- [Requisito 2]
- [Variable de entorno necesaria]

## Licencia

[MIT / Apache-2.0 / Tu licencia]

---

*Agente construido con la plantilla `plantilla_agente` de ~/.claude/plantillas/*
