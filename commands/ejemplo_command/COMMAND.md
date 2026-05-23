# /deploy

## Trigger

`/deploy`

## Descripción

Despliega la rama actual al entorno de staging con validaciones previas.

## Cuándo usar

- Después de terminar una feature y pasar los tests locales.
- Cuando se necesita una preview para revisión de equipo.
- Antes de crear un PR para producción.

## Instrucciones

Cuando el usuario invoque `/deploy`, sigue estos pasos:

1. **Validar estado del repo**:
   - `git status` — debe estar limpio (sin cambios sin commit).
   - Si hay cambios sin commit, preguntar si hacer commit primero.

2. **Ejecutar tests**:
   - `npm test` o `pnpm test` (detectar automáticamente).
   - Si fallan, detenerse y reportar errores.

3. **Build**:
   - `npm run build` o `pnpm build`.
   - Verificar que no hay errores de compilación.

4. **Deploy a staging**:
   - Ejecutar el comando de deploy configurado (ej: `vercel --target staging`).
   - Capturar URL de despliegue.

5. **Reportar**:
   - URL del despliegue.
   - Estado de tests.
   - Cambios incluidos (git log vs. último deploy).

## Parámetros

| Parámetro | Tipo | Descripción | Default |
|-----------|------|-------------|---------|
| `target` | string | Entorno de destino | `staging` |

## Ejemplo de uso

```
/deploy
/deploy target=production
```

## Output esperado

```markdown
## Deploy a staging

- **URL**: https://mi-app-staging.vercel.app
- **Tests**: ✅ 42/42 passing
- **Build**: ✅ Sin errores
- **Cambios**: 3 commits desde último deploy
  - feat: añade auth JWT
  - fix: corrige race condition en login
  - chore: actualiza dependencias
```

## Restricciones

- NUNCA deploy a producción sin confirmación explícita.
- Si tests fallan, NO continuar con el deploy.
- Requiere que el usuario tenga permisos de deploy configurados.
