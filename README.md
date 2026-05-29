# Sistema de Plantillas Modulares para Claude Code

> **Ecosistema de plantillas `claude-init`-ready** para construir agentes, skills,
> comandos, hooks, plugins, MCP servers, repositorios GitHub profesionales, y
> configuraciones `.claude/` completas — con validación automática y CI/CD.

[![Validación](https://img.shields.io/badge/validación-14/14%20✅-green)](./)
[![Versión](https://img.shields.io/badge/versión-v1.0.0-blue)](./CHANGELOG.md)
[![Licencia](https://img.shields.io/badge/licencia-MIT-yellow)](./LICENSE)

---

## ¿Qué es esto?

Un sistema de **plantillas modulares** que te permite inicializar, validar y
mantener componentes de [Claude Code](https://code.claude.com/docs) en segundos.

Cada módulo sigue el mismo patrón:
- **`plantilla_X/`** = playbook instructivo (¿qué pongo aquí?)
- **`ejemplo_X/`** = referencia funcional (¿cómo se ve terminado?)
- **`validar_X.py`** = validador automático con `--strict`
- **`.github/workflows/`** = CI/CD independiente

---

## Módulos disponibles

| Módulo | Descripción | Inicializar |
|---|---|---|
| 🤖 **Agentes** | Orquestador hub-and-spoke con subagentes | `claude-init --modulo agentes` |
| 🛠️ **Skills** | Skills auto-activables por descripción | `claude-init --modulo skills` |
| ⌨️ **Commands** | Comandos slash (`/deploy`, `/test`) | `claude-init --modulo commands` |
| ⚓ **Hooks** | Interceptores pre/post tool, save, error | `claude-init --modulo hooks` |
| 🔌 **Plugins** | Empaquetado distribuible de componentes | `claude-init --modulo plugins` |
| 🔗 **MCP Servers** | Servidores MCP con tools y recursos | `claude-init --modulo mcp` |
| 📦 **dot-claude** | Configuración `.claude/` completa | `cp -r dot-claude/ejemplo_dot_claude ./.claude` |
| 🏛️ **Repositorios** | Repo GitHub profesional al 120% | `claude-init --repositorio` |
| 🧩 **Modulo** | Meta-plantilla para crear nuevos módulos | `claude-init --modulo modulo` |
| 🚀 **Proyecto** | Configuración `.claude/` para proyectos | `claude-init --proyecto` |
| 📱 **Miniapps** | SPA single-file tipo Claude artifact | `claude-init --modulo miniapps` |
| 🔬 **Autoresearch** | Cuadernos de investigación automatizada | `claude-init --modulo autoresearch` |
| 📓 **Cuadernos** | Notas estructuradas del operador | `claude-init --modulo cuadernos` |
| 📚 **Knowledge** | Artículos KB referenciables | `claude-init --modulo knowledge` |

> **Índice completo con estructura visual → [`INDEX.md`](./INDEX.md)**

---

## Instalación

```bash
curl -fsSL https://raw.githubusercontent.com/alexendros/plantillas/main/install.sh | bash
```

O manualmente:

```bash
git clone https://github.com/alexendros/plantillas.git ~/.claude/plantillas
cd ~/.claude/plantillas
```

---

## Uso rápido

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

---

## Validación y CI/CD

- **Motor reusable** en [`validadores/`](./validadores/): `BaseValidator`, checks reutilizables, reporte formateado.
- **14 validadores** individuales, todos pasan `--strict`.
- **14 workflows** de GitHub Actions + workflow central [`validar-todos.yml`](./.github/workflows/validar-todos.yml).
- **Pre-commit hooks** en [`.pre-commit-config.yaml`](./.pre-commit-config.yaml): lint YAML/JSON, detectar placeholders, validar módulos.

---

## Documentación clave

| Documento | Para qué sirve |
|---|---|
| [`INDEX.md`](./INDEX.md) | Índice maestro completo con estructura visual |
| [`ROADMAP.md`](./ROADMAP.md) | Plan de desarrollo (4 fases) |
| [`CHANGELOG.md`](./CHANGELOG.md) | Historia de versiones |
| [`CONTRIBUTING.md`](./CONTRIBUTING.md) | Cómo añadir nuevos módulos |
| [`INTEGRACION.md`](./INTEGRACION.md) | Cómo combinar módulos entre sí |
| [`CODE_OF_CONDUCT.md`](./CODE_OF_CONDUCT.md) | Código de conducta |

---

## Stack

- **Python 3.12+** — Validadores y motor reusable
- **GitHub Actions** — CI/CD
- **pre-commit** — Hooks de calidad
- **pytest** — Tests unitarios y smoke

---

## Licencia

[MIT](./LICENSE) © 2026 Alejandro · Iniciativas Alexendros
