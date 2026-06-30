# Sistema de Plantillas Modulares para Agentes de Código

> **Ecosistema de plantillas** para inicializar, validar y mantener componentes de
> [Claude Code](https://code.claude.com/docs), OpenCode, Devin y Windsurf/Cascade:
> agentes, skills, comandos, hooks, plugins, MCP servers, repositorios GitHub
> profesionales y configuración cross-platform de agentes — con validación
> automática y CI/CD.
>
> **Estado:** en transición hacia el **Bloque 2**, que reestructura el repo como
> paquete Python con CLI unificado (`plantillas`), catálogo central (`modules.yaml`)
> y motor de validación por registry.

[![Validación](https://img.shields.io/badge/validación-12/12%20✅-green)](./)
[![Versión](https://img.shields.io/badge/versión-v1.0.0-blue)](./CHANGELOG.md)
[![Licencia](https://img.shields.io/badge/licencia-MIT-yellow)](./LICENSE)

---

## ¿Qué es esto?

Un sistema de **plantillas modulares** que permite inicializar, validar y
mantener componentes de agentes de código en segundos.

Cada módulo canónico sigue el mismo patrón:

- **`plantilla_X/`** o **`plantilla_X.md`** = playbook instructivo (¿qué pongo aquí?)
- **`ejemplo_X/`** o **`ejemplo_X.md`** = referencia funcional (¿cómo se ve terminado?)
- **`validar_X.py`** = validador automático con `--strict`
- **`.github/workflows/`** = CI/CD independiente

---

## Módulos canónicos (12)

| Módulo              | Tipo                       | Descripción                                             | Inicializar (actual)                                             | Inicializar (Bloque 2)                         |
| ------------------- | -------------------------- | ------------------------------------------------------- | ---------------------------------------------------------------- | ---------------------------------------------- |
| 🤖 **Agentes**      | single-file `.md`          | Orquestador hub-and-spoke con subagentes                | `claude-init --modulo agentes`                                   | `plantillas new agente --nombre mi-agente`     |
| 🛠️ **Skills**       | directorio                 | Skills auto-activables por descripción                  | `claude-init --modulo skills`                                    | `plantillas new skill --nombre mi-skill`       |
| ⌨️ **Commands**     | single-file `.md`          | Comandos slash (`/deploy`, `/test`)                     | `claude-init --modulo commands`                                  | `plantillas new command --nombre mi-command`   |
| ⚓ **Hooks**        | single-file `.sh.template` | Interceptores pre/post tool, save, error                | `claude-init --modulo hooks`                                     | `plantillas new hook --nombre mi-hook`         |
| 🔌 **Plugins**      | directorio                 | Empaquetado distribuible de componentes                 | `claude-init --modulo plugins`                                   | `plantillas new plugin --nombre mi-plugin`     |
| 🔗 **MCP Servers**  | directorio                 | Servidores MCP con tools y recursos                     | `claude-init --modulo mcp`                                       | `plantillas new mcp --nombre mi-mcp`           |
| 🖥️ **Miniapps**     | single-file `.md`          | SPA single-file tipo Claude.ai artifact                 | `claude-init --modulo miniapps`                                  | `plantillas new miniapp --nombre mi-miniapp`   |
| 🌐 **agent-config** | especial                   | Configuración cross-platform para agentes               | `python agent-config/generar_agent_configs.py --home ~ --backup` | `plantillas sync agent-config --backup`        |
| 🏛️ **Repositorios** | directorio                 | Repo GitHub profesional al 120%                         | `claude-init --repositorio`                                      | `plantillas new repositorio --nombre mi-repo`  |
| 🧩 **Módulo**       | especial                   | Meta-template para crear nuevos módulos                 | `cp -r modulo mi-modulo`                                         | `plantillas new modulo --nombre mi-modulo`     |
| 📁 **Proyecto**     | especial                   | Template `.claude/` ligero para inicializar un proyecto | `claude-init --proyecto`                                         | `plantillas new proyecto --nombre mi-proyecto` |
| 📐 **Estándares**   | directorio                 | Catálogo de estándares del portfolio                    | `python estandares/validar_estandares.py estandares --strict`    | `plantillas validate estandares --strict`      |

> **Índice maestro con estructura visual → [`INDEX.md`](./INDEX.md)**
> **Dossier interactivo del Bloque 2 → `docs/dossier-bloque2.html` (no sincronizado en GitHub)**

---

## Instalación

### Modo actual (scripts)

```bash
curl -fsSL https://raw.githubusercontent.com/alexendros/plantillas/main/install.sh | bash
```

O manualmente:

```bash
git clone https://github.com/alexendros/plantillas.git ~/.claude/plantillas
cd ~/.claude/plantillas
```

### Modo Bloque 2 (paquete Python)

```bash
uv pip install -e .
# o
pip install -e .
```

El CLI expone los subcomandos `validate`, `sync`, `new` y `config`.

---

## Uso rápido

### Modo actual (scripts)

```bash
# Listar módulos disponibles
claude-init --list

# Inicializar un agente
claude-init --modulo agentes --nombre mi-agente

# Inicializar un repo GitHub profesional
claude-init --repositorio --nombre mi-proyecto

# Inicializar .claude/ en un proyecto existente
claude-init --proyecto

# Validar cualquier módulo
python agentes/validar_agente.py ~/.claude/agents/mi-agente --strict
```

### Modo Bloque 2 (CLI)

```bash
# Listar módulos
plantillas config list

# Validar todo el repo
plantillas validate --all --strict

# Sincronizar agent-config desde la fuente canónica
plantillas sync agent-config --home ~ --backup

# Crear un nuevo módulo
plantillas new agente --nombre mi-agente
```

---

## Validación y CI/CD

- **Motor reusable** en [`validadores/`](./validadores/): `BaseValidator`, checks reutilizables, reporte formateado.
- **12 validadores** individuales, todos pasan `--strict`.
- **12 workflows** de GitHub Actions + workflow central [`validar-todos.yml`](./.github/workflows/validar-todos.yml).
- **Pre-commit hooks** en [`.pre-commit-config.yaml`](./.pre-commit-config.yaml): lint YAML/JSON, detectar placeholders, validar módulos.

### Bloque 2 (en progreso)

- Workflow `.github/workflows/validar-paquete.yml` ejecuta `ruff`, `pytest` y `plantillas validate`.
- El catálogo de módulos se centraliza en `modules.yaml` y lo leen CI, tests y la CLI.
- Los validadores se registran en `plantillas.registry` y pueden delegar en scripts legacy.

---

## Documentación clave

| Documento                                        | Para qué sirve                                                      |
| ------------------------------------------------ | ------------------------------------------------------------------- |
| [`INDEX.md`](./INDEX.md)                         | Índice maestro completo con estructura visual                       |
| [`ROADMAP.md`](./ROADMAP.md)                     | Plan de desarrollo, incluido el Bloque 2                            |
| [`CHANGELOG.md`](./CHANGELOG.md)                 | Historia de versiones                                               |
| [`CONTRIBUTING.md`](./CONTRIBUTING.md)           | Cómo añadir nuevos módulos y validadores                            |
| [`INTEGRACION.md`](./INTEGRACION.md)             | Cómo combinar módulos entre sí                                      |
| [`PROMPT_INICIO.md`](./PROMPT_INICIO.md)         | Prompt de contexto para abrir un hilo sobre este repo               |
| [`CODE_OF_CONDUCT.md`](./CODE_OF_CONDUCT.md)     | Código de conducta                                                  |
| [`docs/cli.md`](./docs/cli.md)                   | Comandos del CLI `plantillas` (Bloque 2)                            |
| [`docs/modules-yaml.md`](./docs/modules-yaml.md) | Esquema del catálogo `modules.yaml` (Bloque 2)                      |
| [`docs/validators.md`](./docs/validators.md)     | Guía del motor de validación (Bloque 2)                             |
| `docs/dossier-bloque2.html`                      | Dossier visual interactivo del Bloque 2 (no sincronizado en GitHub) |

---

## Stack

### Actual

- **Python 3.12+** — Validadores y motor reusable
- **GitHub Actions** — CI/CD
- **pre-commit** — Hooks de calidad
- **pytest** — Tests unitarios y smoke

### Bloque 2

- **Python 3.12+** + **uv** — Empaquetado y entorno
- **Pydantic v2** — Esquema de `agent-config`
- **Jinja2** — Templates de generación cross-platform
- **Typer** — CLI unificado `plantillas`
- **pytest + snapshots** — Tests unitarios y regresión
- **GitHub Actions** — CI centralizado con `plantillas validate`

## Transición al Bloque 2

El Bloque 2 convierte el repo en un paquete Python instalable (`pyproject.toml`)
con un CLI propio. Durante la transición se mantienen los scripts actuales como
wrappers delegados en `plantillas`. Ver [`ROADMAP.md`](./ROADMAP.md) y el
[dossier interactivo](docs/dossier-bloque2.html) para el detalle de fases.

---

## Licencia

[MIT](./LICENSE) © 2026 Alejandro · Iniciativas Alexendros
