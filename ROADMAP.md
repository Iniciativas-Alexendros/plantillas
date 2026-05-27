# ROADMAP · Sistema de Plantillas Modulares para Claude Code

> **Estado**: Fase 3 COMPLETADA (con items pendientes de automatización)  
> **Última actualización**: 2026-05-23  
> **Propietario**: alexendros  
> **Licencia**: MIT

---

## Resumen ejecutivo

Este documento define el plan de desarrollo del sistema de plantillas modulares.
Cada fase es **reproducible**, con criterios de aceptación claros y dependencias
explícitas. El objetivo final es un ecosistema de plantillas `claude init`-ready
que permita a cualquier usuario (o LLM) inicializar, validar y desplegar
componentes de Claude Code en segundos.

---

## Leyenda

| Símbolo | Estado |
|---------|--------|
| ✅ | Completado |
| 🔄 | En progreso |
| ⏳ | Pendiente |
| 🚫 | Bloqueado |
| 📦 | En producción |

---

## FASE 1: MVP · Fundamentos (COMPLETADA)

> **Objetivo**: Estructura base funcional con al menos 1 módulo completo.
> **Duración estimada**: 2-3 sesiones. **Completado**: 2026-05-23.

### Tareas completadas

| # | Tarea | Módulo | Estado |
|---|-------|--------|--------|
| 1.1 | Estructura modular `plantilla_*` + `ejemplo_*` | Global | ✅ |
| 1.2 | Módulo `agentes` con orquestador hub-and-spoke | Agentes | ✅ |
| 1.3 | Validador `validar_agente.py` con 10 checks | Agentes | ✅ |
| 1.4 | CI/CD GitHub Actions matrix multi-agente | Agentes | ✅ |
| 1.5 | Índice maestro `INDEX.md` con navegación | Global | ✅ |
| 1.6 | Módulos `skills`, `commands`, `hooks`, `plugins`, `mcp` | Componentes | ✅ |
| 1.7 | Meta-módulo `dot-claude` | Global | ✅ |

### Criterios de aceptación Fase 1
- [x] Todo módulo tiene `plantilla_*` y `ejemplo_*`
- [x] `ejemplo_agente` pasa validación `--strict`
- [x] `cp -r plantilla_* ~/.claude/...` produce un componente funcional
- [x] Documentación de cada módulo incluye referencias oficiales

---

## FASE 2: Robustecimiento · Calidad y Cobertura

> **Objetivo**: Cada módulo tiene validador propio, CI/CD, y ejemplos enriquecidos.
> **Dependencias**: Fase 1. **Duración estimada**: 3-4 sesiones. **Completado**: 2026-05-23.

### 2.1 Validadores por módulo

| # | Tarea | Prioridad | Estado | Notas |
|---|-------|-----------|--------|-------|
| 2.1.1 | Extraer motor de validación de `validar_agente.py` a librería compartida | Alta | ✅ | `validadores/` en raíz: BaseValidator, Check, Resultado, Nivel + 5 checks reutilizables |
| 2.1.2 | Crear `validar_skill.py` | Media | ✅ | Checks: estructura, frontmatter SKILL.md, placeholders, contenido mínimo |
| 2.1.3 | Crear `validar_command.py` | Media | ✅ | Checks: estructura, placeholders, contenido mínimo, kebab-case |
| 2.1.4 | Crear `validar_hook.py` | Media | ✅ | Checks: YAML válido, placeholders, contenido mínimo, campo hook/event |
| 2.1.5 | Crear `validar_plugin.py` | Baja | ✅ | Checks: plugin.json válido, componentes existen físicamente |
| 2.1.6 | Crear `validar_mcp.py` | Baja | ✅ | Checks: JSON parseable, manifest o config cliente, server.py/ts con referencias MCP |
| 2.1.7 | Crear `validar_dot_claude.py` | Alta | ✅ | Checks: estructura, settings.json, mcp.json, CLAUDE.md (frontmatter opcional) |

### 2.2 CI/CD por módulo

