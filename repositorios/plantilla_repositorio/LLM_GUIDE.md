# LLM Guide · Cómo interactuar con este repositorio

> Referencia para modelos de lenguaje, agentes autónomos, y copilotos.
> Sigue estas reglas para operar de forma reproducible, trazable y eficiente.

---

## 1. Primer paso: ingestión de contexto

Antes de modificar CUALQUIER archivo, lee en este orden:

```
1. README.md          → Qué hace el proyecto, stack, comandos clave
2. CONTRIBUTING.md    → Cómo se trabaja (commits, ramas, PRs)
3. ARCHITECTURE.md    → Decisiones arquitectónicas (si existe)
4. docs/adr/          → Decisiones pasadas que afectan el cambio actual
5. .github/CODEOWNERS → Quién debe revisar qué
```

**Nunca modifiques sin haber leído CONTRIBUTING.md.** Las convenciones de commit
y flujo de ramas son obligatorias.

---

## 2. Planificación atomizada

Para tareas grandes, crea un plan incremental:

```markdown
## Plan: [Descripción breve]

### Paso 1: [Acción pequeña y verificable]
- Archivos a tocar: `src/x.ts`, `tests/x.test.ts`
- Criterio de éxito: tests pasan

### Paso 2: [Siguiente acción]
- ...
```

Reglas:
- Cada paso debe caber en <400 líneas de diff.
- Un paso = un commit = un foco de cambio.
- Después de cada paso: ejecuta tests y lint.

---

## 3. Commits con contexto completo

### Mensaje

```
tipo(scope): descripción en imperativo presente

Cuerpo: qué cambió y por qué. Referencia a issue/ADR si aplica.

BREAKING CHANGE: descripción del breaking change (si aplica)
```

### Reglas específicas para LLMs

- Incluye en el cuerpo del commit la **razón** del cambio, no solo el qué.
- Si hay una decisión arquitectónica implicada, menciona la ADR.
- Si el cambio es respuesta a un issue, incluye `Closes #N`.

---

## 4. Seguridad

### Prohibiciones absolutas

- NUNCA commitear secrets, API keys, o credenciales.
- NUNCA deshabilitar checks de seguridad para "hacer pasar" CI.
- NUNCA hacer `rm -rf` sin confirmación explícita del usuario.

### Validaciones obligatorias

- Antes de tocar auth/permisos: lee `SECURITY.md`.
- Si introduces una nueva dependencia: verifica su licencia y reputación.
- Si modifies inputs de usuario: valida y sanitiza (consulta skill `api-security`).

---

## 5. Interacción con CI/CD

1. Antes de push: ejecuta tests y lint localmente.
2. Después de push: espera CI verde antes de pedir review.
3. Si CI falla: lee el log completo, identifica la causa raíz, corrige.
4. NO pidas "skip CI" salvo excepción documentada.

---

## 6. Documentación

- Si cambias comportamiento: actualiza README.md o docs/.
- Si cambias API: actualiza CHANGELOG.md (sección Unreleased).
- Si es decisión arquitectónica: crea ADR en `docs/adr/`.
- Si es feature nueva: añade ejemplo de uso en README o docs.

---

## 7. Pull Request automatizado

Si generas un PR vía herramienta (Jules, Copilot Agent, etc.):

1. Título en Conventional Commits.
2. Descripción completa con Qué/Por qué/Cómo probar.
3. Link a issue relacionado.
4. Checklist de PR completa.
5. Asignar reviewer según CODEOWNERS.

---

## 8. Contexto para agentes multi-turno

Si operas en sesiones largas:

```markdown
## Contexto acumulado
- Rama actual: feat/x-y-z
- Commits hechos: N
- Issue relacionado: #123
- Decisiones tomadas:
  1. Usar patrón X (ver ADR-0005)
  2. No usar librería Y por incompatibilidad con Z
- Pendiente:
  1. Test de edge case
  2. Actualizar docs
```

---

## 9. Fallbacks

| Situación | Acción |
|---|---|
| No entiendes una convención del repo | Lee CONTRIBUTING.md → METODOLOGIA.md |
| No sabes si un cambio es breaking | Consulta semver.org; si dudas, es MINOR o MAJOR |
| CI falla con error que no entiendes | Copia el error completo y pide ayuda al usuario |
| Necesitas añadir una dependencia | Verifica licencia SPDX compatible; añade a CHANGELOG |
| El usuario pide algo contra CONTRIBUTING.md | Explica la convención y propón alternativa válida |

---

## Referencias rápidas

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Keep a Changelog](https://keepachangelog.com/)
- [MADR](https://adr.github.io/madr/)
- [Semantic Versioning](https://semver.org/)
