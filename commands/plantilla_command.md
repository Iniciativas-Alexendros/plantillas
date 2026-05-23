---
description: >
  Una a tres líneas describiendo cuándo invocar este comando.
  Incluye el disparador exacto, el dominio técnico y el resultado esperado.
  Claude Code usa este texto para mostrarlo en el listado de comandos.
argument-hint: "<ARG-REQUERIDO> [ARG-OPCIONAL]"
allowed-tools:
  - Read
  - Bash
---

## Trigger

`/NOMBRE-COMANDO-KEBAB`

Activar cuando el usuario invoque explícitamente `/NOMBRE-COMANDO-KEBAB [args]`.
A diferencia de las skills (activación automática), los comandos son siempre
invocados de forma manual e intencional.

## Instrucciones

Cuando el usuario invoque `/NOMBRE-COMANDO-KEBAB`, sigue estos pasos:

1. **PASO-A**: DESCRIPCION-ACCION-A.
   - Sub-paso o condición relevante.
   - Si CONDICION, detener y reportar.

2. **PASO-B**: DESCRIPCION-ACCION-B.
   - Sub-paso o condición relevante.

3. **PASO-C**: DESCRIPCION-ACCION-C.
   - Sub-paso o condición relevante.

4. **Reportar**: Emitir el output en el formato definido en "Output esperado".

## Parámetros

| Parámetro | Tipo | Descripción | Default |
|---|---|---|---|
| `ARG-REQUERIDO` | string | DESCRIPCION-ARG-1 | — |
| `ARG-OPCIONAL` | string | DESCRIPCION-ARG-2 | `VALOR-DEFAULT` |

## Output esperado

```markdown
## TITULO-DEL-INFORME

- **CAMPO-1**: VALOR
- **CAMPO-2**: VALOR
- **CAMPO-3**: VALOR

### Detalle

SECCION-DETALLE-LIBRE
```

## Restricciones

- NUNCA ACCION-DESTRUCTIVA sin confirmación explícita del usuario.
- Si CONDICION-DE-FALLO, NO continuar y reportar el error claramente.
- RESTRICCION-ADICIONAL relevante para este comando.

## Referencias

- Claude Code Commands · https://code.claude.com/docs/en/commands.md
- CLAUDE.md secciones 1-2 (doctrina maestrías + atribución) · `~/.claude/CLAUDE.md`
