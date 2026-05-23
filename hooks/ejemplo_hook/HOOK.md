# Hooks de Ejemplo · Suite completa

> **Propósito**: Este directorio contiene 3 hooks operativos que demuestran
> los principales puntos de interceptación del ciclo de vida de Claude Code.

---

## Hooks incluidos

| Hook | Archivo | Evento | Función |
|---|---|---|---|
| PreToolUse | `pre-tool-use.yaml` | Antes de ejecutar cualquier tool | Seguridad, backups, clasificación de riesgo |
| PostSave | `post-save.yaml` | Después de guardar un archivo | Formateo automático |
| OnError | `on-error.yaml` | Cuando ocurre un error | Reintentos, escalación, clasificación |

---

## Uso

Copia los archivos `.yaml` que necesites a `~/.claude/hooks/`:

```bash
cp hooks/ejemplo_hook/*.yaml ~/.claude/hooks/
```

O copia todo el directorio como base para tu propia suite:

```bash
cp -r hooks/ejemplo_hook ~/.claude/hooks/mi-suite
```

---

## Referencias

- **Claude Code: Hooks**: https://code.claude.com/docs/en/hooks.md
- **Claude Code: Hooks Guide**: https://code.claude.com/docs/en/hooks-guide.md
