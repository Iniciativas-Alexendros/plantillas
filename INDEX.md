# ÍNDICE MAESTRO · Sistema de Plantillas Modulares para Claude Code

> **Punto de entrada universal** para el ecosistema de plantillas.
> Selecciona el módulo que necesitas y accede directamente.
>
> 📢 **2026-05-23 · Canon-Runtime Alignment (BREAKING)** — los módulos
> `agentes`, `commands` y `hooks` colapsan a single-file (`.md` o
> `.sh.template`); 4 módulos canon nuevos añadidos: `miniapps`,
> `autoresearch`, `cuadernos`, `knowledge`. Detalle en `CHANGELOG.md`.

---

## Módulos canónicos (14)

### Single-file `.md` con frontmatter runtime

#### 🤖 Agentes
> Construye agentes especializados con patrón orquestador-especialistas.

| | Archivo | Para qué sirve |
|---|---|---|
| 📋 Plantilla | [`agentes/plantilla_agente.md`](./agentes/plantilla_agente.md) | Single-file con `name`/`description`/`tools`/`model` + 7 secciones canon |
| ✅ Ejemplo | [`agentes/ejemplo_agente.md`](./agentes/ejemplo_agente.md) | Orquestador hub-and-spoke funcional (`dev-arquitectura`) |

**TL;DR**: `cp agentes/plantilla_agente.md ~/.claude/agents/mi-agente.md`

---

#### ⌨️ Commands
> Define comandos slash personalizados (`/mi-comando`).

| | Archivo | Para qué sirve |
|---|---|---|
| 📋 Plantilla | [`commands/plantilla_command.md`](./commands/plantilla_command.md) | Frontmatter `description`/`argument-hint`/`allowed-tools` + 6 secciones canon |
| ✅ Ejemplo | [`commands/ejemplo_command.md`](./commands/ejemplo_command.md) | `/test-cobertura` multi-runner (Jest/Vitest/pytest) |

**TL;DR**: `cp commands/plantilla_command.md ~/.claude/commands/mi-comando.md`

---

#### 🖥️ Miniapps · canon nuevo
> SPA single-file tipo Claude.ai artifact (categorías: dashboard/explorer/tool/playbook).

| | Archivo | Para qué sirve |
|---|---|---|
| 📋 Plantilla | [`miniapps/plantilla_miniapps.md`](./miniapps/plantilla_miniapps.md) | Frontmatter `category`/`runtime`/`version` + estructura HTML reducida |
| ✅ Ejemplo | [`miniapps/ejemplo_miniapps.md`](./miniapps/ejemplo_miniapps.md) | `kpi-mensual` dashboard de KPIs financieros |

**TL;DR**: `cp miniapps/plantilla_miniapps.md ~/.claude/miniapps/<slug>/<slug>.md`

---

#### 🔬 Autoresearch · canon nuevo
> Cuadernos de investigación automatizada (pregunta → fuentes → veredicto).

| | Archivo | Para qué sirve |
|---|---|---|
| 📋 Plantilla | [`autoresearch/plantilla_autoresearch.md`](./autoresearch/plantilla_autoresearch.md) | Frontmatter `topic`/`sources`/`status`/`confidence` + 5 secciones canon |
| ✅ Ejemplo | [`autoresearch/ejemplo_autoresearch.md`](./autoresearch/ejemplo_autoresearch.md) | Prompt caching vs memory en la Claude API |

**TL;DR**: `cp autoresearch/plantilla_autoresearch.md ~/.claude/autoresearch/<slug>/<slug>.md`

---

#### 📓 Cuadernos · canon nuevo
> Notas estructuradas del operador (idea/log/decision/playbook).

| | Archivo | Para qué sirve |
|---|---|---|
| 📋 Plantilla | [`cuadernos/plantilla_cuadernos.md`](./cuadernos/plantilla_cuadernos.md) | Frontmatter `kind`/`tags`/`status` + 3 secciones obligatorias y N recomendadas por kind |
| ✅ Ejemplo | [`cuadernos/ejemplo_cuadernos.md`](./cuadernos/ejemplo_cuadernos.md) | Decisión: colapsar plantillas a single-file |

**TL;DR**: `cp cuadernos/plantilla_cuadernos.md ~/.claude/cuadernos/<slug>/<slug>.md`

---

#### 📚 Knowledge · canon nuevo
> Base de conocimiento referenciable (FAQs, runbooks indexados).

| | Archivo | Para qué sirve |
|---|---|---|
| 📋 Plantilla | [`knowledge/plantilla_knowledge.md`](./knowledge/plantilla_knowledge.md) | Frontmatter `domain`/`references`/`authority`/`status` + 5 secciones canon |
| ✅ Ejemplo | [`knowledge/ejemplo_knowledge.md`](./knowledge/ejemplo_knowledge.md) | Diferencia entre `tools` (agente) y `allowed-tools` (command) |

