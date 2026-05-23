# /test

## Trigger

`/test`

## Descripción

Ejecuta el suite de tests del proyecto y reporta resultados con cobertura.

## Cuándo usar

- Antes de commitear cambios.
- Después de refactorizar código crítico.
- Cuando se necesita verificar que nada se rompió.

## Instrucciones

Cuando el usuario invoque `/test`, sigue estos pasos:

1. **Detectar runner**:
   - Buscar `package.json` → `npm test` / `pnpm test`
   - Buscar `pyproject.toml` / `pytest.ini` → `pytest`
   - Buscar `Cargo.toml` → `cargo test`
   - Buscar `go.mod` → `go test ./...`

2. **Ejecutar tests**:
   - Usar el comando detectado.
   - Si hay flag `--coverage` disponible, incluirlo.

3. **Reportar**:
   - Total de tests, passed, failed, skipped.
   - Cobertura (si disponible).
   - Tiempo de ejecución.
   - Resumen de fallos (si hay), con archivo y línea.

## Parámetros

| Parámetro | Tipo | Descripción | Default |
|-----------|------|-------------|---------|
| `watch` | boolean | Ejecutar en modo watch | `false` |
| `coverage` | boolean | Forzar reporte de cobertura | `true` |

## Ejemplo de uso

```
/test
/test watch=true
/test coverage=false
```

## Output esperado

```markdown
## Resultados de tests

- **Runner**: pytest
- **Tests**: 42 total | ✅ 40 passed | ❌ 2 failed | ⏭️ 0 skipped
- **Cobertura**: 87%
- **Tiempo**: 3.2s

### Fallos

1. `test_auth.py:47` — `test_login_invalid_password`
   - AssertionError: Esperado 401, got 403
```

## Restricciones

- Si tests fallan, sugerir ejecutar el test individual aislado para debug.
- No modificar código para "hacer pasar" tests sin entender la causa raíz.
