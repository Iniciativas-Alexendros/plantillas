# memory/context.md · Playbook de contenido

> **Propósito**: Memoria de **sesión activa** del agente. Se acumula durante
> la conversación actual y se resetea al inicio de cada nueva sesión.
> Es la "pizarra" de trabajo del agente: hechos descubiertos, decisiones
> tomadas, bloqueos pendientes.
>
> **Qué hacer**: Este archivo es un **TEMPLATE VIVO**. El agente lo escribe
> y actualiza durante la sesión. Tú (el creador del agente) defines la
> ESTRUCTURA inicial. Elimina estas instrucciones al final.

---

## INSTRUCCIONES: Estructura de la memoria

Define las secciones que el agente debe mantener actualizadas.
Cada sección debe ser:
- **Concisa**: Bullets, no párrafos.
- **Estructurada**: Formato predecible para parsing.
- **Accionable**: Cada item debe tener utilidad futura.

### Template de estructura:

```markdown
# Contexto de Sesión · [nombre-del-agente]

> Este archivo se acumula durante la sesión activa.
> Se resetea al inicio de cada nueva sesión.

## Estado Actual

- **Sesión iniciada**: [timestamp]
- **Proyecto activo**: [ruta o nombre]
- **Tarea actual**: [descripción breve]
- **Subagentes activos**: [número]
- **Fase actual**: [exploración | planificación | ejecución | revisión | entrega]

## Decisiones Tomadas

<!-- Decisiones arquitectónicas o de diseño durante la sesión -->
- [timestamp] **[Categoría]**: [Decisión] — [Por qué] — [Alternativas descartadas]

## Contexto Descubierto

<!-- Mapeo de codebase, convenciones, gotchas -->
- `[ruta/archivo]`: [Hecho relevante descubierto]
- Convención detectada: [descripción]

## Bloqueos / Pendientes

<!-- Items que requieren input del usuario o investigación externa -->
- [ ] [Descripción del bloqueo] — [Desde cuándo] — [Impacto]

## Aprendizajes de la Sesión

<!-- Insights que podrían persistir a learnings.md -->
- [Insight con contexto suficiente para ser útil en futuras sesiones]
```

---

## INSTRUCCIONES: Qué registrar vs. qué omitir

### SÍ registrar:
- **Decisiones arquitectónicas**: "Elegimos REST sobre gRPC porque el cliente
  no soporta HTTP/2."
- **Convenciones del proyecto**: "Los tests usan pytest con fixtures en
  `conftest.py`."
- **Gotchas**: "El build falla si Node >18.12 porque native deps."
- **Dependencias descubiertas**: "El módulo X depende de Y vía Z."

### NO registrar:
- **Información obvia**: "El proyecto usa Python." (ya está en README)
- **Transitoria**: "Leí el archivo X." (a menos que sea relevante)
- **Opiniones sin contexto**: "Este código es feo." (no accionable)

---

## INSTRUCCIONES: Integración con learnings.md

Al final de la sesión (o cuando se acumulen suficientes insights):

1. Revisa la sección "Aprendizajes de la Sesión".
2. Si un insight es generalizable (aplica a futuras sesiones del mismo proyecto):
   - Añádelo a `memory/learnings.md`.
   - Elimínalo de `context.md` para evitar duplicación.
3. `learnings.md` persiste entre sesiones. `context.md` es efímero.

---

## REFERENCIAS

- **Claude Code: Memory**: https://code.claude.com/docs/en/memory.md
  (Persistent instructions, auto memory, CLAUDE.md)
- **Claude Code: Sessions**: https://code.claude.com/docs/en/sessions.md
  (Session persistence, continue, resume, fork)
- **Claude Code: Context Window**: https://code.claude.com/docs/en/context-window.md
  (How context fills during a session)
- **Google ADK: Session State**: https://google.github.io/adk-docs/sessions/
  (Blackboard pattern, state management)
