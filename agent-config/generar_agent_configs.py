#!/usr/bin/env python3
"""
Generador de configuraciones cross-platform para agentes IA.

Lee `plantilla_agent_config.yaml` (fuente canónica) y emite los artefactos que
consume cada plataforma:

  - Claude Code: ~/.claude/CLAUDE.md + ~/.claude/settings.json + ~/.claude/.mcp.json
  - OpenCode:   ~/AGENTS.md
  - Devin:      ~/.config/devin/AGENTS.md + ~/.config/devin/config.json
  - Windsurf:   ~/.codeium/windsurf/memories/global_rules.md

Uso:
    python generar_agent_configs.py [ruta/canonical.yaml] [--dry-run] [--backup]

Por defecto lee `plantilla_agent_config.yaml` en el mismo directorio y escribe
los artefactos en las rutas de usuario. Con --dry-run solo los muestra por stdout.
"""

import argparse
import json
import shutil
import sys
from pathlib import Path
from typing import Any, Dict

# Permitir ejecución sin dependencias instaladas
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
try:
    import yaml
except ImportError as e:  # pragma: no cover
    print(f"ERROR: instala pyyaml: pip install pyyaml ({e})", file=sys.stderr)
    sys.exit(1)


DEFAULT_HOME = Path.home()
DEFAULT_SOURCE = Path(__file__).resolve().parent / "plantilla_agent_config.yaml"

OUTPUTS = {
    "claude": {
        "claude_md": DEFAULT_HOME / ".claude" / "CLAUDE.md",
        "settings_json": DEFAULT_HOME / ".claude" / "settings.json",
        "mcp_json": DEFAULT_HOME / ".claude" / ".mcp.json",
    },
    "opencode": {
        "agents_md": DEFAULT_HOME / "AGENTS.md",
    },
    "devin": {
        "agents_md": DEFAULT_HOME / ".config" / "devin" / "AGENTS.md",
        "config_json": DEFAULT_HOME / ".config" / "devin" / "config.json",
    },
    "windsurf": {
        "global_rules_md": DEFAULT_HOME
        / ".codeium"
        / "windsurf"
        / "memories"
        / "global_rules.md",
    },
}


def load_config(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"No existe la fuente canónica: {path}")
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def indent(text: str, prefix: str = "  ") -> str:
    return "\n".join(prefix + line if line else line for line in text.splitlines())


# ──────────────────────────────────────────────────────────────────────────
# Renderers
# ──────────────────────────────────────────────────────────────────────────


