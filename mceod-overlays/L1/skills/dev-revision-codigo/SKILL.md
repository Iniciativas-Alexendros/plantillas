---
name: dev-revision-codigo
description: >
  Revisión de cambios antes de integrar a main: bugs, regresiones, simplificación,
  deuda y convenciones. Activa cuando se pida revisar un diff/PR, "code review",
  "revisar cambios", "antes de mergear", o tras cambios grandes. Envuelve el builtin
  /code-review y el validador canónico.
allowed-tools: Read, Grep, Glob, Bash
---

# Revisión de código (pre-integración)

Objetivo: un veredicto accionable de si un cambio puede integrarse a `main`.

## Procedimiento

1. **Diff real** contra el punto base correcto (evita falsos positivos por divergencia):
   ```bash
   set -o pipefail
   base=$(git merge-base origin/main HEAD)
   git diff --stat "$base"..HEAD
   ```
2. **Bugs y simplificación**: ejecuta el builtin `/code-review` sobre el diff.
3. **Estructura/convenciones**: tests pareados, manejo de errores, sin secretos en
   git, `set -o pipefail` en scripts, idioma/estilo (sin emojis), commits convencionales.
4. **Homologación** (si es repo de la cartera):
   `python ~/Repositorios/plantillas/repositorios/validar_repositorio.py <repo> --strict`.

## Salida

Hallazgos por severidad (`bloqueante`/`mayor`/`menor`/`nit`) con `archivo:línea` y
propuesta; veredicto `aprobar`/`aprobar con cambios`/`bloquear`.

## Notas

- Para diffs de campañas de homologación, distinguir boilerplate de bajo riesgo de
  cambios funcionales (bumps de versión, fixes de lógica) que exigen build verde.
