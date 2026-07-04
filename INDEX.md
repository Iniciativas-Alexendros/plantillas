# ÍNDICE MAESTRO · Sistema de Plantillas Modulares para Agentes de Código

> **Punto de entrada universal** para el ecosistema de plantillas.
> Selecciona el módulo que necesitas y accede directamente.
>
> 📢 **2026-06-30 · Cross-platform Config Refactor (BREAKING)** — se eliminan
> `autoresearch/`, `cuadernos/`, `knowledge/` y `dot-claude/`; se añade
> `agent-config/` como fuente canónica cross-platform para Claude Code,
> OpenCode, Devin y Windsurf/Cascade. Detalle en `CHANGELOG.md`.
>
> 🧱 **Bloque 2 en curso**: reestructura del repo como paquete Python con CLI
> `plantillas` y catálogo `modules.yaml`. Ver [`ROADMAP.md`](./ROADMAP.md) y el
> dossier visual regenerable [`docs/dossier-bloque2.html`](./docs/dossier-bloque2.html)
> (single-file, 5 tabs, generado por `plantillas generate dossier`,
> CI lo regenera en cada push a `main`).

---

## Módulos canónicos (12)

> Lista actualizada a los 12 módulos canónicos. En el Bloque 2 todos están
> registrados en `modules.yaml` y se validan con `plantillas validate --all`.

### Single-file `.md` con frontmatter runtime

#### 🤖 Agentes

> Construye agentes especializados con patrón orquestador-especialistas.

|              | Archivo                                                        | Para qué sirve                                                           |
| ------------ | -------------------------------------------------------------- | ------------------------------------------------------------------------ |
| 📋 Plantilla | [`agentes/plantilla_agente.md`](./agentes/plantilla_agente.md) | Single-file con `name`/`description`/`tools`/`model` + 7 secciones canon |
| ✅ Ejemplo   | [`agentes/ejemplo_agente.md`](./agentes/ejemplo_agente.md)     | Orquestador hub-and-spoke funcional (`dev-arquitectura`)                 |

**TL;DR**: `cp agentes/plantilla_agente.md ~/.claude/agents/mi-agente.md`

---

#### ⌨️ Commands

> Define comandos slash personalizados (`/mi-comando`).

|              | Archivo                                                            | Para qué sirve                                                                |
| ------------ | ------------------------------------------------------------------ | ----------------------------------------------------------------------------- |
| 📋 Plantilla | [`commands/plantilla_command.md`](./commands/plantilla_command.md) | Frontmatter `description`/`argument-hint`/`allowed-tools` + 6 secciones canon |
| ✅ Ejemplo   | [`commands/ejemplo_command.md`](./commands/ejemplo_command.md)     | `/test-cobertura` multi-runner (Jest/Vitest/pytest)                           |

**TL;DR**: `cp commands/plantilla_command.md ~/.claude/commands/mi-comando.md`

---

#### 🖥️ Miniapps · canon nuevo

> SPA single-file tipo Claude.ai artifact (categorías: dashboard/explorer/tool/playbook).

|              | Archivo                                                              | Para qué sirve                                                        |
| ------------ | -------------------------------------------------------------------- | --------------------------------------------------------------------- |
| 📋 Plantilla | [`miniapps/plantilla_miniapps.md`](./miniapps/plantilla_miniapps.md) | Frontmatter `category`/`runtime`/`version` + estructura HTML reducida |
| ✅ Ejemplo   | [`miniapps/ejemplo_miniapps.md`](./miniapps/ejemplo_miniapps.md)     | `kpi-mensual` dashboard de KPIs financieros                           |

**TL;DR**: `cp miniapps/plantilla_miniapps.md ~/.claude/miniapps/<slug>/<slug>.md`

---

### Single-file `.sh.template`

#### ⚓ Hooks

> Intercepta y controla el comportamiento del agente en eventos del runtime.

