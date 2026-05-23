# PLAYBOOK DE INICIO · Sistema de Plantillas de Agentes para Claude Code

> **Para quién es esto**: Para ti, LLM, que vas a usar este sistema para crear
> un nuevo agente o adaptar uno existente. Este directorio contiene **dos
> artefactos complementarios** que juntos garantizan un proceso de creación
> replicable, limpio y eficiente.

---

## Los dos directorios: ¿Qué son y para qué sirven?

### 1. `plantilla_agente/` — El Kit de Construcción

**Qué es**: Un **playbook de autorrelleno instructivo**. Cada archivo explica
QUÉ debe contener, POR QUÉ, y CÓMO desarrollarlo. Es un esqueleto con
instrucciones dirigidas a un LLM constructor.

**Para qué sirve**:
- **Crear agentes nuevos** desde cero.
- **Adaptar agentes existentes** a nuevos dominios.
- **Estandarizar** la estructura de agentes en un equipo.

**Contenido de cada archivo**:
- Instrucciones de desarrollo paso a paso.
- Templates rellenables con placeholders claros (`[ASÍ]`).
- Ejemplos de contenido correcto vs. incorrecto.
- Enlaces a fuentes oficiales (Anthropic, OpenAI, Google, OWASP).
- Checklists de validación por archivo.

**Cuándo usarlo**:
```bash
# Crear un nuevo agente desde la plantilla
cp -r ~/.claude/plantillas/plantilla_agente ~/.claude/agents/mi-nuevo-agente
# → Luego sigue los 13 pasos del playbook para autorrellenar
```

---

### 2. `ejemplo_agente/` — La Referencia Viva

**Qué es**: Un **agente completamente funcional** construido siguiendo la
plantilla. Contiene contenido real, no instructivo: prompts concretos,
skills operativas, subagentes definidos, y configuración operativa.

**Para qué sirve**:
- **Ver el resultado final** de aplicar la plantilla.
- **Copiar/adaptar** componentes concretos (ej: "¿Cómo se ve un hook bien configurado?").
- **Entender la arquitectura** hub-and-spoke en la práctica.

**Contenido clave**:
- `AGENT.md` con frontmatter YAML real y sistema de delegación funcional.
- `skills/diagramador/SKILL.md` — una skill operativa que genera Mermaid.
- `subagents/{explorer,planner,reviewer}.md` — subagentes con prompts reales.
- `config/permissions.yaml` — guardrails con regex concretas.
- `references/architecture.md` — diagrama ASCII del flujo de mensajes.

**Cuándo usarlo**:
```bash
# Copiar como punto de partida para personalizar
cp -r ~/.claude/plantillas/agentes/ejemplo_agente ~/.claude/agents/mi-agente
# → Edita directamente los archivos (no necesitas instrucciones)
```

---

## Comparativa rápida

| Dimensión | `plantilla_agente/` | `ejemplo_agente/` |
|---|---|---|
| **Propósito** | Construir agentes nuevos | Usar/copiar agente existente |
| **Contenido** | Instrucciones + placeholders | Contenido real y funcional |
| **Destinatario** | LLM constructor | Usuario final / LLM adaptador |
| **Estado** | Plantilla incompleta (requiere autorrelleno) | Agente operativo (listo para usar) |
| **Tamaño** | ~136 KB (con documentación extensa) | ~76 KB (contenido conciso) |
| **Archivos** | 20 (+ PLAYBOOK_INICIO.md) | 19 |
| **Mejor para** | Primer agente, estandarización | Segundo agente, adaptación rápida |

---

## Flujo de trabajo recomendado

### Escenario A: Primer agente (usar plantilla)

```
1. Leer este PLAYBOOK_INICIO.md
2. Leer plantilla_agente/AGENT.md (Paso 1)
3. Seguir los 13 pasos del playbook en orden
4. Validar con el checklist del playbook
5. Probar: /nombre-del-agente <tarea>
6. Iterar según observaciones
```

### Escenario B: Segundo agente (usar ejemplo)

```
1. Copiar ejemplo_agente/ como punto de partida
2. Editar AGENT.md (nombre, descripción, model)
3. Adaptar prompts/persona.md al nuevo dominio
4. Ajustar subagents/ según necesidades
5. Reemplazar skills/ por skills del nuevo dominio
6. Probar y iterar
```

### Escenario C: Auditoría / CI/CD (usar validador)

```
1. El agente creado se somete a validación automática
2. Se verifica: estructura, frontmatter, JSON, YAML, placeholders
3. Se reportan errores y warnings
4. Se corrige y se revalida
```

---

## Flujo de creación detallado (13 pasos)

### Paso 0: Entender el objetivo

Antes de tocar nada, responde:

1. **¿Qué problema resuelve el agente?**
2. **¿Quién lo usará?**
3. **¿Qué herramientas necesita?**
4. **¿Es un agente único o multi-agente?**

### Paso 1: Copiar la base

```bash
# Opción A: Desde plantilla (recomendado para primer agente)
cp -r ~/.claude/plantillas/plantilla_agente ~/.claude/agents/MI_AGENTE

# Opción B: Desde ejemplo (recomendado para agentes subsiguientes)
cp -r ~/.claude/plantillas/ejemplo_agente ~/.claude/agents/MI_AGENTE
```

> Reemplaza `MI_AGENTE` por `kebab-case` descriptivo.

### Paso 2-13: Autorrellenar (si usaste plantilla)

