# COMMAND.md · Playbook de contenido

> **Propósito**: Los comandos slash (`/comando`) son atajos que el usuario
> invoca explícitamente para ejecutar tareas específicas. A diferencia de las
> skills (que Claude activa automáticamente), los comandos son SIEMPRE
> invocados manualmente.
>
> **Qué hacer**: Define el trigger, el propósito, y las instrucciones que
> Claude debe seguir cuando se invoque este comando. Elimina estas instrucciones.

---

## INSTRUCCIONES: Nombre del archivo

El nombre del archivo determina el trigger del comando:

- `deploy.md` → se invoca como `/deploy`
- `review.md` → se invoca como `/review`
- `test.md` → se invoca como `/test`

**Reglas de naming**:
- `kebab-case` si es multi-palabra: `code-review.md` → `/code-review`
- Corto y memorable: `/d` mejor que `/deploy-to-staging-environment`
- Sin conflictos: evita nombres de comandos built-in de Claude

---

## INSTRUCCIONES: Estructura

```markdown
# /[nombre-del-comando]

## Trigger

`/[nombre]`

## Descripción

[1-2 oraciones de qué hace este comando]

## Cuándo usar

- [Situación 1]
- [Situación 2]

## Instrucciones

Cuando el usuario invoque `/{nombre}`, sigue estos pasos:

1. [Paso 1: qué hacer]
2. [Paso 2: qué hacer]
3. [Paso 3: qué hacer]

## Parámetros (opcional)

| Parámetro | Tipo | Descripción | Default |
|-----------|------|-------------|---------|
| `[param]` | string | [Descripción] | `[default]` |

## Ejemplo de uso

```
/{nombre} [argumentos]
```

## Output esperado

[Formato de la respuesta]

## Restricciones

- [Restricción 1]
- [Restricción 2]
```

---

## INSTRUCCIONES: Diferencia Skill vs Command

| | Skill | Command |
|---|---|---|
| **Activación** | Automática (por descripción) | Manual (por `/nombre`) |
| **Uso** | Conocimiento persistente del dominio | Acción puntual y específica |
| **Frecuencia** | Se aplica en múltiples contextos | Se invoca intencionalmente |
| **Ejemplo** | "Usa cuando escribas Python" | "/deploy a staging" |

**Regla de oro**: Si es conocimiento que aplica en múltiples situaciones → skill.
Si es una acción específica que el usuario pide explícitamente → command.

---

## REFERENCIAS

- **Claude Code: Commands**: https://code.claude.com/docs/en/commands.md
- **Claude Code: Skills vs Commands**: https://code.claude.com/docs/en/features-overview.md
