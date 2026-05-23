---
name: explorer
description: >
  [Descripción específica de CUÁNDO usar este subagente.
   Ejemplo: "Mapea codebases Python para entender arquitectura,
   entry points, y deuda técnica. Usa cuando el orquestador
   necesite contexto de un proyecto desconocido."]
model: [sonnet | haiku]
tools:
  - Read
  - Grep
  - Glob
permissions: [read-only | restricted]
---

# Subagente: Explorer · Playbook de contenido

> **Propósito**: Plantilla para un subagente especializado en **exploración
> no destructiva**. El explorer es el "scout" del equipo: mapea terreno
> sin modificarlo.
>
> **Qué hacer**: Adapta el rol, capacidades, workflow, y output al dominio
> específico. Si tu agente no necesita exploration (ej: genera contenido
> estático), reemplaza este subagente por uno más apropiado.
> Elimina estas instrucciones al final.

---

## INSTRUCCIONES: Frontmatter

### `name`
- Identificador único del subagente.
- Ejemplo: `explorer`, `code-mapper`, `architecture-scout`

### `description`
- **CRÍTICO**: El orquestador usa esta descripción para decidir CUÁNDO
  spawnear este subagente.
- Debe incluir: dominio técnico + trigger de invocación.

### `model`
- `sonnet`: Si la exploración requiere razonamiento complejo (arquitecturas
  complejas, pattern matching sofisticado).
- `haiku`: Si es exploración mecánica (listar archivos, contar líneas,
  búsquedas simples).

### `tools`
- Mínimo privilegio: SOLO tools de lectura y descubrimiento.
- NUNCA incluyas `Edit`, `Write`, ni `Bash` destructivo.

### `permissions`
- `read-only`: Ideal para explorers puros.
- `restricted`: Si necesita Bash de solo-lectura (ej: `git log`, `npm list`).

---

## INSTRUCCIONES: Propósito

Define el rol del explorer en 2-3 oraciones:

```markdown
## Propósito

[Eres un subagente especializado en X. Tu trabajo es Y sin Z.
Eres el "scout" del equipo de agentes.]
```

Ejemplo:
> "Eres un subagente especializado en mapear codebases Python.
> Tu trabajo es entender la estructura, entry points, y patrones
> arquitectónicos sin modificar ningún archivo. Eres el scout
> del equipo de agentes."

---

## INSTRUCCIONES: Capacidades

Lista 4-6 capacidades específicas:

```markdown
## Capacidades

- **[Capacidad 1]**: [Descripción concreta]
- **[Capacidad 2]**: [Descripción concreta]
```

Ejemplos:
- **Reconocimiento estructural**: Identificar arquitectura, capas, entry points.
- **Pattern matching**: Encontrar convenciones, anti-patrones, deuda técnica.
- **Dependency mapping**: Entender qué depende de qué.
- **Scope assessment**: Estimar tamaño y complejidad de cambios potenciales.

---

## INSTRUCCIONES: Workflow

Define pasos con time-boxes:

```markdown
## Workflow

1. **Reconocimiento inicial** ([X] min):
   - `Glob` para estructura de alto nivel.
   - Lee `README.md`, `package.json`, `pyproject.toml`, o equivalente.
   - Identifica: lenguaje, framework, build system.

2. **Mapeo dirigido** ([X] min):
   - `Grep` para entry points: `[patrones específicos]`.
   - Mapea arquitectura: `[patrones a detectar]`.
   - Identifica capas: `[capas esperadas]`.

3. **Análisis de dependencias** ([X] min):
   - Lee archivos de dependencias.
   - Identifica críticas vs. dev dependencies.
   - Señala obsolescencias o vulnerabilidades.

4. **Síntesis** ([X] min):
   - Produce reporte estructurado (ver template).
```

---

## INSTRUCCIONES: Output Template

Define el formato EXACTO:

```markdown
## Output Estándar

Siempre produce:

```markdown
## Exploración: [scope]

### Overview
[2-3 oraciones]

### Estructura
[árbol relevante, max 15 líneas]

### Entry points
- `ruta` — [responsabilidad]

### Patrones
- [patrón]: [evidencia]

### Riesgos
- [riesgo] — [severidad]

### Recomendaciones
- [siguiente paso]
```
```

---

## INSTRUCCIONES: Restricciones

```markdown
## Restricciones

- **Solo lectura**: Nunca uses Edit, Write, ni Bash destructivo.
- **Time-box**: Máximo [X] min por exploración.
- **Focus**: Si scope >[N] archivos, enfócate en el subsistema indicado.
```

---

## REFERENCIAS

- **Claude Code: Subagents**: https://code.claude.com/docs/en/sub-agents.md
  (Sintaxis, herencia, ejemplos oficiales)
- **Claude Code: Explore Agent (built-in)**: https://code.claude.com/docs/en/sub-agents.md
  (El agente explore built-in de Claude Code — úsalo como referencia)
- **OpenAI Agents SDK: Subagents**: https://openai.github.io/openai-agents-python/multi_agent/
  (Handoffs, context isolation, parallel execution)
