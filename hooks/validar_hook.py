#!/usr/bin/env python3
"""
Validador de Hooks Claude Code · v1.0.0

Verifica que un directorio de hook cumpla con la estructura y formato
estipulados por el sistema de plantillas.

Uso:
    python validar_hook.py ~/.claude/hooks/mi-hook
    python validar_hook.py ~/.claude/hooks/mi-hook --strict
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


REQUIRED_FILES = []
REQUIRED_DIRS = []


class HookValidator(BaseValidator):
    def __init__(self, hook_dir: Path, strict: bool = False):
        super().__init__(hook_dir, strict)
        self.checks = [
            Check("estructura", self._check_estructura),
            Check("yaml", self._check_yaml),
            Check("placeholder", self._check_placeholders),
            Check("vacio", self._check_empty_files),
            Check("contenido", self._check_contenido),
        ]

    def _check_estructura(self):
        return check_estructura(self, REQUIRED_DIRS, REQUIRED_FILES)

    def _check_yaml(self):
        resultados = []
        for p in self._archivos("*.yaml") + self._archivos("*.yml"):
            resultados.extend(check_yaml_parseable(self, p))
        return resultados

    def _check_placeholders(self):
        return check_placeholders(self, extensiones=(".md", ".yaml", ".yml", ".txt"))

    def _check_empty_files(self):
        return check_archivos_vacios(self, min_bytes=30)

    def _check_contenido(self):
        resultados = []
        hook_md = self.ruta / "HOOK.md"
        if not hook_md.exists():
            return resultados

        # Verificar archivos yaml que tengan campo 'hook' o 'event'
        for p in self._archivos("*.yaml") + self._archivos("*.yml"):
            if not HAS_YAML:
                continue
            try:
                data = yaml.safe_load(p.read_text(encoding="utf-8"))
                if isinstance(data, dict):
                    if "hook" not in data and "event" not in data:
                        resultados.append(
                            Resultado(
                                Nivel.WARNING, "contenido",
                                f"{self._rel(p)} debería tener campo 'hook' o 'event'",
                                self._rel(p)
                            )
                        )
            except Exception:
                pass

        return resultados


def main() -> int:
    parser = argparse.ArgumentParser(description="Valida un hook Claude Code.")
    parser.add_argument("hook_dir", help="Directorio del hook a validar")
    parser.add_argument("--strict", action="store_true", help="Tratar warnings como errores")
    args = parser.parse_args()

    hook_path = Path(args.hook_dir)
    if not hook_path.exists():
        print(f"❌ El directorio no existe: {hook_path}")
        return 1
    if not hook_path.is_dir():
        print(f"❌ No es un directorio: {hook_path}")
        return 1

    validator = HookValidator(hook_path, strict=args.strict)
    return validator.run()


if __name__ == "__main__":
    sys.exit(main())
