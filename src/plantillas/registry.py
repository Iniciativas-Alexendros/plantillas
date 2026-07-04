"""Registry de validadores compatibles con el catálogo modules.yaml."""

import importlib
import logging
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from plantillas.catalog import Catalog, Module

log = logging.getLogger("plantillas.registry")

DEFAULT_TIMEOUT = 30


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
            log.debug("validator: %s → embedded", module_id)
            return self._funcs[module_id](module, root)
        if module.validator:
            log.debug("validator: %s → script %s", module_id, module.validator)
            return self._run_script(module.validator, module, root)
        log.debug("validator: %s → none", module_id)
        return ValidationResult(
            module_id=module_id, ok=True, message="No validator configured"
        )

    def _run_script(self, script: str, module: Module, root: Path) -> ValidationResult:
        script_path = root / script
        if not script_path.exists():
            return ValidationResult(
                module_id=module.id,
                ok=True,
                message="No validator configured",
            )
        target = root / module.path
        if module.example:
            candidate = root / module.example
            if candidate.exists():
                target = candidate
        cmd = ["python", str(script_path), str(target), "--strict"]
        try:
            subprocess.run(
                cmd, check=True, capture_output=True, text=True, timeout=DEFAULT_TIMEOUT
            )
            return ValidationResult(module_id=module.id, ok=True, message="OK")
        except subprocess.TimeoutExpired:
            return ValidationResult(
                module_id=module.id,
                ok=False,
                message=f"Validator timeout after {DEFAULT_TIMEOUT}s: {script_path.name}",
            )
        except subprocess.CalledProcessError as exc:
            return ValidationResult(
                module_id=module.id,
                ok=False,
                message=f"Validation failed (exit {exc.returncode}):\n{exc.stdout}{exc.stderr}",
            )


def _module_name(module_id: str) -> str:
    return module_id.replace("-", "_")


def discover_validators(registry: ValidatorRegistry, catalog: Catalog) -> list[str]:
    """Descubre validadores registrados en el paquete o delega al script."""

    for module in catalog.modules:
        if module.type != "module":
            continue
        try:
            mod = importlib.import_module(f"plantillas.validators.{_module_name(module.id)}")
            fn = getattr(mod, "validate", None)
            if callable(fn):
                registry.register(module.id, fn)
                log.debug("discover: %s → %s.validate", module.id, mod.__name__)
        except (ModuleNotFoundError, ImportError) as exc:
            log.debug("discover: %s → skip (%s)", module.id, exc.__class__.__name__)
            continue
    return catalog.canonical_ids()
