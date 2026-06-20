# Estándares del portfolio

> **Propósito**: catálogo canónico de la metodología y cultura de trabajo común a los repos del portfolio (`~/repositorios/`). Fuente única que los demás repos adoptan para cohesionar formato, calidad y operación. Extraído de patrones ya vigentes en `dotclaude`, `enfoke` y este repo.
>
> **Qué hacer**: al homologar un repo, recorre las 6 secciones y aplica cada estándar con su checklist. Lo que no aplique al tipo de repo se omite explícitamente, no se ignora en silencio.

## 1. CLAUDE.md con XML suave
Cada repo lleva un `CLAUDE.md` en la raíz con secciones en tags suaves (proyecto, stack, estado, arquitectura, pendiente, notas), lo crítico arriba. Los comandos del bloque stack deben existir de verdad (scripts de package.json / justfile). El estado distingue lo verificado de lo inferido.

## 2. Frontmatter YAML para contenido catalogado
Todo fichero de contenido catalogado (definición, skill, entrada) abre con frontmatter YAML válido: name (kebab-case), description (una línea), version (SemVer).

## 3. Versionado y CHANGELOG
Versión en fichero VERSIÓN (catálogos) o package.json/Cargo.toml (código), SemVer. CHANGELOG.md estilo Keep a Changelog; las entradas [Unreleased] se consolidan en una versión al taggear. Tag de release que case con la versión del manifiesto.

## 4. Calidad local: pre-commit homogéneo
Repos JS/TS: husky + lint-staged + commitlint (Conventional Commits). Python: pre-commit + ruff. El hook formatea/lintea lo staged, no todo el repo.

## 5. Bloque pendiente como TODO canónico
El trabajo abierto vive en el bloque pendiente del CLAUDE.md, no disperso como marcadores en código. Más auditable, sobrevive a refactors, ligado a fase/versión.

## 6. .env.example + validación de entorno
Todo repo con variables de entorno publica .env.example (placeholders, nunca secretos reales) y un check check:env que falla si falta una variable requerida. Nombre canónico .env.example (no .env.local.example).

## Matriz CI mínima (GitHub Actions)
Gate de PR en orden: typecheck, lint, format, test, build — con el comando propio de cada lenguaje (tsc/eslint/prettier/vitest/next para JS; cargo check/clippy/fmt/test/build para Rust; ruff/pytest para Python).

## Referencias
- CONTRIBUTING.md de este repo.
- Conventional Commits: https://www.conventionalcommits.org
- Keep a Changelog: https://keepachangelog.com
