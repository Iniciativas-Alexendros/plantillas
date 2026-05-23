---
name: [nombre-de-skill]
description: >
  [Descripción de CUÁNDO usar esta skill. 1-2 oraciones específicas.
   Esta descripción es lo PRIMERO que Claude ve; debe ser clara y triggerable.]
allowed-tools:
  - [tool1]
  - [tool2]
context:
  - [ruta/a/referencia1.md]
  - [ruta/a/referencia2.md]
---

# [Nombre de la Skill] · Playbook de contenido

> **Propósito**: Las skills son "paquetes de instrucciones reutilizables"
> que Claude carga bajo demanda cuando detecta que son relevantes.
> Esta skill se activa automáticamente cuando la descripción del frontmatter
> coincide con la tarea del usuario, o manualmente vía `/[nombre-de-skill]`.
>
> **Qué hacer**: Desarrolla el cuerpo con reglas, patrones, anti-patrones,
> y plantillas ESPECÍFICAS del dominio. Elimina estas instrucciones.

---

## INSTRUCCIONES: Frontmatter

### Campo: `name`
- Identificador único en `kebab-case`.
- Ejemplo: `react-performance`, `api-security`, `django-orm`

### Campo: `description`
- **CRÍTICO**: Esta descripción determina CUÁNDO Claude carga la skill.
- Debe ser específico del dominio y del trigger.
- Ejemplo bueno: "Usa cuando trabajes con React y necesites optimizar renders,
  memorización, o bundle size."
- Ejemplo malo: "Ayuda con React." (demasiado vago)

### Campo: `allowed-tools`
- Lista de tools que pueden usarse cuando esta skill está activa.
- Principio de mínimo privilegio: solo las necesarias.

### Campo: `context`
- Archivos de referencia que se cargan automáticamente con la skill.
- Útil para docs extensas que no caben en SKILL.md.

---

## INSTRUCCIONES: Cuerpo de la Skill

### Estructura recomendada:

```markdown
# [Nombre de la Skill]

## Cuándo usar

[Lista de triggers específicos. Cuándo se activa esta skill.]

## Reglas / Patrones

### [Categoría 1]

[Regla concreta 1]
[Ejemplo de código CORRECTO]

[Regla concreta 2]
[Ejemplo de código CORRECTO]

### [Categoría 2]
...

## Anti-patrones

1. **[Anti-patrón 1]**: [Descripción del problema]
   - **Por qué es malo**: [Explicación]
   - **Cómo evitarlo**: [Solución]

2. **[Anti-patrón 2]**: ...

## Plantillas

### [Plantilla 1]: [Propósito]

```[lenguaje]
[Código template con placeholders [ASÍ]]
```

### [Plantilla 2]: ...

## Checklist de validación

- [ ] [Criterio 1]
- [ ] [Criterio 2]
```

### Ejemplo completado (skill de Python error handling):

```markdown
# python-error-handling

## Cuándo usar

- Escribiendo funciones que lanzan excepciones.
- Refactorizando bloques try/except.
- Revisando código para robustez.

## Reglas

### Excepciones

- SIEMPRE captura excepciones ESPECÍFICAS, nunca `except:` o `except Exception:`.
- SIEMPRE usa `raise ... from e` cuando re-lanzas para preservar el traceback.
- NUNCA uses bare `raise` fuera de un bloque except (a menos que sea intencional).

### Logging

- Usa `logging` o `structlog`, NUNCA `print` para diagnóstico.
- Incluye contexto estructurado: `logger.error("db_fail", user_id=uid)`.
- Para excepciones no manejadas, usa `logger.exception(...)` para auto-capturar traceback.

## Anti-patrones

1. **Bare except**: Captura KeyboardInterrupt y SystemExit accidentalmente.
   - **Por qué es malo**: Puede prevenir terminación limpia del programa.
   - **Cómo evitarlo**: Usa `except SpecificError:` siempre.

2. **Swallowing exceptions**: `except: pass` o `except: return None`.
   - **Por qué es malo**: Silencia errores que deberían ser visibles.
   - **Cómo evitarlo**: Loggea siempre antes de continuar. Si realmente es opcional,
     documenta POR QUÉ es seguro ignorarlo.

## Plantillas

### Manejo de error en función pública

```python
def process_user(user_id: str) -> User:
    try:
        user = db.get_user(user_id)
    except UserNotFoundError as e:
        logger.warning("user_not_found", user_id=user_id)
        raise UserInputError(f"User {user_id} not found") from e
    except DatabaseError as e:
        logger.exception("database_error", user_id=user_id)
        raise ServiceUnavailable("Database unavailable") from e
    return user
```

## Checklist

- [ ] ¿Las excepciones capturadas son específicas?
- [ ] ¿Hay logging apropiado en cada rama except?
- [ ] ¿Se preserva el traceback con `from e`?
- [ ] ¿No hay `pass` silencioso en bloques except?
```

---

## INSTRUCCIONES: Progressive Disclosure

Claude Code carga skills en etapas:

1. **Etapa 1 (metadata)**: Solo ve `name` y `description` de todas las skills.
2. **Etapa 2 (activación)**: Cuando detecta relevancia, carga el SKILL.md completo.
3. **Etapa 3 (referencias)**: Si `context` lista archivos, se cargan SOLO si se referencian.

**Implicación**: Tu `description` hace todo el trabajo de "marketing". Si es vaga,
Claude nunca activará la skill.

---

## REFERENCIAS

- **Claude Code: Skills**: https://code.claude.com/docs/en/skills.md
  (Cómo crear, gestionar, y compartir skills)
- **Claude Code: Agent Skills in SDK**: https://code.claude.com/docs/en/agent-sdk/skills.md
  (Loading skills from filesystem, progressive disclosure)
- **MCP: Prompts**: https://modelcontextprotocol.io/specification/2025-11-25/server/prompts.md
  (Pre-defined prompt templates, similar concept to skills)
- **OpenAI: Function Calling**: https://platform.openai.com/docs/guides/function-calling
  (Tools with schema, analogous to skill capabilities)
