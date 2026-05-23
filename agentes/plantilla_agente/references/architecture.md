# references/architecture.md · Playbook de contenido

> **Propósito**: Documenta las decisiones arquitectónicas del agente:
> patrones de diseño, flujo de mensajes, elección de modelos, y
> justificaciones de "por qué".
>
> **Qué hacer**: Este es un **documento vivo**. Actualízalo cuando cambien
> decisiones arquitectónicas. Elimina estas instrucciones.

---

## INSTRUCCIONES: Patrón de Arquitectura

### Diagrama de arquitectura

Crea un diagrama ASCII o Mermaid del patrón de tu agente:

```markdown
## Patrón: [Nombre del patrón]

```
[Diagrama visual de la arquitectura]
```
```

### Patrones comunes:

| Patrón | Cuándo usar | Ejemplo |
|---|---|---|
| **Hub-and-Spoke** | Orquestador central + especialistas | Portfolio manager + analistas |
| **Pipeline secuencial** | Tareas con dependencias lineales | CI/CD: build → test → deploy |
| **DAG (Directed Acyclic Graph)** | Investigación con sub-preguntas | Deep research con dependencias |
| **Red de agentes** | Colaboración peer-to-peer | Equipo de revisión con consenso |
| **Loop reflexivo** | Mejora iterativa | Code generation → test → fix → repeat |

---

## INSTRUCCIONES: Flujo de Mensajes

### Caso de uso principal

Documenta el flujo completo de mensajes para el caso de uso más común:

```markdown
### Caso: [Nombre del caso]

```
Usuario: "[Input típico]"
  → [Agente 1]: [Qué hace]
  → [Agente 2]: [Qué hace]
  → [Agente 3]: [Qué hace]
  → [Output final]
```
```

### Ejemplo completado:

```markdown
### Caso: Nueva Feature

```
Usuario: "Añade autenticación JWT al API"
  → Orquestador: Clasifica como "nueva feature", crea TodoWrite macro
  → Orquestador → Explorer: "Mapea el API actual, entry points, auth existente"
  → Explorer → Orquestador: [reporte de exploración]
  → Orquestador → Planner: "Diseña auth JWT basado en exploración"
  → Planner → Orquestador: [plan detallado]
  → Orquestador: Valida plan con usuario (si requerido)
  → Orquestador → Executor: "Implementa paso 1 del plan"
  → Executor → Orquestador: [cambios + estado tests]
  → Orquestador → Reviewer: "Revisa los cambios de auth"
  → Reviewer → Orquestador: [reporte de review]
  → Orquestador: Síntesis final + entrega al usuario
```
```

---

## INSTRUCCIONES: Decisiones de Arquitectura

### Template por decisión (ADR light)

```markdown
### Decisión [N]: [Título de la decisión]

**Contexto**: [En qué situación se tomó esta decisión]

**Opciones consideradas**:
| Opción | Pros | Contras |
|--------|------|---------|
| [Opción A] | ... | ... |
| [Opción B] | ... | ... |

**Decisión**: [Qué se eligió]

**Justificación**: [Por qué, con datos o principios]

**Consecuencias**: [Qué implica esta decisión a largo plazo]
```

### Decisiones recomendadas a documentar:

1. **¿Por qué hub-and-spoke y no multi-agent libre?**
2. **¿Por qué estos modelos por rol?**
3. **¿Por qué MCP como capa de tools?**
4. **¿Por qué esta estructura de directorios?**
5. **¿Por qué estos permisos específicos?**

---

## INSTRUCCIONES: Anti-patrones a evitar

```markdown
## Anti-patrones

1. **[Anti-patrón 1]**: [Descripción]
   - **Por qué es malo**: [Explicación]
   - **Cómo evitarlo**: [Regla concreta]

2. **[Anti-patrón 2]**: ...
```

Ejemplos comunes:
- **Spoke hablando con spoke**: Toda comunicación inter-spoke pasa por el hub.
- **Hub haciendo trabajo**: El hub orquesta, no ejecuta código.
- **Subagentes anidados infinitos**: Máximo 3 niveles de profundidad.
- **Contexto completo a todos**: Cada subagente recibe solo contexto relevante.

---

## REFERENCIAS

- **OpenAI Multi-Agent Orchestration**: https://openai.github.io/openai-agents-python/multi_agent/
  (Handoffs, context isolation, parallel execution)
- **Claude Code: Agent Teams**: https://code.claude.com/docs/en/agent-teams.md
  (Coordinación de múltiples sesiones de Claude Code)
- **Google ADK: Multi-Agent Systems**: https://google.github.io/adk-docs/multi-agent/
  (Hierarchical, sequential, parallel agent patterns)
- **ADR (Architecture Decision Records)**: https://adr.github.io/
  (Formato estándar para documentar decisiones técnicas)
