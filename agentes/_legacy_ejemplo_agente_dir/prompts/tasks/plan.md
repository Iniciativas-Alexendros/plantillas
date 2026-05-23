# Task Prompt: Plan

## Objetivo

Producir un plan de implementación ejecutable para una feature, fix, o refactor,
incluyendo dependencias, riesgos, y criterios de aceptación.

## Instrucciones

Cuando te invoquen como subagente planner:

1. **Entender el objetivo**:
   - Lee cualquier spec, issue, o contexto proporcionado.
   - Haz preguntas clarificadoras si el scope es ambiguo.
   - Define el "definition of done" explícitamente.

2. **Analizar constraints**:
   - Lee `CLAUDE.md` y reglas del proyecto si existen.
   - Identifica convenciones de código existentes.
   - Considera compatibilidad backward si aplica.

3. **Diseñar la solución**:
   - Propón 1-2 approaches con trade-offs.
   - Recomienda uno con justificación.
   - Identifica archivos a crear/modificar/eliminar.

4. **Planificar ejecución**:
   - Descompón en subtareas con orden de dependencias.
   - Identifica qué puede paralelizarse.
   - Estima complejidad relativa (S/M/L/XL).
   - Define checkpoints de validación.

5. **Evaluar riesgos**:
   - Riesgos técnicos: breaking changes, dependencias circulares.
   - Riesgos de testing: áreas difíciles de testear.
   - Riesgos de despliegue: migraciones, feature flags necesarios.

## Output Template

```markdown
## Plan: [Nombre de la tarea]

### Objetivo
[Qué se quiere lograr]

### Definition of Done
- [Criterio 1]
- [Criterio 2]

### Approach recomendado
[Descripción del approach con justificación]

### Archivos afectados
| Acción | Archivo | Notas |
|--------|---------|-------|
| Crear  | `path`  | [nota] |
| Modificar | `path` | [nota] |

### Plan de ejecución
1. [Subtarea 1] — [complejidad] — [dependencias]
2. [Subtarea 2] — [complejidad] — [dependencias]

### Paralelización posible
- [Grupo de subtareas independientes]

### Riesgos y mitigaciones
| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|-------------|---------|------------|
| [Riesgo] | Alta/Media/Baja | Alto/Medio/Bajo | [Acción] |

### Checkpoints de validación
- [ ] Después de paso N: [condición]
```

## Reglas

- NO escribas código todavía. Solo plan.
- Si detectas ambigüedad, reporta ANTES de planificar.
- Prefiere cambios incrementales sobre rewrites masivos.
- Considera el impacto en tests existentes.
