#!/usr/bin/env python3
"""
Validador de Commands Claude Code · v1.0.0

Verifica que un directorio de comando slash cumpla con la estructura
estipulada por el sistema de plantillas.

Uso:
    python validar_command.py ~/.claude/commands/mi-comando
    python validar_command.py ~/.claude/commands/mi-comando --strict
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
    check_placeholders,
    check_archivos_vacios,
    check_estructura,
)


REQUIRED_FILES = ["COMMAND.md"]
REQUIRED_DIRS = []


class CommandValidator(BaseValidator):
    def __init__(self, cmd_dir: Path, strict: bool = False):
        super().__init__(cmd_dir, strict)
        self.checks = [
            Check("estructura", self._check_estructura),
            Check("placeholder", self._check_placeholders),
            Check("vacio", self._check_empty_files),
            Check("contenido", self._check_contenido),
        ]

    def _check_estructura(self):
        return check_estructura(self, REQUIRED_DIRS, REQUIRED_FILES)

    def _check_placeholders(self):
        return check_placeholders(self)

    def _check_empty_files(self):
        return check_archivos_vacios(self, min_bytes=30)

    def _check_contenido(self):
        resultados = []
        cmd_md = self.ruta / "COMMAND.md"
        if not cmd_md.exists():
            return resultados

        content = cmd_md.read_text(encoding="utf-8")

        if "## Trigger" not in content:
            resultados.append(
                Resultado(Nivel.WARNING, "contenido", "COMMAND.md debería tener '## Trigger'", "COMMAND.md")
            )
        if "## Instrucciones" not in content:
            resultados.append(
                Resultado(Nivel.WARNING, "contenido", "COMMAND.md debería tener '## Instrucciones'", "COMMAND.md")
            )
        if "## Ejemplo de uso" not in content:
            resultados.append(
                Resultado(Nivel.WARNING, "contenido", "COMMAND.md debería tener '## Ejemplo de uso'", "COMMAND.md")
            )

        # Verificar que el nombre del archivo es kebab-case (ignorar prefijos de ejemplo/plantilla)
        nombre = self.ruta.name
        nombre_limpio = nombre
        for prefijo in ("ejemplo_", "plantilla_"):
            if nombre_limpio.startswith(prefijo):
                nombre_limpio = nombre_limpio[len(prefijo):]
                break
        if not all(c.islower() or c.isdigit() or c == '-' for c in nombre_limpio):
            resultados.append(
                Resultado(Nivel.WARNING, "contenido", f"Nombre del directorio '{nombre}' no es kebab-case")
            )

        return resultados


def main() -> int:
    parser = argparse.ArgumentParser(description="Valida un comando Claude Code.")
    parser.add_argument("cmd_dir", help="Directorio del comando a validar")
    parser.add_argument("--strict", action="store_true", help="Tratar warnings como errores")
    args = parser.parse_args()

    cmd_path = Path(args.cmd_dir)
    if not cmd_path.exists():
        print(f"❌ El directorio no existe: {cmd_path}")
        return 1
    if not cmd_path.is_dir():
        print(f"❌ No es un directorio: {cmd_path}")
        return 1

    validator = CommandValidator(cmd_path, strict=args.strict)
    return validator.run()


if __name__ == "__main__":
    sys.exit(main())
