# ejemplo-repositorio

> Ejemplo de repositorio profesional siguiendo el canon de plantillas de Alexendros.

[![CI](https://github.com/Alexendros/plantillas/actions/workflows/ci-global.yml/badge.svg)](https://github.com/Alexendros/plantillas/actions/workflows/ci-global.yml)

## Qué es

Este repositorio demuestra una estructura completa, profesional y operativa
al 120% para proyectos GitHub. Incluye community health files, CI/CD,
templates de issue/PR, ADRs, y guías para contribuidores humanos y LLMs.

## Stack

- GitHub Actions (CI/CD)
- Dependabot (actualización de dependencias)
- MADR 4.0.0 (decisiones arquitectónicas)
- Conventional Commits
- Semantic Versioning

## Instala

```bash
git clone git@github.com:alexendros/ejemplo-repositorio.git
cd ejemplo-repositorio
```

## Comandos

| Comando                     | Propósito                       |
| --------------------------- | ------------------------------- |
| `git log --oneline --graph` | Ver historia lineal con merges. |
| `make test`                 | Ejecutar tests (si aplica).     |
| `make lint`                 | Ejecutar linter (si aplica).    |

## Estructura

```
├── README.md              ← Este archivo
├── LICENSE                ← MIT
├── CHANGELOG.md           ← Historia de cambios
├── CONTRIBUTING.md        ← Cómo contribuir
├── SECURITY.md            ← Reporte de vulnerabilidades
├── CODE_OF_CONDUCT.md     ← Normas de comunidad
├── docs/adr/              ← Decisiones arquitectónicas
└── .github/               ← Templates, workflows, CODEOWNERS
```

## Documentación

- [`CONTRIBUTING.md`](CONTRIBUTING.md) — Cómo contribuir (commits, ramas, PRs).
- [`METODOLOGIA.md`](../plantilla_repositorio/METODOLOGIA.md) — Flujo de trabajo completo.
- [`LLM_GUIDE.md`](../plantilla_repositorio/LLM_GUIDE.md) — Guía para agentes/LLMs.
- [`SECURITY.md`](SECURITY.md) — Política de seguridad.
- [`CHANGELOG.md`](CHANGELOG.md) — Cambios por versión.

## Licencia

[MIT](LICENSE) © 2026 Alejandro · Iniciativas Alexendros.

## Contacto

contacto@alexendros.me
