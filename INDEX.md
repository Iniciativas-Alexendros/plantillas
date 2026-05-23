# ÍNDICE MAESTRO · Sistema de Plantillas Modulares para Claude Code

> **Punto de entrada universal** para el ecosistema de plantillas.
> Selecciona el módulo que necesitas y accede directamente.

---

## Módulos disponibles

### 🤖 Agentes
> Construye agentes especializados con patrón orquestador-especialistas.

| | Directorio | Para qué sirve |
|---|---|---|
| 📋 Playbook | [`agentes/plantilla_agente/`](./agentes/plantilla_agente/) | Kit de construcción instructivo (13 pasos) |
| ✅ Ejemplo | [`agentes/ejemplo_agente/`](./agentes/ejemplo_agente/) | Agente hub-and-spoke funcional de referencia |

**TL;DR**: `cp -r agentes/plantilla_agente ~/.claude/agents/mi-agente`

---

### 🛠️ Skills
> Crea skills reutilizables que Claude invoca automáticamente.

| | Directorio | Para qué sirve |
|---|---|---|
| 📋 Playbook | [`skills/plantilla_skill/`](./skills/plantilla_skill/) | Estructura SKILL.md + progressive disclosure |
| ✅ Ejemplo | [`skills/ejemplo_skill/`](./skills/ejemplo_skill/) | Skill operativa de diagramas Mermaid |

**TL;DR**: `cp -r skills/plantilla_skill ~/.claude/skills/mi-skill`

---

### ⌨️ Commands
> Define comandos slash personalizados (`/mi-comando`).

| | Directorio | Para qué sirve |
|---|---|---|
| 📋 Playbook | [`commands/plantilla_command/`](./commands/plantilla_command/) | Estructura de comando slash |
| ✅ Ejemplo | [`commands/ejemplo_command/`](./commands/ejemplo_command/) | Comando `/deploy` funcional |

**TL;DR**: `cp -r commands/plantilla_command ~/.claude/commands/mi-comando.md`

---

### ⚓ Hooks
> Intercepta y controla el comportamiento del agente en puntos clave.

| | Directorio | Para qué sirve |
|---|---|---|
| 📋 Playbook | [`hooks/plantilla_hook/`](./hooks/plantilla_hook/) | Eventos PreToolUse, PostToolUse, etc. |
| ✅ Ejemplo | [`hooks/ejemplo_hook/`](./hooks/ejemplo_hook/) | Hook de auditoría + backup + rate limiting |

**TL;DR**: `cp -r hooks/plantilla_hook ~/.claude/hooks/mi-hook.yaml`

---

### 🔌 Plugins
> Empaqueta agentes, skills, hooks y MCP en unidades distribuibles.

| | Directorio | Para qué sirve |
|---|---|---|
| 📋 Playbook | [`plugins/plantilla_plugin/`](./plugins/plantilla_plugin/) | Estructura de plugin + marketplace |
| ✅ Ejemplo | [`plugins/ejemplo_plugin/`](./plugins/ejemplo_plugin/) | Plugin de integración GitHub funcional |

**TL;DR**: `cp -r plugins/plantilla_plugin ~/.claude/plugins/mi-plugin`

---

### 🔗 MCP Servers
> Construye servidores MCP para exponer tools y recursos externos.

| | Directorio | Para qué sirve |
|---|---|---|
| 📋 Playbook | [`mcp/plantilla_mcp/`](./mcp/plantilla_mcp/) | Estructura de servidor MCP (Python/TS) |
| ✅ Ejemplo | [`mcp/ejemplo_mcp/`](./mcp/ejemplo_mcp/) | MCP server de filesystem funcional |

**TL;DR**: `cp -r mcp/plantilla_mcp ~/mis-mcp-servers/mi-server`

---

### 📦 Meta: dot-claude completo
> Inicializa un directorio `.claude` completo (proyecto o home).

| | Directorio | Para qué sirve |
|---|---|---|
| 📋 Playbook | [`dot-claude/plantilla_dot_claude/`](./dot-claude/plantilla_dot_claude/) | Estructura completa `.claude/` con todos los módulos |
| ✅ Ejemplo | [`dot-claude/ejemplo_dot_claude/`](./dot-claude/ejemplo_dot_claude/) | `.claude/` funcional con contenido real |

**TL;DR**: `cp -r dot-claude/ejemplo_dot_claude ./.claude`

---

### 🏛️ Repositorios
> Estructura profesional y empresarial para repositorios GitHub al 120%.

| | Directorio | Para qué sirve |
|---|---|---|
| 📋 Playbook | [`repositorios/plantilla_repositorio/`](./repositorios/plantilla_repositorio/) | Guía de construcción: metodología, estructura, flujo git |
| ✅ Ejemplo | [`repositorios/ejemplo_repositorio/`](./repositorios/ejemplo_repositorio/) | Repo completo con community health files, CI/CD, ADRs |