| # | Tarea | Prioridad | Estado | Notas |
|---|-------|-----------|--------|-------|
| 2.2.1 | Workflow central `validar-todos.yml` | Alta | ✅ | Valida todos los ejemplos de todos los módulos en matriz |
| 2.2.2 | Workflow para `skills/` | Media | ✅ | `.github/workflows/validar-skills.yml` · descubrimiento + matriz |
| 2.2.3 | Workflow para `commands/` | Media | ✅ | `.github/workflows/validar-commands.yml` · descubrimiento + matriz |
| 2.2.4 | Workflow para `hooks/` | Media | ✅ | `.github/workflows/validar-hooks.yml` · descubrimiento + matriz |
| 2.2.5 | Workflow para `mcp/` | Baja | ✅ | `.github/workflows/validar-mcp.yml` · descubrimiento + matriz |
| 2.2.6 | Workflow para `plugins/` | Media | ✅ | `.github/workflows/validar-plugins.yml` · descubrimiento + matriz |
| 2.2.7 | Workflow para `dot-claude/` | Alta | ✅ | `.github/workflows/validar-dot-claude.yml` · descubrimiento + matriz |

### 2.3 Enriquecimiento de ejemplos

| # | Tarea | Prioridad | Estado | Notas |
|---|-------|-----------|--------|-------|
| 2.3.1 | `ejemplo_skill` con múltiples skills (2-3) | Media | ✅ | `SKILL.md` principal + `testing-pytest/` + `api-security/` |
| 2.3.2 | `ejemplo_command` con múltiples comandos | Media | ✅ | `COMMAND.md` principal + `test/` + `review/` |
| 2.3.3 | `ejemplo_hook` con múltiples hooks | Media | ✅ | `pre-tool-use.yaml` + `post-save.yaml` + `on-error.yaml` + `HOOK.md` |
| 2.3.4 | `ejemplo_mcp` con múltiples tools | Baja | ✅ | `get_timestamp` + `get_weather` en `server.py` |
| 2.3.5 | Documentar integración entre módulos | Alta | ✅ | `INTEGRACION.md` con mapa, decision tree, anti-patrones, ejemplo completo |

### 2.4 Afinado de repositorios (iteración post-Fase 2)

> **Contexto**: El directorio `repos/` existía previamente como motor de canonización
> de repositorios. Se renombró a `repositorios/` y se integró con el sistema de plantillas.

| # | Tarea | Prioridad | Estado | Notas |
|---|-------|-----------|--------|-------|
| 2.4.1 | Renombrar `repos/` → `repositorios/` | Alta | ✅ | Integrado como módulo 8 del sistema |
| 2.4.2 | Crear `plantilla_repositorio/` con playbook completo | Alta | ✅ | `REPOSITORIO.md`, `METODOLOGIA.md`, `LLM_GUIDE.md`, `ESTRUCTURA.md` |
| 2.4.3 | Crear `ejemplo_repositorio/` funcional | Alta | ✅ | 20+ archivos: README, LICENSE, CHANGELOG, CONTRIBUTING, SECURITY, CODE_OF_CONDUCT, AUTHORS, SUPPORT, MAINTAINERS, RELEASE, ROADMAP, .editorconfig, .gitattributes, .gitignore, CODEOWNERS, PR template, issue templates, dependabot, CI workflow, ADR |
| 2.4.4 | Crear `validar_repositorio.py` | Alta | ✅ | 13 checks: estructura, README, licencia, changelog, contributing, security, CODEOWNERS, GitHub files, CI, dependabot, ADRs, placeholders, archivos vacíos |
| 2.4.5 | Crear workflow CI/CD para repositorios | Media | ✅ | `.github/workflows/validar-repositorios.yml` |
| 2.4.6 | Documentar metodología GitHub Flow + Conventional Commits | Alta | ✅ | En `METODOLOGIA.md`: flujo de ramas, commits, PRs, reviews, semver, ADRs |
| 2.4.7 | Documentar guía para LLMs/agentes | Alta | ✅ | En `LLM_GUIDE.md`: contexto, atomización, seguridad, CI, PR automatizado |

### Criterios de aceptación Fase 2
- [x] Todo módulo tiene validador propio ejecutable con `--strict`
- [x] Todo módulo tiene workflow de CI/CD independiente
- [x] `ejemplo_*` de cada módulo tiene ≥2 ejemplos funcionales
- [x] Documentación de integración cruzada entre módulos
- [x] Módulo `repositorios/` integrado con playbook, ejemplo, validador, CI/CD, metodología y guía LLM

---

## FASE 3: Ecosistema · Distribución y Colaboración

> **Objetivo**: El sistema es usable por terceros y soporta versionado.
> **Dependencias**: Fase 2. **Duración estimada**: 4-6 sesiones. **Completado**: 2026-05-23.

### 3.1 Versionado y releases