**TL;DR**: `cp knowledge/plantilla_knowledge.md ~/.claude/knowledge/<slug>/<slug>.md`

---

### Single-file `.sh.template`

#### ⚓ Hooks
> Intercepta y controla el comportamiento del agente en eventos del runtime.

| | Archivo | Para qué sirve |
|---|---|---|
| 📋 Plantilla | [`hooks/plantilla_hook.sh.template`](./hooks/plantilla_hook.sh.template) | Cabecera declarativa `# matcher`/`# tool_pattern` + body JSON `{decision, reason}` |
| ✅ Ejemplo | [`hooks/ejemplo_hook.sh.template`](./hooks/ejemplo_hook.sh.template) | `pre-bash-secret-guard` (escanea GH/OpenAI/AWS tokens) |
| 📄 Doc | [`hooks/HOOK.md`](./hooks/HOOK.md) | Eventos soportados + cómo instalar y probar |

**TL;DR**: `cp hooks/plantilla_hook.sh.template ~/.claude/hooks/mi-hook.sh && chmod +x ~/.claude/hooks/mi-hook.sh`

---

### Dir canon multi-archivo

#### 🛠️ Skills
> Crea skills reutilizables que Claude invoca automáticamente.

| | Directorio | Para qué sirve |
|---|---|---|
| 📋 Plantilla | [`skills/plantilla_skill/`](./skills/plantilla_skill/) | Estructura `SKILL.md` + progressive disclosure |
| ✅ Ejemplo | [`skills/ejemplo_skill/`](./skills/ejemplo_skill/) | Skill operativa de diagramas Mermaid |

**TL;DR**: `cp -r skills/plantilla_skill ~/.claude/skills/mi-skill`

---

#### 🔌 Plugins
> Empaqueta agentes, skills, hooks y MCP en unidades distribuibles.

| | Directorio | Para qué sirve |
|---|---|---|
| 📋 Plantilla | [`plugins/plantilla_plugin/`](./plugins/plantilla_plugin/) | Estructura de plugin + marketplace |
| ✅ Ejemplo | [`plugins/ejemplo_plugin/`](./plugins/ejemplo_plugin/) | Plugin de integración GitHub funcional |

**TL;DR**: `cp -r plugins/plantilla_plugin ~/.claude/plugins/mi-plugin`

---

#### 🔗 MCP Servers
> Construye servidores MCP para exponer tools y recursos externos.

| | Directorio | Para qué sirve |
|---|---|---|
| 📋 Plantilla | [`mcp/plantilla_mcp/`](./mcp/plantilla_mcp/) | Estructura de servidor MCP (Python/TS) |
| ✅ Ejemplo | [`mcp/ejemplo_mcp/`](./mcp/ejemplo_mcp/) | MCP server de filesystem funcional |

**TL;DR**: `cp -r mcp/plantilla_mcp ~/mis-mcp-servers/mi-server`

---

#### 📦 dot-claude
> Inicializa un directorio `.claude/` completo (proyecto o home).

| | Directorio | Para qué sirve |
|---|---|---|
| 📋 Plantilla | [`dot-claude/plantilla_dot_claude/`](./dot-claude/plantilla_dot_claude/) | `CLAUDE.md` + `settings.json` (schema runtime) + `mcp.json` |
| ✅ Ejemplo | [`dot-claude/ejemplo_dot_claude/`](./dot-claude/ejemplo_dot_claude/) | `.claude/` funcional con árbol plano post-reforma |

**TL;DR**: `cp -r dot-claude/ejemplo_dot_claude ./.claude`

---

#### 🏛️ Repositorios
> Estructura profesional y empresarial para repositorios GitHub.

| | Directorio | Para qué sirve |
|---|---|---|
| 📋 Plantilla | [`repositorios/plantilla_repositorio/`](./repositorios/plantilla_repositorio/) | Guía: metodología, estructura, flujo git |
| ✅ Ejemplo | [`repositorios/ejemplo_repositorio/`](./repositorios/ejemplo_repositorio/) | Repo completo con community health files, CI/CD, ADRs |

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

## Scripts de bootstrap

| Script | Para qué sirve | Uso rápido |
|---|---|---|
| [`install.sh`](./install.sh) | Instala el sistema en `~/.claude/plantillas/` | `curl -fsSL .../install.sh \| bash` |
| [`claude-init`](./claude-init) | Inicializa módulos, proyectos o repositorios | `claude-init --modulo agentes --nombre mi-agente` |
| [`update.sh`](./update.sh) | Actualiza el sistema a la última versión | `./update.sh` |

> **Contexto de mantenedor:** [`PROMPT_INICIO.md`](./PROMPT_INICIO.md) — prompt listo
> para pegar al abrir un hilo de Claude que vaya a trabajar sobre este repo (ubicación,
> reglas de oro, comandos rápidos y stack).

