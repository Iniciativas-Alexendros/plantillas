"""Registry de validadores compatibles con el catálogo modules.yaml."""

import importlib
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from plantillas.catalog import Catalog, Module


@dataclass
class ValidationResult:
    module_id: str
    ok: bool
    message: str


ValidatorFn = Callable[[Module, Path], ValidationResult]


class ValidatorRegistry:
    """Registro de validadores que puede ejecutar scripts o funciones Python."""

    def __init__(self) -> None:
        self._funcs: dict[str, ValidatorFn] = {}

    def register(self, module_id: str, fn: ValidatorFn) -> None:
        self._funcs[module_id] = fn

    def validate(self, module_id: str, module: Module, root: Path) -> ValidationResult:
        if module_id in self._funcs:
            return self._funcs[module_id](module, root)
        if module.validator:
            return self._run_script(module.validator, module, root)
        return ValidationResult(
            module_id=module_id, ok=True, message="No validator configured"
        )

    def _run_script(self, script: str, module: Module, root: Path) -> ValidationResult:
        script_path = root / script
        if not script_path.exists():
            return ValidationResult(
                module_id=module.id,
                ok=False,
                message=f"Validator script not found: {script_path}",
            )
        target = root / module.path
        if module.example:
            candidate = root / module.example
            if candidate.exists():
                target = candidate
        cmd = ["python", str(script_path), str(target), "--strict"]
        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            return ValidationResult(module_id=module.id, ok=True, message="OK")
        except subprocess.CalledProcessError as exc:
            return ValidationResult(
                module_id=module.id,
                ok=False,
                message=f"Validation failed:\n{exc.stdout}{exc.stderr}",
            )


def discover_validators(registry: ValidatorRegistry, catalog: Catalog) -> list[str]:
    """Descubre validadores registrados en el paquete o delega al script."""

    for module in catalog.modules:
        if module.type != "module":
            continue
        try:
            mod = importlib.import_module(f"plantillas.validators.{module.id}")
            fn = getattr(mod, "validate", None)
            if callable(fn):
                registry.register(module.id, fn)
        except ModuleNotFoundError:
            continue
    return catalog.canonical_ids()
