#!/usr/bin/env python3
"""
Validador de MCP Servers · v1.0.0

Verifica que un directorio de MCP server cumpla con la estructura,
el manifest JSON, y el código del servidor.

Uso:
    python validar_mcp.py ~/.claude/mcp/mi-server
    python validar_mcp.py ~/.claude/mcp/mi-server --strict
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


REQUIRED_FILES = ["mcp.json"]
REQUIRED_DIRS = []


class MCPValidator(BaseValidator):
    def __init__(self, mcp_dir: Path, strict: bool = False):
        super().__init__(mcp_dir, strict)
        self.checks = [
            Check("estructura", self._check_estructura),
            Check("json", self._check_json),
            Check("placeholder", self._check_placeholders),
            Check("vacio", self._check_empty_files),
            Check("manifest", self._check_manifest),
            Check("servidor", self._check_servidor),
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
            self, extensiones=(".json", ".md", ".py", ".ts", ".js", ".txt")
        )

    def _check_empty_files(self):
        return check_archivos_vacios(self, min_bytes=30)

    def _check_manifest(self):
        resultados = []
        manifest = self.ruta / "mcp.json"
        if not manifest.exists():
            return resultados

        import json

        data = json.loads(manifest.read_text(encoding="utf-8"))

        # Si es un config de cliente (tiene mcpServers), no requiere manifest
        if "mcpServers" in data or "servers" in data:
            return resultados

        # Es un manifest de servidor
        campos_requeridos = ["name", "version", "description"]
        for campo in campos_requeridos:
            if campo not in data:
                resultados.append(
                    Resultado(
                        Nivel.ERROR,
                        "manifest",
                        f"mcp.json falta campo '{campo}'",
                        "mcp.json",
                    )
                )

        # Verificar que hay un server script
        if "server" in data:
            server_path = self.ruta / data["server"]
            if not server_path.exists():
                resultados.append(
                    Resultado(
                        Nivel.WARNING,
                        "manifest",
                        f"Server referenciado no existe: {data['server']}",
                        "mcp.json",
                    )
                )
        else:
            # Verificar si existe server.py o server.ts
            if (
                not (self.ruta / "server.py").exists()
                and not (self.ruta / "server.ts").exists()
            ):
                resultados.append(
                    Resultado(
                        Nivel.WARNING,
                        "manifest",
                        "No se encontró server.py ni server.ts",
                    )
                )

        return resultados

    def _check_servidor(self):
        resultados = []
        server_py = self.ruta / "server.py"
        server_ts = self.ruta / "server.ts"

        for server_file in (server_py, server_ts):
            if not server_file.exists():
                continue
            content = server_file.read_text(encoding="utf-8")
            rel = self._rel(server_file)

            if (
                "mcp" not in content.lower()
                and "modelcontextprotocol" not in content.lower()
            ):
                resultados.append(
                    Resultado(
                        Nivel.WARNING,
                        "servidor",
                        f"{rel} no parece un MCP server (falta referencia a MCP)",
                        rel,
                    )
                )

            if "tool" not in content.lower():
                resultados.append(
                    Resultado(
                        Nivel.WARNING,
                        "servidor",
                        f"{rel} no define tools aparentemente",
                        rel,
                    )
                )

        return resultados


def main() -> int:
    parser = argparse.ArgumentParser(description="Valida un MCP server.")
    parser.add_argument("mcp_dir", help="Directorio del MCP server a validar")
    parser.add_argument(
        "--strict", action="store_true", help="Tratar warnings como errores"
    )
    args = parser.parse_args()

    mcp_path = Path(args.mcp_dir)
    if not mcp_path.exists():
        print(f"❌ El directorio no existe: {mcp_path}")
        return 1
    if not mcp_path.is_dir():
        print(f"❌ No es un directorio: {mcp_path}")
        return 1

    validator = MCPValidator(mcp_path, strict=args.strict)
    return validator.run()


if __name__ == "__main__":
    sys.exit(main())
