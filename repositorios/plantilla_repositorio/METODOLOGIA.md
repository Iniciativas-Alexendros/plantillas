# Metodología de trabajo · GitHub Flow + Conventional Commits

> Este documento define CÓMO se trabaja en el repositorio. Es la referencia
> obligatoria para todo contribuidor (humano o agente).

---

## 1. Filosofía

- **Trunk-based development**: `main` siempre desplegable.
- **Commits atómicos**: cada commit hace una sola cosa y la hace bien.
- **PRs pequeños**: <400 líneas de diff siempre que sea posible.
- **Revisión obligatoria**: todo pasa por PR; nada directo a `main`.
- **CI como guardián**: si CI no está verde, no se mergea.

---

## 2. GitHub Flow

```
main (protegida, siempre desplegable)
  ↑
  PR: feat/auth-jwt —→ review —→ squash merge —→ delete branch
```

### Pasos

1. **Sincroniza**: `git checkout main && git pull origin main`
2. **Crea rama**: `git checkout -b <tipo>/<scope>-<descripción>`
3. **Commits atómicos** con mensajes Conventional Commits.
4. **Push**: `git push -u origin <rama>`
5. **Abre PR**: usa la plantilla, rellena Qué/Por qué/Cómo probar.
6. **Espera CI**: debe estar verde.
7. **Revisión**: al menos 1 aprobación; CODEOWNER si aplica.
8. **Squash merge**: el mensaje del squash sigue Conventional Commits.
9. **Borra rama**: local y remota.

---

## 3. Conventional Commits

### Formato

```
<tipo>(<scope opcional>): <descripción corta>

<cuerpo opcional>

<footer opcional>
```

### Tipos

| Tipo       | Cuándo usar                           | Ejemplo                                                |
| ---------- | ------------------------------------- | ------------------------------------------------------ |
| `feat`     | Nueva funcionalidad                   | `feat(api): añade endpoint de login JWT`               |
| `fix`      | Corrección de bug                     | `fix(auth): corrige race condition en logout`          |
| `docs`     | Documentación                         | `docs(readme): actualiza instrucciones de install`     |
| `style`    | Formateo (sin cambio de lógica)       | `style: aplica prettier a src/`                        |
| `refactor` | Refactor sin cambio de comportamiento | `refactor(db): extrae lógica de queries a repositorio` |
| `test`     | Tests                                 | `test(auth): añade tests para login edge cases`        |
| `chore`    | Tareas de mantenimiento               | `chore(deps): actualiza next.js a 15.2`                |
| `ci`       | CI/CD                                 | `ci: añade job de seguridad con gha-scanner`           |
| `build`    | Sistema de build                      | `build: configura esbuild para workers`                |
| `perf`     | Mejora de rendimiento                 | `perf(db): añade índice compuesto en users_email`      |
| `security` | Fix de seguridad                      | `security(auth): sanitiza input en login`              |

### Reglas

- Descripción en imperativo presente: "añade", no "añadí" ni "añadiendo".
- Sin punto final en la primera línea.
- Si hay `BREAKING CHANGE:` en el footer o `!` después del tipo, es breaking.

---

## 4. Nomenclatura de ramas

```
<tipo>/<scope>-<descripción-corta-en-kebab-case>
```

Ejemplos:

- `feat/api-jwt-auth`
- `fix/ui-mobile-nav`
- `docs/adr-database-migration`
- `chore/deps-update-eslint`

Prohibido:

- `main`, `master`, `develop` (reservadas)
- Nombres sin tipo
- Mayúsculas o underscores

---

## 5. Pull Requests

### Apertura

1. Título en formato Conventional Commits (será el mensaje de squash merge).
2. Plantilla completa:
   - **Qué**: descripción del cambio.
   - **Por qué**: motivación y contexto.
   - **Cómo probar**: pasos para validar.
   - **Checklist**: tests, docs, ADR si aplica.
3. Link a issue: `Closes #123` o `Relates to #456`.
4. Screenshots/GIFs si hay cambios visuales.

### Revisión

- **Reviewer**: verifica correctitud, legibilidad, tests, seguridad.
- **Comentarios**: se resuelven antes del merge.
- **Aprobación**: al menos 1; CODEOWNER para archivos críticos.

### Merge

- Siempre **squash merge** (historia lineal en `main`).
- Mensaje del squash = título del PR.
- Borrar rama tras merge.

---

## 6. Issues

### Apertura

- Usar templates de issue (bug, feature, question, security).
- Título descriptivo: `[scope] descripción breve`.
- Labels obligatorios: `bug`, `feature`, `question`, `security`, `docs`.

### Gestión

- Todo issue debe estar asignado o en backlog.
- Issues de seguridad: label `security` + milestone del próximo patch.
- Stale bot: cierra issues sin actividad en 90 días (con aviso previo).

---

## 7. Versionado (Semver)

```
vMAJOR.MINOR.PATCH
```

| Cambio                              | Versión | Ejemplo             |
| ----------------------------------- | ------- | ------------------- |
| Breaking change                     | MAJOR   | `v1.2.3` → `v2.0.0` |
| Nueva feature (backward compatible) | MINOR   | `v1.2.3` → `v1.3.0` |
| Bugfix                              | PATCH   | `v1.2.3` → `v1.2.4` |

- Tag en Git: `git tag -a v1.3.0 -m "Release v1.3.0"`
- Release en GitHub con notas automáticas desde CHANGELOG.

---

## 8. Decisiones arquitectónicas (ADR)

- Cada decisión arquitectónica transversal se documenta en `docs/adr/`.
- Formato MADR 4.0.0.
- Numeración secuencial: `0001`, `0002`, etc.
- Status: `proposed`, `accepted`, `deprecated`, `superseded by NNNN`.

---

## 9. Comunicación async

- **Discusiones técnicas**: GitHub Discussions o issues con label `discussion`.
- **Dudas rápidas**: issue con label `question`.
- **Urgente/seguridad**: email a `security@` o `contacto@` (ver `SECURITY.md`).
- **NO**: Slack/Discord para decisiones técnicas (se pierde el contexto).

---

## 10. Checklist diario del contribuidor

```markdown
- [ ] Rama sincronizada con main
- [ ] Commits atómicos con Conventional Commits
- [ ] Tests pasan localmente
- [ ] Lint/format pasan
- [ ] PR usa plantilla
- [ ] CI verde antes de pedir review
- [ ] Generar contrato OpenAPI (v3.1.0)
- [ ] Crear scaffold hexagonal (ports, adapters, impl)
- [ ] Implementar lógica de negocio (ping service)
- [ ] Generar pruebas unitarias
- [ ] Ejecutar lint y test suite
- [ ] Verificar contrato con OpenAPI validator
```
