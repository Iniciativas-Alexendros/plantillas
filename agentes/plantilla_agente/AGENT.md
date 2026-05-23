# AGENT.md · Playbook de contenido

> **Propósito de este archivo**: Define la identidad técnica del agente.
> Claude Code usa este archivo para entender QUÉ eres, QUÉ puedes hacer,
> y CUÁNDO invocarte. Es el corazón del agente.
>
> **Qué hacer**: Lee las secciones de INSTRUCCIONES y reemplaza TODO el
> contenido entre corchetes `[]` con valores específicos del agente que
> estás construyendo. Elimina estas instrucciones una vez completado.

---

## INSTRUCCIONES: Frontmatter YAML (obligatorio)

El bloque superior entre `---` es **YAML frontmatter** parseado por Claude Code.
Cada campo tiene una función específica. Completa TODOS los campos.

### Campo: `name`

- **Qué es**: Identificador único del agente en `kebab-case`.
- **Reglas**: Solo letras minúsculas, números, y guiones. Sin espacios.
- **Ejemplos buenos**: `security-reviewer`, `deploy-orchestrator`, `api-doc-generator`
- **Ejemplos malos**: `Mi Agente`, `agente_v1`, `reviewer` (demasiado genérico)
- **Cómo decidir**: Usa `[dominio]-[rol]`. El dominio lo hace único.

```yaml
name: [dominio]-[rol]
```

### Campo: `description`

- **Qué es**: Texto que Claude Code usa para decidir SI invocarte automáticamente.
- **Reglas**: Debe describir CUÁNDO eres relevante, no solo QUÉ eres.
- **Longitud**: 1-3 oraciones. Sé específico.
- **Ejemplo bueno**:
  > "Revisa código Python en busca de vulnerabilidades de seguridad
  > (SQL injection, XSS, path traversal). Usa después de cada PR o
  > antes de desplegar a producción."
- **Ejemplo malo**:
  > "Soy un agente que ayuda con código." (demasiado vago para triggers)

```yaml
description: >
  [1-3 oraciones describiendo CUÁNDO usar este agente.
   Incluye: dominio técnico, trigger de invocación,
   y diferenciador respecto a otros agentes.]
```

### Campo: `model`

- **Qué es**: Modelo de Claude que usará este agente.
- **Opciones válidas**: `opus` | `sonnet` | `haiku` | `opusplan`
- **Cómo decidir**:
  - `opus`: Tareas de razonamiento profundo, arquitectura, debugging complejo.
  - `sonnet`: Balance general. Default recomendado para la mayoría de agentes.
  - `haiku`: Tareas rápidas, paralelizables, bajo coste (reviews, clasificación).
  - `opusplan`: Planificación ultra-compleja (usa Opus con extended thinking).

```yaml
model: [opus | sonnet | haiku | opusplan]
```

### Campo: `tools`

- **Qué es**: Lista de herramientas nativas de Claude Code que este agente puede usar.
- **Principio**: Mínimo privilegio. Lista SOLO las que necesita.
- **Opciones disponibles**:
  - `Read` — Leer archivos
  - `Grep` — Búsqueda regex
  - `Glob` — Listar archivos por patrón
  - `Edit` — Modificar archivos (diff)
  - `Write` — Crear/sobrescribir archivos
  - `Bash` — Ejecutar comandos shell
  - `Agent` — Spawn subagentes
  - `TodoWrite` — Gestionar listas de tareas
  - `WebFetch` — Leer contenido web (si disponible)
- **Ejemplo**: Un agente de solo lectura no necesita `Edit`, `Write`, ni `Bash`.

```yaml
tools:
  - [tool1]
  - [tool2]
```

### Campo: `skills` (opcional pero recomendado)

- **Qué es**: Lista de skills embebidas en este agente que se pre-cargan.
- **Reglas**: Deben coincidir con directorios en `skills/`.
- **Nota**: Las skills se inyectan completas en el contexto al inicio.
  No abuses; cada skill consume tokens.

```yaml
skills:
  - [nombre-de-skill-1]
  - [nombre-de-skill-2]
```

### Campo: `permissions` (opcional)

- **Qué es**: Mode de permisos por defecto.
- **Opciones**: `unrestricted` | `restricted` | `ask`
- **Recomendación**: `restricted` siempre. Usa `permissions.yaml` para granularidad.

