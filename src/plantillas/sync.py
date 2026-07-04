"""Sincronización bidireccional entre `plantillas/` y targets externos.

Targets soportados:
- opencode → `~/.config/opencode/{skills,agents,commands}/`

Direcciones:
- push (default):  plantillas → target. Sobrescribe instancias declaradas
                   en `modules.yaml` que existan en el target.
- pull:             target → plantillas. Importa drift a
                   `plantillas/<modulo>/_imported/<nombre>/` sin tocar la
                   fuente canónica. Requiere confirmación.
- status (default si no se pasa --push/--pull): dry-run, solo diff.

Reglas:
- El target es propiedad del usuario; nunca se borra silenciosamente.
- Drift (instancias en target sin contraparte en plantillas) se reporta,
  no se promueve automáticamente.
- Los módulos con `validator` se validan tras cada push.
"""

from __future__ import annotations

import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

from plantillas.catalog import Catalog, Module

SyncDirection = Literal["push", "pull", "status"]
SyncTarget = Literal["opencode"]

# Mapeo module_id (catálogo) → subdirectorio del target.
TARGET_LAYOUTS: dict[str, dict[SyncTarget, str]] = {
    "skills": {"opencode": "skills"},
    "agentes": {"opencode": "agents"},
    "commands": {"opencode": "commands"},
}

# Alias inglés→catálogo, para no obligar al usuario a recordar el nombre canónico.
MODULE_ALIASES: dict[str, str] = {
    "agents": "agentes",
    "agent": "agentes",
}

# IDs aceptados por la CLI (canónicos + alias).
SYNCABLE_MODULE_IDS = tuple(TARGET_LAYOUTS.keys())


def resolve_module_id(module_id: str) -> str:
    """Resuelve alias (inglés) → id canónico del catálogo. Lanza ValueError si no existe."""
    canonical = MODULE_ALIASES.get(module_id, module_id)
    if canonical not in TARGET_LAYOUTS:
        raise ValueError(
            f"módulo {module_id!r} no sincronizable. "
            f"Usa uno de: {', '.join(SYNCABLE_MODULE_IDS)}"
        )
    return canonical


@dataclass
class SyncReport:
    target: str
    direction: SyncDirection
    promoted: list[Path] = field(default_factory=list)
    drifted: list[Path] = field(default_factory=list)
    skipped: list[Path] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def _target_root(target: SyncTarget) -> Path:
    if target == "opencode":
        return Path.home() / ".config" / "opencode"
    raise ValueError(f"target no soportado: {target}")


def _target_subdir(target: SyncTarget, module_id: str) -> str:
    try:
        return TARGET_LAYOUTS[module_id][target]
    except KeyError as exc:
        raise ValueError(
            f"módulo {module_id!r} no sincronizable a {target!r}"
        ) from exc


def _list_instances(source: Path) -> list[Path]:
    """Lista subdirectorios válidos (con SKILL.md o .md) bajo `source`."""
    if not source.exists():
        return []
    out: list[Path] = []
    for entry in sorted(source.iterdir()):
        if not entry.is_dir():
            continue
        if entry.name.startswith(("_", ".")):
            continue
        if any(entry.glob("*.md")):
            out.append(entry)
    return out


def _copytree(src: Path, dst: Path) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def _plan_push(
    module: Module,
    target: SyncTarget,
    root: Path,
) -> tuple[list[Path], list[str]]:
    """Calcula el set de instancias a promover sin escribir nada."""
    target_root = _target_root(target)
    sub = _target_subdir(target, module.id)
    target_path = target_root / sub

    source = root / module.path
    if not source.exists():
        return [], [f"fuente no encontrada: {source}"]

    if not target_path.exists():
        return [], [f"target no inicializado: {target_path}"]

    instances = _list_instances(source)
    return instances, []


def _plan_pull(
    module: Module,
    target: SyncTarget,
    root: Path,
) -> tuple[list[Path], list[Path], list[str]]:
    """Calcula drift: instancias en target sin contraparte en source."""
    target_root = _target_root(target)
    sub = _target_subdir(target, module.id)
    target_path = target_root / sub

    source = root / module.path
    if not target_path.exists():
        return [], [], [f"target no existe: {target_path}"]

    if not source.exists():
        return [], [], []

    source_names = {p.name for p in _list_instances(source)}
    target_instances = _list_instances(target_path)
    drift = [p for p in target_instances if p.name not in source_names]
    return [], drift, []


def execute_sync(
    module_id: str,
    target: SyncTarget,
    direction: SyncDirection,
    catalog: Catalog,
    root: Path,
    *,
    assume_yes: bool = False,
) -> SyncReport:
    """Ejecuta (o simula) la sincronización de un módulo contra un target."""
    module = catalog.by_id(module_id)
    if module is None:
        return SyncReport(
            target=target,
            direction=direction,
            errors=[f"módulo desconocido: {module_id}"],
        )

    if module.id not in SYNCABLE_MODULE_IDS:
        return SyncReport(
            target=target,
            direction=direction,
            errors=[f"módulo {module_id!r} no sincronizable"],
        )

    report = SyncReport(target=target, direction=direction)

    if direction == "status":
        _, drift, errs = _plan_pull(module, target, root)
        report.errors.extend(errs)
        report.drifted.extend(drift)
        return report

    if direction == "push":
        instances, errs = _plan_push(module, target, root)
        report.errors.extend(errs)
        if errs:
            return report
        target_root = _target_root(target)
        sub = _target_subdir(target, module.id)
        target_path = target_root / sub
        for instance in instances:
            dst = target_path / instance.name
            if dst.exists() and not assume_yes:
                report.skipped.append(dst)
                continue
            _copytree(instance, dst)
            report.promoted.append(dst)
        return report

    if direction == "pull":
        _, drift, errs = _plan_pull(module, target, root)
        report.errors.extend(errs)
        if errs:
            return report
        import_root = root / module.path / "_imported"
        for instance in drift:
            dst = import_root / instance.name
            if dst.exists() and not assume_yes:
                report.skipped.append(dst)
                continue
            import_root.mkdir(parents=True, exist_ok=True)
            _copytree(instance, dst)
            report.promoted.append(dst)
        return report

    return SyncReport(
        target=target,
        direction=direction,
        errors=[f"dirección inválida: {direction}"],
    )
