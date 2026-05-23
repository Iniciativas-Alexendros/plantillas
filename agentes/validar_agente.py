#!/usr/bin/env python3
"""
Validador de Agentes Claude Code · v2.0.0

Usa el motor de validación reusable del sistema de plantillas.

Uso:
    python validar_agente.py ~/.claude/agents/mi-agente
    python validar_agente.py ~/.claude/agents/mi-agente --strict

Referencia:
    - Claude Code Subagents: https://code.claude.com/docs/en/sub-agents.md
    - MCP Spec: https://modelcontextprotocol.io/specification/2025-11-25/index.md
"""

import argparse
import re
import sys
from pathlib import Path

# Motor de validación reusable
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from validadores import (
    BaseValidator,
    Check,
    Resultado,
    Nivel,
    check_yaml_frontmatter,
    check_json_parseable,
    check_yaml_parseable,
    check_placeholders,
    check_archivos_vacios,
    check_estructura,
)


try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN ESPECÍFICA DE AGENTES
# ═══════════════════════════════════════════════════════════════════════════════

REQUIRED_DIRS = [
    "config",
    "prompts",
    "prompts/tasks",
    "tools",
    "tools/custom",
    "skills",
    "memory",
    "hooks",
    "subagents",
    "references",
]

REQUIRED_FILES = [
    "AGENT.md",
    "README.md",
    "config/settings.json",
    "config/permissions.yaml",
    "prompts/system.md",
    "prompts/persona.md",
    "tools/mcp.json",
    "memory/context.md",
]

JSON_FILES = [
    "config/settings.json",
    "tools/mcp.json",
]

YAML_FILES = [
    "config/permissions.yaml",
]

PLAYBOOK_FILES = {"PLAYBOOK_INICIO.md"}


# ═══════════════════════════════════════════════════════════════════════════════
# VALIDADOR DE AGENTES
# ═══════════════════════════════════════════════════════════════════════════════

