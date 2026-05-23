# REPOSITORIO.md · Playbook de construcción

> **Propósito**: Este playbook describe cómo estructurar un repositorio GitHub
> profesional, empresarial y operativo al 120%. Sigue los estándares de
> community health de GitHub, Conventional Commits, GitHub Flow, y MADR.
>
> **Qué hacer**: Lee cada sección, copia los archivos indicados, rellena los
> placeholders `[ASÍ]` y elimina estas instrucciones.

---

## ¿Por dónde empezar?

```
1. Lee ESTE archivo (REPOSITORIO.md) — entiende el sistema.
2. Lee ESTRUCTURA.md — conoce el mapa de archivos.
3. Lee METODOLOGIA.md — entiende el flujo de trabajo.
4. Lee LLM_GUIDE.md — si usas LLMs/agentes, configúralos con esto.
5. Aplica los archivos comunes → comun/ (README, LICENSE, CHANGELOG, etc.).
6. Aplica el perfil de tu stack → [web-nextjs|mcp-server|library-design-system|...]/
7. Ejecuta validar_repositorio.py --strict
```

---

## Pilares del repositorio al 120%

| Pilar | Qué garantiza | Archivos clave |
|---|---|---|
| **Descubrimiento** | Cualquiera entiende qué hace el proyecto en 30 segundos | `README.md`, `ROADMAP.md` |
| **Confianza** | El proyecto parece mantenido y profesional | `LICENSE`, `CHANGELOG`, `CODE_OF_CONDUCT` |
| **Seguridad** | Vulnerabilidades se reportan y patchan correctamente | `SECURITY.md`, `.github/dependabot.yml` |
| **Colaboración** | Contribuidores saben cómo y qué esperar | `CONTRIBUTING.md`, `CODEOWNERS`, PR template |
| **Gobernanza** | Decisiones arquitectónicas son trazables | `docs/adr/` (MADR) |
| **Automatización** | CI/CD, linting, y formatado son automáticos | `.github/workflows/ci.yml`, `.editorconfig` |
| **Contexto LLM** | Un agente/LLM puede operar sin preguntar | `LLM_GUIDE.md`, comentarios estructurados |

---

## Instrucciones por archivo

### README.md
- Badge de CI arriba del todo.
- Secciones obligatorias: Qué es, Stack, Instala, Comandos, Despliegue, Estructura, Documentación, Licencia, Contacto.
- Máximo 2 minutos de lectura. Lo demás va a docs/.

### LICENSE / COPYRIGHT.md
- Open source: `LICENSE` en raíz (GitHub lo detecta).
- Privado: `COPYRIGHT.md` en raíz.

### CHANGELOG.md
- Formato Keep a Changelog.
- Secciones: `[Unreleased]`, versiones semver.
- Cada versión lista: Added, Changed, Deprecated, Removed, Fixed, Security.

### CONTRIBUTING.md
- Entorno de desarrollo (pasos para levantar).
- Conventional Commits obligatorios.
- Flujo de ramas: `<tipo>/<scope>-<descripción-corta>`.
- Commits firmados (SSH/GPG).
- PRs con squash merge.

### SECURITY.md
- Cómo reportar (email cifrado o GitHub Security Advisories).
- Versiones soportadas (tabla).
- Política de embargo.

### CODE_OF_CONDUCT.md
- Estándar Contributor Covenant 2.1.
- Cómo reportar violaciones.

### .github/CODEOWNERS
- Cada directorio/archivo tiene owner.
- Usa equipos (@org/equipo) más que individuales.
- Requiere review de CODEOWNER para cambios críticos.

### .github/PULL_REQUEST_TEMPLATE.md
- Qué, Por qué, Cómo probar, Checklist.
- Link a issue relacionado (`Closes #N`).

### .github/ISSUE_TEMPLATE/
- `bug.yml` — formulario estructurado.
- `feature.yml` — propuesta de feature.
- `question.yml` — dudas de uso.
- `security.yml` — reporte de vulnerabilidad.
- `config.yml` — links externos (docs, Discord, etc.).

### docs/adr/0001-usar-madr-para-adrs.md
- Primera ADR: "Usamos MADR 4.0.0 para decisiones arquitectónicas".
- Plantilla en `docs/adr/`. Cada ADR numerada secuencialmente.

---

## Checklist de validación

- [ ] `README.md` con badge de CI y secciones obligatorias
- [ ] `LICENSE` o `COPYRIGHT.md` presente
- [ ] `CHANGELOG.md` con formato Keep a Changelog
- [ ] `CONTRIBUTING.md` con Conventional Commits y flujo de ramas
- [ ] `SECURITY.md` con email de reporte
- [ ] `CODE_OF_CONDUCT.md` (Contributor Covenant)
- [ ] `.github/CODEOWNERS` con owners por área
- [ ] `.github/PULL_REQUEST_TEMPLATE.md`
- [ ] `.github/ISSUE_TEMPLATE/` (bug, feature, question, security, config)
- [ ] `.github/dependabot.yml` habilitado
- [ ] `.github/workflows/ci.yml` con test + lint + typecheck
- [ ] `docs/adr/0001-template.md` (MADR)
- [ ] `.editorconfig` y `.gitattributes`
- [ ] `validar_repositorio.py --strict` pasa

---

## Referencias

- **GitHub: Community Health Files**: https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file
- **Keep a Changelog**: https://keepachangelog.com/
- **Conventional Commits**: https://www.conventionalcommits.org/
- **MADR**: https://adr.github.io/madr/
- **Contributor Covenant**: https://www.contributor-covenant.org/
- **Semantic Versioning**: https://semver.org/
