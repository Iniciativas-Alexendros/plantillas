---
name: hooks
description: >
  Módulo de hooks para Claude Code. Los hooks son scripts bash que interceptan
  eventos del ciclo de vida del runtime (PreToolUse, PostToolUse, SessionStart,
  etc.) y devuelven una decisión JSON (allow / deny / continue) que el runtime
  ejecuta. Permiten guardrails de seguridad, auditoría y automatizaciones
  sin modificar el flujo principal del agente.
---

## Eventos soportados

| Evento             | Cuándo se dispara                            | Salida esperada      |
| ------------------ | -------------------------------------------- | -------------------- |
| `PreToolUse`       | Antes de ejecutar cualquier herramienta      | `allow` o `deny`     |
| `PostToolUse`      | Tras la ejecución de una herramienta         | `allow` o `continue` |
| `SessionStart`     | Al iniciar una sesión de Claude Code         | `allow`              |
| `SessionEnd`       | Al cerrar una sesión                         | `allow`              |
| `UserPromptSubmit` | Justo antes de enviar el prompt del operador | `allow` o `deny`     |
| `Stop`             | Cuando Claude Code va a detener el turno     | `allow` o `deny`     |
| `Notification`     | Evento de notificación del sistema           | `allow`              |
| `PreCompact`       | Antes de compactar el contexto               | `allow` o `deny`     |

El campo `matcher` en la cabecera del hook restringe qué herramientas lo activan.
Usa glob: `Bash(*)` para cualquier invocación de Bash, `Write(*.md)` para
escrituras sobre markdown, `*` para todo.

## Anti-patrones

- **Bloquear sin razón**: siempre incluir un `reason` legible en castellano
  para que el operador entienda por qué se denegó la acción.
- **Leer archivos grandes en el hook**: los hooks tienen restricciones de tiempo;
  operaciones lentas degradan la experiencia interactiva.
- **Escribir a stdout mensajes de debug**: stderr es el canal de logging;
  stdout es SOLO para el JSON de decisión.
- **Asumir que `jq` siempre está disponible**: usar siempre el patrón
  jq-con-fallback-a-python3 del ejemplo.
- **Lógica compleja sin tests**: un hook que falla silenciosamente puede
  bloquear todo el runtime. Testear con `echo '{"tool_input":{...}}' | bash hook.sh`.
- **Hardcodear rutas absolutas**: los hooks se instalan en entornos variados;
  usar rutas relativas o variables de entorno (`$HOME`, `$CLAUDE_DIR`).

## Cómo instalar un hook

1. Copiar `plantilla_hook.sh.template` a `~/.claude/hooks/<nombre-hook>.sh`.
2. Rellenar la cabecera declarativa (name, matcher, tool_pattern, description).
3. Implementar la lógica de detección en la sección marcada.
4. Hacer el archivo ejecutable: `chmod +x ~/.claude/hooks/<nombre-hook>.sh`.
5. Registrar el hook en `~/.claude/settings.json` bajo la clave `hooks`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash(*)",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/<nombre-hook>.sh"
          }
        ]
      }
    ]
  }
}
```

6. Validar con `python hooks/validar_hook.py ~/.claude/hooks/<nombre-hook>.sh --strict`.

## Cómo probar localmente

```bash
# Simular un PreToolUse con un comando inofensivo
echo '{"tool_name":"Bash","tool_input":{"command":"ls -la"}}' \
  | bash hooks/ejemplo_hook.sh.template

# Simular detección de secreto (usa un valor inventado, no un token real)
echo '{"tool_name":"Bash","tool_input":{"command":"echo FAKE_TOKEN_PLACEHOLDER"}}' \
  | bash hooks/ejemplo_hook.sh.template

# Validar formato del hook de plantilla (normal, con warnings esperados)
python hooks/validar_hook.py hooks/plantilla_hook.sh.template

# Validar el hook de ejemplo en modo estricto (debe pasar sin errores)
python hooks/validar_hook.py hooks/ejemplo_hook.sh.template --strict
```

## Referencias

- Claude Code Hooks (reference): https://code.claude.com/docs/en/hooks.md
- Claude Code Hooks Guide: https://code.claude.com/docs/en/hooks-guide
- Plantilla canon: `hooks/plantilla_hook.sh.template`
- Ejemplo funcional: `hooks/ejemplo_hook.sh.template`
