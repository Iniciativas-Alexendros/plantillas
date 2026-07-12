# Sistema de Plantillas Modulares para Agentes de Código

Plantillas para inicializar, validar y mantener componentes de agentes de código: agentes, skills, commands, hooks, plugins, MCP servers, repositorios GitHub profesionales y configuración cross-platform.

[![Validación](https://img.shields.io/badge/validación-12/12%20✅-green)](./)
[![Licencia](https://img.shields.io/badge/licencia-MIT-yellow)](./LICENSE)

---

## Módulos canónicos (12)

| Módulo       | Tipo              | Descripción                               |
| ------------ | ----------------- | ----------------------------------------- |
| Agentes      | single-file `.md` | Orquestador hub-and-spoke con subagentes  |
| Skills       | directorio        | Skills auto-activables por descripción    |
| Commands     | single-file `.md` | Comandos slash (`/deploy`, `/test`)       |
| Hooks        | `.sh.template`    | Interceptores pre/post tool, save, error  |
| Plugins      | directorio        | Empaquetado distribuible de componentes   |
| MCP Servers  | directorio        | Servidores MCP con tools y recursos       |
| Miniapps     | single-file `.md` | SPA single-file tipo artifact             |
| agent-config | especial          | Configuración cross-platform para agentes |
| Repositorios | directorio        | Repo GitHub profesional                   |
| Módulo       | especial          | Meta-template para crear nuevos módulos   |
| Proyecto     | especial          | Template `.claude/` ligero                |
| Estándares   | directorio        | Catálogo de estándares del portfolio      |

> Índice visual: [`INDEX.md`](./INDEX.md)

---

## Instalación

### Scripts (actual)

```bash
curl -fsSL https://raw.githubusercontent.com/alexendros/plantillas/main/install.sh | bash
```

### CLI Python (Bloque 2)

```bash
uv pip install -e .
```

---

## Uso rápido

```bash
# Listar módulos
claude-init --list

# Inicializar un agente
claude-init --modulo agentes --nombre mi-agente

# Validar
python agentes/validar_agente.py ~/.claude/agents/mi-agente --strict
```

CLI Bloque 2: `plantillas validate --all --strict`, `plantillas new agente --nombre mi-agente`.

---

## Validación

- **12 validadores** individuales, todos pasan `--strict`
- **12 workflows** GitHub Actions + workflow central [`validar-todos.yml`](./.github/workflows/validar-todos.yml)
- **Pre-commit hooks** en [`.pre-commit-config.yaml`](./.pre-commit-config.yaml)
- Motor reusable en [`validadores/`](./validadores/)

---

## Documentación

| Documento                              | Contenido                             |
| -------------------------------------- | ------------------------------------- |
| [`INDEX.md`](./INDEX.md)               | Índice maestro con estructura visual  |
| [`ROADMAP.md`](./ROADMAP.md)           | Plan de desarrollo, incluido Bloque 2 |
| [`CHANGELOG.md`](./CHANGELOG.md)       | Historia de versiones                 |
| [`CONTRIBUTING.md`](./CONTRIBUTING.md) | Cómo añadir módulos y validadores     |
| [`docs/cli.md`](./docs/cli.md)         | CLI `plantillas` (Bloque 2)           |

---

## Stack

- **Python 3.12+** — Validadores y CLI
- **GitHub Actions** — CI/CD
- **pre-commit** — Hooks de calidad
- **pytest** — Tests

---

## Licencia

[MIT](./LICENSE) © 2026 Alejandro · Iniciativas Alexendros
