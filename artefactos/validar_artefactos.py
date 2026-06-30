#!/usr/bin/env python3
"""Validador mínimo del módulo artefactos."""

import argparse
import sys
from pathlib import Path


def validate(path: Path, strict: bool = False) -> int:
    readme = path / "README.md"
    if not readme.is_file():
        print(f"❌ Falta README.md en {path}")
        return 1
    print("✅ artefactos OK")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validar módulo artefactos")
    parser.add_argument("path", type=Path)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    sys.exit(validate(args.path, args.strict))