def render_claude_md(cfg: Dict[str, Any]) -> str:
    op = cfg.get("operator", {})
    st = cfg.get("style", {})
    fl = cfg.get("flow", {})
    hier = cfg.get("hierarchy", [])

    lines = [
        "# CLAUDE.md — Capa de control (global)",
        "",
        "<!-- ~/.claude/CLAUDE.md: se carga en todas las sesiones. Solo verdades estables y globales. -->",
        "<!-- Lo deterministico (permisos, hooks, env) se impone en settings.json, no se pide aquí. -->",
        "<!-- Tipado XML ligero y homogéneo: cada sección = un tag plano y descriptivo. -->",
        "",
        "<operador>",
        f"{op.get('name', 'Operador')} — {op.get('location', '')}. Idioma: {op.get('language', '')};",
    ]
    for note in op.get("notes", []):
        lines.append(note)
    lines.extend(
        [
            "</operador>",
            "",
            "<estilo>",
            f"Cada respuesta entrega valor concreto: código ejecutable, decisión tomada, análisis con conclusión o siguiente paso numerado. {'Sin preámbulos ni cierres de cortesía.' if st.get('no_preamble') else ''}",
            "Jerarquía visual: negrita en lo accionable (comando, decisión, dato clave), nunca párrafos enteros; lo crítico arriba, el detalle debajo.",
            "Comandos y rutas siempre en `code`. Listas y tablas frente a muros de texto. Brevedad por densidad, no por omisión.",
            "</estilo>",
            "",
            "<flujo>",
            f"Tarea ≥{fl.get('plan_threshold', 3)} pasos o difícil de revertir: arquitectura → plan corto → fases con verificación real (comando + salida). Trivial: ejecutar directo.",
            "Acción destructiva: reversible (backup/tar antes de borrar) + confirmación previa. Lo que se lanza, se cierra.",
            "Reportar fielmente: fallo → mostrarlo con su salida; 'hecho' solo tras verificar. Premisa falsa del operador → corregirla con el dato.",
            f"Secretos: vía `{fl.get('secrets_via', 'pass-cli')}`; nunca hardcodear ni pegar en chat.",
            "</flujo>",
            "",
            "<jerarquia_de_verdad>",
            "Cuando las fuentes se contradigan, gana la de mayor autoridad:",
        ]
    )
    for i, h in enumerate(hier, start=1):
        lines.append(f"{i}. {h['name'].replace('_', ' ').title()}: {h['value']}.")
    lines.extend(
        [
            "Hecho posterior a enero 2026 del que dude: verificar (WebFetch/WebSearch) con fuente antes de afirmar.",
            "</jerarquia_de_verdad>",
            "",
            "<seguridad>",
            "- `.env` y archivos de credenciales: denegar lectura/escritura salvo `.env.example`.",
            "- `git push`: preguntar siempre.",
            "- `rm` y comandos destructivos: preguntar siempre (excepto en `/tmp`).",
            "- Tokens y API keys: solo vía variables de entorno o `pass-cli`; nunca en JSON ni chat.",
            "- Antes de exponer cualquier secret: severidad Crítica, bloquear y notificar.",
            "</seguridad>",
            "",
            "<tooling>",
            "- Preferir MCP `search_graph` / `trace_path` de `codebase-memory-mcp` sobre grep/glob para descubrimiento de código.",
            "- Usar `context7` SIEMPRE que se pregunte por una API, framework o librería.",
            "- Usar `github` para operaciones de issues, PRs y repos.",
            "- Usar `playwright` para testing web, navegación y scraping.",
            "- Usar `filesystem` con alcance restringido a `/home/alexendros`.",
            "</tooling>",
            "",
            "<code_style>",
            "- No añadir comentarios salvo petición explícita.",
            "- No introducir dependencias nuevas sin justificación.",
            "- Respetar la estructura y convenciones existentes del proyecto.",
            "- Seguir el code style del archivo que se edita.",
            "- Formatear con prettier, shfmt, rustfmt o ruff según extensión.",
            "</code_style>",
            "",
            "<memoria>",
            "Ruta canónica de auto-memoria: `~/.claude/projects/-home-alexendros/memory/` (índice MEMORY.md), la nativa del harness: no la reubiques.",
            "Dos sistemas ortogonales, sin duplicar entre sí ni con este CLAUDE.md: `/memory` (hechos duraderos) y `remember` (`~/.remember/`, estado de sesión).",
            "</memoria>",
        ]
    )
    return "\n".join(lines) + "\n"