**TL;DR**: `cp -r repositorios/ejemplo_repositorio ./mi-nuevo-repo`

**Metodología**: [`METODOLOGIA.md`](./repositorios/plantilla_repositorio/METODOLOGIA.md) · **Guía LLM**: [`LLM_GUIDE.md`](./repositorios/plantilla_repositorio/LLM_GUIDE.md) · **Integración**: [`INTEGRACION.md`](./INTEGRACION.md)

---

## Scripts de bootstrap

| Script | Para qué sirve | Uso rápido |
|---|---|---|
| [`install.sh`](./install.sh) | Instala el sistema de plantillas en `~/.claude/plantillas/` | `curl -fsSL .../install.sh \| bash` |
| [`claude-init`](./claude-init) | Inicializa módulos, proyectos o repositorios | `claude-init --modulo agentes --nombre mi-agente` |
| [`update.sh`](./update.sh) | Actualiza el sistema a la última versión | `./update.sh` |

---

## Integración entre módulos

¿No sabes cómo combinar agentes + skills + hooks + MCP?
→ Lee [`INTEGRACION.md`](./INTEGRACION.md) — mapa de relaciones, decision tree, y ejemplo completo de proyecto backend.

---

## ¿Qué necesitas hoy?

| Si quieres... | Ve a... | Comando rápido |
|---|---|---|
| Crear un agente nuevo | `agentes/plantilla_agente/` | `claude-init --modulo agentes --nombre X` |
| Crear una skill nueva | `skills/plantilla_skill/` | `claude-init --modulo skills --nombre X` |
| Crear un comando slash | `commands/plantilla_command/` | `claude-init --modulo commands --nombre X` |
| Crear un hook | `hooks/plantilla_hook/` | `claude-init --modulo hooks --nombre X` |
| Crear un plugin | `plugins/plantilla_plugin/` | `claude-init --modulo plugins --nombre X` |
| Crear un MCP server | `mcp/plantilla_mcp/` | `claude-init --modulo mcp --nombre X` |
| Inicializar `.claude/` completo | `dot-claude/ejemplo_dot_claude/` | `cp -r dot-claude/ejemplo_dot_claude ./.claude` |
| Crear un repo GitHub profesional | `repositorios/ejemplo_repositorio/` | `claude-init --repositorio --nombre mi-repo` |
| Inicializar `.claude/` en proyecto | `proyecto/` | `claude-init --proyecto` |
| Crear un nuevo módulo | `modulo/` | `cp -r modulo mi-modulo` |

---

## Validación y CI/CD

Cada módulo tiene su propio validador y workflow de CI/CD. Todos usan el **motor de validación reusable** [`validadores/`](./validadores/).

| Módulo | Validador | Workflow CI/CD |
|---|---|---|
| 🤖 Agentes | [`validar_agente.py`](./agentes/validar_agente.py) | [`validar-agentes.yml`](./agentes/.github/workflows/validar-agentes.yml) |
| 🛠️ Skills | [`validar_skill.py`](./skills/validar_skill.py) | [`validar-skills.yml`](./skills/.github/workflows/validar-skills.yml) |
| ⌨️ Commands | [`validar_command.py`](./commands/validar_command.py) | [`validar-commands.yml`](./commands/.github/workflows/validar-commands.yml) |
| ⚓ Hooks | [`validar_hook.py`](./hooks/validar_hook.py) | [`validar-hooks.yml`](./hooks/.github/workflows/validar-hooks.yml) |
| 🔌 Plugins | [`validar_plugin.py`](./plugins/validar_plugin.py) | [`validar-plugins.yml`](./plugins/.github/workflows/validar-plugins.yml) |
| 🔗 MCP | [`validar_mcp.py`](./mcp/validar_mcp.py) | [`validar-mcp.yml`](./mcp/.github/workflows/validar-mcp.yml) |
| 📦 dot-claude | [`validar_dot_claude.py`](./dot-claude/validar_dot_claude.py) | [`validar-dot-claude.yml`](./dot-claude/.github/workflows/validar-dot-claude.yml) |
| 🏛️ Repositorios | [`validar_repositorio.py`](./repositorios/validar_repositorio.py) | [`validar-repositorios.yml`](./repositorios/.github/workflows/validar-repositorios.yml) |
| 🧩 Módulo (template) | [`validar_modulo.py`](./modulo/validar_modulo.py) | [`validar-modulo.yml`](./modulo/.github/workflows/validar-modulo.yml) |
| 📁 Proyecto (template) | [`validar_proyecto.py`](./proyecto/validar_proyecto.py) | [`validar-proyecto.yml`](./proyecto/.github/workflows/validar-proyecto.yml) |

**Workflow central** (todos los módulos): [`validar-todos.yml`](./.github/workflows/validar-todos.yml)

### CI/CD Global (protección del repositorio)