---

## Integración entre módulos

¿No sabes cómo combinar agentes + skills + hooks + MCP + miniapps + cuadernos + knowledge?
→ Lee [`INTEGRACION.md`](./INTEGRACION.md) — mapa de relaciones, decision tree, ejemplo completo.

---

## ¿Qué necesitas hoy?

| Si quieres... | Ve a... | Comando rápido |
|---|---|---|
| Crear un agente nuevo | `agentes/plantilla_agente.md` | `claude-init --modulo agentes --nombre X` |
| Crear una skill nueva | `skills/plantilla_skill/` | `claude-init --modulo skills --nombre X` |
| Crear un comando slash | `commands/plantilla_command.md` | `claude-init --modulo commands --nombre X` |
| Crear un hook | `hooks/plantilla_hook.sh.template` | `claude-init --modulo hooks --nombre X` |
| Crear un plugin | `plugins/plantilla_plugin/` | `claude-init --modulo plugins --nombre X` |
| Crear un MCP server | `mcp/plantilla_mcp/` | `claude-init --modulo mcp --nombre X` |
| Crear una mini-app | `miniapps/plantilla_miniapps.md` | `claude-init --modulo miniapps --nombre X` |
| Crear un cuaderno de investigación | `autoresearch/plantilla_autoresearch.md` | `claude-init --modulo autoresearch --nombre X` |
| Crear un cuaderno propio | `cuadernos/plantilla_cuadernos.md` | `claude-init --modulo cuadernos --nombre X` |
| Crear un artículo KB | `knowledge/plantilla_knowledge.md` | `claude-init --modulo knowledge --nombre X` |
| Inicializar `.claude/` completo | `dot-claude/ejemplo_dot_claude/` | `cp -r dot-claude/ejemplo_dot_claude ./.claude` |
| Crear un repo GitHub profesional | `repositorios/ejemplo_repositorio/` | `claude-init --repositorio --nombre mi-repo` |
| Inicializar `.claude/` en proyecto | `proyecto/` | `claude-init --proyecto` |
| Crear un nuevo módulo | `modulo/` | `cp -r modulo mi-modulo` |

---

## Validación y CI/CD

Cada módulo tiene su propio validador y workflow de CI/CD. Todos usan el **motor de validación reusable** [`validadores/`](./validadores/).

| Módulo | Validador | Workflow CI/CD per-módulo |
|---|---|---|
| 🤖 Agentes | [`validar_agente.py`](./agentes/validar_agente.py) | [`validar-agentes.yml`](./agentes/.github/workflows/validar-agentes.yml) |
| 🛠️ Skills | [`validar_skill.py`](./skills/validar_skill.py) | [`validar-skills.yml`](./skills/.github/workflows/validar-skills.yml) |
| ⌨️ Commands | [`validar_command.py`](./commands/validar_command.py) | [`validar-commands.yml`](./commands/.github/workflows/validar-commands.yml) |
| ⚓ Hooks | [`validar_hook.py`](./hooks/validar_hook.py) | [`validar-hooks.yml`](./hooks/.github/workflows/validar-hooks.yml) |
| 🔌 Plugins | [`validar_plugin.py`](./plugins/validar_plugin.py) | [`validar-plugins.yml`](./plugins/.github/workflows/validar-plugins.yml) |
| 🔗 MCP | [`validar_mcp.py`](./mcp/validar_mcp.py) | [`validar-mcp.yml`](./mcp/.github/workflows/validar-mcp.yml) |
| 📦 dot-claude | [`validar_dot_claude.py`](./dot-claude/validar_dot_claude.py) | [`validar-dot-claude.yml`](./dot-claude/.github/workflows/validar-dot-claude.yml) |
| 🏛️ Repositorios | [`validar_repositorio.py`](./repositorios/validar_repositorio.py) | [`validar-repositorios.yml`](./repositorios/.github/workflows/validar-repositorios.yml) |
| 🖥️ Miniapps | [`validar_miniapps.py`](./miniapps/validar_miniapps.py) | [`validar-miniapps.yml`](./miniapps/.github/workflows/validar-miniapps.yml) |
| 🔬 Autoresearch | [`validar_autoresearch.py`](./autoresearch/validar_autoresearch.py) | [`validar-autoresearch.yml`](./autoresearch/.github/workflows/validar-autoresearch.yml) |
| 📓 Cuadernos | [`validar_cuadernos.py`](./cuadernos/validar_cuadernos.py) | [`validar-cuadernos.yml`](./cuadernos/.github/workflows/validar-cuadernos.yml) |
| 📚 Knowledge | [`validar_knowledge.py`](./knowledge/validar_knowledge.py) | [`validar-knowledge.yml`](./knowledge/.github/workflows/validar-knowledge.yml) |
| 🧩 Módulo (template) | [`validar_modulo.py`](./modulo/validar_modulo.py) | [`validar-modulo.yml`](./modulo/.github/workflows/validar-modulo.yml) |
| 📁 Proyecto (template) | [`validar_proyecto.py`](./proyecto/validar_proyecto.py) | [`validar-proyecto.yml`](./proyecto/.github/workflows/validar-proyecto.yml) |