def render_claude_settings_json(cfg: Dict[str, Any]) -> str:
    overrides = cfg.get("target_overrides", {}).get("claude", {}).get("settings", {})
    hooks_cfg = cfg.get("target_overrides", {}).get("claude", {}).get("hooks", {})
    plugins = cfg.get("target_overrides", {}).get("claude", {}).get("plugins", [])
    model = cfg.get("models", {}).get("claude", {}).get("default", "opus[1m]")

    settings = {
        "permissions": {
            "defaultMode": overrides.get("defaultMode", "acceptEdits"),
            "allow": [
                "Bash(pnpm install)",
                "Bash(pnpm install:*)",
                "Bash(pnpm i:*)",
                "Bash(pnpm run build:*)",
                "Bash(pnpm run test:*)",
                "Bash(pnpm run lint:*)",
                "Bash(pnpm run typecheck:*)",
                "Bash(pnpm run dev:*)",
                "Bash(pnpm run e2e:*)",
                "Bash(pnpm build:*)",
                "Bash(pnpm test:*)",
                "Bash(pnpm lint:*)",
                "Bash(pnpm typecheck:*)",
                "Bash(pnpm dev:*)",
                "Bash(npm install)",
                "Bash(npm ci:*)",
                "Bash(npm run build:*)",
                "Bash(npm run test:*)",
                "Bash(npm run lint:*)",
                "Bash(npm run typecheck:*)",
                "Bash(npm run dev:*)",
                "Bash(npm test:*)",
                "Bash(npx vitest:*)",
                "Bash(npx playwright:*)",
                "Bash(npx eslint:*)",
                "Bash(npx prettier:*)",
                "Bash(npx tsc:*)",
                "Bash(vitest:*)",
                "Bash(playwright:*)",
                "Bash(eslint:*)",
                "Bash(prettier:*)",
                "Bash(tsc:*)",
                "Bash(cargo build:*)",
                "Bash(cargo test:*)",
                "Bash(cargo check:*)",
                "Bash(cargo clippy:*)",
                "Bash(cargo fmt:*)",
                "Bash(cargo run:*)",
                "Bash(rustfmt:*)",
                "Bash(ruff check:*)",
                "Bash(ruff format:*)",
                "Bash(gh run list:*)",
                "Bash(gh run view:*)",
                "Bash(gh run watch:*)",
                "Bash(gh pr view:*)",
                "Bash(gh pr list:*)",
                "Bash(gh pr diff:*)",
                "Bash(gh pr checks:*)",
                "Bash(gh workflow list:*)",
                "Bash(gh workflow view:*)",
                "Bash(git status:*)",
                "Bash(git diff:*)",
                "Bash(git log:*)",
                "Bash(git show:*)",
                "Bash(git branch:*)",
                "Bash(docker compose ps:*)",
                "Bash(docker compose logs:*)",
                "Bash(docker compose config:*)",
            ],
            "ask": [
                "Bash(git push:*)",
                "Bash(gh pr merge:*)",
                "Bash(pnpm publish:*)",
                "Bash(npm publish:*)",
                "Bash(cargo publish:*)",
                "Bash(vercel:*)",
                "Bash(supabase db push:*)",
            ],
            "deny": [
                "Bash(rm -rf:*)",
                "Bash(git reset --hard:*)",
                "Bash(git clean:*)",
                "Bash(supabase db reset:*)",
            ],
        },
        "model": model,
        "hooks": {
            "SessionStart": [
                {
                    "hooks": [
                        {
                            "type": "command",
                            "command": hooks_cfg.get(
                                "session_start",
                                "~/.claude/hooks/session-start-context.sh",
                            ),
                        }
                    ]
                },
                {
                    "matcher": "startup",
                    "hooks": [
                        {
                            "type": "command",
                            "command": hooks_cfg.get(
                                "session_reminder",
                                "~/.claude/hooks/cbm-session-reminder",
                            ),
                        }
                    ],
                },
                {
                    "matcher": "resume",
                    "hooks": [
                        {
                            "type": "command",
                            "command": hooks_cfg.get(
                                "session_reminder",
                                "~/.claude/hooks/cbm-session-reminder",
                            ),
                        }
                    ],
                },
                {
                    "matcher": "clear",
                    "hooks": [
                        {
                            "type": "command",
                            "command": hooks_cfg.get(
                                "session_reminder",
                                "~/.claude/hooks/cbm-session-reminder",
                            ),
                        }
                    ],
                },
                {
                    "matcher": "compact",
                    "hooks": [
                        {
                            "type": "command",
                            "command": hooks_cfg.get(
                                "session_reminder",
                                "~/.claude/hooks/cbm-session-reminder",
                            ),
                        }
                    ],
                },
            ],
            "PostToolUse": [
                {
                    "matcher": "Edit|Write",
                    "hooks": [
                        {
                            "type": "command",
                            "command": hooks_cfg.get(
                                "post_edit", "~/.claude/hooks/post-edit.sh"
                            ),
                        }
                    ],
                }
            ],
            "PreToolUse": [
                {
                    "matcher": "Grep|Glob",
                    "hooks": [
                        {
                            "type": "command",
                            "command": hooks_cfg.get(
                                "code_discovery",
                                "~/.claude/hooks/cbm-code-discovery-gate",
                            ),
                            "timeout": 5,
                        }
                    ],
                }
            ],
        },
        "enabledPlugins": {plugin: True for plugin in plugins},
        "language": overrides.get("language", "Español"),
        "theme": overrides.get("theme", "auto"),
        "editorMode": overrides.get("editorMode", "normal"),
        "remoteControlAtStartup": overrides.get("remoteControlAtStartup", True),
        "inputNeededNotifEnabled": overrides.get("inputNeededNotifEnabled", True),
        "agentPushNotifEnabled": overrides.get("agentPushNotifEnabled", True),
    }
    return json.dumps(settings, indent=2, ensure_ascii=False) + "\n"