|              | Archivo                                                                  | Para qué sirve                                                                     |
| ------------ | ------------------------------------------------------------------------ | ---------------------------------------------------------------------------------- |
| 📋 Plantilla | [`hooks/plantilla_hook.sh.template`](./hooks/plantilla_hook.sh.template) | Cabecera declarativa `# matcher`/`# tool_pattern` + body JSON `{decision, reason}` |
| ✅ Ejemplo   | [`hooks/ejemplo_hook.sh.template`](./hooks/ejemplo_hook.sh.template)     | `pre-bash-secret-guard` (escanea GH/OpenAI/AWS tokens)                             |
| 📄 Doc       | [`hooks/HOOK.md`](./hooks/HOOK.md)                                       | Eventos soportados + cómo instalar y probar                                        |

**TL;DR**: `cp hooks/plantilla_hook.sh.template ~/.claude/hooks/mi-hook.sh && chmod +x ~/.claude/hooks/mi-hook.sh`

---

### Dir canon multi-archivo

#### 🛠️ Skills

> Crea skills reutilizables que Claude invoca automáticamente.

|              | Directorio                                             | Para qué sirve                                 |
| ------------ | ------------------------------------------------------ | ---------------------------------------------- |
| 📋 Plantilla | [`skills/plantilla_skill/`](./skills/plantilla_skill/) | Estructura `SKILL.md` + progressive disclosure |
| ✅ Ejemplo   | [`skills/ejemplo_skill/`](./skills/ejemplo_skill/)     | Skill operativa de diagramas Mermaid           |

**TL;DR**: `cp -r skills/plantilla_skill ~/.claude/skills/mi-skill`

---

#### 🔌 Plugins

> Empaqueta agentes, skills, hooks y MCP en unidades distribuibles.

|              | Directorio                                                 | Para qué sirve                         |
| ------------ | ---------------------------------------------------------- | -------------------------------------- |
| 📋 Plantilla | [`plugins/plantilla_plugin/`](./plugins/plantilla_plugin/) | Estructura de plugin + marketplace     |
| ✅ Ejemplo   | [`plugins/ejemplo_plugin/`](./plugins/ejemplo_plugin/)     | Plugin de integración GitHub funcional |

**TL;DR**: `cp -r plugins/plantilla_plugin ~/.claude/plugins/mi-plugin`

---

#### 🔗 MCP Servers

> Construye servidores MCP para exponer tools y recursos externos.

|              | Directorio                                   | Para qué sirve                         |
| ------------ | -------------------------------------------- | -------------------------------------- |
| 📋 Plantilla | [`mcp/plantilla_mcp/`](./mcp/plantilla_mcp/) | Estructura de servidor MCP (Python/TS) |
| ✅ Ejemplo   | [`mcp/ejemplo_mcp/`](./mcp/ejemplo_mcp/)     | MCP server de filesystem funcional     |

**TL;DR**: `cp -r mcp/plantilla_mcp ~/mis-mcp-servers/mi-server`

---

#### 🌐 agent-config

> Configuración cross-platform para Claude Code, OpenCode, Devin y Windsurf/Cascade.

|              | Archivo                                                                                  | Para qué sirve                                         |
| ------------ | ---------------------------------------------------------------------------------------- | ------------------------------------------------------ |
| 📋 Plantilla | [`agent-config/plantilla_agent_config.yaml`](./agent-config/plantilla_agent_config.yaml) | Fuente canónica YAML de reglas, skills, MCPs y modelos |
| ✅ Ejemplo   | [`agent-config/ejemplo_agent_config/`](./agent-config/ejemplo_agent_config/)             | Salidas generadas para las 4 plataformas               |

**TL;DR**: `python agent-config/generar_agent_configs.py --home ~ --backup`

---

#### 🏛️ Repositorios

> Estructura profesional y empresarial para repositorios GitHub.

