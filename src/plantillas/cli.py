"""CLI unificada del paquete plantillas."""

from pathlib import Path
from typing import Optional

import typer

from plantillas import __version__
from plantillas.catalog import load_catalog
from plantillas.registry import ValidatorRegistry, discover_validators
from plantillas.sync import (
    SYNCABLE_MODULE_IDS,
    SyncDirection,
    SyncTarget,
    execute_sync,
    resolve_module_id,
)

app = typer.Typer(
    name="plantillas",
    help="CLI del sistema de plantillas modulares.",
    add_completion=False,
)


@app.command()
def validate(
    module: Optional[str] = typer.Argument(None, help="ID del módulo a validar."),
    strict: bool = typer.Option(True, "--strict/--no-strict", help="Modo estricto."),
    catalog_path: Optional[Path] = typer.Option(
        None, "--catalog", help="Ruta a modules.yaml."
    ),
) -> None:
    """Valida uno o todos los módulos registrados."""

    catalog = load_catalog(catalog_path)
    registry = ValidatorRegistry()
    discover_validators(registry, catalog)
    root = Path(__file__).resolve().parents[2]

    module_ids = [module] if module else catalog.canonical_ids()
    errors = 0
    for module_id in module_ids:
        entry = catalog.by_id(module_id)
        if entry is None:
            typer.echo(f"❌ Módulo desconocido: {module_id}", err=True)
            errors += 1
            continue
        result = registry.validate(module_id, entry, root)
        prefix = "✅" if result.ok else "❌"
        typer.echo(f"{prefix} {result.module_id}: {result.message}")
        if not result.ok:
            errors += 1

    if errors:
        raise typer.Exit(code=1)


@app.command()
def sync(
    module: str = typer.Argument(
        ...,
        help=(
            f"ID del módulo a sincronizar. Sincronizables: {', '.join(SYNCABLE_MODULE_IDS)}."
        ),
    ),
    target: SyncTarget = typer.Option(
        "opencode", "--target", help="Destino de la sincronización."
    ),
    direction: SyncDirection = typer.Option(
        "status",
        "--direction",
        help="push: plantillas→target · pull: target→plantillas · status: dry-run.",
    ),
    yes: bool = typer.Option(
        False, "--yes", "-y", help="Sobrescribe sin pedir confirmación (pull/push)."
    ),
    catalog_path: Optional[Path] = typer.Option(
        None, "--catalog", help="Ruta a modules.yaml."
    ),
) -> None:
    """Sincroniza un módulo entre `plantillas/` y un target externo."""

    if module not in SYNCABLE_MODULE_IDS and module not in {
        "agents",
        "agent",
    }:
        typer.echo(
            f"❌ Módulo {module!r} no sincronizable. "
            f"Usa uno de: {', '.join(SYNCABLE_MODULE_IDS)} (o alias: agents)",
            err=True,
        )
        raise typer.Exit(code=1)

    catalog = load_catalog(catalog_path)
    root = Path(__file__).resolve().parents[2]

    def _display(p: Path) -> str:
        try:
            return str(p.relative_to(root.parent))
        except ValueError:
            return str(p)

    canonical_id = resolve_module_id(module)
    report = execute_sync(
        module_id=canonical_id,
        target=target,
        direction=direction,
        catalog=catalog,
        root=root,
        assume_yes=yes,
    )

    if not report.ok:
        for err in report.errors:
            typer.echo(f"❌ {err}", err=True)
        raise typer.Exit(code=1)

    arrow = {
        "push": "plantillas →",
        "pull": "→ plantillas",
        "status": "·",
    }[report.direction]
    typer.echo(f"🔄 {canonical_id} {arrow} {report.target}")

    for p in report.promoted:
        typer.echo(f"  ✅ {_display(p)}")
    for p in report.skipped:
        typer.echo(f"  ⏭️  ya existe, omitido: {_display(p)}")
    for p in report.drifted:
        typer.echo(f"  ⚠️  drift: {_display(p)}")

    if not (report.promoted or report.skipped or report.drifted):
        typer.echo("  (sin cambios)")


@app.command()
def new(
    name: str = typer.Argument(..., help="Nombre del nuevo módulo."),
    type: str = typer.Option("module", "--type", help="Tipo de módulo."),
) -> None:
    """Crea un nuevo módulo a partir de la plantilla base."""

    typer.echo(f"🆕 Creando módulo {type}/{name}...")
    typer.echo(
        "ℹ️  Comando en desarrollo. Copia manualmente `modulo/` como scaffold mientras tanto."
    )
    raise typer.Exit(code=0)


@app.command()
def config() -> None:
    """Muestra la configuración activa del sistema."""

    catalog = load_catalog()
    typer.echo(f"Versión del catálogo: {catalog.version}")
    typer.echo(f"Módulos canónicos: {', '.join(catalog.canonical_ids())}")


@app.command()
def version() -> None:
    """Muestra la versión del paquete."""

    typer.echo(__version__)