| Workflow | Propósito | Archivo |
|---|---|---|
| 🌍 CI Global | Lint YAML/JSON/Markdown/Python/Shell + validación de estructura | [`ci-global.yml`](./.github/workflows/ci-global.yml) |
| 🛡️ PR Guardian | Título Conventional Commit, tamaño, archivos protegidos, CHANGELOG | [`pr-guardian.yml`](./.github/workflows/pr-guardian.yml) |
| 🔒 Security Scan | Detección de secrets, tokens, archivos prohibidos | [`security-scan.yml`](./.github/workflows/security-scan.yml) |
| 🔍 Validador Repo | Motor Python que valida estructura canónica completa | [`validar_repo.py`](./validar_repo.py) |

```bash
# Validar cualquier módulo
python agentes/validar_agente.py ~/.claude/agents/mi-agente --strict
python skills/validar_skill.py ~/.claude/skills/mi-skill --strict
python commands/validar_command.py ~/.claude/commands/mi-cmd --strict
python hooks/validar_hook.py ~/.claude/hooks/mi-hook --strict
python plugins/validar_plugin.py ~/.claude/plugins/mi-plugin --strict
python mcp/validar_mcp.py ~/mis-mcp-servers/mi-server --strict
python dot-claude/validar_dot_claude.py ./.claude --strict

# Validar estructura completa del repositorio
python validar_repo.py --strict
```

---

## Estructura visual del sistema

```
plantillas/
├── INDEX.md                          ← ESTE ARCHIVO
├── ROADMAP.md                        ← Plan de desarrollo
├── CHANGELOG.md                      ← Historia de versiones
├── CONTRIBUTING.md                   ← Guía para contribuidores
├── CODE_OF_CONDUCT.md                ← Código de conducta
├── INTEGRACION.md                    ← Integración cruzada entre módulos
├── install.sh                        ← Instalador del sistema
├── claude-init                       ← Inicializador de módulos/proyectos/repos
├── update.sh                         ← Actualizador de versiones
├── .pre-commit-config.yaml           ← Hooks de pre-commit (lint, validación)
├── tests/                            ← Tests pytest + smoke
│   ├── test_validadores.py
│   └── test_smoke.py
├── validadores/                      ← Motor de validación reusable
│   ├── __init__.py
│   ├── base.py                       ← BaseValidator, Check, Resultado, Nivel
│   ├── checks.py                     ← Checks reutilizables
│   └── reporte.py                    ← Formateo de salida
├── modulo/                           ← Template para crear nuevos módulos
├── proyecto/                         ← Template .claude/ ligera para proyectos
├── .github/workflows/
│   └── validar-todos.yml             ← CI/CD central (todos los módulos)
│
├── agentes/
│   ├── plantilla_agente/             ← 🤖 Kit de construcción
│   └── ejemplo_agente/               ← 🤖 Referencia viva
│
├── skills/
│   ├── plantilla_skill/              ← 🛠️ Kit de construcción
│   └── ejemplo_skill/                ← 🛠️ Referencia viva
│
├── commands/
│   ├── plantilla_command/            ← ⌨️ Kit de construcción
│   └── ejemplo_command/              ← ⌨️ Referencia viva
│
├── hooks/
│   ├── plantilla_hook/               ← ⚓ Kit de construcción
│   └── ejemplo_hook/                 ← ⚓ Referencia viva
│
├── plugins/
│   ├── plantilla_plugin/             ← 🔌 Kit de construcción
│   └── ejemplo_plugin/               ← 🔌 Referencia viva
│
├── mcp/
│   ├── plantilla_mcp/                ← 🔗 Kit de construcción
│   └── ejemplo_mcp/                  ← 🔗 Referencia viva
│
├── dot-claude/
│   ├── plantilla_dot_claude/         ← 📦 Meta-módulo
│   └── ejemplo_dot_claude/           ← 📦 Referencia viva
│
└── repositorios/
    ├── plantilla_repositorio/        ← 🏛️ Playbook de construcción
    │   ├── REPOSITORIO.md
    │   ├── METODOLOGIA.md
    │   ├── LLM_GUIDE.md
    │   └── ESTRUCTURA.md
    ├── ejemplo_repositorio/          ← 🏛️ Referencia viva
    │   ├── README.md, LICENSE, CHANGELOG, ...
    │   ├── .github/workflows/ci.yml
    │   ├── .github/ISSUE_TEMPLATE/
    │   └── docs/adr/
    ├── aplica-canon-repo.sh          ← Script de aplicación
    ├── auditoria-canon-repo.sh       ← Script de auditoría
    ├── repos.yaml                    ← Fuente de verdad
    └── [perfiles por stack]/         ← web-nextjs, mcp-server, ...
```

---

> **Regla de oro**: Cada módulo sigue el mismo patrón:
> `plantilla_X/` = playbook instructivo (¿qué pongo aquí?)
> `ejemplo_X/` = referencia funcional (¿cómo se ve terminado?)