|              | Directorio                                                                     | Para qué sirve                                        |
| ------------ | ------------------------------------------------------------------------------ | ----------------------------------------------------- |
| 📋 Plantilla | [`repositorios/plantilla_repositorio/`](./repositorios/plantilla_repositorio/) | Guía: metodología, estructura, flujo git              |
| ✅ Ejemplo   | [`repositorios/ejemplo_repositorio/`](./repositorios/ejemplo_repositorio/)     | Repo completo con community health files, CI/CD, ADRs |

**TL;DR**: `cp -r repositorios/ejemplo_repositorio ./mi-nuevo-repo`

---

#### 🧩 Módulo (meta-template)

> Template para crear nuevos módulos en este sistema de plantillas.

`modulo/` — raíz es la plantilla; usar `cp -r modulo mi-modulo`.

---

#### 📁 Proyecto (meta-template)

> Template `.claude/` ligero para inicializar un proyecto.

`proyecto/` — raíz es la plantilla; usar `claude-init --proyecto`.

---

#### 📐 Estándares (módulo canónico)

> Módulo canónico de estándares del portfolio: la metodología común (CLAUDE.md, frontmatter, versionado, pre-commit, .env.example, matriz CI) que el resto de repos adoptan.

`estandares/` — raíz es la plantilla; consultar `estandares/ESTANDARES.md` y homologar cada repo.

---

## Scripts de bootstrap

| Script                         | Para qué sirve                                | Uso rápido                                        |
| ------------------------------ | --------------------------------------------- | ------------------------------------------------- |
| [`install.sh`](./install.sh)   | Instala el sistema en `~/.claude/plantillas/` | `curl -fsSL .../install.sh \| bash`               |
| [`claude-init`](./claude-init) | Inicializa módulos, proyectos o repositorios  | `claude-init --modulo agentes --nombre mi-agente` |
| [`update.sh`](./update.sh)     | Actualiza el sistema a la última versión      | `./update.sh`                                     |

> **Contexto de mantenedor:** [`PROMPT_INICIO.md`](./PROMPT_INICIO.md) — prompt listo
> para pegar al abrir un hilo de Claude que vaya a trabajar sobre este repo (ubicación,
> reglas de oro, comandos rápidos y stack).

---

## Integración entre módulos

¿No sabes cómo combinar agentes + skills + hooks + MCP + miniapps + agent-config?
→ Lee [`INTEGRACION.md`](./INTEGRACION.md) — mapa de relaciones, decision tree, ejemplo completo.

---

## ¿Qué necesitas hoy?

| Si quieres...                      | Ve a...                                    | Comando rápido                                                   |
| ---------------------------------- | ------------------------------------------ | ---------------------------------------------------------------- |
| Crear un agente nuevo              | `agentes/plantilla_agente.md`              | `claude-init --modulo agentes --nombre X`                        |
| Crear una skill nueva              | `skills/plantilla_skill/`                  | `claude-init --modulo skills --nombre X`                         |
| Crear un comando slash             | `commands/plantilla_command.md`            | `claude-init --modulo commands --nombre X`                       |
| Crear un hook                      | `hooks/plantilla_hook.sh.template`         | `claude-init --modulo hooks --nombre X`                          |
| Crear un plugin                    | `plugins/plantilla_plugin/`                | `claude-init --modulo plugins --nombre X`                        |
| Crear un MCP server                | `mcp/plantilla_mcp/`                       | `claude-init --modulo mcp --nombre X`                            |
| Crear una mini-app                 | `miniapps/plantilla_miniapps.md`           | `claude-init --modulo miniapps --nombre X`                       |
| Sincronizar reglas cross-platform  | `agent-config/plantilla_agent_config.yaml` | `python agent-config/generar_agent_configs.py --home ~ --backup` |
| Crear un repo GitHub profesional   | `repositorios/ejemplo_repositorio/`        | `claude-init --repositorio --nombre mi-repo`                     |
| Inicializar `.claude/` en proyecto | `proyecto/`                                | `claude-init --proyecto`                                         |
| Crear un nuevo módulo              | `modulo/`                                  | `cp -r modulo mi-modulo`                                         |
| Homologar un repo a los estándares | `estandares/ESTANDARES.md`                 | `python estandares/validar_estandares.py estandares --strict`    |