| # | Tarea | Prioridad | Estado | Notas |
|---|-------|-----------|--------|-------|
| 3.1.1 | Semver para el sistema de plantillas | Alta | ✅ | `v1.0.0` en CHANGELOG.md; tag listo para aplicar |
| 3.1.2 | `CHANGELOG.md` con formato Keep a Changelog | Alta | ✅ | Documenta Fase 1, Fase 2, y Unreleased |
| 3.1.3 | Versionado por módulo | Media | ⏳ | Pendiente: añadir versión en manifest de cada módulo |
| 3.1.4 | Releases automatizadas vía GitHub Actions | Media | ⏳ | Pendiente: workflow `release.yml` que genere tag → release notes |

### 3.2 Instalación y bootstrap

| # | Tarea | Prioridad | Estado | Notas |
|---|-------|-----------|--------|-------|
| 3.2.1 | Script `install.sh` idempotente | Alta | ✅ | Descarga release o clona repo; `--prefix`, `--version`, `--dry-run`, `--symlink` |
| 3.2.2 | Comando `claude-init` script | Alta | ✅ | Wrapper interactivo: `--modulo`, `--ejemplo`, `--proyecto`, `--repositorio`, `--list` |
| 3.2.3 | Plantilla para `.claude` a nivel de proyecto | Alta | ✅ | `proyecto/`: CLAUDE.md, settings.json, ci.yml mínimo |
| 3.2.4 | Actualizador (`update.sh`) | Media | ✅ | Detecta versión remota, backup, actualiza con `--force` o `--check` |

### 3.3 Testing y calidad

| # | Tarea | Prioridad | Estado | Notas |
|---|-------|-----------|--------|-------|
| 3.3.1 | Tests unitarios para validadores | Alta | ✅ | `tests/test_validadores.py` — pytest: estructura, archivos vacíos, placeholders, BaseValidator |
| 3.3.2 | Tests de integración "smoke" | Alta | ✅ | `tests/test_smoke.py` — valida que todos los ejemplos pasan `--strict`; copiar plantilla detecta placeholders |
| 3.3.3 | Pre-commit hooks (git) | Media | ✅ | `.pre-commit-config.yaml`: trailing-whitespace, check-yaml/json, detect-private-key, detect-placeholders custom, validate-modules custom |
| 3.3.4 | Formateo automático (prettier/yamlfmt) | Media | ⏳ | Pendiente: añadir prettier/yamlfmt al pre-commit cuando estén disponibles |
| 3.3.5 | Coverage de documentación | Baja | ⏳ | Pendiente: script de auditoría de secciones completadas |

### 3.4 Colaboración

| # | Tarea | Prioridad | Estado | Notas |
|---|-------|-----------|--------|-------|
| 3.4.1 | `CONTRIBUTING.md` | Alta | ✅ | Guía completa: estructura de módulo, validador, workflow, testing, convenciones |
| 3.4.2 | Template para nuevos módulos | Alta | ✅ | `modulo/`: README.md, MODULO.md, ejemplo_modulo/EJEMPLO.md |
| 3.4.3 | Issue templates en GitHub | Media | ✅ | `bug.yml`, `feature.yml`, `nuevo-modulo.yml`, `config.yml` en `.github/ISSUE_TEMPLATE/` |
| 3.4.4 | Code of Conduct | Baja | ✅ | `CODE_OF_CONDUCT.md` — Contributor Covenant 2.1 |

### Criterios de aceptación Fase 3
- [x] Sistema versionado con semver (`CHANGELOG.md` con v1.0.0)
- [x] Script de instalación de 1 línea funciona en Linux/macOS
- [x] Suite de tests ejecutable con `pytest` (o runner manual si pytest no está instalado)
- [x] Pre-commit hooks aplican lint/validación automática
- [x] Un contribuidor externo puede añadir un módulo siguiendo CONTRIBUTING.md

---

## FASE 4: Producción · Escalado y Mantenimiento

> **Objetivo**: El sistema es mantenido activamente con monitoreo.
> **Dependencias**: Fase 3. **Duración estimada**: Continuo.

### 4.1 Monitoreo

| # | Tarea | Prioridad | Estado | Notas |
|---|-------|-----------|--------|-------|
| 4.1.1 | Métricas de uso de plantillas | Baja | ⏳ | Contador de `cp plantilla_*` vía hooks (opt-in) |
| 4.1.2 | Dashboard de calidad | Baja | ⏳ | Badge de CI en README por módulo |
| 4.1.3 | Alertas de rotura | Media | ⏳ | Slack/email si CI de main falla |

### 4.2 Mantenimiento continuo

