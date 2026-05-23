# /review

## Trigger

`/review`

## Descripción

Revisa el diff de cambios no commiteados (o de un PR/rama) con criterios de calidad.

## Cuándo usar

- Antes de commitear para auto-revisión.
- Como pre-check antes de pedir review humana.
- Al revisar un PR como reviewer.

## Instrucciones

Cuando el usuario invoque `/review`, sigue estos pasos:

1. **Obtener diff**:
   - `git diff` para cambios no staged.
   - `git diff --staged` para cambios staged.
   - Si hay un PR/rama objetivo, `git diff main...<rama>`.

2. **Analizar por dimensiones**:
   - **Correctitud**: ¿Hay bugs obvios? ¿Edge cases no manejados?
   - **Legibilidad**: ¿Nombres claros? ¿Complejidad ciclomática razonable?
   - **Tests**: ¿Hay tests nuevos/modificados? ¿Cobertura suficiente?
   - **Seguridad**: ¿Nuevos inputs sin validar? ¿Secrets expuestos?
   - **Performance**: ¿N+1 queries? ¿Algoritmos ineficientes?
   - **Estilo**: ¿Sigue las convenciones del proyecto?

3. **Reportar**:
   - Issues críticos (bloqueantes) primero.
   - Sugerencias de mejora.
   - Praise por buenas prácticas encontradas.

## Parámetros

| Parámetro | Tipo | Descripción | Default |
|-----------|------|-------------|---------|
| `scope` | string | `staged`, `unstaged`, `branch`, `pr` | `unstaged` |
| `focus` | string | Dimensiones a enfocar (comma-separated) | `all` |

## Ejemplo de uso

```
/review
/review scope=staged
/review focus=security,performance
```

## Output esperado

```markdown
## Code Review

### 🚨 Crítico
- `src/auth.py:42` — Falta validación de `redirect_uri` contra whitelist

### 💡 Sugerencias
- `src/users.py:15` — Extraer magic number `86400` a constante `SECONDS_IN_DAY`

### ✅ Bien hecho
- Uso de `try/except` específico en `src/payments.py` en lugar de bare `except`
```

## Restricciones

- No reescribir código automáticamente; solo sugerir.
- Si el diff es >500 líneas, enfocar en los archivos críticos primero.
