# prompts/tasks/explore.md · Playbook de contenido

> **Propósito**: Prompt especializado para el subagente (o modo) de **exploración
> y descubrimiento** de codebases. Este prompt se activa cuando el agente
> necesita entender un proyecto, subsistema, o tecnología desconocida.
>
> **Qué hacer**: Adapta cada sección al dominio específico del agente.
> Si tu agente NO necesita explorar codebases (ej: un agente de generación
> de contenido), reemplaza este archivo por un prompt de exploración de
> documentación o datos. Elimina estas instrucciones al final.

---

## INSTRUCCIONES: Objetivo

Define QUÉ debe lograr el modo explore:

```markdown
## Objetivo

Mapear rápidamente [tipo de objetivo: codebase / subsistema / tecnología / dataset]
para entender:

1. [Qué aspecto estructural identificar]
2. [Qué puntos de entrada encontrar]
3. [Qué dependencias clave mapear]
4. [Qué patrones arquitectónicos detectar]
5. [Qué riesgos o deuda técnica visualizar]
```

#### Ejemplos por dominio:

| Dominio | Objetivo específico |
|---|---|
| Backend API | Endpoints, middleware, modelos de datos, capas de servicio |
| Frontend React | Componentes, estado, routing, hooks personalizados |
| Infra/DevOps | Pipelines, manifests, configuración, dependencias de servicios |
| Data/ML | Datasets, modelos, feature engineering, pipelines de entrenamiento |
| Legal/Compliance | Estructura documental, cláusulas clave, referencias normativas |

---

## INSTRUCCIONES: Workflow paso a paso

Define los pasos EXACTOS que el explorador debe seguir, con time-boxes:

```markdown
## Workflow

### Paso 1: [Nombre del paso] ([time-box])

**Acciones**:
- [Tool a usar] — [Qué hacer específicamente]
- [Tool a usar] — [Qué hacer específicamente]

**Output esperado**: [Qué información debe obtenerse]

### Paso 2: [Nombre del paso] ([time-box])
...
```

#### Template de workflow genérico:

```markdown
## Workflow

### Paso 1: Reconocimiento inicial (2 min)

**Acciones**:
- `Glob` — Estructura de directorios de alto nivel (max depth 3).
- `Read` — Archivos de configuración del proyecto (README, package.json, etc.).
- Identificar: lenguaje principal, framework, build system, convenciones.

**Output**: Lista de tecnologías y convenciones detectadas.

### Paso 2: Mapeo dirigido (5 min)

**Acciones**:
- `Grep` — Encontrar puntos de entrada: `[patrones de búsqueda específicos]`.
- `Read` — Archivos clave identificados en el paso anterior.
- Mapear arquitectura: ¿MVC? ¿Clean? ¿Hexagonal? ¿Layered?
- Identificar capas: API, dominio, infraestructura, presentación.

**Output**: Diagrama o lista de capas y sus responsables.

### Paso 3: Análisis de dependencias (3 min)

**Acciones**:
- `Read` — Archivos de dependencias (`requirements.txt`, `package.json`, etc.).
- Identificar dependencias críticas vs. dev dependencies.
- Buscar dependencias obsoletas o con vulnerabilidades conocidas.

**Output**: Lista de dependencias con riesgos señalados.

### Paso 4: Síntesis (1 min)

**Output**: Reporte estructurado siguiendo el template de abajo.
```

---

## INSTRUCCIONES: Output Template

Define el formato EXACTO de salida. Usa markdown estructurado:

```markdown
## Output Template

```markdown
## Exploración: [Nombre del proyecto/subsistema]

### Overview
[2-3 oraciones que resuman qué es y para qué sirve]

### Estructura clave
```
[árbol simplificado de dirs relevantes, max 15 líneas]
```

### Entry points
- `[ruta/al/archivo]` — [responsabilidad específica]
- `[ruta/al/archivo]` — [responsabilidad específica]

### Patrones arquitectónicos
- [Patrón detectado]: [evidencia concreta, ej: "cada controller tiene un service"]

### Riesgos / Deuda técnica
- [Riesgo]: [severidad: alta/media/baja] — [justificación breve]

### Recomendaciones
- [Siguiente paso sugerido para el equipo]
```
```

---

## INSTRUCCIONES: Restricciones

Define prohibiciones explícitas para el modo explore:

```markdown
## Restricciones

- **Solo lectura**: NUNCA uses `Edit`, `Write`, ni `Bash` destructivo.
- **Time-box**: Máximo [X] min por exploración. Si necesitas más, pide permiso.
- **Focus**: Si el scope es >[N] archivos, enfócate en el subsistema indicado.
- **No juicios prematuros**: Reporta lo que ves, no asumas intenciones del autor.
```

---

## REFERENCIAS

- **Claude Code: Exploring codebases**: https://code.claude.com/docs/en/common-workflows.md
  (Guía oficial de exploración de codebases)
- **GrepTool Best Practices**: https://code.claude.com/docs/en/tools-reference.md
  (Regex, ripgrep syntax, performance)
- **MCP: Resources**: https://modelcontextprotocol.io/specification/2025-11-25/server/resources.md
  (Exposing structured data to agents)
- **OpenAI: Function Tools**: https://openai.github.io/openai-agents-python/tools/
  (Definiendo tools para descubrimiento)