| # | Tarea | Frecuencia | Estado | Notas |
|---|-------|-----------|--------|-------|
| 4.2.1 | Revisión de enlaces rotos | Trimestral | ⏳ | Links a docs oficiales de Anthropic/OpenAI/Google |
| 4.2.2 | Actualización por cambios en Claude Code | Event-driven | ⏳ | Cuando Anthropic cambia spec de subagents/skills |
| 4.2.3 | Auditoría de dependencias | Semestral | ⏳ | MCP SDKs, GitHub Actions versions |
| 4.2.4 | Purga de plantillas obsoletas | Anual | ⏳ | Marcar deprecadas, migrar a nuevas |

### 4.3 Roadmap v2

| # | Idea | Contexto |
|---|------|----------|
| 4.3.1 | Web UI para generar plantillas | Formulario → descarga ZIP personalizado |
| 4.3.2 | Marketplace de plantillas comunidad | PR → review → merge → publicación |
| 4.3.3 | Integración con `claude init` nativo | Que Anthropic reconozca estas plantillas |
| 4.3.4 | Soporte multi-idioma | Plantillas en EN/ES/FR/DE |
| 4.3.5 | Playground interactivo | Probar un agente antes de instalarlo |

---

## Contexto de desarrollo

### Stack tecnológico

| Capa | Tecnología |
|---|---|
| Lenguaje validadores | Python 3.12+ |
| CI/CD | GitHub Actions |
| Formato configs | YAML, JSON |
| Documentación | Markdown |
| Testing | pytest |
| Linting | prettier, yamlfmt, jsonlint |

### Entornos

| Entorno | Ubicación | Propósito |
|---|---|---|
| Desarrollo | `~/.claude/plantillas/` | Edición y prueba de plantillas |
| Staging | `/tmp/plantillas-test/` | Smoke tests de validadores |
| Producción | Repo Git público | Distribución y versionado |
| Local usuario | `~/.claude/` o `./.claude/` | Uso real de plantillas generadas |

### Flujo de trabajo git recomendado

```
main (protegida)
  ↑
  PR: feature/fase-2-validadores
    ← rama: feature/2.1.1-motor-validacion
    ← rama: feature/2.3.2-comandos-extra
  ↑
  PR: hotfix/links-rotos-2026-Q2
```

### Convenciones de commits

```
feat(agentes): añade validador de subagentes
fix(skills): corrige regex de placeholders
docs(hooks): actualiza referencias a docs oficiales
ci(global): añade composite action reusable
test(mcp): añade tests de integración
```

---

## Dependencias externas

| Dependencia | Versión | Usada en | Estado |
|---|---|---|---|
| Python | 3.12+ | Validadores | ✅ Requerida |
| pyyaml | latest | Validadores | ✅ Opcional (fallback a json) |
| pytest | latest | Tests | ⏳ Fase 3 |
| prettier | latest | Formateo | ⏳ Fase 3 |
| GitHub Actions | ubuntu-latest | CI/CD | ✅ Activa |

---

## Riesgos y mitigaciones

| Riesgo | Probabilidad | Impacto | Mitigación |
|---|---|---|---|
| Anthropic cambia spec de subagents | Media | Alto | Monitor changelog semanal, versión por módulo |
| Validador produce falsos positivos | Media | Medio | Tests con fixtures conocidos, modo `--strict` opcional |
| Plantillas quedan obsoletas | Alta | Medio | Roadmap de revisión trimestral, comunidad |
| Complejidad abruma a nuevos usuarios | Media | Alto | INDEX.md claro, ejemplos funcionales, TL;DR en cada módulo |

---

## Métricas de éxito

| Métrica | Meta Fase 2 | Meta Fase 3 | Medición |
|---|---|---|---|
| Módulos con validador | 8/8 | 8/8 | `ls */validar_*.py` |
| Módulos con CI/CD | 8/8 | 8/8 | `ls */.github/workflows/` |
| Ejemplos por módulo | 1 | ≥2 | Conteo manual |
| Tiempo `claude init` | — | <30s | `time ./install.sh` |
| Tests passing | — | 100% | `pytest --tb=short` |
| Documentación completa | 80% | 100% | Auditoría por checklist |

---

> **Próximo paso inmediato**: Fase 4 — Producción: monitoreo (badges CI,
> dashboard de calidad), mantenimiento continuo (revisión de links, actualización
> por cambios en Claude Code), y roadmap v2 (web UI, marketplace, multi-idioma).
