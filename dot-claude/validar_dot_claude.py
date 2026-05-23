#!/usr/bin/env python3
"""
Validador de configuraciones .claude/ · v1.0.0

Verifica que un directorio de configuración Claude Code (raíz .claude/)
cumpla con la estructura, settings, y referencias correctas.

Uso:
    python validar_dot_claude.py ~/.claude
    python validar_dot_claude.py ~/.claude --strict
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from validadores import (
    BaseValidator,
    Check,
    Resultado,
    Nivel,
    check_json_parseable,
    check_placeholders,
    check_archivos_vacios,
    check_estructura,
)


try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


REQUIRED_FILES = ["CLAUDE.md", "settings.json", "mcp.json"]
REQUIRED_DIRS = ["agents", "skills", "commands", "hooks"]


class DotClaudeValidator(BaseValidator):
    def __init__(self, dot_dir: Path, strict: bool = False):
        super().__init__(dot_dir, strict)
        self.checks = [
            Check("estructura", self._check_estructura),
            Check("json", self._check_json),
            Check("placeholder", self._check_placeholders),
            Check("vacio", self._check_empty_files),
            Check("settings", self._check_settings),
            Check("mcp", self._check_mcp_config),
            Check("claude_md", self._check_claude_md),
        ]

    def _check_estructura(self):
        return check_estructura(self, REQUIRED_DIRS, REQUIRED_FILES)

    def _check_json(self):
        resultados = []
        for p in self._archivos("*.json"):
            resultados.extend(check_json_parseable(self, p))
        return resultados

    def _check_placeholders(self):
        return check_placeholders(self, extensiones=(".json", ".md", ".yaml", ".yml", ".txt"))

    def _check_empty_files(self):
        return check_archivos_vacios(self, min_bytes=30)

    def _check_settings(self):
        resultados = []
        settings = self.ruta / "settings.json"
        if not settings.exists():
            return resultados

        data = json.loads(settings.read_text(encoding="utf-8"))

        # Verificar campos comunes de settings
        if "model" in data:
            model = data["model"]
            if model not in ("opus", "sonnet", "haiku", "opusplan"):
                resultados.append(
                    Resultado(Nivel.WARNING, "settings", f"settings.json 'model' no reconocido: '{model}'", "settings.json")
                )

        return resultados

    def _check_mcp_config(self):
        resultados = []
        mcp = self.ruta / "mcp.json"
        if not mcp.exists():
            return resultados

        data = json.loads(mcp.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            resultados.append(
                Resultado(Nivel.ERROR, "mcp", "mcp.json debe ser un objeto", "mcp.json")
            )
            return resultados

        if "mcpServers" not in data and "servers" not in data:
            resultados.append(
                Resultado(Nivel.WARNING, "mcp", "mcp.json debería tener 'mcpServers' o 'servers'", "mcp.json")
            )

        return resultados

    def _check_claude_md(self):
        resultados = []
        claude_md = self.ruta / "CLAUDE.md"
        if not claude_md.exists():
            return resultados

        content = claude_md.read_text(encoding="utf-8")

        # Verificar frontmatter (opcional, warning)
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3 and HAS_YAML:
                try:
                    data = yaml.safe_load(parts[1])
                    if isinstance(data, dict) and "name" not in data:
                        resultados.append(
                            Resultado(Nivel.WARNING, "claude_md", "CLAUDE.md falta campo 'name' en frontmatter", "CLAUDE.md")
                        )
                except Exception as e:
                    resultados.append(
                        Resultado(Nivel.WARNING, "claude_md", f"CLAUDE.md YAML inválido: {e}", "CLAUDE.md")
                    )
        # else: sin frontmatter es válido, no generar warning

        # Verificar secciones mínimas
        if "## Estructura" not in content and "## Introducción" not in content:
            resultados.append(
                Resultado(Nivel.WARNING, "claude_md", "CLAUDE.md debería tener '## Estructura' o '## Introducción'", "CLAUDE.md")
            )

        return resultados


def main() -> int:
    parser = argparse.ArgumentParser(description="Valida una configuración .claude/.")
    parser.add_argument("dot_dir", help="Directorio .claude/ a validar")
    parser.add_argument("--strict", action="store_true", help="Tratar warnings como errores")
    args = parser.parse_args()

    dot_path = Path(args.dot_dir)
    if not dot_path.exists():
        print(f"❌ El directorio no existe: {dot_path}")
        return 1
    if not dot_path.is_dir():
        print(f"❌ No es un directorio: {dot_path}")
        return 1

    validator = DotClaudeValidator(dot_path, strict=args.strict)
    return validator.run()


if __name__ == "__main__":
    sys.exit(main())
