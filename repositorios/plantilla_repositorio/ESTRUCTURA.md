# Estructura de archivos · Mapa completo

> Referencia visual de qué archivos van dónde y por qué.

---

## Raíz

```
repo/
├── README.md              ← Portal de entrada. Badge CI, stack, install.
├── LICENSE                ← Licencia (GitHub la detecta). Obligatorio open source.
│   o COPYRIGHT.md         ← Si es privado/propietario.
├── CHANGELOG.md           ← Historia de cambios (Keep a Changelog).
├── CONTRIBUTING.md        ← Cómo contribuir (commits, ramas, PRs).
├── SECURITY.md            ← Cómo reportar vulnerabilidades.
├── CODE_OF_CONDUCT.md     ← Normas de comportamiento (Contributor Covenant).
├── AUTHORS.md             ← Lista de contribuidores principales.
├── SUPPORT.md             ← Dónde obtener ayuda.
├── MAINTAINERS.md         ← Quién mantiene qué.
├── RELEASE.md             ← Proceso de release (checklist).
├── ROADMAP.md             ← Plan a futuro.
├── .editorconfig          ← Consistencia de espacios/tabs entre editores.
├── .gitattributes         ← Normalización de finales de línea (LF).
├── .gitignore             ← Qué NO versionar.
└── [código fuente]        ← src/, app/, lib/, etc. (depende del stack)
```

## `.github/`

```
.github/
├── CODEOWNERS                        ← Owners por directorio/archivo.
├── PULL_REQUEST_TEMPLATE.md          ← Plantilla de PR.
├── FUNDING.yml                       ← Sponsorship (solo públicos).
├── dependabot.yml                    ← Actualización automática de deps.
│
├── ISSUE_TEMPLATE/
│   ├── bug.yml                       ← Formulario de bug.
│   ├── feature.yml                   ← Propuesta de feature.
│   ├── question.yml                  ← Pregunta de uso.
│   ├── security.yml                  ← Reporte de seguridad.
│   └── config.yml                    ← Links externos (docs, Discord, etc.).
│
└── workflows/
    ├── ci.yml                        ← Tests + lint + typecheck.
    └── [otros workflows específicos]
```

## `docs/`

```
docs/
├── README.md              ← Índice de documentación.
└── adr/
    ├── 0001-usar-madr-para-adrs.md   ← Primera ADR (meta).
    ├── 0002-*.md                     ← Decisiones sucesivas.
    └── README.md                     ← Índice de ADRs.
```

---

## Matriz: ¿Qué archivo necesito?

| Si quiero... | Crear/Editar |
|---|---|
| Que la gente entienda el proyecto | `README.md` |
| Que contribuyan correctamente | `CONTRIBUTING.md` |
| Que reporten bugs estructurados | `.github/ISSUE_TEMPLATE/bug.yml` |
| Que propongan features | `.github/ISSUE_TEMPLATE/feature.yml` |
| Que PRs sean consistentes | `.github/PULL_REQUEST_TEMPLATE.md` |
| Que reviews vayan al experto correcto | `.github/CODEOWNERS` |
| Documentar una decisión arquitectónica | `docs/adr/NNNN-*.md` |
| Que dependencias se actualicen solas | `.github/dependabot.yml` |
| Que el código tenga formato consistente | `.editorconfig` |
| Que Git normalice finales de línea | `.gitattributes` |

---

## Convenciones de naming

- Archivos markdown: `MAYÚSCULAS.md` en raíz; `minúsculas.md` en subdirectorios.
- ADRs: `NNNN-descripción-corta-en-kebab-case.md`.
- Workflows: `nombre-descriptivo.yml` (kebab-case).
- Templates de issue: `tipo.yml` (bug, feature, etc.).
