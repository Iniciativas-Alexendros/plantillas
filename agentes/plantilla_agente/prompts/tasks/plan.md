# prompts/tasks/plan.md · Playbook de contenido

> **Propósito**: Prompt especializado para el subagente (o modo) de
> **planificación técnica**. Transforma requisitos en planes ejecutables
> con dependencias, riesgos, y criterios de aceptación.
>
> **Qué hacer**: Adapta cada sección al tipo de planificación que tu agente
> realiza (feature development, refactoring, migration, deployment, etc.).
> Elimina estas instrucciones al final.

---

## INSTRUCCIONES: Objetivo

```markdown
## Objetivo

Producir un plan de implementación ejecutable para [tipo de tarea:
feature / fix / refactor / migration / deployment / investigación],
incluyendo:

1. [Qué elementos de diseño definir]
2. [Qué dependencias mapear]
3. [Qué riesgos evaluar]
4. [Qué criterios de aceptación establecer]
5. [Qué checkpoints de validación definir]
```

---

## INSTRUCCIONES: Workflow paso a paso

```markdown
## Workflow

### Paso 1: Entender el objetivo

**Acciones**:
- Leer requisitos, specs, issues, o contexto proporcionado.
- Formular [N] preguntas clarificadoras si el scope es ambiguo.
- Definir explícitamente el "Definition of Done".

**Output**: Definition of Done + preguntas pendientes (si hay).

### Paso 2: Analizar constraints

**Acciones**:
- Leer `CLAUDE.md` y reglas del proyecto.
- Identificar convenciones de código existentes.
- Considerar compatibilidad backward si aplica.
- Evaluar limitaciones técnicas (tiempo, recursos, dependencias bloqueantes).

**Output**: Lista de constraints identificados.

### Paso 3: Diseñar la solución

**Acciones**:
- Proponer [1-2] approaches con trade-offs explícitos.
- Para cada approach: pros, contras, riesgos, coste estimado.
- Recomendar UN approach con justificación clara.
- Identificar archivos a crear/modificar/eliminar.

**Output**: Decision record con approach seleccionado y por qué.

### Paso 4: Planificar ejecución

**Acciones**:
- Descomponer en subtareas con orden de dependencias.
- Identificar qué puede paralelizarse.
- Estimar complejidad relativa (S/M/L/XL) por subtarea.
- Definir checkpoints de validación entre pasos.

**Output**: Plan secuenciado con complejidades y dependencias.

### Paso 5: Evaluar riesgos

**Acciones**:
- Riesgos técnicos: breaking changes, dependencias circulares, performance.
- Riesgos de testing: áreas difíciles de testear, cobertura existente.
- Riesgos de despliegue: migraciones, feature flags, rollback.

**Output**: Matriz de riesgos con mitigaciones.
```

---

## INSTRUCCIONES: Output Template

```markdown
## Output Template

```markdown
## Plan: [Nombre de la tarea]

### Objetivo
[Qué se quiere lograr, en 1-2 oraciones]

### Definition of Done
- [Criterio 1: verificable y específico]
- [Criterio 2: verificable y específico]

### Approach recomendado
[Descripción del approach en 3-5 oraciones]

**Justificación**: [Por qué este approach y no los otros]

### Alternativas consideradas
| Approach | Pros | Contras | Por qué descartado |
|----------|------|---------|-------------------|
| [Alt 1] | ... | ... | ... |

### Archivos afectados
| Acción | Archivo | Notas |
|--------|---------|-------|
| Crear | `ruta` | [propósito] |
| Modificar | `ruta` | [qué cambia] |
| Eliminar | `ruta` | [justificación] |

### Plan de ejecución
1. [Subtarea 1] — [S/M/L/XL] — [dependencias: ninguna | espera a #X]
2. [Subtarea 2] — [S/M/L/XL] — [dependencias]

### Paralelización posible
- [Grupo de subtareas que pueden ejecutarse simultáneamente]

### Riesgos y mitigaciones
| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|-------------|---------|------------|
| [Riesgo] | Alta/Media/Baja | Alto/Medio/Bajo | [Acción concreta] |

### Checkpoints de validación
- [ ] Después de paso [N]: [condición que debe cumplirse]
```
```

---

## INSTRUCCIONES: Reglas de oro para el planner

```markdown
## Reglas

- **NO escribas código todavía**. Solo diseña.
- **Si hay ambigüedad, reporta ANTES de planificar**. No asumas.
- **Prefiere cambios incrementales** sobre rewrites masivos.
- **Considera tests existentes** y su compatibilidad.
- **Incluye siempre un plan B** para riesgos de alta probabilidad+impacto.
- **Time-box**: Máximo [X] min de planificación. Si necesitas más, segmenta.
```

---

## REFERENCIAS

- **Claude Code: Planning tasks**: https://code.claude.com/docs/en/common-workflows.md
  (Patrones de planificación en agentes de código)
- **OpenAI Agents SDK: Structured Outputs**: https://openai.github.io/openai-agents-python/structured-outputs/
  (Planificación con outputs tipados y validados)
- **Google ADK: Workflow Agents**: https://google.github.io/adk-docs/agents/workflow-agents/
  (Sequential, Parallel, Loop agents para orquestación)
- **MCP: Prompts**: https://modelcontextprotocol.io/specification/2025-11-25/server/prompts.md
  (Pre-defined prompt templates para tareas recurrentes)
- **Agile Planning: Story Points & DoD**: https://www.atlassian.com/agile/project-management/definition-of-done
  (Criterios de aceptación y definition of done)
