---
name: ecosystem-conventions
description: >
  Convenciones del ecosistema Alexendros y guía de desarrollo específica para
  el repo plantillas (sistema de plantillas modulares para Claude Code).
  Activar al trabajar en este repo, crear módulos, o modificar validadores.
---

# Convenciones Ecosistema Alexendros — Plantillas

## Repo Profile
- **Tipo**: Python + Bash + Markdown
- **Stack**: Python 3.12+ (validadores), Bash (entrypoints), GitHub Actions (CI)
- **Dependencia**: pyyaml (única dep Python)
- **Licencia**: MIT

## Comandos esenciales
```bash
python validar_repo.py --strict          # validación global de estructura
pre-commit run --all-files               # lint completo (YAML, JSON, Python, Shell, Markdown)
pytest tests/ -v                         # smoke + unit tests
python <modulo>/validar_<modulo>.py <ruta> --strict  # validador individual
```

## Pre-PR Checklist
1. `pre-commit run --all-files` — sin errores
2. `python validar_repo.py --strict` — estructura válida
3. `pytest tests/ -v` — todos los tests pasan
4. Si se modifican módulos: actualizar CHANGELOG.md (enforced por PR Guardian)
5. Título del PR: Conventional Commits (`feat|fix|docs|ci|chore...`)

## Estructura de módulos
Cada módulo sigue el patrón canónico:
```
<modulo>/
├── plantilla_<modulo>/    # Template para crear nuevos (con placeholders)
├── ejemplo_<modulo>/      # Referencia funcional (pasa --strict)
├── validar_<modulo>.py    # Validador Python con BaseValidator
└── README.md              # Documentación del módulo
```

## Motor de validación (validadores/)
- `base.py`: `BaseValidator` — clase base con `Check`, `Resultado`, `Nivel`
- `checks.py`: checks reutilizables (archivos vacíos, placeholders, YAML, etc.)
- `reporte.py`: generación de reportes de validación
- `base.py` es archivo PROTEGIDO — requiere issue previo para modificar

## Archivos protegidos (PR Guardian)
Modificar estos archivos requiere issue previo:
- INDEX.md, README.md, CONTRIBUTING.md, CODE_OF_CONDUCT.md, ROADMAP.md
- INTEGRACION.md, claude-init, update.sh, validadores/base.py

## Workflows CI
- `ci-global.yml`: lint YAML/JSON/Python + validar estructura
- `pr-guardian.yml`: título CC, tamaño PR, archivos protegidos, CHANGELOG
- `validar-todos.yml`: valida todos los ejemplos de todos los módulos
- `_lib-*.yml`: workflows reutilizables (lint, supply-chain, release, etc.)

## Git
- Branch: `devin/<timestamp>-<descripcion>`
- Commits: Conventional Commits
- Nunca push a `main`. Branch protection activa.
- PRs > 800 líneas generan warning

## Anti-patrones
- NO improvisar estructuras — siempre usar plantilla del módulo
- NO crear módulos sin validador + ejemplo + README
- NO modificar archivos protegidos sin issue previo
- NO usar `pip install` sin actualizar requirements.txt
- NO añadir dependencias Python innecesarias (solo pyyaml)
