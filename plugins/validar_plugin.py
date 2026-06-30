#!/usr/bin/env python3
"""
Validador de Plugins Claude Code · v1.0.0

Verifica que un directorio de plugin cumpla con el manifest,
estructura de componentes, y referencias cruzadas.

Uso:
    python validar_plugin.py ~/.claude/plugins/mi-plugin
    python validar_plugin.py ~/.claude/plugins/mi-plugin --strict
"""

import argparse
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


REQUIRED_FILES = ["plugin.json", "README.md"]
REQUIRED_DIRS = []


class PluginValidator(BaseValidator):
    def __init__(self, plugin_dir: Path, strict: bool = False):
        super().__init__(plugin_dir, strict)
        self.checks = [
            Check("estructura", self._check_estructura),
            Check("json", self._check_json),
            Check("placeholder", self._check_placeholders),
            Check("vacio", self._check_empty_files),
            Check("manifest", self._check_manifest),
            Check("componentes", self._check_componentes),
        ]

    def _check_estructura(self):
        return check_estructura(self, REQUIRED_DIRS, REQUIRED_FILES)

    def _check_json(self):
        resultados = []
        for p in self._archivos("*.json"):
            resultados.extend(check_json_parseable(self, p))
        return resultados

    def _check_placeholders(self):
        return check_placeholders(
            self, extensiones=(".json", ".md", ".yaml", ".yml", ".txt")
        )

    def _check_empty_files(self):
        return check_archivos_vacios(self, min_bytes=30)

    def _check_manifest(self):
        resultados = []
        manifest = self.ruta / "plugin.json"
        if not manifest.exists():
            return resultados

        import json

        data = json.loads(manifest.read_text(encoding="utf-8"))

        campos_requeridos = ["name", "version", "description"]
        for campo in campos_requeridos:
            if campo not in data:
                resultados.append(
                    Resultado(
                        Nivel.ERROR,
                        "manifest",
                        f"plugin.json falta campo '{campo}'",
                        "plugin.json",
                    )
                )

        if "components" not in data:
            resultados.append(
                Resultado(
                    Nivel.WARNING,
                    "manifest",
                    "plugin.json debería tener 'components'",
                    "plugin.json",
                )
            )

        return resultados

    def _check_componentes(self):
        resultados = []
        manifest = self.ruta / "plugin.json"
        if not manifest.exists():
            return resultados

        import json

        data = json.loads(manifest.read_text(encoding="utf-8"))
        if not isinstance(data, dict) or "components" not in data:
            return resultados

        components = data["components"]
        if not isinstance(components, dict):
            return resultados

        # Verificar que los componentes declarados existen físicamente
        component_dirs = {
            "agents": "agents",
            "skills": "skills",
            "hooks": "hooks",
            "mcpServers": "mcp",
        }

        for comp_key, dir_name in component_dirs.items():
            items = components.get(comp_key, [])
            if not items:
                continue
            comp_dir = self.ruta / dir_name
            if not comp_dir.exists():
                # En ejemplos/plantillas, los componentes ilustrativos sin dir son OK
                if self.ruta.name.startswith(("ejemplo_", "plantilla_")):
                    continue
                resultados.append(
                    Resultado(
                        Nivel.WARNING,
                        "componentes",
                        f"plugin.json declara {comp_key} pero no existe directorio {dir_name}/",
                    )
                )
                continue

            for item in items:
                # Skills y MCP son directorios; agents, hooks son archivos
                if comp_key in ("skills", "mcpServers"):
                    if not (comp_dir / item).is_dir():
                        resultados.append(
                            Resultado(
                                Nivel.WARNING,
                                "componentes",
                                f"Componente {comp_key}/{item} no existe",
                            )
                        )
                else:
                    # agents: .md, hooks: .yaml/.yml
                    ext = ".md" if comp_key == "agents" else ".yaml"
                    if (
                        not (comp_dir / f"{item}{ext}").exists()
                        and not (comp_dir / item).exists()
                    ):
                        resultados.append(
                            Resultado(
                                Nivel.WARNING,
                                "componentes",
                                f"Componente {comp_key}/{item} no encontrado",
                            )
                        )

        return resultados


def main() -> int:
    parser = argparse.ArgumentParser(description="Valida un plugin Claude Code.")
    parser.add_argument("plugin_dir", help="Directorio del plugin a validar")
    parser.add_argument(
        "--strict", action="store_true", help="Tratar warnings como errores"
    )
    args = parser.parse_args()

    plugin_path = Path(args.plugin_dir)
    if not plugin_path.exists():
        print(f"❌ El directorio no existe: {plugin_path}")
        return 1
    if not plugin_path.is_dir():
        print(f"❌ No es un directorio: {plugin_path}")
        return 1

    validator = PluginValidator(plugin_path, strict=args.strict)
    return validator.run()


if __name__ == "__main__":
    sys.exit(main())
