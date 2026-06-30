"""CLI unificada del paquete plantillas."""

from pathlib import Path
from typing import Optional

import typer

from plantillas import __version__
from plantillas.catalog import load_catalog
from plantillas.registry import ValidatorRegistry, discover_validators

app = typer.Typer(
    name="plantillas",
    help="CLI del sistema de plantillas modulares.",
    add_completion=False,
)


@app.command()
def validate(
    module: Optional[str] = typer.Argument(None, help="ID del módulo a validar."),
    strict: bool = typer.Option(True, "--strict/--no-strict", help="Modo estricto."),
    catalog_path: Optional[Path] = typer.Option(None, "--catalog", help="Ruta a modules.yaml."),
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
    module: str = typer.Argument(..., help="ID del módulo a sincronizar."),
    catalog_path: Optional[Path] = typer.Option(None, "--catalog", help="Ruta a modules.yaml."),
) -> None:
    """Sincroniza un módulo (por ejemplo, agent-config) desde su fuente canónica."""

    catalog = load_catalog(catalog_path)
    entry = catalog.by_id(module)
    if entry is None:
        typer.echo(f"❌ Módulo desconocido: {module}", err=True)
        raise typer.Exit(code=1)

    typer.echo(f"🔄 Sincronizando {module}...")
    # Placeholder: delegación a script específico del módulo.
    raise typer.Exit(code=0)


@app.command()
def new(
    name: str = typer.Argument(..., help="Nombre del nuevo módulo."),
    type: str = typer.Option("module", "--type", help="Tipo de módulo."),
) -> None:
    """Crea un nuevo módulo a partir de la plantilla base."""

    typer.echo(f"🆕 Creando módulo {type}/{name}...")
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