class AgentValidator(BaseValidator):
    """Validador específico para módulos de agentes."""

    def __init__(self, agent_dir: Path, strict: bool = False):
        super().__init__(agent_dir, strict)
        self.checks = [
            Check("estructura", self._check_estructura),
            Check("frontmatter", self._check_frontmatter),
            Check("json", self._check_json),
            Check("yaml", self._check_yaml),
            Check("placeholder", self._check_placeholders),
            Check("skills", self._check_skills_consistency),
            Check("subagentes", self._check_subagents_consistency),
            Check("vacio", self._check_empty_files),
            Check("readme", self._check_readme),
            Check("permisos", self._check_permissions),
        ]

    # ──────────────────────────────────────────────────────────────────────────

    def _check_estructura(self):
        return check_estructura(self, REQUIRED_DIRS, REQUIRED_FILES)

    def _check_frontmatter(self):
        resultados = []
        for rel_path in ["AGENT.md"] + self._glob("subagents/*.md"):
            p = self.ruta / rel_path
            if not p.exists():
                continue

            campos = ("name", "description", "model") if rel_path == "AGENT.md" else ("name", "description")
            resultados.extend(check_yaml_frontmatter(self, p, campos))

        # Validación adicional: modelo reconocido en AGENT.md
        agent_md = self.ruta / "AGENT.md"
        if HAS_YAML and agent_md.exists():
            content = agent_md.read_text(encoding="utf-8")
            if "---" in content:
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    try:
                        data = yaml.safe_load(parts[1])
                        if isinstance(data, dict) and "model" in data:
                            model = data["model"]
                            if model not in ("opus", "sonnet", "haiku", "opusplan"):
                                self.agregar_warning(
                                    "frontmatter",
                                    f"AGENT.md 'model' no reconocido: '{model}'",
                                    "AGENT.md"
                                )
                    except Exception:
                        pass

        return resultados

    def _check_json(self):
        resultados = []
        for rel_path in JSON_FILES:
            p = self.ruta / rel_path
            if p.exists():
                resultados.extend(check_json_parseable(self, p))
        return resultados

    def _check_yaml(self):
        resultados = []
        if not HAS_YAML:
            self.agregar_warning("yaml", "Instala 'pyyaml' para validar archivos YAML")
            return resultados

        for rel_path in YAML_FILES + self._glob("hooks/*.yaml") + self._glob("hooks/*.yml"):
            p = self.ruta / rel_path
            if p.exists():
                resultados.extend(check_yaml_parseable(self, p))
        return resultados

    def _check_placeholders(self):
        return check_placeholders(self, archivos_ignorados=list(PLAYBOOK_FILES))

    def _check_skills_consistency(self):
        resultados = []
        agent_md = self.ruta / "AGENT.md"
        if not agent_md.exists() or not HAS_YAML:
            return resultados

        content = agent_md.read_text(encoding="utf-8")
        if "---" not in content:
            return resultados

        parts = content.split("---", 2)
        if len(parts) < 3:
            return resultados

        try:
            data = yaml.safe_load(parts[1])
        except Exception:
            return resultados

        if not isinstance(data, dict):
            return resultados

        skills = data.get("skills", [])
        if not skills:
            return resultados

        skills_dir = self.ruta / "skills"
        existing_skills = {d.name for d in skills_dir.iterdir() if d.is_dir()} if skills_dir.exists() else set()

        for skill in skills:
            if skill not in existing_skills:
                resultados.append(
                    Resultado(
                        Nivel.ERROR, "skills",
                        f"AGENT.md referencia skill '{skill}' pero no existe en skills/"
                    )
                )
        return resultados

    def _check_subagents_consistency(self):
        resultados = []
        subagents_dir = self.ruta / "subagents"
        if not subagents_dir.exists():
            return resultados

        for subagent_file in subagents_dir.glob("*.md"):
            content = subagent_file.read_text(encoding="utf-8")
            if not content.startswith("---"):
                resultados.append(
                    Resultado(
                        Nivel.ERROR, "subagentes",
                        f"{subagent_file.name} no tiene frontmatter YAML",
                        self._rel(subagent_file)
                    )
                )
        return resultados

    def _check_empty_files(self):
        return check_archivos_vacios(self, min_bytes=50, archivos_ignorados=list(PLAYBOOK_FILES))

    def _check_readme(self):
        resultados = []
        readme = self.ruta / "README.md"
        if not readme.exists():
            return resultados

        content = readme.read_text(encoding="utf-8")
        required_sections = ["## Qué es", "## Uso", "## Arquitectura"]
        for section in required_sections:
            if section not in content:
                resultados.append(
                    Resultado(Nivel.WARNING, "readme", f"README.md falta sección '{section}'")
                )
        return resultados

    def _check_permissions(self):
        resultados = []
        perms = self.ruta / "config/permissions.yaml"
        if not perms.exists():
            return resultados

        content = perms.read_text(encoding="utf-8")
        if "denylist" not in content.lower():
            resultados.append(
                Resultado(Nivel.WARNING, "permisos", "permissions.yaml no tiene sección 'denylist'")
            )
        if "require_confirmation" not in content.lower():
            resultados.append(
                Resultado(Nivel.WARNING, "permisos", "permissions.yaml no tiene 'require_confirmation'")
            )
        return resultados

    def _glob(self, pattern: str):
        return [str(p.relative_to(self.ruta)) for p in self.ruta.glob(pattern)]


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Valida un agente Claude Code según el sistema de plantillas."
    )
    parser.add_argument("agent_dir", help="Directorio del agente a validar")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Tratar warnings como errores (para CI/CD)",
    )
    args = parser.parse_args()

    agent_path = Path(args.agent_dir)
    if not agent_path.exists():
        print(f"❌ El directorio no existe: {agent_path}")
        return 1
    if not agent_path.is_dir():
        print(f"❌ No es un directorio: {agent_path}")
        return 1

    validator = AgentValidator(agent_path, strict=args.strict)
    return validator.run()


if __name__ == "__main__":
    sys.exit(main())
