---
description: >
  Ejecuta la suite de tests del proyecto, calcula cobertura por archivo y
  emite un informe markdown. Invocar tras cambios en el código fuente o
  antes de abrir un PR para garantizar que la cobertura no regresa.
argument-hint: "<path> [--update-snapshots]"
allowed-tools:
  - Read
  - Bash
---

## Trigger

`/test-cobertura`

Activar cuando el usuario invoque `/test-cobertura [path] [--update-snapshots]`.
El parámetro `path` restringe los tests a un subdirectorio o archivo concreto;
`--update-snapshots` regenera los snapshots desactualizados antes del informe.

## Instrucciones

Cuando el usuario invoque `/test-cobertura`, sigue estos pasos:

1. **Detectar el runner de tests**:
   - Comprueba si existe `package.json` con `scripts.test` → usa `npm test` o
     `pnpm test` según qué binario esté disponible.
   - Si existe `pyproject.toml` o `pytest.ini` → usa `pytest --cov`.
   - Si no se detecta runner, reporta el error y detente.

2. **Aplicar `--update-snapshots` si se pidió**:
   - Ejecuta el runner con el flag equivalente (`--updateSnapshot` en Jest,
     `--snapshot-update` en Vitest) antes de la pasada de cobertura.
   - Informa al usuario qué snapshots se actualizaron.

3. **Ejecutar tests con cobertura**:
   - Restringe al `path` proporcionado (si se dio).
   - Captura stdout/stderr completo.
   - Si los tests fallan, registra los fallos pero continúa para generar el
     informe parcial; marca la cobertura como INCOMPLETA.

4. **Parsear los resultados de cobertura**:
   - Extrae tabla de cobertura por archivo (líneas, ramas, funciones, stmts).
   - Identifica archivos por debajo del umbral configurado (busca en
     `jest.config.*`, `vitest.config.*` o `pyproject.toml`; si no hay umbral,
     avisa que no está definido).

5. **Emitir el informe** en el formato definido en "Output esperado".

## Parámetros

| Parámetro | Tipo | Descripción | Default |
|---|---|---|---|
| `path` | string | Subdirectorio o archivo a testear | `.` (todo el proyecto) |
| `--update-snapshots` | flag | Regenera snapshots antes de medir cobertura | desactivado |

## Output esperado

```markdown
## Informe de cobertura · /test-cobertura

- **Runner detectado**: Jest 29.7 (pnpm)
- **Scope**: src/auth/
- **Estado de tests**: ✅ 47/47 passing  _(o ❌ 45/47 — 2 fallos)_
- **Snapshots**: 3 actualizados

### Cobertura por archivo

| Archivo | Stmts | Branch | Funcs | Lines |
|---|---|---|---|---|
| src/auth/login.ts | 98% | 92% | 100% | 98% |
| src/auth/logout.ts | 85% | 75% | 90% | 85% |
| src/auth/refresh.ts | 72% | 60% | 80% | 72% |

### Resumen global

| Métrica | Valor | Umbral | Estado |
|---|---|---|---|
| Statements | 88% | 80% | ✅ |
| Branches | 76% | 70% | ✅ |
| Functions | 90% | 80% | ✅ |
| Lines | 88% | 80% | ✅ |

### Archivos bajo umbral

_Ninguno_ _(o lista de archivos con cobertura insuficiente)_

### Próximos pasos

- Añadir tests para las ramas no cubiertas en `src/auth/refresh.ts:45-62`.
```

## Restricciones

- NUNCA ejecutar con `--update-snapshots` en CI sin confirmación explícita;
  la actualización de snapshots debe ser una decisión consciente del autor.
- Si los tests lanzan errores de compilación o importación, reportarlos en
  detalle antes de abortar; no silenciar stderr.
- No modificar archivos de configuración de cobertura ni umbrales definidos
  en el proyecto; solo leer y respetar los existentes.
- Si el `path` apunta a un archivo que no existe, reportar error inmediatamente.

## Referencias

- Jest coverage · https://jestjs.io/docs/configuration#collectcoverage-boolean
- Vitest coverage · https://vitest.dev/guide/coverage
- pytest-cov · https://pytest-cov.readthedocs.io/
- Claude Code Commands · https://code.claude.com/docs/en/commands.md