```yaml
permissions: restricted
```

### Campo: `context` (opcional)

- **Qué es**: Overrides de configuración de contexto.
- **Campos**:
  - `max_tokens`: Límite de tokens para este agente.
  - `temperature`: 0.0 (determinista) a 1.0 (creativo). Agentes de código: 0.1-0.3.
  - `thinking`: `enabled` | `disabled`. Habilita extended thinking (Opus/Sonnet).

```yaml
context:
  max_tokens: [80000 | 120000 | 200000]
  temperature: [0.0 - 1.0]
  thinking: [enabled | disabled]
```

---

## INSTRUCCIONES: Cuerpo del archivo (markdown)

Después del frontmatter, escribe las instrucciones del sistema en markdown.
Este es el "system prompt" del agente. Estructúralo así:

### 1. Identidad (3-5 oraciones)

Quién eres, qué haces, y para quién. Sé específico del dominio.

### 2. Doctrina Operativa (4-7 principios)

Reglas de comportamiento que guían todas tus decisiones. Formato: imperativo.
Ejemplos:
- "NUNCA ejecutes código sin validar inputs primero."
- "Delega tareas de exploración al subagente `explorer`."
- "Prefiere parches quirúrgicos sobre rewrites completos."

### 3. Flujo de Trabajo Estándar

Diagrama o lista del proceso que sigues para cada tarea.
Ejemplo para un agente orquestador:

```
Entrada → Clasificar → Planificar → Delegar → Sintetizar → Entregar
```

### 4. Reglas de Delegación (si usas subagentes)

Tabla: Tipo de tarea → Subagente → Condición de activación.

### 5. Restricciones de Seguridad

Prohibiciones explícitas. Ejemplos:
- NUNCA ejecutar `sudo` directo.
- NUNCA escribir secrets en archivos no-.env.
- NUNCA hacer `git push` sin confirmación.

### 6. Modelo de Memoria

Cómo gestionas el estado entre turnos. Referencia a `memory/context.md`.

### 7. Output Esperado

Formato estándar de entrega. Ejemplo:
- Resumen ejecutivo (3-5 bullets)
- Decisiones tomadas y por qué
- Archivos modificados/creados
- Pendientes identificados

---

## REFERENCIAS

- **Subagent Frontmatter Spec**: https://code.claude.com/docs/en/sub-agents.md
  (Campos disponibles, herencia, ejemplos oficiales)
- **Claude Code Agent SDK**: https://code.claude.com/docs/en/agent-sdk/overview.md
  (Programmatic agent definition)
- **MCP Architecture**: https://modelcontextprotocol.io/docs/learn/architecture.md
  (Cómo se conectan tools y agentes)
- **OpenAI Agents SDK - Agent Definition**: https://openai.github.io/openai-agents-python/agents/
  (Comparativa de campos: name, instructions, tools, handoffs)
- **Google ADK Agent Types**: https://google.github.io/adk-docs/agents/
  (LlmAgent, WorkflowAgent, LoopAgent, ParallelAgent)

---

## PLANTILLA FRONTMATTER (copiar y rellenar)

```yaml
---
name: [dominio]-[rol]
description: >
  [CUÁNDO usar este agente. 1-3 oraciones específicas.
   Incluye dominio técnico y trigger de invocación.]
model: [sonnet | haiku | opus]
tools:
  - [tool1]
  - [tool2]
  - [tool3]
skills:
  - [skill-embebida-1]
permissions: restricted
context:
  max_tokens: 200000
  temperature: 0.2
  thinking: enabled
---

# [Nombre del Agente]

## Identidad

[Eres X, especializado en Y, diseñado para Z.]

## Doctrina Operativa

1. [Principio 1]
2. [Principio 2]
3. [Principio 3]

## Flujo de Trabajo

```
[Diagrama de flujo]
```

## Reglas de Delegación

| Tarea | Subagente | Condición |
|---|---|---|
| [Tipo] | [nombre] | [cuándo delegar] |

## Restricciones

- NUNCA [prohibición 1]
- NUNCA [prohibición 2]

## Memoria

- Contexto: [cómo se mantiene estado]

## Output

1. [Formato de entrega]
```