---

## Validación y CI/CD

Cada módulo tiene su propio validador y workflow de CI/CD. Todos usan el **motor de validación reusable** [`validadores/`](./validadores/).

| Módulo                   | Validador                                                           | Workflow CI/CD per-módulo                                                               |
| ------------------------ | ------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| 🤖 Agentes               | [`validar_agente.py`](./agentes/validar_agente.py)                  | [`validar-agentes.yml`](./agentes/.github/workflows/validar-agentes.yml)                |
| 🛠️ Skills                | [`validar_skill.py`](./skills/validar_skill.py)                     | [`validar-skills.yml`](./skills/.github/workflows/validar-skills.yml)                   |
| ⌨️ Commands              | [`validar_command.py`](./commands/validar_command.py)               | [`validar-commands.yml`](./commands/.github/workflows/validar-commands.yml)             |
| ⚓ Hooks                 | [`validar_hook.py`](./hooks/validar_hook.py)                        | [`validar-hooks.yml`](./hooks/.github/workflows/validar-hooks.yml)                      |
| 🔌 Plugins               | [`validar_plugin.py`](./plugins/validar_plugin.py)                  | [`validar-plugins.yml`](./plugins/.github/workflows/validar-plugins.yml)                |
| 🔗 MCP                   | [`validar_mcp.py`](./mcp/validar_mcp.py)                            | [`validar-mcp.yml`](./mcp/.github/workflows/validar-mcp.yml)                            |
| 🌐 agent-config          | [`validar_agent_config.py`](./agent-config/validar_agent_config.py) | [`validar-agent-config.yml`](./agent-config/.github/workflows/validar-agent-config.yml) |
| 🏛️ Repositorios          | [`validar_repositorio.py`](./repositorios/validar_repositorio.py)   | [`validar-repositorios.yml`](./repositorios/.github/workflows/validar-repositorios.yml) |
| 🖥️ Miniapps              | [`validar_miniapps.py`](./miniapps/validar_miniapps.py)             | [`validar-miniapps.yml`](./miniapps/.github/workflows/validar-miniapps.yml)             |
| 🧩 Módulo (template)     | [`validar_modulo.py`](./modulo/validar_modulo.py)                   | [`validar-modulo.yml`](./modulo/.github/workflows/validar-modulo.yml)                   |
| 📁 Proyecto (template)   | [`validar_proyecto.py`](./proyecto/validar_proyecto.py)             | [`validar-proyecto.yml`](./proyecto/.github/workflows/validar-proyecto.yml)             |
| 📐 Estándares (canónico) | [`validar_estandares.py`](./estandares/validar_estandares.py)       | [`validar-todos.yml`](./.github/workflows/validar-todos.yml)                            |

**Workflow central** (todos los módulos en matriz declarativa): [`validar-todos.yml`](./.github/workflows/validar-todos.yml)

### CI/CD Global (protección del repositorio)

| Workflow          | Propósito                                                          | Archivo                                                      |
| ----------------- | ------------------------------------------------------------------ | ------------------------------------------------------------ |
| 🌍 CI Global      | Lint YAML/JSON/Markdown/Python/Shell + validación de estructura    | [`ci-global.yml`](./.github/workflows/ci-global.yml)         |
| 🛡️ PR Guardian    | Título Conventional Commit, tamaño, archivos protegidos, CHANGELOG | [`pr-guardian.yml`](./.github/workflows/pr-guardian.yml)     |
| 🔒 Security Scan  | Detección de secrets, tokens, archivos prohibidos                  | [`security-scan.yml`](./.github/workflows/security-scan.yml) |
| 🔍 Validador Repo | Motor Python que valida estructura canónica completa               | [`validar_repo.py`](./validar_repo.py)                       |