**Workflow central** (todos los módulos en matriz declarativa): [`validar-todos.yml`](./.github/workflows/validar-todos.yml)

### CI/CD Global (protección del repositorio)

| Workflow | Propósito | Archivo |
|---|---|---|
| 🌍 CI Global | Lint YAML/JSON/Markdown/Python/Shell + validación de estructura | [`ci-global.yml`](./.github/workflows/ci-global.yml) |
| 🛡️ PR Guardian | Título Conventional Commit, tamaño, archivos protegidos, CHANGELOG | [`pr-guardian.yml`](./.github/workflows/pr-guardian.yml) |
| 🔒 Security Scan | Detección de secrets, tokens, archivos prohibidos | [`security-scan.yml`](./.github/workflows/security-scan.yml) |
| 🔍 Validador Repo | Motor Python que valida estructura canónica completa | [`validar_repo.py`](./validar_repo.py) |

```bash
# Validar plantillas/ejemplos single-file
python agentes/validar_agente.py agentes/ejemplo_agente.md --strict
python commands/validar_command.py commands/ejemplo_command.md --strict
python miniapps/validar_miniapps.py miniapps/ejemplo_miniapps.md --strict
python autoresearch/validar_autoresearch.py autoresearch/ejemplo_autoresearch.md --strict
python cuadernos/validar_cuadernos.py cuadernos/ejemplo_cuadernos.md --strict
python knowledge/validar_knowledge.py knowledge/ejemplo_knowledge.md --strict
python hooks/validar_hook.py hooks/ejemplo_hook.sh.template --strict

# Validar dir canon
python skills/validar_skill.py ~/.claude/skills/mi-skill --strict
python plugins/validar_plugin.py ~/.claude/plugins/mi-plugin --strict
python mcp/validar_mcp.py ~/mis-mcp-servers/mi-server --strict
python dot-claude/validar_dot_claude.py ./.claude --strict

# Validar estructura completa del repositorio (14 módulos canon)
python validar_repo.py --strict
```

---

## Estructura visual del sistema

```
plantillas/
├── INDEX.md                          ← ESTE ARCHIVO
├── ROADMAP.md
├── CHANGELOG.md                      ← entrada [Unreleased] = canon-runtime alignment
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── INTEGRACION.md
├── install.sh · claude-init · update.sh
├── .pre-commit-config.yaml
├── validar_repo.py                   ← acepta file-or-dir + 14 módulos canon
├── tests/
│   ├── test_validadores.py
│   └── test_smoke.py
├── validadores/                      ← Motor de validación reusable
│   ├── base.py · checks.py · reporte.py · __init__.py
├── modulo/ · proyecto/               ← Meta-templates
├── .github/workflows/
│   ├── validar-todos.yml             ← Matriz declarativa de 14 módulos
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
├── autoresearch/                     ← 🔬 Canon nuevo
│   ├── plantilla_autoresearch.md
│   ├── ejemplo_autoresearch.md
│   └── validar_autoresearch.py
│
├── cuadernos/                        ← 📓 Canon nuevo
│   ├── plantilla_cuadernos.md
│   ├── ejemplo_cuadernos.md
│   └── validar_cuadernos.py
│
├── knowledge/                        ← 📚 Canon nuevo
│   ├── plantilla_knowledge.md
│   ├── ejemplo_knowledge.md
│   └── validar_knowledge.py
│
├── skills/
│   ├── plantilla_skill/              ← 🛠️ Dir canon
│   └── ejemplo_skill/
│
├── plugins/                          ← 🔌 Dir canon
├── mcp/                              ← 🔗 Dir canon
├── dot-claude/                       ← 📦 Dir canon (settings.json schema runtime)
├── repositorios/                     ← 🏛️ Dir canon
└── artefactos/                       ← Plano (outputs operador, no canon)
```

---

> **Regla de oro post-reforma**: cada módulo sigue uno de tres formatos:
>
> - **Single-file `.md`**: `plantilla_X.md` + `ejemplo_X.md` (canon nuevo).
> - **Single-file `.sh.template`**: `plantilla_X.sh.template` + `ejemplo_X.sh.template` (hooks).
> - **Dir multi-archivo**: `plantilla_X/` + `ejemplo_X/` (skills, plugins, mcp, dot-claude, repositorios).
>
> El validador global `validar_repo.py` reconoce los tres patrones vía glob por extensión.
