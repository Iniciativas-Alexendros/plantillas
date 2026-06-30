#!/usr/bin/env python3
"""
Validador de Módulo · v1.0.0

Valida la estructura del template para crear nuevos módulos.
Uso:
    python validar_modulo.py /ruta/al/modulo
    python validar_modulo.py /ruta/al/modulo --strict
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from validadores import BaseValidator, Check, Resultado, check_estructura


class ValidadorModulo(BaseValidator):
    def __init__(self, ruta: Path, strict: bool = False):
        super().__init__(ruta, strict)
        self.checks = [
            Check("estructura", self._check_estructura),
        ]

    def _check_estructura(self) -> list[Resultado]:
        return check_estructura(
            self,
            dirs_requeridos=["ejemplo_modulo"],
            archivos_requeridos=["README.md", "MODULO.md", "ejemplo_modulo/EJEMPLO.md"],
        )


def main():
    parser = argparse.ArgumentParser(description="Validador de template de módulo")
    parser.add_argument(
        "modulo", nargs="?", default=".", help="Ruta al directorio modulo"
    )
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    validator = ValidadorModulo(Path(args.modulo), strict=args.strict)
    sys.exit(validator.run())


if __name__ == "__main__":
    main()
