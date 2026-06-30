"""Validador embebido de ejemplo para agent-config."""

from pathlib import Path

from plantillas.catalog import Module
from plantillas.registry import ValidationResult


def validate(module: Module, root: Path) -> ValidationResult:
    target = root / module.path
    required = ["README.md", "plantilla_agent_config.yaml"]
    for name in required:
        if not (target / name).is_file():
            return ValidationResult(
                module_id=module.id,
                ok=False,
                message=f"Falta {name} en {target}",
            )
    return ValidationResult(module_id=module.id, ok=True, message="OK")