```bash
# Validar plantillas/ejemplos single-file
python agentes/validar_agente.py agentes/ejemplo_agente.md --strict
python commands/validar_command.py commands/ejemplo_command.md --strict
python miniapps/validar_miniapps.py miniapps/ejemplo_miniapps.md --strict
python hooks/validar_hook.py hooks/ejemplo_hook.sh.template --strict

# Validar dir canon
python skills/validar_skill.py ~/.claude/skills/mi-skill --strict
python plugins/validar_plugin.py ~/.claude/plugins/mi-plugin --strict
python mcp/validar_mcp.py ~/mis-mcp-servers/mi-server --strict
python agent-config/validar_agent_config.py agent-config --strict

# Validar estructura completa del repositorio (12 módulos canon)
python validar_repo.py --strict
```

---

## Estructura visual del sistema

```
plantillas/
├── INDEX.md                          ← ESTE ARCHIVO
├── ROADMAP.md
├── CHANGELOG.md                      ← entrada [Unreleased] = Cross-platform Config Refactor
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── INTEGRACION.md
├── install.sh · claude-init · update.sh
├── .pre-commit-config.yaml
├── validar_repo.py                   ← acepta file-or-dir + 12 módulos canon
├── tests/
│   ├── test_validadores.py
│   └── test_smoke.py
├── validadores/                      ← Motor de validación reusable
│   ├── base.py · checks.py · reporte.py · __init__.py
├── modulo/ · proyecto/               ← Meta-templates
├── .github/workflows/
│   ├── validar-todos.yml             ← Matriz declarativa de 12 módulos
│   ├── ci-global.yml · pr-guardian.yml · security-scan.yml
│
├── agentes/
│   ├── plantilla_agente.md           ← 🤖 Single-file canon
│   ├── ejemplo_agente.md
│   └── validar_agente.py
│
├── commands/
│   ├── plantilla_command.md          ← ⌨️ Single-file canon
│   ├── ejemplo_command.md
│   └── validar_command.py
│
├── hooks/
│   ├── plantilla_hook.sh.template    ← ⚓ Single-file canon
│   ├── ejemplo_hook.sh.template
│   ├── HOOK.md
│   └── validar_hook.py
│
├── miniapps/                         ← 🖥️ Canon nuevo
│   ├── plantilla_miniapps.md
│   ├── ejemplo_miniapps.md (kpi-mensual)
│   ├── validar_miniapps.py
│   └── README.md
│
├── agent-config/                     ← 🌐 Configuración cross-platform
│   ├── plantilla_agent_config.yaml
│   ├── generar_agent_configs.py
│   ├── validar_agent_config.py
│   ├── ejemplo_agent_config/
│   └── README.md
│
├── skills/
│   ├── plantilla_skill/              ← 🛠️ Dir canon
│   └── ejemplo_skill/
│
├── plugins/                          ← 🔌 Dir canon
├── mcp/                              ← 🔗 Dir canon
├── repositorios/                     ← 🏛️ Dir canon
└── artefactos/                       ← Plano (outputs operador, no canon)
```

---

> **Regla de oro post-reforma**: cada módulo sigue uno de tres formatos:
>
> - **Single-file `.md`**: `plantilla_X.md` + `ejemplo_X.md` (canon nuevo).
> - **Single-file `.sh.template`**: `plantilla_X.sh.template` + `ejemplo_X.sh.template` (hooks).
> - **Dir multi-archivo**: `plantilla_X/` + `ejemplo_X/` (skills, plugins, mcp, repositorios); `agent-config/` usa `plantilla_agent_config.yaml` + `ejemplo_agent_config/`.
>
> El validador global `validar_repo.py` reconoce los tres patrones vía glob por extensión.
