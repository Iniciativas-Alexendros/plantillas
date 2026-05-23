# HOOK.md · Playbook de contenido

> **Propósito**: Los hooks interceptan eventos del ciclo de vida de Claude
> Code y permiten ejecutar acciones automáticas: validar, auditar, notificar,
> o transformar inputs/outputs.
>
> **Qué hacer**: Define el evento a interceptar, la condición de activación,
> y la acción a ejecutar. Elimina estas instrucciones.

---

## INSTRUCCIONES: Tipos de hooks disponibles

| Evento | Cuándo se dispara | Uso típico |
|---|---|---|
| `pre_tool_use` | Antes de ejecutar cualquier tool | Validación de seguridad, backups |
| `post_tool_use` | Después de ejecutar una tool | Logging, notificaciones |
| `pre_save` | Antes de guardar un archivo | Formateo, linting |
| `post_task` | Al completar una tarea | Resumen, cleanup |
| `on_error` | Cuando ocurre un error | Escalación, rollback |

---

## INSTRUCCIONES: Estructura

```yaml
# hooks/[nombre-del-hook].yaml

hook: [tipo-de-evento]
description: >
  [Descripción de qué hace este hook]

triggers:
  - tool: [nombre-tool]      # o condition: [condición]
    condition: [siempre | regex | estado]
    action: [nombre-de-acción]

rules:
  [nombre_de_regla]:
    # Configuración específica de la regla

  # Ejemplos de reglas comunes:
  risk_classification:
    gray: [patrones seguros]
    green: [patrones recuperables]
    amber: [patrones que requieren confirmación]
    red: [patrones bloqueados]
    action_per_level:
      gray: allow
      green: allow
      amber: confirm
      red: block_and_escalate

  audit_log:
    enabled: true
    format: jsonl
    fields: [timestamp, tool, args, decision]
    destination: ".claude/logs/audit.jsonl"
```

---

## INSTRUCCIONES: Acciones disponibles

| Acción | Descripción |
|---|---|
| `allow` | Permite la ejecución sin interrupción |
| `confirm` | Pausa y pide confirmación al usuario |
| `block` | Bloquea la ejecución |
| `block_and_warn` | Bloquea y muestra advertencia |
| `block_and_escalate` | Bloquea y notifica al orquestador |
| `audit_and_confirm` | Registra en audit log + pide confirmación |
| `validate_backup` | Verifica que existe backup antes de modificar |

---

## INSTRUCCIONES: Ejemplo completo

Ver `ejemplo_hook/pre-tool-use.yaml` para un hook operativo con:
- Clasificación de riesgo gray/green/amber/red
- Backups automáticos antes de edits
- Audit log en JSONL
- Rate limiting

---

## REFERENCIAS

- **Claude Code: Hooks**: https://code.claude.com/docs/en/hooks.md
- **Claude Code: Hooks Guide**: https://code.claude.com/docs/en/hooks-guide.md
- **Claude Code: Hooks Reference**: https://code.claude.com/docs/en/hooks-reference.md
