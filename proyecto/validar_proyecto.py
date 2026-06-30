#!/usr/bin/env python3
"""
Validador de Proyecto · v1.0.0

Valida la estructura del template .claude/ para proyectos.
Uso:
    python validar_proyecto.py /ruta/al/proyecto
    python validar_proyecto.py /ruta/al/proyecto --strict
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from validadores import BaseValidator, Check, Resultado, check_estructura
from validadores.checks import check_json_parseable


class ValidadorProyecto(BaseValidator):
    def __init__(self, ruta: Path, strict: bool = False):
        super().__init__(ruta, strict)
        self.checks = [
            Check("estructura", self._check_estructura),
            Check("json", self._check_json),
        ]

    def _check_estructura(self) -> list[Resultado]:
        return check_estructura(
            self,
            dirs_requeridos=[".github/workflows"],
            archivos_requeridos=[
                "README.md",
                "CLAUDE.md",
                "settings.json",
                "mcp.json",
                ".github/workflows/ci.yml",
            ],
        )

    def _check_json(self) -> list[Resultado]:
        resultados = []
        for nombre in ("settings.json", "mcp.json"):
            path = self.ruta / nombre
            if path.is_file():
                resultados.extend(check_json_parseable(self, path))
        return resultados


def main():
    parser = argparse.ArgumentParser(description="Validador de template de proyecto")
    parser.add_argument(
        "proyecto", nargs="?", default=".", help="Ruta al directorio proyecto"
    )
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    validator = ValidadorProyecto(Path(args.proyecto), strict=args.strict)
    sys.exit(validator.run())


if __name__ == "__main__":
    main()
