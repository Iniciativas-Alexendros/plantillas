#!/usr/bin/env python3
"""
Validador de Estándares · v1.0.0

Valida la estructura del módulo de estándares del portfolio.
Uso:
    python estandares/validar_estandares.py estandares --strict
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from validadores import BaseValidator, Check, Resultado, check_estructura


class ValidadorEstandares(BaseValidator):
    def __init__(self, ruta: Path, strict: bool = False):
        super().__init__(ruta, strict)
        self.checks = [
            Check("estructura", self._check_estructura),
        ]

    def _check_estructura(self) -> list[Resultado]:
        return check_estructura(
            self,
            dirs_requeridos=["ejemplo_estandares"],
            archivos_requeridos=[
                "README.md",
                "ESTANDARES.md",
                "ejemplo_estandares/EJEMPLO.md",
            ],
        )


def main():
    parser = argparse.ArgumentParser(description="Validador del módulo de estándares")
    parser.add_argument(
        "estandares", nargs="?", default=".", help="Ruta al directorio estandares"
    )
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    validator = ValidadorEstandares(Path(args.estandares), strict=args.strict)
    sys.exit(validator.run())


if __name__ == "__main__":
    main()
