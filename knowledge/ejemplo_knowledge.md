---
name: tools-vs-allowed-tools
description: >
  Explica la diferencia semántica entre el campo `tools` del frontmatter
  de un agente y el campo `allowed-tools` del frontmatter de un command
  slash en Claude Code. Cuándo usar cada uno, efectos en runtime y
  anti-patrones comunes.
domain: claude-code-internals
references:
  - "Anthropic Docs · Agents overview · https://docs.claude.com/en/claude-code/agents"
  - "Anthropic Docs · Slash commands · https://docs.claude.com/en/claude-code/slash-commands"
related_skills:
  - CREA_skill
  - CREA_mcp
status: published
last_updated: 2026-05-23
authority: official
---

## Resumen

En Claude Code existen dos mecanismos distintos para declarar qué herramientas
puede invocar un componente: `tools` (frontmatter de agente sub-agent) y
`allowed-tools` (frontmatter de command slash). Aunque ambos restringen el
acceso a herramientas, operan en capas diferentes del runtime y su semántica
difiere en alcance, herencia y momento de evaluación. Confundirlos es el
error más frecuente al crear agentes y commands nuevos.

## Contenido

### `tools` — frontmatter de agente

El campo `tools` aparece en el YAML frontmatter del archivo `.md` que define
un **sub-agente** (bajo `~/.claude/agents/<slug>.md`). Declara la lista
explícita de herramientas (built-in o MCP) que el agente puede invocar
durante su ejecución autónoma.

```yaml
---
name: mi-agente
description: Hace X cuando Y.
tools:
  - Read
  - Bash
  - mcp__hostinger__VPS_getVirtualMachinesV1
---
```

Comportamiento en runtime:
- Claude rechazará con error cualquier intento del agente de llamar a una
  herramienta no listada en `tools`.
- Si el campo `tools` está ausente, el agente hereda las herramientas
  disponibles en el contexto padre (puede ser amplio).
- Lista vacía (`tools: []`) = agente sin herramientas (solo razonamiento).
- El operador humano puede ampliar o reducir la lista sin modificar el
  comportamiento lógico del agente.

### `allowed-tools` — frontmatter de command slash

El campo `allowed-tools` aparece en el YAML frontmatter de un **command slash**
(archivo `.md` bajo `.claude/commands/<slug>.md`). Declara qué herramientas
puede invocar Claude durante la ejecución de ese command concreto.

```yaml
---
description: Ejecuta un análisis rápido.
allowed-tools:
  - Read
  - Glob
---
```

Comportamiento en runtime:
- Restringe las herramientas disponibles **para esa sesión de command**.
- No afecta a sub-agentes invocados desde dentro del command; esos agentes
  siguen usando su propia lista `tools`.
- Si `allowed-tools` está ausente, el command no añade restricciones propias
  (hereda el contexto del hilo).

### Tabla comparativa

| Aspecto              | `tools` (agente)            | `allowed-tools` (command)          |
|----------------------|-----------------------------|------------------------------------|
| Archivo              | `agents/<slug>.md`          | `commands/<slug>.md`               |
| Ámbito               | Toda la ejecución del agente| Solo durante el command            |
| Herencia al padre    | No (agente es autónomo)     | No aplica (el command IS el hilo)  |
| Herencia a hijos     | Hijos definen las suyas     | Sub-agentes usan sus propias `tools`|
| Ausente = ...        | Hereda contexto padre       | Sin restricción extra              |
| Lista vacía = ...    | Sin herramientas            | Sin restricción extra (vacía se ignora)|

## Aplicación

- **Cuándo usar `tools` en agente**: siempre que el agente deba operar con
  autonomía limitada (principio de mínimo privilegio). Listar solo lo que el
  agente necesita; no usar wildcard.
- **Cuándo usar `allowed-tools` en command**: cuando quieras que un command
  slash exponga solo un subconjunto de herramientas al usuario que lo invoca,
  independientemente de cuáles estén disponibles globalmente.
- **Anti-patrón — campo cruzado**: poner `allowed-tools` en un agente o `tools`
  en un command no causa error de parse (YAML lo acepta), pero el runtime
  ignora el campo equivocado; el agente queda sin restricciones o el command
  sin las esperadas.
- **Anti-patrón — lista vacía en command**: `allowed-tools: []` no restringe
  nada en la mayoría de versiones del runtime; omitir el campo es equivalente
  y más claro.

```yaml
# CORRECTO — agente con mínimo privilegio
tools:
  - Read
  - mcp__mi_server__get_data

# CORRECTO — command que solo necesita lectura
allowed-tools:
  - Read
  - Glob
  - LS

# INCORRECTO — allowed-tools en agente (el runtime lo ignora)
allowed-tools:
  - Read
```

## Limitaciones

- El comportamiento exacto cuando `tools` está ausente en un agente puede
  variar entre versiones de Claude Code. Siempre declarar `tools` explícitamente
  para comportamiento predecible.
- MCP tools en `tools` requieren que el servidor MCP esté registrado en
  `mcp.json` del proyecto; de lo contrario el agente falla en runtime aunque
  la herramienta esté listada.
- `allowed-tools` no admite wildcards ni patrones glob; solo nombres exactos
  de herramientas.
- Este artículo refleja el comportamiento documentado a 2026-05-23. Verificar
  notas de release al actualizar Claude Code.

## Referencias

- Anthropic Docs · Agents overview · https://docs.claude.com/en/claude-code/agents
- Anthropic Docs · Slash commands · https://docs.claude.com/en/claude-code/slash-commands