def render_claude_mcp_json(cfg: Dict[str, Any]) -> str:
    servers = cfg.get("mcp_servers", [])
    mcp_servers = {}
    for s in servers:
        name = s.get("name")
        cmd = s.get("command")
        if name and cmd:
            mcp_servers[name] = {"command": cmd}
    return json.dumps({"mcpServers": mcp_servers}, indent=2, ensure_ascii=False) + "\n"


def render_agents_md(cfg: Dict[str, Any]) -> str:
    op = cfg.get("operator", {})
    st = cfg.get("style", {})
    fl = cfg.get("flow", {})
    models = cfg.get("models", {}).get("opencode", {})
    mcp_servers = cfg.get("mcp_servers", [])
    skills = cfg.get("skills", [])
    agents = cfg.get("agents", [])
    commands = cfg.get("commands", [])

    lines = [
        "# AGENTS.md — Instrucciones globales para agentes",
        "",
        "## Operador",
        "",
        f"- {op.get('name', 'Operador')} — {op.get('location', '')}. {op.get('language', '')} con tildes; tecnicismos en su forma original.",
        "- Infra propia. Rigor técnico, no hand-holding.",
        "",
        "## Estilo",
        "",
    ]
    if st.get("first_line"):
        lines.append(
            f"- Primera línea = {st.get('first_line')}: código, decisión, análisis con conclusión."
        )
    if st.get("no_preamble"):
        lines.append("- Sin preámbulos, sin cierres de cortesía, sin relleno.")
    if st.get("commands_in_code"):
        lines.append("- Comandos y rutas siempre en `code`.")
    if st.get("lists_and_tables"):
        lines.append("- Listas y tablas frente a muros de texto.")
    if st.get("brevity_by_density"):
        lines.append("- Brevedad por densidad, no por omisión.")
    if st.get("bold_for_actionable"):
        lines.append("- Negrita solo en lo accionable (comando, decisión, dato clave).")
    lines.extend(
        [
            "",
            "## Flujo",
            "",
            f"- Tarea ≥{fl.get('plan_threshold', 3)} pasos o difícil de revertir: arquitectura → plan corto → fases con verificación real.",
            "- Tarea trivial: ejecutar directo.",
            "- Acción destructiva: backup/tar previo + confirmación.",
            f"- Secretos: vía `{fl.get('secrets_via', 'pass-cli')}`; nunca hardcodear ni pegar en chat.",
            "",
            "## Modelos",
            "",
            f"- Principal: `{models.get('default', 'opencode/mimo-v2.5-free')}`",
        ]
    )
    for alt in models.get("alternatives", []):
        lines.append(f"- Alternativa: `{alt}`")
    if models.get("paid_requires_explicit_request"):
        lines.append("- No usar modelos de pago salvo petición explícita.")
    lines.extend(
        [
            "",
            "## Herramientas",
            "",
            "### MCP",
            "",
        ]
    )
    for s in mcp_servers:
        lines.append(f"- **{s.get('name')}**: {s.get('command')}")
    lines.extend(
        [
            "",
            "- **context7**: documentación de librerías y frameworks. Usar SIEMPRE que se pregunte por una API, framework o librería.",
            "- **github**: operaciones GitHub (issues, PRs, repos). Token configurado en env.",
            "- **playwright**: testing web, navegación y scraping de sitios en producción.",
            "- **memory**: memory graph para persistir hechos entre sesiones.",
            "- **filesystem**: acceso a archivos del sistema.",
            "",
            "### Skills",
            "",
        ]
    )
    for sk in skills:
        lines.append(
            f"- `{sk.get('name')}`: {sk.get('description')}. Usar con `{sk.get('usage', '')}`."
        )
    lines.extend(
        [
            "",
            "### Agentes",
            "",
        ]
    )
    for ag in agents:
        lines.append(f"- `{ag.get('name')}`: {ag.get('description')}")
    lines.extend(
        [
            "",
            "### Comandos",
            "",
        ]
    )
    for cmd in commands:
        lines.append(f"- `{cmd.get('name')}`: {cmd.get('description')}")
    lines.extend(
        [
            "",
            "## Reglas",
            "",
            "### Seguridad",
            "",
            "- `.env` files: deny por defecto.",
            "- `git push`: ask (requiere confirmación).",
            "- `rm`: ask (excepto en directorios temporales /tmp).",
            "- Ediciones de código: ask (primera vez por sesión, luego allow).",
            "- GitHub token: solo vía env, nunca en código ni chat.",
            "",
            "### Edición",
            "",
            "1. Respetar la estructura y convenciones existentes del proyecto.",
            "2. No introducir dependencias nuevas sin justificación.",
            "3. No comments salvo petición explícita.",
            "4. Seguir el code style del archivo que se edita.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_devin_config_json(cfg: Dict[str, Any]) -> str:
    overrides = cfg.get("target_overrides", {}).get("devin", {})
    read_config = overrides.get(
        "read_config_from", {"cursor": True, "windsurf": True, "claude": True}
    )
    mcp_servers = cfg.get("mcp_servers", [])

    mcp = {}
    for s in mcp_servers:
        name = s.get("name")
        cmd = s.get("command")
        if name and cmd:
            mcp[name] = {"command": cmd}

    config = {
        "read_config_from": read_config,
        "permissions": {
            "allow": [
                "Read(**)",
                "Exec(git)",
                "Bash(git status:*)",
                "Bash(git diff:*)",
                "Bash(git log:*)",
                "Bash(pnpm run test:*)",
                "Bash(npm run test:*)",
                "Bash(cargo test:*)",
                "Bash(ruff check:*)",
                "Bash(ruff format:*)",
                "Bash(prettier:*)",
                "Bash(eslint:*)",
                "Bash(tsc:*)",
                "Bash(vitest:*)",
                "Bash(playwright:*)",
                "Bash(rustfmt:*)",
                "Bash(shfmt:*)",
                "Bash(gh pr view:*)",
                "Bash(gh pr list:*)",
                "Bash(gh pr diff:*)",
                "Bash(gh pr checks:*)",
                "Bash(gh run list:*)",
                "Bash(gh run view:*)",
                "Bash(gh workflow list:*)",
                "Bash(gh workflow view:*)",
                "Bash(docker compose ps:*)",
                "Bash(docker compose logs:*)",
                "Bash(docker compose config:*)",
            ],
            "ask": [
                "Bash(git push:*)",
                "Bash(gh pr merge:*)",
                "Bash(pnpm publish:*)",
                "Bash(npm publish:*)",
                "Bash(cargo publish:*)",
                "Bash(vercel:*)",
                "Bash(supabase db push:*)",
                "Bash(rm -rf:*)",
                "Bash(rm -r *)",
            ],
            "deny": [
                "Bash(rm -rf:*)",
                "Bash(git reset --hard:*)",
                "Bash(git clean:*)",
                "Bash(supabase db reset:*)",
            ],
        },
    }
    if mcp:
        config["mcpServers"] = mcp
    return json.dumps(config, indent=2, ensure_ascii=False) + "\n"


def render_windsurf_global_rules_md(cfg: Dict[str, Any]) -> str:
    """Renderiza global_rules.md para Windsurf/Cascade. Mantiene el contenido
    conciso para respetar el límite de ~6.000 caracteres."""
    op = cfg.get("operator", {})
    fl = cfg.get("flow", {})
    hier = cfg.get("hierarchy", [])

    lines = [
        "# Global Rules — Alexendros",
        "",
        "<!-- ~/.codeium/windsurf/memories/global_rules.md — always-on rules for Cascade -->",
        "",
        "## Operator",
        "",
        f"- {op.get('name', 'Operador')} — {op.get('location', '')}. Idioma: {op.get('language', '')}; tecnicismos en su forma original.",
        "- Infra propia. Rigor técnico, no hand-holding.",
        "",
        "## Style",
        "",
        "- Primera línea = sustancia: código, decisión, análisis con conclusión o siguiente paso numerado.",
        "- Sin preámbulos, sin cierres de cortesía, sin relleno.",
        "- Comandos y rutas siempre en `code`.",
        "- Listas y tablas frente a muros de texto.",
        "- Brevedad por densidad, no por omisión.",
        "- Lo crítico arriba; negrita solo en lo accionable (comando, decisión, dato clave).",
        "",
        "## Flow",
        "",
        f"- Tarea ≥ {fl.get('plan_threshold', 3)} pasos o difícil de revertir: arquitectura → plan corto → fases con verificación real (comando + salida).",
        "- Tarea trivial: ejecutar directo.",
        "- Acción destructiva: backup/tar previo + confirmación explícita.",
        "- Lo que se lanza, se cierra. Reportar fallos con su salida; 'hecho' solo tras verificar.",
        "- Premisa falsa del operador: corregirla con el dato.",
        f"- Secretos: vía `{fl.get('secrets_via', 'pass-cli')}`; nunca hardcodear ni pegar en chat.",
        "",
        "## Security",
        "",
        "- `.env` y archivos de credenciales: denegar lectura/escritura salvo `.env.example`.",
        "- `git push`: preguntar siempre.",
        "- `rm` y comandos destructivos: preguntar siempre (excepto en `/tmp`).",
        "- Tokens y API keys: solo vía variables de entorno o `pass-cli`; nunca en JSON ni chat.",
        "- Antes de exponer cualquier secret: severidad Crítica, bloquear y notificar.",
        "",
        "## Tooling",
        "",
        "- Preferir MCP `search_graph` / `trace_path` de `codebase-memory-mcp` sobre grep/glob para descubrimiento de código.",
        "- Usar `context7` SIEMPRE que se pregunte por una API, framework o librería.",
        "- Usar `github` para operaciones de issues, PRs y repos.",
        "- Usar `playwright` para testing web, navegación y scraping.",
        "- Usar `filesystem` con alcance restringido a `/home/alexendros`.",
        "",
        "## Code style",
        "",
        "- No añadir comentarios salvo petición explícita.",
        "- No introducir dependencias nuevas sin justificación.",
        "- Respetar la estructura y convenciones existentes del proyecto.",
        "- Seguir el code style del archivo que se edita.",
        "- Formatear con prettier, shfmt, rustfmt o ruff según extensión.",
        "",
        "## Jerarquía de verdad",
        "",
    ]
    for i, h in enumerate(hier, start=1):
        lines.append(f"{i}. {h['name'].replace('_', ' ').title()}: {h['value']}.")
    lines.extend(
        [
            "",
            "## Misc",
            "",
            "- Hechos posteriores a enero 2026: verificar con WebSearch/WebFetch antes de afirmar.",
            "- Cuando las fuentes se contradigan, ganan `settings.json` + verificable, y se reporta la discrepancia.",
        ]
    )
    return "\n".join(lines) + "\n"


# ──────────────────────────────────────────────────────────────────────────
# I/O
# ──────────────────────────────────────────────────────────────────────────


def generate_all(cfg: Dict[str, Any]) -> Dict[str, str]:
    return {
        "claude_md": render_claude_md(cfg),
        "claude_settings_json": render_claude_settings_json(cfg),
        "claude_mcp_json": render_claude_mcp_json(cfg),
        "agents_md": render_agents_md(cfg),
        "devin_config_json": render_devin_config_json(cfg),
        "windsurf_global_rules_md": render_windsurf_global_rules_md(cfg),
    }


def write_outputs(
    outputs: Dict[str, str], paths: Dict[str, Path], dry_run: bool, backup: bool
) -> None:
    mapping = {
        "claude_md": paths["claude_claude_md"],
        "claude_settings_json": paths["claude_settings_json"],
        "claude_mcp_json": paths["claude_mcp_json"],
        "agents_md": paths["opencode_agents_md"],
        "devin_config_json": paths["devin_config_json"],
        "windsurf_global_rules_md": paths["windsurf_global_rules_md"],
    }
    # Devin AGENTS.md es el mismo contenido que OpenCode AGENTS.md
    devin_agents_path = paths["devin_agents_md"]
    mapping["devin_agents_md"] = devin_agents_path

    generated = outputs.copy()
    generated["devin_agents_md"] = generated["agents_md"]

    for key, content in generated.items():
        path = mapping.get(key)
        if not path:
            continue
        if dry_run:
            print(f"--- {path} ---")
            print(content)
            print()
            continue

        if backup and path.exists():
            backup_path = path.with_suffix(path.suffix + ".backup")
            shutil.copy2(path, backup_path)
            print(f"Backup: {backup_path}")

        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        print(f"Escrito: {path}")


def build_paths(cfg: Dict[str, Any], home: Path) -> Dict[str, Path]:
    return {
        "claude_claude_md": home / ".claude" / "CLAUDE.md",
        "claude_settings_json": home / ".claude" / "settings.json",
        "claude_mcp_json": home / ".claude" / ".mcp.json",
        "opencode_agents_md": home / "AGENTS.md",
        "devin_agents_md": home / ".config" / "devin" / "AGENTS.md",
        "devin_config_json": home / ".config" / "devin" / "config.json",
        "windsurf_global_rules_md": home
        / ".codeium"
        / "windsurf"
        / "memories"
        / "global_rules.md",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "source",
        nargs="?",
        default=DEFAULT_SOURCE,
        help="Fuente canónica YAML (default: plantilla_agent_config.yaml)",
    )
    parser.add_argument(
        "--home",
        default=str(DEFAULT_HOME),
        help="Directorio home de destino (default: ~)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Mostrar salidas por stdout sin escribir archivos",
    )
    parser.add_argument(
        "--backup",
        action="store_true",
        help="Hacer backup de archivos existentes antes de sobrescribir",
    )
    args = parser.parse_args()

    source = Path(args.source)
    home = Path(args.home)
    cfg = load_config(source)
    outputs = generate_all(cfg)
    paths = build_paths(cfg, home)

    # Advertencia de longitud para Windsurf global_rules.md
    windsurf_len = len(outputs["windsurf_global_rules_md"])
    max_chars = (
        cfg.get("target_overrides", {}).get("windsurf", {}).get("max_chars", 6000)
    )
    if windsurf_len > max_chars:
        print(
            f"⚠️  ADVERTENCIA: Windsurf global_rules.md excede {max_chars} chars ({windsurf_len}). "
            "Reduce contenido para evitar truncamiento.",
            file=sys.stderr,
        )

    write_outputs(outputs, paths, args.dry_run, args.backup)
    return 0


if __name__ == "__main__":
    sys.exit(main())
