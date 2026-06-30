#!/usr/bin/env python3
"""
Validador de Skills Claude Code · v1.0.0

Verifica que un directorio de skill cumpla con la estructura y calidad
estipuladas por el sistema de plantillas.

Uso:
    python validar_skill.py ~/.claude/skills/mi-skill
    python validar_skill.py ~/.claude/skills/mi-skill --strict
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
    check_yaml_frontmatter,
    check_placeholders,
    check_archivos_vacios,
    check_estructura,
)


REQUIRED_FILES = ["SKILL.md"]
REQUIRED_DIRS = []


class SkillValidator(BaseValidator):
    def __init__(self, skill_dir: Path, strict: bool = False):
        super().__init__(skill_dir, strict)
        self.checks = [
            Check("estructura", self._check_estructura),
            Check("frontmatter", self._check_frontmatter),
            Check("placeholder", self._check_placeholders),
            Check("vacio", self._check_empty_files),
            Check("contenido", self._check_contenido),
        ]

    def _check_estructura(self):
        return check_estructura(self, REQUIRED_DIRS, REQUIRED_FILES)

    def _check_frontmatter(self):
        skill_md = self.ruta / "SKILL.md"
        if not skill_md.exists():
            return []
        return check_yaml_frontmatter(
            self, skill_md, campos_requeridos=["name", "description"]
        )

    def _check_placeholders(self):
        return check_placeholders(self)

    def _check_empty_files(self):
        return check_archivos_vacios(self, min_bytes=50)

    def _check_contenido(self):
        resultados = []
        skill_md = self.ruta / "SKILL.md"
        if not skill_md.exists():
            return resultados

        content = skill_md.read_text(encoding="utf-8")

        if "## Cuándo usar" not in content and "## Cuándo Usar" not in content:
            resultados.append(
                Resultado(
                    Nivel.WARNING,
                    "contenido",
                    "SKILL.md debería tener sección '## Cuándo usar'",
                    "SKILL.md",
                )
            )
        if "## Reglas" not in content and "## Anti-patrones" not in content:
            resultados.append(
                Resultado(
                    Nivel.WARNING,
                    "contenido",
                    "SKILL.md debería tener 'Reglas' o 'Anti-patrones'",
                    "SKILL.md",
                )
            )

        return resultados


def main() -> int:
    parser = argparse.ArgumentParser(description="Valida una skill Claude Code.")
    parser.add_argument("skill_dir", help="Directorio de la skill a validar")
    parser.add_argument(
        "--strict", action="store_true", help="Tratar warnings como errores"
    )
    args = parser.parse_args()

    skill_path = Path(args.skill_dir)
    if not skill_path.exists():
        print(f"❌ El directorio no existe: {skill_path}")
        return 1
    if not skill_path.is_dir():
        print(f"❌ No es un directorio: {skill_path}")
        return 1

    validator = SkillValidator(skill_path, strict=args.strict)
    return validator.run()


if __name__ == "__main__":
    sys.exit(main())