| Orden | Archivo | Qué defines |
|-------|---------|-------------|
| 1 | `AGENT.md` | Identidad, modelo, tools, permisos |
| 2 | `prompts/persona.md` | Personalidad, tono, valores |
| 3 | `prompts/system.md` | Principios, flujo, estilo |
| 4 | `config/settings.json` | Config técnica |
| 5 | `config/permissions.yaml` | Guardrails |
| 6 | `prompts/tasks/*.md` | Prompts especializados |
| 7 | `subagents/*.md` | Especialistas |
| 8 | `skills/*/SKILL.md` | Skills embebidas |
| 9 | `tools/mcp.json` | Servidores MCP |
| 10 | `hooks/*.yaml` | Hooks de interceptación |
| 11 | `memory/context.md` | Plantilla de memoria |
| 12 | `references/*.md` | Documentación de dominio |
| 13 | `README.md` | Doc para usuario humano |

### Validación final (checklist)

- [ ] `AGENT.md` tiene `name` y `description` específicos del dominio.
- [ ] `description` explica CUÁNDO usar el agente (triggers).
- [ ] `tools` lista solo las necesarias (mínimo privilegio).
- [ ] `subagents/*.md` definen roles NO solapados.
- [ ] `permissions.yaml` tiene denylist en `bash` y `filesystem`.
- [ ] `skills/` ha sido renombrada y contiene reglas reales.
- [ ] `tools/mcp.json` solo incluye servidores configurados.
- [ ] No quedan placeholders sin rellenar (`[ASÍ]`).

---

## Reglas de oro

1. **Especificidad > Genericidad**: "Revisa código Python buscando SQL injection"
   es mejor que "Revisa código".
2. **Mínimo privilegio**: Lista solo las tools que necesita.
3. **Un subagente = una responsabilidad**.
4. **Los prompts son código**: Trátalos con la misma rigurosidad.
5. **Documenta las decisiones**: Pon el "por qué" en `references/architecture.md`.

---

## CI/CD de Validación

Este sistema incluye un validador automático que verifica:

### Qué valida

| Verificación | Descripción |
|---|---|
| **Estructura** | ¿Todos los archivos/directorios obligatorios existen? |
| **Frontmatter** | ¿YAML válido en AGENT.md y subagents/*.md? |
| **JSON** | ¿settings.json y mcp.json son parseables? |
| **YAML** | ¿permissions.yaml y hooks/*.yaml son parseables? |
| **Placeholders** | ¿Quedan `[placeholders]` sin rellenar? |
| **Skills** | ¿Las skills referenciadas en AGENT.md existen en skills/? |
| **Subagentes** | ¿Los subagentes referenciados existen en subagents/? |
| **Vacíos** | ¿Hay archivos con <50 bytes (probablemente vacíos)? |

### Cómo ejecutar

```bash
# Local
python ~/.claude/plantillas/agentes/validar_agente.py ~/.claude/agents/mi-agente

# En CI/CD (GitHub Actions)
# Se ejecuta automáticamente en cada PR que modifique agentes/
```

---

## Referencias oficiales

| Recurso | URL | Para qué usarlo |
|---------|-----|-----------------|
| Claude Code Docs (índice) | https://code.claude.com/docs/llms.txt | Todo sobre skills, subagents, hooks |
| Subagents Reference | https://code.claude.com/docs/en/sub-agents.md | Sintaxis de frontmatter, herencia |
| Skills in SDK | https://code.claude.com/docs/en/agent-sdk/skills.md | Estructura SKILL.md |
| Hooks Reference | https://code.claude.com/docs/en/hooks.md | Eventos, schemas |
| MCP Spec | https://modelcontextprotocol.io/specification/2025-11-25/index.md | Protocolo completo |
| OpenAI Agents SDK | https://openai.github.io/openai-agents-python/ | Handoffs, guardrails, tracing |
| Google ADK Docs | https://google.github.io/adk-docs/ | Multi-agent, A2A, deployment |

---

## Estructura del sistema de plantillas

```
~/.claude/plantillas/
├── PLAYBOOK_INICIO.md          ← ESTE ARCHIVO (guía maestra)
├── validar_agente.py           ← Validador automático (CI/CD)
├── .github/workflows/          ← GitHub Actions para CI/CD
│   └── validar-agentes.yml
│
└── agentes/                    ← Plantillas de AGENTES
    ├── plantilla_agente/       ← Kit de construcción (playbook instructivo)
    │   ├── AGENT.md
    │   ├── README.md
    │   ├── config/
    │   ├── prompts/
    │   ├── tools/
    │   ├── skills/
    │   ├── memory/
    │   ├── hooks/
    │   ├── subagents/
    │   └── references/
    │
    └── ejemplo_agente/         ← Referencia viva (agente funcional)
        ├── AGENT.md
        ├── README.md
        ├── config/
        ├── prompts/
        ├── tools/
        ├── skills/diagramador/
        ├── memory/
        ├── hooks/
        ├── subagents/
        └── references/
```

---

> **Nota final**: Este sistema fue construido a partir de una investigación de
> fuentes oficiales de Anthropic, OpenAI, y Google en mayo de 2026.
> Si las APIs o convenciones han cambiado, consulta los enlaces de referencia
> oficiales arriba antes de completar el agente.

**¡Manos a la obra!**
- **¿Primer agente?** → Empieza por `plantilla_agente/AGENT.md`.
- **¿Ya tienes experiencia?** → Copia `ejemplo_agente/` y adapta.
- **¿Quieres verificar?** → Ejecuta `validar_agente.py`.
